# MCP Orchestrator

Intelligent routing orchestrator for Model Context Protocol (MCP) servers, specifically designed to route queries between GCP BigQuery (EV data) and AWS S3 Tables (state-wise tax data).

## Features

- 🎯 **Intelligent Query Routing**: Automatically routes queries to the appropriate data source
- 🔗 **Multi-Server Support**: Connects to both GCP BigQuery and AWS S3 Tables MCP servers
- 📊 **Confidence Scoring**: Provides confidence scores for routing decisions
- 🚀 **Easy Integration**: Simple API for processing queries
- ⚛️ **React Frontend**: User-friendly web interface for natural language queries

## Quick Start

### Development Environment

1. **Install Python dependencies:**
   ```bash
   pip install -e ".[dev]"
   pip install -r backend/requirements.txt
   ```

2. **Install React dependencies:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

3. **Start development servers:**
   ```bash
   ./start-dev.sh
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Python API Usage

```python
import asyncio
from mcp_orchestrator import MCPOrchestrator

async def main():
    orchestrator = MCPOrchestrator()
    
    # Configure server commands
    gcp_command = ["python", "-m", "mcp_bigquery_server"]
    aws_command = ["python", "-m", "mcp_s3tables_server"]
    
    # Connect to servers
    await orchestrator.connect(gcp_command, aws_command)
    
    # Process query
    result = await orchestrator.process_query(
        "What is the average range of electric vehicles?"
    )
    print(result)

asyncio.run(main())
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  FastAPI Backend│    │ MCP Orchestrator│
│                 │    │                 │    │                 │
│ - Query Input   │───▶│ - REST API      │───▶│ - Query Routing │
│ - Results UI    │◀───│ - CORS Support  │◀───│ - Server Mgmt   │
│ - Examples      │    │ - Error Handling│    │ - Confidence    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                               ┌────────┴────────┐
                                               ▼                 ▼
                                    ┌─────────────────┐ ┌─────────────────┐
                                    │  GCP BigQuery   │ │  AWS S3 Tables  │
                                    │   (EV Data)     │ │   (Tax Data)    │
                                    └─────────────────┘ └─────────────────┘
```

## Configuration

Set environment variables for server configuration:

```bash
export GCP_MCP_COMMAND="python -m mcp_bigquery_server"
export AWS_MCP_COMMAND="python -m mcp_s3tables_server"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
export GCP_PROJECT_ID="your-project-id"
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-east-1"
```

## Routing Logic

The orchestrator uses keyword-based analysis to route queries:

- **EV Data (BigQuery)**: Queries containing keywords like "ev", "electric vehicle", "charging", "battery", "tesla"
- **Tax Data (S3 Tables)**: Queries containing keywords like "tax", "state", "revenue", plus state names

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type check
mypy src/
```

## Project Structure

```
mcp-aws-gcp-orchestrator/
├── src/
│   └── mcp_orchestrator/
│       ├── __init__.py
│       ├── orchestrator.py
│       └── config.py
├── tests/
│   └── test_orchestrator.py
├── examples/
│   └── basic_usage.py
├── docs/
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
└── README.md
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome! Please read CONTRIBUTING.md first.
