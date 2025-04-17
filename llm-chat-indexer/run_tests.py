"""
Test runner script to run all tests or specific test modules.

This script uses pytest to run tests for the LLM Chat Indexer.
It supports running specific test modules, test types (unit, integration),
and provides options for test coverage reporting.
"""

import sys
import argparse
import pytest


def run_tests(test_module=None, test_type=None, coverage=False):
    """
    Run tests using pytest.

    Args:
        test_module (str, optional): Specific test module to run (e.g., 'test_parsing').
            If None, runs all tests.
        test_type (str, optional): Type of tests to run ('unit' or 'integration').
            If None, runs all tests.
        coverage (bool, optional): Whether to generate a coverage report.

    Returns:
        int: pytest exit code (0 for success).
    """
    # Base pytest arguments
    pytest_args = ['-v', '--color=yes']

    # Add coverage if requested
    if coverage:
        pytest_args.extend(['--cov=src', '--cov-report=term', '--cov-report=html'])

    # Add test module if specified
    if test_module:
        if not test_module.startswith('test_'):
            test_module = f'test_{test_module}'
        pytest_args.append(f'tests/{test_module}.py')
    else:
        pytest_args.append('tests')

    # Add test type marker if specified
    if test_type:
        pytest_args.append(f'-m {test_type}')

    # Run pytest
    print(f"Running pytest with args: {' '.join(pytest_args)}")
    return pytest.main(pytest_args)


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run tests for LLM Chat Indexer.')
    parser.add_argument('--module', type=str, help='Specific test module to run (e.g., parsing)')
    parser.add_argument('--type', type=str, choices=['unit', 'integration'],
                        help='Type of tests to run (unit or integration)')
    parser.add_argument('--coverage', action='store_true', help='Generate coverage report')
    args = parser.parse_args()

    sys.exit(run_tests(args.module, args.type, args.coverage))
