from backend.Resume.services.grounding_service import GroundingService


def test_skill_grounding():
    service = GroundingService()

    resume_text = """
    Technical Skills:
    Python, FastAPI, React.js, PostgreSQL

    Projects:
    TradeNova

    Built a quantitative risk analysis platform using
    Python, LightGBM, FastAPI and React.js.
    """

    skills = [
        "Python",
        "FastAPI",
        "React",
        "MongoDB",
    ]

    grounded, unresolved = service.ground_skills(
        skills=skills,
        resume_text=resume_text,
    )

    assert "Python" in grounded
    assert "FastAPI" in grounded
    assert "React" in grounded

    assert "MongoDB" in unresolved


def test_java_is_not_matched_inside_javascript():
    service = GroundingService()

    resume_text = """
    Worked extensively with JavaScript applications.
    """

    grounded, unresolved = service.ground_skills(
        skills=["Java"],
        resume_text=resume_text,
    )

    assert "Java" not in grounded
    assert "Java" in unresolved


def test_case_insensitive_matching():
    service = GroundingService()

    resume_text = """
    Technical Skills:
    PYTHON, FASTAPI, PostgreSQL
    """

    grounded, unresolved = service.ground_skills(
        skills=["python", "FastAPI", "postgresql"],
        resume_text=resume_text,
    )

    assert "python" in grounded
    assert "FastAPI" in grounded
    assert "postgresql" in grounded

    assert unresolved == []


def test_react_js_variant():
    service = GroundingService()

    resume_text = """
    Technical Skills:
    React.js
    """

    grounded, unresolved = service.ground_skills(
        skills=["React"],
        resume_text=resume_text,
    )

    assert "React" in grounded
    assert unresolved == []


def test_node_js_variants():
    service = GroundingService()

    resume_text = """
    Backend:
    Node.js
    """

    grounded, unresolved = service.ground_skills(
        skills=["Node JS"],
        resume_text=resume_text,
    )

    assert "Node JS" in grounded
    assert unresolved == []


def test_missing_skill_is_unresolved():
    service = GroundingService()

    resume_text = """
    Technical Skills:
    Python, FastAPI
    """

    grounded, unresolved = service.ground_skills(
        skills=["Python", "Kubernetes"],
        resume_text=resume_text,
    )

    assert "Python" in grounded
    assert "Kubernetes" in unresolved


def test_empty_resume_does_not_ground_skill():
    service = GroundingService()

    grounded, unresolved = service.ground_skills(
        skills=["Python"],
        resume_text="",
    )

    assert grounded == []
    assert unresolved == ["Python"]


def test_empty_skill_is_unresolved():
    service = GroundingService()

    grounded, unresolved = service.ground_skills(
        skills=[""],
        resume_text="Python FastAPI",
    )

    assert grounded == []
    assert unresolved == [""]


def test_word_boundary_prevents_partial_word_match():
    service = GroundingService()

    resume_text = """
    Experience with Dockerized applications.
    """

    grounded, unresolved = service.ground_skills(
        skills=["Docker"],
        resume_text=resume_text,
    )

    assert "Docker" not in grounded
    assert "Docker" in unresolved

def test_project_title_grounding():
    service = GroundingService()

    resume_text = """
    Projects:

    TradeNova

    Built a quantitative risk analysis platform.
    """

    assert service.ground_project_title(
        title="TradeNova",
        resume_text=resume_text,
    ) is True


def test_project_title_not_grounded_when_missing():
    service = GroundingService()

    resume_text = """
    Projects:

    Placeko

    Built an AI-powered career platform.
    """

    assert service.ground_project_title(
        title="TradeNova",
        resume_text=resume_text,
    ) is False


def test_project_technology_grounding():
    service = GroundingService()

    resume_text = """
    TradeNova

    Built using Python, LightGBM, FastAPI and React.js.
    """

    technologies = [
        "Python",
        "LightGBM",
        "FastAPI",
        "React",
        "MongoDB",
    ]

    grounded, unresolved = service.ground_project_technologies(
        technologies=technologies,
        resume_text=resume_text,
    )

    assert "Python" in grounded
    assert "LightGBM" in grounded
    assert "FastAPI" in grounded
    assert "React" in grounded

    assert "MongoDB" in unresolved

def test_node_does_not_match_node_js():
    service = GroundingService()

    resume_text = """
    Backend:
    Node.js
    """

    grounded, unresolved = service.ground_skills(
        skills=["Node"],
        resume_text=resume_text,
    )

    assert "Node" not in grounded
    assert "Node" in unresolved