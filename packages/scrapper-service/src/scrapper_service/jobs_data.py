"""Mock job data for testing and development."""

from typing import List

from faker import Faker

from job_scrapper_contracts import Job, JobDict

faker = Faker()


def get_mock_jobs_as_dicts() -> List[JobDict]:
    """Return mock job data as dictionaries."""
    return [
        {
            "job_id": faker.random_int(),
            "title": "Backend Engineer (Python / FastAPI)",
            "url": faker.url(),
            "description": "We are looking for a Backend Engineer to join our data platform team. You'll be responsible for building scalable APIs, integrating ML services, and improving system reliability. Our stack includes FastAPI, PostgreSQL, Redis, and Docker.",
            "company": {"name": faker.name(), "website": faker.url()},
            "category": "Backend",
            "date_posted": "2025-10-31T20:15:00.000000",
            "valid_through": "2025-11-30T20:15:00.000000",
            "employment_type": "FULL_TIME",
            "salary": {"currency": "USD", "min_value": 3500, "max_value": 5000},
            "location": {"region": "Poland", "is_remote": True, "can_apply": False},
            "experience_months": 48.0,
            "industry": "software",
        },
        {
            "job_id": faker.random_int(),
            "title": "Full-stack Engineer (Node.js / Nest.js / React)",
            "url": faker.url(),
            "description": (
                "We are looking for a Full-stack Engineer experienced with Node.js, Nest.js, and React "
                "to join our growing product team. You will build scalable web applications, design robust APIs, "
                "and implement responsive UIs. Our stack includes TypeScript, MongoDB, and Redis for caching and background jobs. "
                "You’ll collaborate closely with backend and frontend engineers to deliver high-performance, maintainable software. "
                "Strong understanding of REST, microservices, and modern frontend development is expected."
            ),
            "company": {"name": faker.company(), "website": faker.url()},
            "category": "Fullstack",
            "date_posted": "2025-10-30T12:00:00.000000",
            "valid_through": "2025-11-29T12:00:00.000000",
            "employment_type": "FULL_TIME",
            "salary": {"currency": "USD", "min_value": 4000, "max_value": 6000},
            "location": {"region": "Poland", "is_remote": True, "can_apply": True},
            "experience_months": 36.0,
            "industry": "software development",
        },
        {
            "job_id": faker.random_int(),
            "title": "DevOps Engineer (AWS / Kubernetes)",
            "url": faker.url(),
            "description": "Looking for an experienced DevOps Engineer to maintain CI/CD pipelines, automate deployments, and manage Kubernetes clusters on AWS. Strong knowledge of Terraform and observability tools required.",
            "company": {"name": faker.name(), "website": faker.url()},
            "category": "DevOps",
            "date_posted": "2025-10-29T10:45:00.000000",
            "valid_through": "2025-11-28T10:45:00.000000",
            "employment_type": "FULL_TIME",
            "salary": {"currency": "USD", "min_value": 4000, "max_value": 6000},
            "location": {"region": "Ukraine", "is_remote": True, "can_apply": True},
            "experience_months": 60.0,
            "industry": "cloud",
        },
        {
            "job_id": faker.random_int(),
            "title": "Frontend Developer (React / TypeScript)",
            "url": faker.url(),
            "description": "We're hiring a Frontend Developer to build intuitive web interfaces and design systems using React and TypeScript. Collaboration with UX designers and backend engineers is a key part of this role.",
            "company": {"name": faker.name(), "website": faker.url()},
            "category": "Frontend",
            "date_posted": "2025-10-27T16:30:00.000000",
            "valid_through": "2025-11-26T16:30:00.000000",
            "employment_type": "FULL_TIME",
            "salary": {"currency": "USD", "min_value": 2500, "max_value": 4000},
            "location": {"region": "Portugal", "is_remote": True, "can_apply": True},
            "experience_months": 36.0,
            "industry": "software",
        },
        {
            "job_id": faker.random_int(),
            "title": "AI Research Engineer",
            "url": faker.url(),
            "description": "Work with the latest LLM and multimodal architectures. Your mission is to fine-tune and deploy state-of-the-art AI models for text and image understanding tasks.",
            "company": {"name": faker.name(), "website": faker.url()},
            "category": "AI",
            "date_posted": "2025-10-28T11:00:00.000000",
            "valid_through": "2025-11-27T11:00:00.000000",
            "employment_type": "FULL_TIME",
            "salary": {"currency": "USD", "min_value": 5000, "max_value": 8000},
            "location": {"region": "USA", "is_remote": True, "can_apply": True},
            "experience_months": 72.0,
            "industry": "artificial intelligence",
        },
        {
            "job_id": faker.random_int(),
            "title": "Product Manager (EdTech)",
            "url": faker.url(),
            "description": "We're looking for a Product Manager to lead roadmap development and feature delivery for our online learning platform. You'll collaborate closely with design, marketing, and engineering teams.",
            "company": {"name": faker.name(), "website": faker.url()},
            "category": "Product",
            "date_posted": "2025-10-25T09:15:00.000000",
            "valid_through": "2025-11-24T09:15:00.000000",
            "employment_type": "FULL_TIME",
            "salary": {"currency": "USD", "min_value": 3000, "max_value": 4500},
            "location": {"region": "Romania", "is_remote": False, "can_apply": True},
            "experience_months": 48.0,
            "industry": "education",
        },
        {
            "job_id": faker.random_int(),
            "title": "AI Engineer (Python / LangChain / LangGraph)",
            "url": faker.url(),
            "description": (
                "We are seeking an AI Engineer to design and implement intelligent, multi-agent systems "
                "using Python, LangChain, and LangGraph. You will build pipelines that integrate large language models "
                "with external tools, vector databases, and retrieval systems. Responsibilities include designing agent workflows, "
                "evaluating model performance, and deploying production-grade AI systems. "
                "Experience with OpenAI APIs, embeddings, and asynchronous Python is a strong plus."
            ),
            "company": {"name": "Cognify Labs", "website": faker.url()},
            "category": "AI",
            "date_posted": "2025-10-26T14:45:00.000000",
            "valid_through": "2025-11-25T14:45:00.000000",
            "employment_type": "FULL_TIME",
            "salary": {"currency": "USD", "min_value": 5000, "max_value": 7000},
            "location": {"region": "Ukraine", "is_remote": True, "can_apply": True},
            "experience_months": 48.0,
            "industry": "artificial intelligence",
        },
        {
            "job_id": faker.random_int(),
            "title": "UX/UI Designer",
            "url": faker.url(),
            "description": "Join our design team to create clean, accessible, and delightful user experiences across mobile and web. You'll work closely with developers and product managers to shape our design system.",
            "company": {"name": faker.name(), "website": faker.url()},
            "category": "Design",
            "date_posted": "2025-10-29T17:10:00.000000",
            "valid_through": "2025-11-28T17:10:00.000000",
            "employment_type": "FULL_TIME",
            "salary": {"currency": "USD", "min_value": 2000, "max_value": 3000},
            "location": {"region": "Ukraine", "is_remote": False, "can_apply": True},
            "experience_months": 24.0,
            "industry": "design",
        },
        {
            "job_id": faker.random_int(),
            "title": "Customer Success Manager",
            "url": faker.url(),
            "description": "We're expanding our customer success team! You'll ensure clients achieve their business goals using our SaaS platform, drive renewals, and collect product feedback.",
            "company": {"name": faker.name(), "website": faker.url()},
            "category": "Customer Success",
            "date_posted": "2025-10-30T13:30:00.000000",
            "valid_through": "2025-11-29T13:30:00.000000",
            "employment_type": "FULL_TIME",
            "salary": {"currency": "USD", "min_value": 2500, "max_value": 4000},
            "location": {"region": "United Kingdom", "is_remote": True, "can_apply": True},
            "experience_months": 48.0,
            "industry": "saas",
        },
        {
            "job_id": faker.random_int(),
            "title": "Marketing Copywriter",
            "url": faker.url(),
            "description": "We're seeking a creative copywriter to craft engaging marketing materials across social, email, and landing pages. You'll work in a fast-paced team that values clarity and storytelling.",
            "company": {"name": faker.name(), "website": faker.url()},
            "category": "Marketing",
            "date_posted": "2025-10-31T08:45:00.000000",
            "valid_through": "2025-11-30T08:45:00.000000",
            "employment_type": "PART_TIME",
            "salary": {"currency": "USD", "min_value": 1500, "max_value": 2200},
            "location": {"region": "Ukraine", "is_remote": True, "can_apply": True},
            "experience_months": 24.0,
            "industry": "marketing",
        },
    ]


def get_mock_jobs() -> List[Job]:
    """
    Return mock job data as Job instances.

    This function converts the dictionary data into Job objects using the
    Job class constructor or from_dict method.
    """
    job_dicts = get_mock_jobs_as_dicts()

    # Convert dictionaries to Job instances
    # Assuming Job class has a from_dict class method or accepts dict in constructor
    jobs = []
    for job_dict in job_dicts:
        try:
            # Try using from_dict method if available
            if hasattr(Job, 'from_dict'):
                jobs.append(Job.from_dict(job_dict))
            else:
                # Try unpacking the dict as kwargs
                jobs.append(Job(**job_dict))
        except Exception as e:
            # If conversion fails, you may need to adjust based on Job class structure
            raise ValueError(f"Failed to convert job dict to Job instance: {e}")

    return jobs


# For backward compatibility and convenience
MOCK_JOBS_DICTS = get_mock_jobs_as_dicts()
