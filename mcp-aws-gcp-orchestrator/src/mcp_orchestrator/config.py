"""Configuration management for MCP Orchestrator"""

import os
from dataclasses import dataclass
from typing import List


@dataclass
class ServerConfig:
    """Configuration for an MCP server"""
    name: str
    command: List[str]
    env: dict = None


class OrchestratorConfig:
    """Main configuration for the orchestrator"""
    
    def __init__(self):
        self.gcp_server = ServerConfig(
            name="GCP BigQuery",
            command=self._get_gcp_command(),
            env=self._get_gcp_env()
        )
        
        self.aws_server = ServerConfig(
            name="AWS S3 Tables",
            command=self._get_aws_command(),
            env=self._get_aws_env()
        )
    
    def _get_gcp_command(self) -> List[str]:
        """Get GCP server command from environment or default"""
        cmd = os.getenv("GCP_MCP_COMMAND", "python -m mcp_bigquery_server")
        return cmd.split()
    
    def _get_aws_command(self) -> List[str]:
        """Get AWS server command from environment or default"""
        cmd = os.getenv("AWS_MCP_COMMAND", "python -m mcp_s3tables_server")
        return cmd.split()
    
    def _get_gcp_env(self) -> dict:
        """Get GCP environment variables"""
        return {
            "GOOGLE_APPLICATION_CREDENTIALS": os.getenv("GOOGLE_APPLICATION_CREDENTIALS", ""),
            "GCP_PROJECT_ID": os.getenv("GCP_PROJECT_ID", "")
        }
    
    def _get_aws_env(self) -> dict:
        """Get AWS environment variables"""
        return {
            "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID", ""),
            "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY", ""),
            "AWS_REGION": os.getenv("AWS_REGION", "us-east-1")
        }
