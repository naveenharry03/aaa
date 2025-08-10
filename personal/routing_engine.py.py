""
Routing engine for intelligent source selection in Multi-Source RAG
"""

import time
from typing import Dict, Any, List, Tuple
from config import Config
from retriever import MultiSourceRetriever, QueryClassifier
from state_manager import StateManager, RoutingDecision, RAGState
from databricks_langchain import ChatDatabricks

class RoutingEngine:
    """Handles intelligent routing between data sources"""
    
    def __init__(self, config: Config, retriever: MultiSourceRetriever):
        self.config = config
        self.retriever = retriever
        self.classifier = QueryClassifier(config)
        self.state_manager = StateManager()
    
    def route_and_retrieve(self, query: str) -> Dict[str, Any]:
        """Main routing and retrieval method"""
        start_time = time.time()
        
        # Initialize state
        state = self.state_manager.create_initial_state(query)
        
        try:
            # Step 1: Classify query
            classification = self.classifier.classify_query(query)
            state = self.state_manager.update_classification(state, classification)
            
            if self.config.VERBOSE_LOGGING:
                print(f"🔍 Processing query: {query}")
                print(f"📊 Classification: {classification.predicted_source} "
                      f"(confidence: {classification.confidence:.2f})")
            
            # Step 2: Probe all sources
            state = self.state_manager.update_stage(state, state["stage"])
            probe_results = self.retriever.probe_all_sources(query)
            
            for probe_result in probe_results:
                state = self.state_manager.add_probe_result(state, probe_result)
            
            # Step 3: Make routing decision
            routing_decision = self._make_routing_decision(classification, probe_results)
            state = self.state_manager.update_routing_decision(state, routing_decision)
            
            if self.config.VERBOSE_LOGGING:
                print(f"🎯 Routing decision: {routing_decision.decision_reason}")
                print(f"📍 Chosen sources: {', '.join(routing_decision.chosen_sources)}")
            
            # Step 4: Retrieve and generate answer
            final_passages = self._execute_routing_decision(query, routing_decision, state)
            state = self.state_manager.update_reranked_passages(state, final_passages)
            
            # Step 5: Generate answer
            answer = self._generate_answer(final_passages, query)
            quality_score = self._assess_answer_quality(answer, final_passages)
            state = self.state_manager.update_answer(state, answer, quality_score)
            
            # Step 6: Quality check and fallback if needed
            if self._needs_fallback(answer, quality_score, routing_decision):
                fallback_result = self._attempt_fallback(query, routing_decision, state)
                if fallback_result:
                    answer = fallback_result["answer"]
                    final_passages = fallback_result["passages"]
                    routing_decision.chosen_sources = fallback_result["sources"]
            
            # Step 7: Finalize results
            processing_time = time.time() - start_time
            source_used = self._get_source_summary(routing_decision.chosen_sources)
            confidence = routing_decision.final_confidence
            
            state = self.state_manager.finalize_state(
                state, answer, source_used, confidence, processing_time
            )
            
            return {
                "status": "success",
                "answer": answer,
                "source_used": source_used,
                "confidence": confidence,
                "processing_time": processing_time,
                "routing_info": state["routing_info"],
                "passages_used": len(final_passages)
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = str(e)
            state = self.state_manager.set_error(state, error_msg)
            
            if self.config.VERBOSE_LOGGING:
                print(f"❌ Routing failed: {error_msg}")
            
            return {
                "status": "failed",
                "error": error_msg,
                "processing_time": processing_time,
                "answer": f"I encountered an error while processing your query: {error_msg}"
            }
    
    def _make_routing_decision(self, classification, probe_results) -> RoutingDecision:
        """Make intelligent routing decision based on classification and probe results"""
        
        # Calculate probe confidences by source
        probe_confidences = {
            probe.source_name: probe.confidence 
            for probe in probe_results if probe.error is None
        }
        
        # Decision logic
        if classification.confidence >= self.config.CLASSIFICATION_CONFIDENCE_THRESHOLD:
            # High classification confidence
            if classification.predicted_source in probe_confidences:
                chosen_sources = [classification.predicted_source]
                decision_reason = f"High classification confidence for {classification.predicted_source}"
                final_confidence = classification.confidence
            else:
                # Fallback to best probe result
                best_source = max(probe_confidences.keys(), key=lambda k: probe_confidences[k])
                chosen_sources = [best_source]
                decision_reason = f"Classification target unavailable, using best probe: {best_source}"
                final_confidence = probe_confidences[best_source]
        else:
            # Low classification confidence - use probe results
            if not probe_confidences:
                chosen_sources = []
                decision_reason = "No successful probes"
                final_confidence = 0.0
            else:
                # Check if probe scores are close
                sorted_sources = sorted(probe_confidences.keys(), 
                                      key=lambda k: probe_confidences[k], reverse=True)
                
                if len(sorted_sources) >= 2:
                    best_score = probe_confidences[sorted_sources[0]]
                    second_score = probe_confidences[sorted_sources[1]]
                    
                    if abs(best_score - second_score) < self.config.PROBE_SCORE_DIFFERENCE_THRESHOLD:
                        # Close scores - merge sources
                        chosen_sources = sorted_sources[:2]
                        decision_reason = f"Close probe scores - merging {' + '.join(chosen_sources)}"
                        final_confidence = (best_score + second_score) / 2
                    else:
                        # Clear winner
                        chosen_sources = [sorted_sources[0]]
                        decision_reason = f"Probe winner: {sorted_sources[0]}"
                        final_confidence = best_score
                else:
                    # Only one source available
                    chosen_sources = [sorted_sources[0]]
                    decision_reason = f"Single available source: {sorted_sources[0]}"
                    final_confidence = probe_confidences[sorted_sources[0]]
        
        return RoutingDecision(
            chosen_sources=chosen_sources,
            decision_reason=decision_reason,
            classification_result=classification,
            probe_results=probe_results,
            final_confidence=final_confidence
        )
    
    def _execute_routing_decision(self, query: str, routing_decision: RoutingDecision, 
                                state: RAGState) -> List[Dict[str, Any]]:
        """Execute the routing decision and retrieve final passages"""
        
        if not routing_decision.chosen_sources:
            return []
        
        if len(routing_decision.chosen_sources) == 1:
            # Single source - full retrieval
            source_name = routing_decision.chosen_sources[0]
            passages = self.retriever.full_retrieve_from_source(query, source_name)
            state = self.state_manager.update_full_retrieval(state, source_name, passages)
            return passages
        else:
            # Multiple sources - merge and rerank
            all_passages = []
            
            for source_name in routing_decision.chosen_sources:
                passages = self.retriever.full_retrieve_from_source(query, source_name)
                state = self.state_manager.update_full_retrieval(state, source_name, passages)
                all_passages.extend(passages)
            
            # Global reranking
            final_passages = self.retriever.global_rerank(query, all_passages)
            return final_passages
    
    def _generate_answer(self, passages: List[Dict[str, Any]], query: str) -> str:
        """Generate answer using LLM"""
        if not passages:
            return "I could not find any relevant information in the configured data sources."
        
        # Prepare context
        rag_context = "\n\n".join([
            f"Source: {p.get('source', 'Unknown')}\n"
            f"File: {p.get('file', 'Unknown')}\n"
            f"Chunk ID: {p.get('chunk_id', 'Unknown')}\n"
            f"Text: {p.get('text', '')}"
            for p in passages
        ])

        system_prompt = (
            "You are a helpful IT support assistant. Use the provided context to answer "
            "the user's question as accurately as possible. Focus on actionable solutions "
            "for pipeline errors and technical issues. If the answer is not present in the context, "
            "say 'I could not find the answer in the provided information.' "
            "Always cite which source(s) you used in your answer."
        )

        user_prompt = f"""Context:
{rag_context}

