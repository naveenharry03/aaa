"""
Main entry point for the Multi-Source RAG Agent System
Handles pipeline error log analysis using SharePoint and ServiceNow data sources
"""

import asyncio
import logging
import os
from typing import Dict, Any
from databricks_langchain import ChatDatabricks
import mlflow.deployments

# Import your project modules
from config import Config
from orchestrator import MultiSourceRAGOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MultiSourceRAGSystem:
    """Main system class for handling pipeline error analysis"""
    
    def __init__(self):
        # Initialize configuration
        self.config = Config()
        
        # Initialize Databricks components
        self.vsc_client = self._initialize_vector_search_client()
        self.llm = self._initialize_llm()
        
        # Initialize orchestrator
        self.orchestrator = MultiSourceRAGOrchestrator(
            config=self.config,
            vsc_client=self.vsc_client,
            llm=self.llm
        )
        
        logger.info("Multi-Source RAG System initialized successfully")
    
    def _initialize_vector_search_client(self):
        """Initialize vector search client - replace with your actual implementation"""
        try:
            # TODO: Replace this with your actual vector search client initialization
            # This is a placeholder - you'll need to import and initialize your VSC client
            
            # Example (replace with your actual implementation):
            # from databricks.vector_search.client import VectorSearchClient
            # return VectorSearchClient()
            
            # For now, return a mock object to prevent errors
            class MockVSC:
                def get_index(self, endpoint_name, index_name):
                    class MockIndex:
                        def similarity_search(self, query_vector, columns, num_results):
                            # Mock response structure
                            return {
                                'result': {
                                    'data_array': [
                                        ["Sample chunk text", "sample_file.txt", "chunk_1", 0.85],
                                        ["Another chunk", "another_file.txt", "chunk_2", 0.75]
                                    ]
                                }
                            }
                    return MockIndex()
            
            logger.warning("Using mock vector search client - replace with actual implementation")
            return MockVSC()
            
        except Exception as e:
            logger.error(f"Failed to initialize vector search client: {e}")
            raise
    
    def _initialize_llm(self):
        """Initialize the LLM"""
        try:
            llm = ChatDatabricks(
                endpoint=self.config.LLM_ENDPOINT,
                max_tokens=self.config.MAX_TOKENS,
                temperature=self.config.TEMPERATURE
            )
            logger.info(f"LLM initialized with endpoint: {self.config.LLM_ENDPOINT}")
            return llm
            
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise
    
    async def process_error_log(self, error_message: str) -> Dict[str, Any]:
        """
        Process a pipeline error log message and return analysis results
        
        Args:
            error_message: The error message from pipeline failed logs
            
        Returns:
            Dict containing the analysis results and metadata
        """
        try:
            logger.info(f"Processing error log: {error_message[:100]}...")
            
            # Run the orchestrator
            result = await self.orchestrator.run(error_message)
            
            logger.info("Error log processing completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error processing log: {str(e)}")
            return {
                "error": str(e),
                "status": "failed",
                "message": "Failed to process error log"
            }
    
    def process_error_log_sync(self, error_message: str) -> Dict[str, Any]:
        """Synchronous wrapper for processing error logs"""
        return asyncio.run(self.process_error_log(error_message))

def setup_environment():
    """Setup environment variables and configuration"""
    
    # Set default values if not provided
    os.environ.setdefault("SHAREPOINT_ENDPOINT_NAME", "your_sharepoint_endpoint")
    os.environ.setdefault("SHAREPOINT_INDEX_NAME", "your_sharepoint_index")
    os.environ.setdefault("SERVICENOW_ENDPOINT_NAME", "your_servicenow_endpoint")
    os.environ.setdefault("SERVICENOW_INDEX_NAME", "your_servicenow_index")
    
    print("🔧 Environment Setup:")
    print(f"   SharePoint Endpoint: {os.getenv('SHAREPOINT_ENDPOINT_NAME')}")
    print(f"   SharePoint Index: {os.getenv('SHAREPOINT_INDEX_NAME')}")
    print(f"   ServiceNow Endpoint: {os.getenv('SERVICENOW_ENDPOINT_NAME')}")
    print(f"   ServiceNow Index: {os.getenv('SERVICENOW_INDEX_NAME')}")
    print()

async def run_interactive_mode(rag_system: MultiSourceRAGSystem):
    """Run interactive mode for testing"""
    print("🎯 Interactive Mode - Enter 'quit' to exit")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\n💬 Enter your pipeline error message: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                print("⚠️  Please enter a valid error message")
                continue
            
            print(f"\n🔍 Processing: {user_input}")
            print("=" * 60)
            
            result = await rag_system.process_error_log(user_input)
            
            if result.get("status") == "success":
                print(f"✅ Status: {result['status']}")
                print(f"🎯 Source Used: {result.get('source_used', 'Unknown')}")
                print(f"📊 Confidence: {result.get('confidence', 0):.3f}")
                print(f"⏱️  Processing Time: {result.get('processing_time', 0):.2f}s")
                print(f"\n💡 Answer:")
                print("-" * 30)
                print(result.get('answer', 'No answer provided'))
                
                if result.get('routing_info'):
                    routing = result['routing_info']
                    print(f"\n🔍 Routing Details:")
                    print(f"   - Classification: {routing.get('predicted_source')} ({routing.get('classification_confidence', 0):.2f})")
                    print(f"   - SharePoint Score: {routing.get('sharepoint_confidence', 0):.3f}")
                    print(f"   - ServiceNow Score: {routing.get('servicenow_confidence', 0):.3f}")
                    print(f"   - Decision: {routing.get('decision_reason', 'Unknown')}")
            else:
                print(f"❌ Status: {result['status']}")
                print(f"🚨 Error: {result.get('error', 'Unknown error')}")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

