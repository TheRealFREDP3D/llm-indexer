"""
Test runner script to run all tests or specific test modules.
"""

import unittest
import sys
import argparse


def run_tests(test_module=None):
    """
    Run tests in the tests directory.

    Args:
        test_module (str, optional): Specific test module to run (e.g., 'test_parsing').
            If None, runs all tests.

    Returns:
        int: 0 if tests were successful, 1 otherwise.
    """
    # Set up the test runner
    test_runner = unittest.TextTestRunner(verbosity=2)

    if test_module:
        # Run a specific test module
        print(f"Running tests in {test_module}...")
        try:
            module = __import__(f'tests.{test_module}', fromlist=[''])
            test_suite = unittest.defaultTestLoader.loadTestsFromModule(module)
            result = test_runner.run(test_suite)
        except ImportError:
            print(f"Error: Test module 'tests.{test_module}' not found.")
            return 1
    else:
        # Discover and run all tests
        print("Running all tests...")
        test_suite = unittest.defaultTestLoader.discover('tests')
        result = test_runner.run(test_suite)

    # Return non-zero exit code if tests failed
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run tests for LLM Chat Indexer.')
    parser.add_argument('--module', type=str, help='Specific test module to run (e.g., test_parsing)')
    args = parser.parse_args()

    sys.exit(run_tests(args.module))
