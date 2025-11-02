"""
Scrapper Manager - Centralized service to handle all job scrappers

This module provides a unified interface that abstracts away multiple scrapper
implementations, presenting them as a single scraping service.
"""

from datetime import datetime
from typing import List, Optional

from job_scrapper_contracts import Job, JobDict, ScrapperServiceInterface

from .jobs_data import get_mock_jobs, get_mock_jobs_as_dicts



class ScrapperManager(ScrapperServiceInterface):
    """
    Unified job scraping service that aggregates results from multiple sources.

    This class implements ScrapperServiceInterface and hides the complexity of managing
    multiple scrapper implementations. Users interact with a single, simple interface
    without needing to know about individual scrapper sources.
    """

    def scrape_jobs(
        self,
        salary: int = 4000,
        employment: str = "remote",
        posted_after: Optional[datetime] = None,
        timeout: int = 30
    ) -> List[Job]:
        """
        Scrape jobs from all registered sources and return unified results.

        This method aggregates jobs from all scrapper implementations transparently,
        hiding the complexity of multiple data sources from the user.

        Args:
            salary: Minimum salary filter (default: 4000)
            employment: Employment type filter (default: "remote")
            posted_after: Only return jobs posted after this datetime (default: None, returns all jobs)
            timeout: Request timeout in seconds (default: 30)

        Returns:
            Combined list of Job objects from all sources

        Raises:
            Exception: If any scrapper fails and no results can be returned

        Example:
            >>> from datetime import datetime, timedelta
            >>> manager = ScrapperManager()
            >>> cutoff_date = datetime.now() - timedelta(days=7)
            >>> jobs = manager.scrape_jobs(salary=5000, posted_after=cutoff_date)
            >>> print(f"Found {len(jobs)} jobs total")
        """
        # Return mocked data for testing
        return get_mock_jobs()

    def scrape_jobs_as_dicts(
        self,
        salary: int = 4000,
        employment: str = "remote",
        posted_after: Optional[datetime] = None,
        timeout: int = 30
    ) -> List[JobDict]:
        """
        Scrape jobs from all sources and return as dictionaries.

        This method aggregates jobs from all scrapper implementations and returns
        them as dictionaries, useful for JSON serialization or API responses.

        Args:
            salary: Minimum salary filter (default: 4000)
            employment: Employment type filter (default: "remote")
            posted_after: Only return jobs posted after this datetime (default: None, returns all jobs)
            timeout: Request timeout in seconds (default: 30)

        Returns:
            Combined list of job dictionaries from all sources

        Example:
            >>> from datetime import datetime, timedelta
            >>> cutoff_date = datetime.now() - timedelta(days=7)
            >>> jobs = manager.scrape_jobs_as_dicts(salary=5000, posted_after=cutoff_date)
        """
        # Return mocked data for testing
        return get_mock_jobs_as_dicts()