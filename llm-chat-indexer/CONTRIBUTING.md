# Contributing to LLM Chat Indexer

Thank you for your interest in contributing to LLM Chat Indexer! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to foster an inclusive and respectful community.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment (see below)
4. Create a new branch for your feature or bug fix
5. Make your changes
6. Run tests to ensure your changes don't break existing functionality
7. Submit a pull request

## Development Environment

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- git

### Setup

1. Clone your fork of the repository:

```bash
git clone https://github.com/yourusername/llm-chat-indexer.git
cd llm-chat-indexer
```

2. Create and activate a virtual environment:

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

4. Download the Spacy language model:

```bash
python -m spacy download en_core_web_sm
```

5. Set up pre-commit hooks:

```bash
pre-commit install
```

## Coding Standards

We follow these coding standards:

- **PEP 8**: For Python code style
- **Black**: For code formatting
- **isort**: For import sorting
- **Flake8**: For linting

You can check your code with:

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .
```

### Docstrings

Use Google-style docstrings for all functions, classes, and modules:

```python
def example_function(param1, param2):
    """
    Brief description of the function.
    
    Args:
        param1 (type): Description of param1.
        param2 (type): Description of param2.
        
    Returns:
        type: Description of return value.
        
    Raises:
        ExceptionType: When and why this exception is raised.
    """
    # Function implementation
```

## Pull Request Process

1. Create a new branch for your feature or bug fix:

```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit them with clear, descriptive commit messages:

```bash
git commit -m "Add feature X" -m "This feature adds functionality to do X, which helps with Y."
```

3. Push your branch to your fork:

```bash
git push origin feature/your-feature-name
```

4. Submit a pull request to the main repository's `main` branch
5. Ensure all CI checks pass
6. Address any feedback from reviewers
7. Once approved, your PR will be merged

## Testing

We use pytest for testing. All new features should include tests, and bug fixes should include tests that verify the fix.

### Running Tests

```bash
# Run all tests
python run_tests.py

# Run specific test modules
python run_tests.py --module test_parsing

# Run with coverage report
python run_tests.py --coverage
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with the prefix `test_`
- Name test functions with the prefix `test_`
- Use descriptive test names that explain what is being tested
- Use fixtures from `conftest.py` where appropriate

Example test:

```python
def test_json_parser_with_valid_input():
    """Test that the JSON parser correctly parses valid input."""
    parser = JSONParser()
    result = parser.parse('{"messages": [{"role": "user", "content": "Hello"}]}')
    assert len(result) == 1
    assert result[0]["role"] == "user"
    assert result[0]["content"] == "Hello"
```

## Documentation

Good documentation is essential. Please update documentation when you make changes:

- Update docstrings for any modified code
- Update README.md if your changes affect usage
- Update API.md if your changes affect the API
- Add examples for new features

## Issue Reporting

If you find a bug or have a feature request, please create an issue on GitHub:

1. Check if the issue already exists
2. Use the appropriate issue template
3. Provide as much detail as possible:
   - For bugs: steps to reproduce, expected behavior, actual behavior, and environment details
   - For features: clear description of the feature and its benefits

## License

By contributing to LLM Chat Indexer, you agree that your contributions will be licensed under the project's MIT License.
