"""
LangGraph orchestrator for the Multi-Source RAG System
"""

import asyncio
import time
from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from config import Config
from state_manager import StateManager, RAGState, ProcessingStage
from retriever import MultiSourceRetriever, QueryClassifier
from routing_engine import RoutingEngine
from agent_tools import RAGAgent

class MultiSourceRAGOrchestrator:
    """LangGraph-based orchestrator for multi-source RAG workflow"""
    
    def __init__(self, config: Config, vsc_client=None, llm=None):
        self.config = config
        self.vsc_client = vsc_client  # You'll need to pass this in
        self.llm = llm  # You'll need to pass this in
        
        # Initialize components
        self.state_manager = StateManager()
        self.retriever = MultiSourceRetriever(config, vsc_client) if vsc_client else None
        self.routing_engine = RoutingEngine(config, self.retriever) if self.retriever else None
        self.agent = RAGAgent(config, self.retriever, self.routing_engine, llm) if all([self.retriever, self.routing_engine, llm]) else None
        
        # Create the workflow graph
        self.workflow = self._create_workflow()
        self.app = self.workflow.compile(checkpointer=MemorySaver())
    
    def _create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow"""
        
        # Define the workflow graph
        workflow = StateGraph(RAGState)
        
        # Add nodes
        workflow.add_node("initialize", self._initialize_node)
        workflow.add_node("classify_query", self._classify_query_node)
        workflow.add_node("probe_sources", self._probe_sources_node)
        workflow.add_node("make_routing_decision", self._make_routing_decision_node)
        workflow.add_node("retrieve_full", self._retrieve_full_node)
        workflow.add_node("generate_answer", self._generate_answer_node)
        workflow.add_node("quality_check", self._quality_check_node)
        workflow.add_node("fallback", self._fallback_node)
        workflow.add_node("agent_process", self._agent_process_node)
        workflow.add_node("finalize", self._finalize_node)
        
        # Define edges
        workflow.set_entry_point("initialize")
        
        workflow.add_edge("initialize", "classify_query")
        workflow.add_edge("classify_query", "probe_sources")
        workflow.add_edge("probe_sources", "make_routing_decision")
        workflow.add_edge("make_routing_decision", "retrieve_full")
        workflow.add_edge("retrieve_full", "generate_answer")
        workflow.add_edge("generate_answer", "quality_check")
        
        # Conditional edges for quality check
        workflow.add_conditional_edges(
            "quality_check",
            self._should_use_fallback,
            {
                "fallback": "fallback",
                "agent": "agent_process",
                "finalize": "finalize"
            }
        )
        
        workflow.add_edge("fallback", "finalize")
        workflow.add_edge("agent_process", "finalize")
        workflow.add_edge("finalize", END)
        
        return workflow
    
    async def run(self, query: str) -> Dict[str, Any]:
        """Run the orchestrator workflow"""
        
        # Create initial state
        initial_state = self.state_manager.create_initial_state(query)
        
        # Run the workflow
        config = {"configurable": {"thread_id": f"thread_{int(time.time())}"}}
        
        try:
            final_state = None
            async for state in self.app.astream(initial_state, config):
                final_state = state
            
            # Extract results from final state
            if final_state and "finalize" in final_state:
                result_state = final_state["finalize"]
                
                return {
                    "status": "success" if result_state["stage"] == ProcessingStage.COMPLETED else "failed",
                    "answer": result_state.get("final_answer", "No answer generated"),
                    "source_used": result_state.get("source_used", "Unknown"),
                    "confidence": result_state.get("confidence", 0.0),
                    "processing_time": result_state.get("processing_time", 0.0),
                    "routing_info": result_state.get("routing_info", {}),
                    "error": result_state.get("error")
                }
            else:
                return {
                    "status": "failed",
                    "error": "Workflow did not complete properly",
                    "answer": "I encountered an error while processing your query."
                }
                
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "answer": f"I encountered an error while processing your query: {str(e)}"
            }
    
    # Node implementations
    
    def _initialize_node(self, state: RAGState) -> RAGState:
        """Initialize the processing"""
        state = self.state_manager.update_stage(state, ProcessingStage.INITIALIZED)
        
        if self.config.VERBOSE_LOGGING:
            print(f"🚀 Initializing workflow for query: {state['query'][:100]}...")
        
        return state
    
    def _classify_query_node(self, state: RAGState) -> RAGState:
        """Classify the query to predict best source"""
        if not self.retriever:
            return self.state_manager.set_error(state, "Retriever not initialized")
        
        try:
            classifier = QueryClassifier(self.config)
            classification = classifier.classify_query(state["query"])
            state = self.state_manager.update_classification(state, classification)
            
            if self.config.VERBOSE_LOGGING:
                print(f"📊 Classification: {classification.predicted_source} "
                      f"(confidence: {classification.confidence:.2f})")
            
            return state
            
        except Exception as e:
            return self.state_manager.set_error(state, f"Classification failed: {str(e)}")
    
    def _probe_sources_node(self, state: RAGState) -> RAGState:
        """Probe all data sources"""
        if not self.retriever:
            return self.state_manager.set_error(state, "Retriever not initialized")
        
        try:
            state = self.state_manager.update_stage(state, ProcessingStage.PROBING)
            probe_results = self.retriever.probe_all_sources(state["query"])
            
            for probe_result in probe_results:
                state = self.state_manager.add_probe_result(state, probe_result)
            
            if self.config.VERBOSE_LOGGING:
                for probe in probe_results:
                    print(f"🔬 Probe {probe.source_name}: {probe.confidence:.3f} confidence")
            
            return state
            
        except Exception as e:
            return self.state_manager.set_error(state, f"Probing failed: {str(e)}")
    
    def _make_routing_decision_node(self, state: RAGState) -> RAGState:
        """Make routing decision based on classification and probes"""
        if not self.routing_engine:
            return self.state_manager.set_error(state, "Routing engine not initialized")
        
        try:
            classification = state["classification"]
            probe_results = state["probe_results"]
            
            routing_decision = self.routing_engine._make_routing_decision(
                classification, probe_results
            )
            
            state = self.state_manager.update_routing_decision(state, routing_decision)
            
            if self.config.VERBOSE_LOGGING:
                print(f"🎯 Routing decision: {routing_decision.decision_reason}")
                print(f"📍 Chosen sources: {', '.join(routing_decision.chosen_sources)}")
            
            return state
            
        except Exception as e:
            return self.state_manager.set_error(state, f"Routing decision failed: {str(e)}")
    
    def _retrieve_full_node(self, state: RAGState) -> RAGState:
        """Perform full retrieval from chosen sources"""
        if not self.retriever or not self.routing_engine:
            return self.state_manager.set_error(state, "Components not initialized")
        
        try:
            state = self.state_manager.update_stage(state, ProcessingStage.RETRIEVING)
            
            routing_decision = state["routing_decision"]
            final_passages = self.routing_engine._execute_routing_decision(
                state["query"], routing_decision, state
            )
            
            state = self.state_manager.update_reranked_passages(state, final_passages)
            
            if self.config.VERBOSE_LOGGING:
                print(f"📚 Retrieved {len(final_passages)} final passages")
            
            return state
            
        except Exception as e:
            return self.state_manager.set_error(state, f"Full retrieval failed: {str(e)}")
    
    def _generate_answer_node(self, state: RAGState) -> RAGState:
        """Generate answer using LLM"""
        if not self.routing_engine:
            return self.state_manager.set_error(state, "Routing engine not initialized")
        
        try:
            state = self.state_manager.update_stage(state, ProcessingStage.GENERATING)
            
            passages = state["reranked_passages"]
            answer = self.routing_engine._generate_answer(passages, state["query"])
            quality_score = self.routing_engine._assess_answer_quality(answer, passages)
            
            state = self.state_manager.update_answer(state, answer, quality_score)
            
            if self.config.VERBOSE_LOGGING:
                print(f"💡 Generated answer (quality: {quality_score:.2f})")
            
            return state
            
        except Exception as e:
            return self.state_manager.set_error(state, f"Answer generation failed: {str(e)}")
    
    def _quality_check_node(self, state: RAGState) -> RAGState:
        """Check answer quality and determine next step"""
        state = self.state_manager.update_stage(state, ProcessingStage.QUALITY_CHECK)
        
        answer = state["answer"]
        quality_score = state["answer_quality_score"]
        routing_decision = state["routing_decision"]
        
        # Add quality assessment to debug info
        state = self.state_manager.add_debug_info(state, "quality_assessment", {
            "quality_score": quality_score,
            "answer_length": len(answer) if answer else 0,
            "needs_fallback": self.routing_engine._needs_fallback(answer, quality_score, routing_decision) if self.routing_engine else False,
            "can_use_agent": self.agent is not None
        })
        
        return state
    
    def _should_use_fallback(self, state: RAGState) -> str:
        """Determine the next step based on quality check"""
        if state["stage"] == ProcessingStage.FAILED:
            return "finalize"
        
        answer = state["answer"]
        quality_score = state["answer_quality_score"]
        routing_decision = state["routing_decision"]
        
        # Check if fallback is needed and available
        if (self.routing_engine and 
            self.routing_engine._needs_fallback(answer, quality_score, routing_decision)):
            return "fallback"
        
        # Check if agent processing might help
        if (self.agent and quality_score and quality_score < 0.6 and 
            not state["fallback_attempted"]):
            return "agent"
        
        return "finalize"
    
    def _fallback_node(self, state: RAGState) -> RAGState:
        """Attempt fallback to alternative source"""
        if not self.routing_engine:
            return self.state_manager.set_error(state, "Routing engine not initialized")
        
        try:
            state = self.state_manager.update_stage(state, ProcessingStage.FALLBACK)
            
            routing_decision = state["routing_decision"]
            fallback_result = self.routing_engine._attempt_fallback(
                state["query"], routing_decision, state
            )
            
            if fallback_result:
                state = self.state_manager.update_fallback(
                    state, 
                    fallback_result["sources"][0], 
                    fallback_result["answer"]
                )
                
                if self.config.VERBOSE_LOGGING:
                    print(f"✅ Fallback successful")
            else:
                if self.config.VERBOSE_LOGGING:
                    print(f"⚠️ Fallback unsuccessful")
            
            return state
            
        except Exception as e:
            return self.state_manager.set_error(state, f"Fallback failed: {str(e)}")
    
    def _agent_process_node(self, state: RAGState) -> RAGState:
        """Use agent for additional processing"""
        if not self.agent:
            return self.state_manager.set_error(state, "Agent not initialized")
        
        try:
            if self.config.VERBOSE_LOGGING:
                print(f"🤖 Using agent for additional processing")
            
            agent_result = self.agent.process_query(state["query"])
            
            if agent_result["status"] == "success":
                # Update state with agent results
                state["answer"] = agent_result["answer"]
                state["answer_quality_score"] = 0.8  # Assume good quality from agent
                
                state = self.state_manager.add_debug_info(state, "agent_used", True)
                state = self.state_manager.add_debug_info(state, "agent_steps", 
                                                        agent_result.get("intermediate_steps", []))
            
            return state
            
        except Exception as e:
            return self.state_manager.set_error(state, f"Agent processing failed: {str(e)}")
    
    def _finalize_node(self, state: RAGState) -> RAGState:
        """Finalize the results"""
        try:
            # Determine final answer
            if state["fallback_attempted"] and state["fallback_answer"]:
                final_answer = state["fallback_answer"]
                source_used = f"{state['fallback_source']} (fallback)"
            else:
                final_answer = state["answer"] or "I could not find a satisfactory answer."
                routing_decision = state["routing_decision"]
                if routing_decision:
                    source_used = self.routing_engine._get_source_summary(routing_decision.chosen_sources)
                else:
                    source_used = "Unknown"
            
            # Calculate final confidence
            confidence = state["routing_decision"].final_confidence if state["routing_decision"] else 0.0
            
            # Calculate processing time (placeholder - you'd track this properly)
            processing_time = 0.0  # This should be calculated from start time
            
            state = self.state_manager.finalize_state(
                state, final_answer, source_used, confidence, processing_time
            )
            
            if self.config.VERBOSE_LOGGING:
                print(f"🏁 Workflow completed: {source_used}")
            
            return state
            
        except Exception as e:
            return self.state_manager.set_error(state, f"Finalization failed: {str(e)}")