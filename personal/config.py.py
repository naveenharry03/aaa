"""
Configuration settings for the Multi-Source RAG System
"""

import os
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class DataSourceConfig:
    """Configuration for a single data source"""
    name: str
    endpoint_name: str
    index_name: str
    description: str
    keywords: List[str]

@dataclass
class Config:
    """Main configuration class for the RAG system"""
    
    # Databricks endpoints
    EMBEDDINGS_ENDPOINT: str = "your_embeddings_endpoint"
    LLM_ENDPOINT: str = "databricks-meta-llama-3-3-70b-instruct"
    
    # Data sources configuration
    DATA_SOURCES: List[DataSourceConfig] = None
    
    # Retrieval settings
    PROBE_RESULTS_COUNT: int = 3  # Number of results for initial probe
    FULL_RESULTS_COUNT: int = 8   # Number of results for full retrieval
    FINAL_RESULTS_COUNT: int = 5  # Number of final results after reranking
    
    # Routing thresholds
    CLASSIFICATION_CONFIDENCE_THRESHOLD: float = 0.7
    PROBE_SCORE_DIFFERENCE_THRESHOLD: float = 0.1
    DOMINANCE_THRESHOLD: float = 0.6  # If >=60% of top results from one source
    
    # Quality check settings
    MIN_ANSWER_LENGTH: int = 50
    QUALITY_CHECK_ENABLED: bool = True
    FALLBACK_ENABLED: bool = True
    
    # Reranking settings
    RERANKER_MODEL: str = "rank-T5-flan"
    RERANKER_CACHE_DIR: str = "/tmp/flashrank_cache"
    RERANKING_ENABLED: bool = True
    
    # LLM settings
    MAX_TOKENS: int = 300
    TEMPERATURE: float = 0.1
    
    # Logging settings
    VERBOSE_LOGGING: bool = True
    LOG_ROUTING_DECISIONS: bool = True
    
    def __post_init__(self):
        """Initialize data sources configuration"""
        if self.DATA_SOURCES is None:
            self.DATA_SOURCES = [
                DataSourceConfig(
                    name="SharePoint",
                    endpoint_name=os.getenv("SHAREPOINT_ENDPOINT_NAME", "your_sharepoint_endpoint"),
                    index_name=os.getenv("SHAREPOINT_INDEX_NAME", "your_sharepoint_index"),
                    description="Documentation, runbooks, procedures, and how-to guides",
                    keywords=[
                        'how to', 'procedure', 'guide', 'documentation', 'runbook',
                        'policy', 'process', 'steps', 'manual', 'instruction',
                        'configure', 'setup', 'install', 'grant', 'assign'
                    ]
                ),
                DataSourceConfig(
                    name="ServiceNow",
                    endpoint_name=os.getenv("SERVICENOW_ENDPOINT_NAME", "your_servicenow_endpoint"),
                    index_name=os.getenv("SERVICENOW_INDEX_NAME", "your_servicenow_index"),
                    description="Incident records, problem resolutions, and operational alerts",
                    keywords=[
                        'incident', 'ticket', 'inc', 'problem', 'alert', 'failed', 'error',
                        'outage', 'down', 'issue', 'bug', 'failure', 'exception', 'log',
                        'resolved', 'closed', 'workaround', 'root cause'
                    ]
                )
            ]
    
    def get_data_source_by_name(self, name: str) -> DataSourceConfig:
        """Get data source configuration by name"""
        for source in self.DATA_SOURCES:
            if source.name.lower() == name.lower():
                return source
        raise ValueError(f"Data source '{name}' not found")
    
    def get_all_source_names(self) -> List[str]:
        """Get list of all configured data source names"""
        return [source.name for source in self.DATA_SOURCES]