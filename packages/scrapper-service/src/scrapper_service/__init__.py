"""
Mock scrapper service package that surfaces the contract-compatible manager.

Importing the package exposes `ScrapperManager`, a stand-in implementation that
delivers fabricated job listings for integration tests and demos.
"""

from .manager import ScrapperManager

__all__ = ["ScrapperManager"]