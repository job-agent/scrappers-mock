"""Pytest configuration and fixtures for quality tests."""

from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).parent.parent
PACKAGES_DIR = PROJECT_ROOT / "packages"


@pytest.fixture
def project_root() -> Path:
    """Return the project root directory path."""
    return PROJECT_ROOT


@pytest.fixture
def packages_dir() -> Path:
    """Return the packages directory path."""
    return PACKAGES_DIR
