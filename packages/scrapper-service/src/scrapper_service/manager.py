from typing import Callable, List, Optional

from job_scrapper_contracts import Job, ScrapeJobsFilter, ScrapperServiceInterface

from .jobs_data import get_mock_jobs


class ScrapperManager(ScrapperServiceInterface):
    def scrape_jobs(
        self,
        filters: ScrapeJobsFilter,
        timeout: int = 30,
        batch_size: int = 50,
        on_jobs_batch: Optional[Callable[[List[Job], bool], None]] = None,
    ) -> List[Job]:
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
