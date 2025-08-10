"""
Multi-source retrieval system for SharePoint and ServiceNow data
"""

import time
import mlflow.deployments
from typing import List, Dict, Any, Tuple, Optional
from flashrank import Ranker, RerankRequest
from config import Config, DataSourceConfig
from state_manager import ProbeResult, ClassificationResult

class MultiSourceRetriever:
    """Handles retrieval from multiple data sources with reranking"""
    
    def __init__(self, config: Config, vsc_client):
        self.config = config
        self.vsc = vsc_client
        self.deploy_client = mlflow.deployments.get_deploy_client("databricks")
        
        # Initialize reranker if enabled
        self.ranker = None
        if config.RERANKING_ENABLED:
            self.ranker = Ranker(
                model_name=config.RERANKER_MODEL,
                cache_dir=config.RERANKER_CACHE_DIR
            )
    
    def get_embeddings(self, query: str) -> List[float]:
        """Get embeddings for a query"""
        try:
            response = self.deploy_client.predict(
                endpoint=self.config.EMBEDDINGS_ENDPOINT,
                inputs={"input": [query]}
            )
            return [e['embedding'] for e in response.data][0]
        except Exception as e:
            raise Exception(f"Failed to get embeddings: {str(e)}")
    
    def retrieve_from_source(self, query: str, source_config: DataSourceConfig, 
                           num_results: int = 5) -> Tuple[List[Dict[str, Any]], float]:
        """Retrieve and rerank results from a single source"""
        start_time = time.time()
        
        try:
            # Get embeddings
            embeddings = self.get_embeddings(query)
            
            # Vector search
            results = self.vsc.get_index(
                endpoint_name=source_config.endpoint_name,
                index_name=source_config.index_name
            ).similarity_search(
                query_vector=embeddings,
                columns=["chunk_text", "file_name", "chunk_id"],
                num_results=num_results
            )
            
            # Format passages
            passages = []
            for doc in results.get('result', {}).get('data_array', []):
                passage = {
                    "file": doc[1],
                    "text": doc[0],
                    "chunk_id": doc[2],
                    "score": doc[3],
                    "source": source_config.name
                }
                passages.append(passage)
            
            if not passages:
                return [], 0.0
            
            # Rerank if enabled
            if self.config.RERANKING_ENABLED and self.ranker:
                rerank_request = RerankRequest(query=query, passages=passages)
                reranked_results = self.ranker.rerank(rerank_request)
                passages = reranked_results
            
            # Calculate confidence (average of top 3 scores)
            top_scores = [p.score for p in passages[:3]]
            confidence = sum(top_scores) / len(top_scores) if top_scores else 0.0
            
            retrieval_time = time.time() - start_time
            return passages, confidence
            
        except Exception as e:
            retrieval_time = time.time() - start_time
            if self.config.VERBOSE_LOGGING:
                print(f"Error retrieving from {source_config.name}: {str(e)}")
            return [], 0.0
    
    def probe_all_sources(self, query: str) -> List[ProbeResult]:
        """Probe all configured data sources with small k"""
        probe_results = []
        
        for source_config in self.config.DATA_SOURCES:
            start_time = time.time()
            
            try:
                passages, confidence = self.retrieve_from_source(
                    query, source_config, self.config.PROBE_RESULTS_COUNT
                )
                
                retrieval_time = time.time() - start_time
                
                probe_result = ProbeResult(
                    source_name=source_config.name,
                    passages=passages,
                    confidence=confidence,
                    retrieval_time=retrieval_time
                )
                
                if self.config.VERBOSE_LOGGING:
                    print(f"🔬 Probe {source_config.name}: {confidence:.3f} confidence, "
                          f"{len(passages)} passages, {retrieval_time:.2f}s")
                
            except Exception as e:
                retrieval_time = time.time() - start_time
                probe_result = ProbeResult(
                    source_name=source_config.name,
                    passages=[],
                    confidence=0.0,
                    retrieval_time=retrieval_time,
                    error=str(e)
                )
                
                if self.config.VERBOSE_LOGGING:
                    print(f"❌ Probe {source_config.name} failed: {str(e)}")
            
            probe_results.append(probe_result)
        
        return probe_results
    
    def full_retrieve_from_source(self, query: str, source_name: str) -> List[Dict[str, Any]]:
        """Perform full retrieval from a specific source"""
        source_config = self.config.get_data_source_by_name(source_name)
        passages, _ = self.retrieve_from_source(
            query, source_config, self.config.FULL_RESULTS_COUNT
        )
        return passages
    
    def global_rerank(self, query: str, all_passages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Perform global reranking across all passages"""
        if not self.config.RERANKING_ENABLED or not self.ranker or not all_passages:
            return all_passages[:self.config.FINAL_RESULTS_COUNT]
        
        try:
            rerank_request = RerankRequest(query=query, passages=all_passages)
            reranked_results = self.ranker.rerank(rerank_request)
            return reranked_results[:self.config.FINAL_RESULTS_COUNT]
        except Exception as e:
            if self.config.VERBOSE_LOGGING:
                print(f"Global reranking failed: {str(e)}")
            return all_passages[:self.config.FINAL_RESULTS_COUNT]

class QueryClassifier:
    """Classifies queries to predict the best data source"""
    
    def __init__(self, config: Config):
        self.config = config
    
    def classify_query(self, query: str) -> ClassificationResult:
        """Classify query to predict best data source"""
        query_lower = query.lower()
        keyword_scores = {}
        
        # Calculate keyword scores for each source
        for source_config in self.config.DATA_SOURCES:
            score = sum(1 for keyword in source_config.keywords if keyword in query_lower)
            keyword_scores[source_config.name] = score
        
        # Find the source with highest score
        if not keyword_scores or all(score == 0 for score in keyword_scores.values()):
            # No keywords matched - ambiguous
            return ClassificationResult(
                predicted_source="ambiguous",
                confidence=0.5,
                keyword_scores=keyword_scores
            )
        
        best_source = max(keyword_scores.keys(), key=lambda k: keyword_scores[k])
        total_score = sum(keyword_scores.values())
        confidence = keyword_scores[best_source] / (total_score + 1) if total_score > 0 else 0.5
        
        return ClassificationResult(
            predicted_source=best_source,
            confidence=confidence,
            keyword_scores=keyword_scores
        )