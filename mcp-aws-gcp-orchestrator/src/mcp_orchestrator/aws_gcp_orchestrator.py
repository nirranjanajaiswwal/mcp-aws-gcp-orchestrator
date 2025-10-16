import asyncio
import json
import re
from typing import Any, Dict, List, Optional
from enum import Enum
from dataclasses import dataclass

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class DataSource(Enum):
    """Enumeration of available data sources"""
    GCP_BIGQUERY = "gcp_bigquery"
    AWS_S3_TABLES = "aws_s3_tables"


@dataclass
class QueryRoute:
    """Represents a query routing decision"""
    source: DataSource
    query: str
    confidence: float
    reason: str


class MCPOrchestrator:
    """
    MCP Orchestrator that routes queries between:
    
    GCP BigQuery - Electric Vehicle Data:
    - vehicle_id: Unique vehicle identifier
    - make: Vehicle manufacturer (Tesla, Ford, BMW, etc.)
    - model: Vehicle model (Model 3, Mustang Mach-E, etc.)
    - year: Manufacturing year
    - range_miles: Electric range in miles
    - battery_capacity_kwh: Battery capacity in kWh
    - state: Registration state
    - registration_date: Vehicle registration date
    
    AWS S3 Tables - State Tax Data (state_local_tax table):
    - state: State code (CA, TX, CO, etc.)
    - state_name: Full state name
    - state_tax_rate: State sales tax rate
    - state_tax_rank: State tax ranking
    - avg_local_tax_rate: Average local tax rate
    - combined_rate: Combined state + local tax rate
    - combined_rank: Combined tax ranking
    - max_local_tax_rate: Maximum local tax rate
    """
    
    def __init__(self):
        self.gcp_session: Optional[ClientSession] = None
        self.aws_session: Optional[ClientSession] = None
        self.gcp_tools = {}
        self.aws_tools = {}
        
        # Keywords for intelligent routing
        self.ev_keywords = [
            'ev', 'electric vehicle', 'charging', 'battery', 'tesla',
            'vehicle', 'car', 'automotive', 'range', 'kwh', 'model',
            'registration', 'charging station'
        ]
        
        self.tax_keywords = [
            'tax', 'tax rate', 'sales tax', 'local tax', 'combined tax',
            'tax rank', 'tax ranking', 'state tax', 'revenue', 'taxation',
            'fiscal', 'state-wise', 'statewise'
        ]
    
    async def connect(self, 
                     gcp_server_command: List[str],
                     aws_server_command: List[str]):
        """Connect to both MCP servers"""
        print("🔗 Connecting to MCP servers...")
        
        try:
            gcp_params = StdioServerParameters(
                command=gcp_server_command[0],
                args=gcp_server_command[1:] if len(gcp_server_command) > 1 else []
            )
            
            aws_params = StdioServerParameters(
                command=aws_server_command[0],
                args=aws_server_command[1:] if len(aws_server_command) > 1 else []
            )
            
            # Store connection info for later use
            self.gcp_params = gcp_params
            self.aws_params = aws_params
            
            print(f"✅ MCP server parameters configured")
            print(f"GCP command: {gcp_server_command}")
            print(f"AWS command: {aws_server_command}")
            
        except Exception as e:
            print(f"❌ Failed to configure MCP servers: {e}")
            raise
    
    def analyze_query(self, query: str) -> QueryRoute:
        """Analyze query and determine routing"""
        query_lower = query.lower()
        
        ev_score = sum(1 for keyword in self.ev_keywords if keyword in query_lower)
        tax_score = sum(1 for keyword in self.tax_keywords if keyword in query_lower)
        
        # Enhanced state detection including abbreviations
        state_pattern = r'\b(california|ca|texas|tx|new york|ny|florida|fl|illinois|il|pennsylvania|pa|ohio|oh|georgia|ga|north carolina|nc|michigan|mi|colorado|co)\b'
        has_state = bool(re.search(state_pattern, query_lower))
        
        # Strong preference for S3 Tables ONLY when querying state tax data
        if has_state and any(keyword in query_lower for keyword in ['tax', 'rate', 'ranking', 'revenue']):
            tax_score += 10  # Very strong preference for tax + state queries
        elif has_state and ev_score == 0:  # Only boost for state if NO EV keywords present
            tax_score += 3   # Moderate preference for state-only queries
        
        # Boost tax score for specific tax-related terms
        if any(term in query_lower for term in ['tax rate', 'sales tax', 'combined rate', 'tax rank']):
            tax_score += 3
        
        if ev_score > tax_score:
            return QueryRoute(
                source=DataSource.GCP_BIGQUERY,
                query=query,
                confidence=min(ev_score / (ev_score + tax_score + 1), 0.95),
                reason=f"Query contains EV-related keywords (score: {ev_score})"
            )
        elif tax_score > ev_score:
            return QueryRoute(
                source=DataSource.AWS_S3_TABLES,
                query=query,
                confidence=min(tax_score / (ev_score + tax_score + 1), 0.95),
                reason=f"Query contains tax/state-related keywords (score: {tax_score})"
            )
        else:
            return QueryRoute(
                source=DataSource.GCP_BIGQUERY,
                query=query,
                confidence=0.5,
                reason="Ambiguous query - defaulting to GCP BigQuery"
            )
    
    async def execute_query(self, route: QueryRoute) -> Dict[str, Any]:
        """Execute query on the appropriate data source"""
        print(f"\n🎯 Routing to: {route.source.value}")
        print(f"📊 Confidence: {route.confidence:.2%}")
        print(f"💡 Reason: {route.reason}\n")
        
        try:
            if route.source == DataSource.GCP_BIGQUERY:
                if not self.gcp_session:
                    raise Exception("GCP session not initialized")
                
                tool_name = self._find_query_tool(self.gcp_tools)
                result = await self.gcp_session.call_tool(
                    tool_name,
                    arguments={"query": route.query}
                )
            else:
                if not self.aws_session:
                    raise Exception("AWS session not initialized")
                
                tool_name = self._find_query_tool(self.aws_tools)
                result = await self.aws_session.call_tool(
                    tool_name,
                    arguments={"query": route.query}
                )
            
            return {
                "status": "success",
                "source": route.source.value,
                "data": result.content,
                "confidence": route.confidence
            }
            
        except Exception as e:
            return {
                "status": "error",
                "source": route.source.value,
                "error": str(e),
                "confidence": route.confidence
            }
    
    def _find_query_tool(self, tools: Dict) -> str:
        """Find the appropriate query tool"""
        query_tools = ['query', 'execute_query', 'run_query', 'sql_query']
        
        for tool_name in query_tools:
            if tool_name in tools:
                return tool_name
        
        if tools:
            return list(tools.keys())[0]
        
        raise Exception("No query tools available")
    
    async def process_query(self, query: str) -> Dict[str, Any]:
        """Main entry point: analyze and execute query"""
        route = self.analyze_query(query)
        
        # Create fresh connection for each query
        if route.source == DataSource.GCP_BIGQUERY:
            async with stdio_client(self.gcp_params) as (read, write):
                session = ClientSession(read, write)
                await session.initialize()
                tools_result = await session.list_tools()
                tools = {tool.name: tool for tool in tools_result.tools}
                
                tool_name = self._find_query_tool(tools)
                result = await session.call_tool(tool_name, arguments={"query": query})
                
                return {
                    "status": "success",
                    "source": route.source.value,
                    "data": result.content,
                    "confidence": route.confidence
                }
        else:
            async with stdio_client(self.aws_params) as (read, write):
                session = ClientSession(read, write)
                await session.initialize()
                tools_result = await session.list_tools()
                tools = {tool.name: tool for tool in tools_result.tools}
                
                tool_name = self._find_query_tool(tools)
                result = await session.call_tool(tool_name, arguments={"query": query})
                
                return {
                    "status": "success",
                    "source": route.source.value,
                    "data": result.content,
                    "confidence": route.confidence
                }
