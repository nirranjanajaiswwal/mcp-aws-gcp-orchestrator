"""
MCP Orchestrator - Intelligent routing for BigQuery and S3 Tables
"""

__version__ = "0.1.0"
__author__ = "Nirranjana Jaiswwal"

from .aws_gcp_orchestrator import MCPOrchestrator, DataSource, QueryRoute

__all__ = ["MCPOrchestrator", "DataSource", "QueryRoute"]
