"""
State management for the Multi-Source RAG System using LangGraph
"""

from typing import Dict, List, Any, Optional, TypedDict
from dataclasses import dataclass, field
from enum import Enum

class ProcessingStage(Enum):
    """Enumeration of processing stages"""
    INITIALIZED = "initialized"
    CLASSIFYING = "classifying"
    PROBING = "probing"
    RETRIEVING = "retrieving"
    RERANKING = "reranking"
    GENERATING = "generating"
    QUALITY_CHECK = "quality_check"
    FALLBACK = "fallback"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class ProbeResult:
    """Result from probing a single data source"""
    source_name: str
    passages: List[Dict[str, Any]]
    confidence: float
    retrieval_time: float
    error: Optional[str] = None

@dataclass
class ClassificationResult:
    """Result from query classification"""
    predicted_source: str
    confidence: float
    keyword_scores: Dict[str, int]

@dataclass
class RoutingDecision:
    """Information about routing decision made"""
    chosen_sources: List[str]
    decision_reason: str
    classification_result: ClassificationResult
    probe_results: List[ProbeResult]
    final_confidence: float

class RAGState(TypedDict):
    """State dictionary for LangGraph workflow"""
    
    # Input
    query: str
    
    # Processing stage
    stage: ProcessingStage
    
    # Classification results
    classification: Optional[ClassificationResult]
    
    # Probe results from all sources
    probe_results: List[ProbeResult]
    
    # Full retrieval results
    full_retrieval_results: Dict[str, List[Dict[str, Any]]]
    
    # Reranked results
    reranked_passages: List[Dict[str, Any]]
    
    # Routing decision
    routing_decision: Optional[RoutingDecision]
    
    # Generated answer
    answer: Optional[str]
    answer_quality_score: Optional[float]
    
    # Fallback information
    fallback_attempted: bool
    fallback_source: Optional[str]
    fallback_answer: Optional[str]
    
    # Final results
    final_answer: Optional[str]
    source_used: Optional[str]
    confidence: Optional[float]
    
    # Metadata
    processing_time: Optional[float]
    error: Optional[str]
    routing_info: Optional[Dict[str, Any]]
    
    # Debug information
    debug_info: Dict[str, Any]

class StateManager:
    """Manages state transitions and updates for the RAG workflow"""
    
    def __init__(self):
        self.state_history: List[RAGState] = []
    
    def create_initial_state(self, query: str) -> RAGState:
        """Create initial state for a new query"""
        state = RAGState(
            query=query,
            stage=ProcessingStage.INITIALIZED,
            classification=None,
            probe_results=[],
            full_retrieval_results={},
            reranked_passages=[],
            routing_decision=None,
            answer=None,
            answer_quality_score=None,
            fallback_attempted=False,
            fallback_source=None,
            fallback_answer=None,
            final_answer=None,
            source_used=None,
            confidence=None,
            processing_time=None,
            error=None,
            routing_info=None,
            debug_info={}
        )
        
        self.state_history.append(state)
        return state
    
    def update_stage(self, state: RAGState, new_stage: ProcessingStage) -> RAGState:
        """Update the processing stage"""
        state["stage"] = new_stage
        return state
    
    def update_classification(self, state: RAGState, classification: ClassificationResult) -> RAGState:
        """Update classification results"""
        state["classification"] = classification
        state["stage"] = ProcessingStage.CLASSIFYING
        return state
    
    def add_probe_result(self, state: RAGState, probe_result: ProbeResult) -> RAGState:
        """Add a probe result"""
        state["probe_results"].append(probe_result)
        return state
    
    def update_full_retrieval(self, state: RAGState, source_name: str, 
                            passages: List[Dict[str, Any]]) -> RAGState:
        """Update full retrieval results for a source"""
        state["full_retrieval_results"][source_name] = passages
        return state
    
    def update_reranked_passages(self, state: RAGState, 
                               passages: List[Dict[str, Any]]) -> RAGState:
        """Update reranked passages"""
        state["reranked_passages"] = passages
        state["stage"] = ProcessingStage.RERANKING
        return state
    
    def update_routing_decision(self, state: RAGState, 
                              routing_decision: RoutingDecision) -> RAGState:
        """Update routing decision"""
        state["routing_decision"] = routing_decision
        return state
    
    def update_answer(self, state: RAGState, answer: str, 
                     quality_score: Optional[float] = None) -> RAGState:
        """Update generated answer"""
        state["answer"] = answer
        state["answer_quality_score"] = quality_score
        state["stage"] = ProcessingStage.GENERATING
        return state
    
    def update_fallback(self, state: RAGState, fallback_source: str, 
                       fallback_answer: str) -> RAGState:
        """Update fallback information"""
        state["fallback_attempted"] = True
        state["fallback_source"] = fallback_source
        state["fallback_answer"] = fallback_answer
        state["stage"] = ProcessingStage.FALLBACK
        return state
    
    def finalize_state(self, state: RAGState, final_answer: str, 
                      source_used: str, confidence: float, 
                      processing_time: float) -> RAGState:
        """Finalize the state with results"""
        state["final_answer"] = final_answer
        state["source_used"] = source_used
        state["confidence"] = confidence
        state["processing_time"] = processing_time
        state["stage"] = ProcessingStage.COMPLETED
        
        # Create routing info for response
        if state["routing_decision"]:
            routing = state["routing_decision"]
            state["routing_info"] = {
                "predicted_source": routing.classification_result.predicted_source,
                "classification_confidence": routing.classification_result.confidence,
                "decision_reason": routing.decision_reason,
                "probe_results": {
                    probe.source_name: {
                        "confidence": probe.confidence,
                        "retrieval_time": probe.retrieval_time,
                        "passages_count": len(probe.passages)
                    }
                    for probe in routing.probe_results
                },
                "sharepoint_confidence": next(
                    (p.confidence for p in routing.probe_results if p.source_name == "SharePoint"), 0.0
                ),
                "servicenow_confidence": next(
                    (p.confidence for p in routing.probe_results if p.source_name == "ServiceNow"), 0.0
                )
            }
        
        return state
    
    def set_error(self, state: RAGState, error: str) -> RAGState:
        """Set error state"""
        state["error"] = error
        state["stage"] = ProcessingStage.FAILED
        return state
    
    def add_debug_info(self, state: RAGState, key: str, value: Any) -> RAGState:
        """Add debug information"""
        state["debug_info"][key] = value
        return state
    
    def get_current_stage(self, state: RAGState) -> ProcessingStage:
        """Get current processing stage"""
        return state["stage"]
    
    def is_completed(self, state: RAGState) -> bool:
        """Check if processing is completed"""
        return state["stage"] in [ProcessingStage.COMPLETED, ProcessingStage.FAILED]
    
    def get_state_summary(self, state: RAGState) -> Dict[str, Any]:
        """Get a summary of the current state"""
        return {
            "query": state["query"],
            "stage": state["stage"].value,
            "classification": state["classification"].__dict__ if state["classification"] else None,
            "probe_results_count": len(state["probe_results"]),
            "has_answer": state["answer"] is not None,
            "fallback_attempted": state["fallback_attempted"],
            "error": state["error"],
            "processing_time": state["processing_time"]
        }