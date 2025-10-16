"""Tests for MCP Orchestrator"""

import pytest
from mcp_orchestrator import MCPOrchestrator, DataSource


def test_orchestrator_initialization():
    """Test orchestrator initialization"""
    orchestrator = MCPOrchestrator()
    assert orchestrator.gcp_session is None
    assert orchestrator.aws_session is None


def test_ev_query_routing():
    """Test EV query routing"""
    orchestrator = MCPOrchestrator()
    route = orchestrator.analyze_query("What is the range of Tesla Model 3?")
    assert route.source == DataSource.GCP_BIGQUERY


def test_tax_query_routing():
    """Test tax query routing"""
    orchestrator = MCPOrchestrator()
    route = orchestrator.analyze_query("Show California state tax data")
    assert route.source == DataSource.AWS_S3_TABLES


def test_ambiguous_query():
    """Test ambiguous query routing"""
    orchestrator = MCPOrchestrator()
    route = orchestrator.analyze_query("Show me data")
    assert route.confidence == 0.5