async def run_batch_tests(rag_system: MultiSourceRAGSystem):
    """Run predefined test cases"""
    
    # Test cases - typical pipeline error messages
    test_cases = [
        {
            "name": "Permission Error",
            "message": "permission denied for this service principal account",
            "expected_source": "SharePoint"  # Likely needs documentation on how to fix
        },
        {
            "name": "Database Connection",
            "message": "database connection timeout error in data pipeline",
            "expected_source": "Ambiguous"  # Could be either source
        },
        {
            "name": "Key Vault Access",
            "message": "azure key vault access denied - secret not found",
            "expected_source": "SharePoint"  # Likely needs configuration docs
        },
        {
            "name": "Cluster Start Failure",
            "message": "databricks cluster failed to start - insufficient permissions",
            "expected_source": "SharePoint"  # Likely needs setup documentation
        },
        {
            "name": "Storage Access",
            "message": "storage account blob access forbidden error",
            "expected_source": "SharePoint"  # Likely needs permission setup docs
        },
        {
            "name": "Generic Pipeline Failure",
            "message": "pipeline execution failed with exit code 1",
            "expected_source": "ServiceNow"  # Likely operational/incident data
        }
    ]
    
    print("🚀 Multi-Source RAG System - Batch Testing")
    print("=" * 60)
    
    results_summary = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['name']}")
        print(f"📝 Message: {test_case['message']}")
        print(f"🎯 Expected Source: {test_case['expected_source']}")
        print("-" * 50)
        
        try:
            result = await rag_system.process_error_log(test_case['message'])
            
            if result.get("status") == "success":
                print(f"✅ Status: {result['status']}")
                print(f"🎯 Source Used: {result.get('source_used', 'Unknown')}")
                print(f"📊 Confidence: {result.get('confidence', 0):.3f}")
                print(f"⏱️  Processing Time: {result.get('processing_time', 0):.2f}s")
                print(f"💡 Answer Preview: {result.get('answer', 'No answer')[:150]}...")
                
                # Check if routing matches expectation
                source_used = result.get('source_used', 'Unknown')
                expected = test_case['expected_source']
                
                if expected == "Ambiguous" or expected.lower() in source_used.lower():
                    print("🎉 Routing matches expectation!")
                    routing_correct = True
                else:
                    print(f"⚠️  Routing mismatch - expected {expected}, got {source_used}")
                    routing_correct = False
                
                results_summary.append({
                    "test_case": test_case['name'],
                    "status": "success",
                    "routing_correct": routing_correct,
                    "confidence": result.get('confidence', 0),
                    "processing_time": result.get('processing_time', 0)
                })
                
            else:
                print(f"❌ Status: {result['status']}")
                print(f"🚨 Error: {result.get('error', 'Unknown error')}")
                
                results_summary.append({
                    "test_case": test_case['name'],
                    "status": "failed",
                    "routing_correct": False,
                    "confidence": 0,
                    "processing_time": 0
                })
                
        except Exception as e:
            print(f"❌ Failed to process: {str(e)}")
            results_summary.append({
                "test_case": test_case['name'],
                "status": "error",
                "routing_correct": False,
                "confidence": 0,
                "processing_time": 0
            })
    
    # Print summary
    print("\n" + "="*60)
    print("📊 BATCH TEST SUMMARY")
    print("="*60)
    
    successful_tests = sum(1 for r in results_summary if r['status'] == 'success')
    correct_routing = sum(1 for r in results_summary if r['routing_correct'])
    avg_confidence = sum(r['confidence'] for r in results_summary) / len(results_summary)
    avg_time = sum(r['processing_time'] for r in results_summary) / len(results_summary)
    
    print(f"✅ Successful Tests: {successful_tests}/{len(test_cases)}")
    print(f"🎯 Correct Routing: {correct_routing}/{len(test_cases)}")
    print(f"📊 Average Confidence: {avg_confidence:.3f}")
    print(f"⏱️  Average Processing Time: {avg_time:.2f}s")
    
    print("\n📋 Individual Results:")
    for result in results_summary:
        status_icon = "✅" if result['status'] == 'success' else "❌"
        routing_icon = "🎯" if result['routing_correct'] else "⚠️"
        print(f"   {status_icon} {routing_icon} {result['test_case']}: "
              f"{result['confidence']:.3f} confidence, {result['processing_time']:.2f}s")

async def main():
    """Main function"""
    
    print("🚀 Multi-Source RAG System")
    print("=" * 40)
    
    # Setup environment
    setup_environment()
    
    try:
        # Initialize the system
        print("🔧 Initializing system...")
        rag_system = MultiSourceRAGSystem()
        print("✅ System initialized successfully!\n")
        
        # Choose mode
        print("Select mode:")
        print("1. Batch Tests (predefined test cases)")
        print("2. Interactive Mode (enter your own queries)")
        
        while True:
            choice = input("\nEnter your choice (1 or 2): ").strip()
            
            if choice == "1":
                await run_batch_tests(rag_system)
                break
            elif choice == "2":
                await run_interactive_mode(rag_system)
                break
            else:
                print("⚠️  Please enter 1 or 2")
        
    except Exception as e:
        logger.error(f"System initialization failed: {e}")
        print(f"❌ Failed to initialize system: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check your Databricks endpoint configurations")
        print("2. Ensure vector search client is properly initialized")
        print("3. Verify your environment variables are set correctly")
        return 1
    
    print("\n🏁 Session completed!")
    return 0

if __name__ == "__main__":
    # Run the main function
    exit_code = asyncio.run(main())
    exit(exit_code)