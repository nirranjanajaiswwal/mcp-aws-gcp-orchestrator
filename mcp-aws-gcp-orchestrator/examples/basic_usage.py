#!/usr/bin/env python3
"""
Basic usage example for MCP AWS-GCP Orchestrator.

This example demonstrates how to use the orchestrator to route queries
between GCP BigQuery (EV data) and AWS S3 Tables (tax data).
"""

import asyncio
import os
from mcp_orchestrator import MCPOrchestrator


async def main():
    """Main example function."""
    # Initialize the orchestrator
    orchestrator = MCPOrchestrator()
    
    # Configure server commands (adjust paths as needed)
    gcp_command = ["python", "-m", "mcp_bigquery_server"]
    aws_command = ["python", "-m", "mcp_s3tables_server"]
    
    try:
        # Connect to both servers
        print("Connecting to MCP servers...")
        await orchestrator.connect(gcp_command, aws_command)
        print("Connected successfully!")
        
        # Example queries
        queries = [
            "What is the average range of electric vehicles?",
            "Show me tax revenue by state",
            "How many Tesla vehicles are in the dataset?",
            "What are the top 5 states by tax revenue?",
        ]
        
        # Process each query
        for query in queries:
            print(f"\nQuery: {query}")
            print("-" * 50)
            
            result = await orchestrator.process_query(query)
            
            print(f"Routed to: {result['server']}")
            print(f"Confidence: {result['confidence']:.2f}")
            print(f"Result: {result['result']}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Clean up connections
        await orchestrator.disconnect()
        print("\nDisconnected from servers.")


if __name__ == "__main__":
    # Set up environment variables if needed
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/credentials.json"
    # os.environ["GCP_PROJECT_ID"] = "your-project-id"
    # os.environ["AWS_ACCESS_KEY_ID"] = "your-access-key"
    # os.environ["AWS_SECRET_ACCESS_KEY"] = "your-secret-key"
    
    asyncio.run(main())
