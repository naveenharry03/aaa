"""
LangChain agent tools for the Multi-Source RAG System
"""

from typing import Dict, Any, List
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from databricks_langchain import ChatDatabricks
from config import Config
from retriever import MultiSourceRetriever
from routing_engine import RoutingEngine
from prompts import REACT_AGENT_PROMPT, RAG_SYSTEM_PROMPT, RAG_USER_PROMPT_TEMPLATE

class RAGTools:
    """Collection of tools for the RAG agent"""
    
    def __init__(self, config: Config, retriever: MultiSourceRetriever, 
                 routing_engine: RoutingEngine, llm):
        self.config = config
        self.retriever = retriever
        self.routing_engine = routing_engine
        self.llm = llm
    
    def create_tools(self) -> List[Tool]:
        """Create all tools for the agent"""
        return [
            Tool(
                name="search_knowledge_base",
                func=self._search_knowledge_base,
                description=(
                    "Search across all configured knowledge bases (SharePoint, ServiceNow, etc.) "
                    "to find relevant information for pipeline errors and technical issues. "
                    "Input should be a clear error message or technical question. "
                    "The tool automatically determines the best data sources to search."
                )
            ),
            Tool(
                name="search_specific_source",
                func=self._search_specific_source,
                description=(
                    "Search a specific data source by name. "
                    "Input format: 'source_name|query' where source_name is SharePoint or ServiceNow. "
                    "Use this when you need to force searching a particular source."
                )
            ),
            Tool(
                name="get_source_info",
                func=self._get_source_info,
                description=(
                    "Get information about available data sources and their capabilities. "
                    "No input required. Returns list of configured sources and their descriptions."
                )
            )
        ]
    
    def _search_knowledge_base(self, query: str) -> str:
        """Main search tool that uses routing engine"""
        try:
            result = self.routing_engine.route_and_retrieve(query)
            
            if result.get("status") == "success":
                answer = result.get("answer", "No answer generated")
                source_info = result.get("source_used", "Unknown")
                confidence = result.get("confidence", 0.0)
                
                # Add metadata to response
                response = f"{answer}\n\n"
                response += f"[Source: {source_info}, Confidence: {confidence:.3f}]"
                
                # Add routing details if verbose
                if self.config.VERBOSE_LOGGING and result.get("routing_info"):
                    routing = result["routing_info"]
                    response += f"\n[Routing: {routing.get('decision_reason', 'Unknown')}]"
                
                return response
            else:
                return f"Search failed: {result.get('error', 'Unknown error')}"
                
        except Exception as e:
            return f"Error during search: {str(e)}"
    
    def _search_specific_source(self, input_str: str) -> str:
        """Search a specific data source"""
        try:
            if "|" not in input_str:
                return "Invalid input format. Use: 'source_name|query'"
            
            source_name, query = input_str.split("|", 1)
            source_name = source_name.strip()
            query = query.strip()
            
            # Validate source name
            available_sources = self.config.get_all_source_names()
            if source_name not in available_sources:
                return f"Invalid source '{source_name}'. Available sources: {', '.join(available_sources)}"
            
            # Retrieve from specific source
            passages = self.retriever.full_retrieve_from_source(query, source_name)
            
            if not passages:
                return f"No relevant information found in {source_name} for query: {query}"
            
            # Generate answer using LLM
            answer = self._generate_answer(passages, query)
            return f"{answer}\n\n[Source: {source_name} (forced), Results: {len(passages)}]"
            
        except Exception as e:
            return f"Error searching specific source: {str(e)}"
    
    def _get_source_info(self, _: str = "") -> str:
        """Get information about available data sources"""
        try:
            info = "Available Data Sources:\n\n"
            
            for source_config in self.config.DATA_SOURCES:
                info += f"📁 {source_config.name}:\n"
                info += f"   Description: {source_config.description}\n"
                info += f"   Keywords: {', '.join(source_config.keywords[:5])}...\n"
                info += f"   Endpoint: {source_config.endpoint_name}\n\n"
            
            info += f"Configuration:\n"
            info += f"   - Probe results: {self.config.PROBE_RESULTS_COUNT}\n"
            info += f"   - Full results: {self.config.FULL_RESULTS_COUNT}\n"
            info += f"   - Reranking: {'Enabled' if self.config.RERANKING_ENABLED else 'Disabled'}\n"
            info += f"   - Fallback: {'Enabled' if self.config.FALLBACK_ENABLED else 'Disabled'}\n"
            
            return info
            
        except Exception as e:
            return f"Error getting source info: {str(e)}"
    
    def _generate_answer(self, passages: List[Dict[str, Any]], query: str) -> str:
        """Generate answer using LLM with retrieved passages"""
        if not passages:
            return "I could not find any relevant information in the provided sources."
        
        # Prepare context with source info
        rag_context = "\n\n".join([
            f"Source: {p.get('source', 'Unknown')}\n"
            f"File: {p.get('file', 'Unknown')}\n"
            f"Chunk ID: {p.get('chunk_id', 'Unknown')}\n"
            f"Text: {p.get('text', '')}"
            for p in passages
        ])

        system_prompt = RAG_SYSTEM_PROMPT
        user_prompt = RAG_USER_PROMPT_TEMPLATE.format(
            context=rag_context,
            question=query
        )

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

class RAGAgent:
    """Main RAG agent using LangChain"""
    
    def __init__(self, config: Config, retriever: MultiSourceRetriever, 
                 routing_engine: RoutingEngine, llm):
        self.config = config
        self.rag_tools = RAGTools(config, retriever, routing_engine, llm)
        self.llm = llm
        
        # Create tools and agent
        self.tools = self.rag_tools.create_tools()
        self.agent = self._create_agent()
        self.agent_executor = self._create_executor()
    
    def _create_agent(self):
        """Create the ReAct agent"""
        prompt = PromptTemplate.from_template(REACT_AGENT_PROMPT)
        
        return create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
    
    def _create_executor(self):
        """Create the agent executor"""
        return AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=self.config.VERBOSE_LOGGING,
            handle_parsing_errors=True,
            max_iterations=5,
            early_stopping_method="generate"
        )
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a query using the agent"""
        try:
            result = self.agent_executor.invoke({"input": query})
            
            return {
                "status": "success",
                "answer": result.get("output", "No answer generated"),
                "intermediate_steps": result.get("intermediate_steps", []),
                "agent_used": True
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "answer": f"Agent processing failed: {str(e)}",
                "agent_used": True
            }