Question:
{query}

Answer:"""

        try:
            llm = ChatDatabricks(
                endpoint=self.config.LLM_ENDPOINT,
                max_tokens=self.config.MAX_TOKENS,
                temperature=self.config.TEMPERATURE
            )
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            response = llm.invoke(messages)
            return response.content
            
        except Exception as e:
            return f"Error generating answer: {str(e)}"
    
    def _assess_answer_quality(self, answer: str, passages: List[Dict[str, Any]]) -> float:
        """Assess the quality of the generated answer"""
        if not answer or "could not find" in answer.lower():
            return 0.0
        
        if len(answer.strip()) < self.config.MIN_ANSWER_LENGTH:
            return 0.3
        
        # Check if answer contains actionable content
        actionable_indicators = [
            "step", "configure", "set", "add", "remove", "grant", "assign",
            "check", "verify", "ensure", "update", "modify", "create"
        ]
        
        actionable_score = sum(1 for indicator in actionable_indicators 
                             if indicator in answer.lower()) / len(actionable_indicators)
        
        # Base quality score
        base_score = min(len(answer) / 200, 1.0)  # Normalize by expected length
        
        # Combine scores
        quality_score = (base_score * 0.7) + (actionable_score * 0.3)
        
        return min(quality_score, 1.0)
    
    def _needs_fallback(self, answer: str, quality_score: float, 
                       routing_decision: RoutingDecision) -> bool:
        """Determine if fallback is needed"""
        if not self.config.FALLBACK_ENABLED:
            return False
        
        if len(routing_decision.chosen_sources) > 1:
            return False  # Already used multiple sources
        
        # Check quality thresholds
        if quality_score < 0.4 or "could not find" in answer.lower():
            return True
        
        if len(answer.strip()) < self.config.MIN_ANSWER_LENGTH:
            return True
        
        return False
    
    def _attempt_fallback(self, query: str, routing_decision: RoutingDecision, 
                         state: RAGState) -> Dict[str, Any]:
        """Attempt fallback to alternative source"""
        used_sources = set(routing_decision.chosen_sources)
        available_sources = set(self.config.get_all_source_names())
        fallback_sources = list(available_sources - used_sources)
        
        if not fallback_sources:
            return None
        
        if self.config.VERBOSE_LOGGING:
            print(f"⚠️ Attempting fallback to: {', '.join(fallback_sources)}")
        
        # Try the first available fallback source
        fallback_source = fallback_sources[0]
        fallback_passages = self.retriever.full_retrieve_from_source(query, fallback_source)
        
        if fallback_passages:
            fallback_answer = self._generate_answer(fallback_passages, query)
            fallback_quality = self._assess_answer_quality(fallback_answer, fallback_passages)
            
            if fallback_quality > 0.4 and "could not find" not in fallback_answer.lower():
                state = self.state_manager.update_fallback(state, fallback_source, fallback_answer)
                
                if self.config.VERBOSE_LOGGING:
                    print(f"✅ Fallback successful with {fallback_source}")
                
                return {
                    "answer": f"{fallback_answer}\n\n[Retrieved from {fallback_source} after fallback]",
                    "passages": fallback_passages,
                    "sources": [fallback_source]
                }
        
        return None
    
    def _get_source_summary(self, chosen_sources: List[str]) -> str:
        """Get a summary string of chosen sources"""
        if not chosen_sources:
            return "None"
        elif len(chosen_sources) == 1:
            return chosen_sources[0]
        else:
            return f"Multiple ({', '.join(chosen_sources)})