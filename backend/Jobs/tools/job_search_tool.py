"""
Job Search Tool
Responsible for communicating with the external JSearch API.
Responsibilities:
- Send job-search requests to JSearch.
- Receive fresh job postings.
- Convert external API responses into the internal Job schema.
"""

from typing import List
import requests
from backend.config.settings import settings
from backend.Jobs.schemas.job import Job


class JobSearchTool:

    def __init__(self):
        self.base_url = (
            "https://jsearch.p.rapidapi.com/search"
        )

        self.headers = {
            "X-RapidAPI-Key": settings.RAPID_API_KEY,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
        }

    # Search Jobs
   
    def search_jobs(self,query: str,country: str = "in",page: int = 1) -> List[Job]:
        """
        Search JSearch for fresh job postings.

        Args:
            query:
                Search query generated from the CandidateProfile.

            country:
                ISO country code used by JSearch.
                Defaults to India ("in").

            page:
                JSearch result page.

        Returns:
            List[Job]:
                Fresh jobs converted to the internal Job schema.
        """

        if not query.strip():
            raise ValueError(
                "Job search query cannot be empty."
            )

        params = {
            "query": query,
            "page": page,
            "num_pages": 2,
            "country": country,
        }

        try:
            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params,
                timeout=80,
            )

            response.raise_for_status()

            data = response.json()

        except requests.RequestException as error:
            raise RuntimeError(
                f"Job Search API Error: {error}"
            ) from error

        except ValueError as error:
            raise RuntimeError(
                "JSearch returned an invalid JSON response."
            ) from error

        # JSearch stores job postings under "data".

        jobs = [
            self._map_to_job(item)
            for item in data.get("data", [])
            if isinstance(item, dict)
        ]
        return jobs

   
    # Map API Response → Job
   

    def _map_to_job(self,item: dict) -> Job:
        """
        Convert one JSearch API response item into
        the application's internal Job schema.
        """
        return Job(
            job_id=item.get("job_id"),
            title=item.get(
                "job_title",
                "",
            ),
            company=item.get(
                "employer_name",
                "",
            ),
            location=item.get(
                "job_location",
                "",
            ),
            employment_type=item.get(
                "job_employment_type"
            ),
            experience=None,
            salary=item.get(
                "job_salary_string"
            ),
            skills=self._extract_skills(
                item
            ),
            description=item.get(
                "job_description",
                "",
            ),
            apply_url=item.get(
                "job_apply_link"
            ),
            source=item.get(
                "job_publisher",
                "Unknown",
            ),
        )

    # Extract Skills
   

    def _extract_skills(self,item: dict) -> List[str]:
        """
        Return structured skills from the JSearch job.

        JSearch does not provide a reliable structured
        skills field in the response used by this application.

        Therefore, skills are currently left empty.

        Skill extraction should remain separate from the
        core job-search → Pinecone pipeline unless a dedicated
        extraction stage is introduced later.
        """

        return []