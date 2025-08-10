"""
Main entry point for the Multi-Source RAG Agent System
Handles pipeline error log analysis using SharePoint and ServiceNow data sources
"""

import asyncio
import logging
from typing import Dict, Any
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
        self.config = Config()
        self.orchestrator = MultiSourceRAGOrchestrator(self.config)
        logger.info("Multi-Source RAG System initialized")
    
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

async def main():
    """Main function for testing the system"""
    
    # Initialize the system
    rag_system = MultiSourceRAGSystem()
    
    # Test cases - typical pipeline error messages
    test_cases = [
        "permission denied for this service principal account",
        "database connection timeout error in data pipeline",
        "azure key vault access denied - secret not found",
        "databricks cluster failed to start - insufficient permissions",
        "storage account blob access forbidden error"
    ]
    
    print("🚀 Multi-Source RAG System - Pipeline Error Analysis")
    print("=" * 60)
    
    for i, error_message in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {error_message}")
        print("-" * 50)
        
        try:
            result = await rag_system.process_error_log(error_message)
            
            if result.get("status") == "success":
                print(f"✅ Status: {result['status']}")
                print(f"🎯 Source Used: {result.get('source_used', 'Unknown')}")
                print(f"📊 Confidence: {result.get('confidence', 0):.3f}")
                print(f"💡 Answer: {result.get('answer', 'No answer provided')[:200]}...")
                
                if result.get('routing_info'):
                    routing = result['routing_info']
                    print(f"🔍 Routing Details:")
                    print(f"   - Classification: {routing.get('predicted_source')} ({routing.get('classification_confidence', 0):.2f})")
                    print(f"   - SharePoint Score: {routing.get('sharepoint_confidence', 0):.3f}")
                    print(f"   - ServiceNow Score: {routing.get('servicenow_confidence', 0):.3f}")
            else:
                print(f"❌ Status: {result['status']}")
                print(f"🚨 Error: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Failed to process: {str(e)}")
        
        print()
    
    print("🏁 Testing completed!")

if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())