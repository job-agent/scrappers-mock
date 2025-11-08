"""
Mock scrapper service that mimics the production-facing manager interface.

The module exposes a concrete `ScrapperServiceInterface` implementation that
delegates to the local mock data helpers in `jobs_data`. It keeps the public API
identical to the real service while returning deterministic, in-memory records
for documentation, demos, and automated tests.
"""

from datetime import datetime
from typing import Callable, List, Optional

from job_scrapper_contracts import Job, ScrapperServiceInterface

from .jobs_data import get_mock_jobs


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
        min_salary: int = 4000,
        employment_location: str = "remote",
        posted_after: Optional[datetime] = None,
        timeout: int = 30,
        batch_size: int = 50,
        on_jobs_batch: Optional[Callable[[List[Job], bool], None]] = None,
    ) -> List[Job]:
        """
        Return the mock job listings as concrete `Job` instances.

        The parameters mirror the production service to keep client integrations intact,
        yet the mock ignores every filter and simply relays the static payload from
        `get_mock_jobs`. The helper will raise a `ValueError` if the fake payload cannot
        be materialised as `Job` objects.

        Args:
            min_salary: Part of the public contract; unused by the mock implementation.
            employment_location: Part of the public contract; unused by the mock implementation.
            posted_after: Part of the public contract; unused by the mock implementation.
            timeout: Part of the public contract; unused by the mock implementation.
            batch_size: Controls the number of jobs forwarded to the callback.
            on_jobs_batch: Optional callback receiving each emitted batch and a final flag.

        Returns:
            List of `Job` instances generated from the mock dataset.

        Raises:
            ValueError: Propagated from `get_mock_jobs` when the conversion to `Job`
                fails for any generated record.
        """
        jobs = get_mock_jobs()
        if not on_jobs_batch:
            return jobs

        effective_batch_size = batch_size if batch_size and batch_size > 0 else max(len(jobs), 1)
        buffer: List[Job] = []

        for job in jobs:
            buffer.append(job)
            if len(buffer) == effective_batch_size:
                on_jobs_batch(list(buffer), False)
                buffer.clear()

        if buffer:
            on_jobs_batch(list(buffer), True)
        else:
            on_jobs_batch([], True)

        return jobs
