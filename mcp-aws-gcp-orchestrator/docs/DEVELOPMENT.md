# Development Guide

## Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd mcp-aws-gcp-orchestrator
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -e ".[dev]"
   pip install -r backend/requirements.txt
   ```

3. **Install React dependencies:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

### Development Workflow

1. **Start development servers:**
   ```bash
   ./start-dev.sh
   ```
   This starts both the FastAPI backend (port 8000) and React frontend (port 3000).

2. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API docs: http://localhost:8000/docs

### Testing

```bash
# Run Python tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_orchestrator.py
```

### Code Quality

```bash
# Format code
black src/ tests/ backend/

# Lint code
flake8 src/ tests/ backend/

# Type checking
mypy src/
```

### Project Structure

```
mcp-aws-gcp-orchestrator/
├── src/
│   └── mcp_aws_gcp_orchestrator/
│       ├── __init__.py
│       ├── aws_gcp_orchestrator.py
│       └── config.py
├── backend/
│   ├── main.py              # FastAPI application
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── components/
│   ├── public/
│   └── package.json
├── tests/
│   └── test_orchestrator.py
├── examples/
│   └── basic_usage.py
├── docs/
│   ├── API.md
│   └── DEVELOPMENT.md
├── .github/
│   └── workflows/
│       └── tests.yml
├── pyproject.toml
├── requirements.txt
├── start-dev.sh
├── README.md
├── LICENSE
├── CONTRIBUTING.md
└── .gitignore
```

### Environment Configuration

Create a `.env` file in the root directory:

```bash
# GCP Configuration
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
GCP_PROJECT_ID=your-project-id
GCP_MCP_COMMAND=python -m mcp_bigquery_server

# AWS Configuration
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
AWS_MCP_COMMAND=python -m mcp_s3tables_server
```

### Adding New Features

1. **Backend changes:**
   - Modify `src/mcp_aws_gcp_orchestrator/aws_gcp_orchestrator.py`
   - Add tests in `tests/`
   - Update API endpoints in `backend/main.py`

2. **Frontend changes:**
   - Modify React components in `frontend/src/`
   - Update styling in `frontend/src/App.css`

3. **Documentation:**
   - Update `docs/API.md` for API changes
   - Update `README.md` for user-facing changes

### Debugging

1. **Backend debugging:**
   ```bash
   # Run with debug logging
   PYTHONPATH=src python -m uvicorn backend.main:app --reload --log-level debug
   ```

2. **Frontend debugging:**
   ```bash
   cd frontend
   npm start
   # Open browser dev tools for debugging
   ```

### Common Issues

1. **MCP server connection issues:**
   - Ensure MCP servers are installed and accessible
   - Check environment variables are set correctly
   - Verify credentials have proper permissions

2. **CORS issues:**
   - Backend includes CORS middleware for development
   - For production, configure proper CORS origins

3. **Port conflicts:**
   - Backend runs on port 8000
   - Frontend runs on port 3000
   - Change ports in `start-dev.sh` if needed
