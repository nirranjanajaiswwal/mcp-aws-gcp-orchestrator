# API Documentation

## MCPOrchestrator Class

The main orchestrator class that handles routing queries between GCP BigQuery and AWS S3 Tables MCP servers.

### Methods

#### `__init__()`
Initialize the orchestrator.

#### `async connect(gcp_command: List[str], aws_command: List[str]) -> None`
Connect to both MCP servers.

**Parameters:**
- `gcp_command`: Command to start the GCP BigQuery MCP server
- `aws_command`: Command to start the AWS S3 Tables MCP server

**Raises:**
- `ConnectionError`: If unable to connect to either server

#### `async disconnect() -> None`
Disconnect from all MCP servers and clean up resources.

#### `async process_query(query: str) -> Dict[str, Any]`
Process a natural language query by routing it to the appropriate server.

**Parameters:**
- `query`: Natural language query string

**Returns:**
Dictionary containing:
- `server`: Which server handled the query ("gcp" or "aws")
- `confidence`: Confidence score for the routing decision (0.0-1.0)
- `result`: Query result from the selected server
- `query`: Original query string

**Example:**
```python
result = await orchestrator.process_query("What is the average range of electric vehicles?")
# Returns: {
#     "server": "gcp",
#     "confidence": 0.95,
#     "result": {...},
#     "query": "What is the average range of electric vehicles?"
# }
```

## REST API Endpoints

When using the FastAPI backend:

### `POST /query`
Process a natural language query.

**Request Body:**
```json
{
    "query": "What is the average range of electric vehicles?"
}
```

**Response:**
```json
{
    "server": "gcp",
    "confidence": 0.95,
    "result": {...},
    "query": "What is the average range of electric vehicles?"
}
```

### `GET /health`
Health check endpoint.

**Response:**
```json
{
    "status": "healthy",
    "servers": {
        "gcp": "connected",
        "aws": "connected"
    }
}
```

## Configuration

### Environment Variables

- `GCP_MCP_COMMAND`: Command to start GCP BigQuery MCP server
- `AWS_MCP_COMMAND`: Command to start AWS S3 Tables MCP server
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to GCP service account credentials
- `GCP_PROJECT_ID`: GCP project ID
- `AWS_ACCESS_KEY_ID`: AWS access key ID
- `AWS_SECRET_ACCESS_KEY`: AWS secret access key
- `AWS_REGION`: AWS region (default: us-east-1)

### Query Routing Logic

The orchestrator uses keyword-based analysis to determine which server should handle each query:

**GCP BigQuery (EV Data):**
- Keywords: "ev", "electric vehicle", "charging", "battery", "tesla", "range", "efficiency"

**AWS S3 Tables (Tax Data):**
- Keywords: "tax", "state", "revenue", plus US state names

**Confidence Scoring:**
- High confidence (0.8+): Multiple relevant keywords found
- Medium confidence (0.5-0.8): Some relevant keywords found
- Low confidence (<0.5): Few or no relevant keywords found
