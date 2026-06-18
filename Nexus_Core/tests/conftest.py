"""
Pytest configuration for tests.

Configures anyio to only use asyncio backend (not trio).
Checks that the nexus_core package is installed before running tests.
"""

import sys

import pytest


def pytest_configure(config):  # noqa: ARG001
    """Check if package is installed before running tests."""
    try:
        import nexus_core  # noqa: F401
    except ModuleNotFoundError:
        print("\n" + "=" * 70)
        print("ERROR: nexus_core package not installed")
        print("=" * 70)
        print("\nPlease install the package in editable mode first:")
        print("  pip install -e .")
        print("\nOr activate your virtual environment if you already installed it.")
        print("=" * 70 + "\n")
        sys.exit(1)


@pytest.fixture(scope="session")
def anyio_backend():
    """Override anyio backend to only use asyncio (not trio)."""
    return "asyncio"


@pytest.fixture(autouse=True)
def _reset_execution_context():
    """Reset the ExecutionContext singleton before and after every test.

    Without this, a test that calls ExecutionContext.initialize() poisons
    all subsequent tests in the same process.
    """
    from nexus_core.cli.execution_context import ExecutionContext

    ExecutionContext.reset()
    yield
    ExecutionContext.reset()
