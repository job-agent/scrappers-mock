"""
Mock scrapper service that mimics the production-facing manager interface.

The module exposes a concrete `ScrapperServiceInterface` implementation that
delegates to the local mock data helpers in `jobs_data`. It keeps the public API
identical to the real service while returning deterministic, in-memory records
for documentation, demos, and automated tests.
"""

from datetime import datetime
from typing import List, Optional

from job_scrapper_contracts import Job, JobDict, ScrapperServiceInterface

from .jobs_data import get_mock_jobs, get_mock_jobs_as_dicts


class ScrapperManager(ScrapperServiceInterface):
    """
    Facade that returns mock job listings while honouring the production contract.

    The manager accepts the same signature as the real scrapper service so client code
    can exercise the integration without hitting network providers. Internally it
    proxies to `get_mock_jobs` and `get_mock_jobs_as_dicts`, ignoring filter arguments
    and always serving the static dataset.
    """

    def scrape_jobs(
        self,
        salary: int = 4000,
        employment: str = "remote",
        posted_after: Optional[datetime] = None,
        timeout: int = 30,
    ) -> List[Job]:
        """
        Return the mock job listings as concrete `Job` instances.

        The parameters mirror the production service to keep client integrations intact,
        yet the mock ignores every filter and simply relays the static payload from
        `get_mock_jobs`. The helper will raise a `ValueError` if the fake payload cannot
        be materialised as `Job` objects.

        Args:
            salary: Part of the public contract; unused by the mock implementation.
            employment: Part of the public contract; unused by the mock implementation.
            posted_after: Part of the public contract; unused by the mock implementation.
            timeout: Part of the public contract; unused by the mock implementation.

        Returns:
            List of `Job` instances generated from the mock dataset.

        Raises:
            ValueError: Propagated from `get_mock_jobs` when the conversion to `Job`
                fails for any generated record.
        """
        return get_mock_jobs()

    def scrape_jobs_as_dicts(
        self,
        salary: int = 4000,
        employment: str = "remote",
        posted_after: Optional[datetime] = None,
        timeout: int = 30,
    ) -> List[JobDict]:
        """
        Return the mock job listings in serialisable dictionary form.

        Just like `scrape_jobs`, the method keeps the production call signature so
        downstream code can test error handling and data flows. The mock ignores the
        parameters and relays the dictionaries produced by `get_mock_jobs_as_dicts`.

        Args:
            salary: Part of the public contract; unused by the mock implementation.
            employment: Part of the public contract; unused by the mock implementation.
            posted_after: Part of the public contract; unused by the mock implementation.
            timeout: Part of the public contract; unused by the mock implementation.

        Returns:
            List of dictionaries that share the schema of production job payloads.
        """
        return get_mock_jobs_as_dicts()
