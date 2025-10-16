# Contributing to MCP Orchestrator

Thank you for your interest in contributing!

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Code Style

- Use Black for formatting: `black src/ tests/`
- Follow PEP 8 guidelines
- Add type hints to all functions
- Write docstrings for public APIs

## Testing

- Write tests for new features
- Ensure all tests pass: `pytest`
- Maintain code coverage above 80%

## Pull Request Process

1. Create a feature branch
2. Make your changes
3. Add/update tests
4. Update documentation
5. Submit PR with clear description

## Code Review

All submissions require review. We'll provide feedback within 48 hours.
