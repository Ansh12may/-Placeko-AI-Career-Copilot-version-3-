from backend.Resume.services.grounding_service import GroundingService


def main():
    service = GroundingService()

    resume_text = """
    Ashutosh Kushwaha

    Technical Skills:
    Python, FastAPI, React.js, PostgreSQL, JavaScript, LightGBM

    Projects:

    TradeNova
    Built a quantitative risk analysis platform using
    Python, LightGBM, FastAPI and React.js.
    Used PostgreSQL for persistent data storage.

    Placeko
    Built an AI-powered career platform using Python and FastAPI.
    """

    entities = [
        "PostgreSQL",
        "MongoDB",
        "Machine Learning",
        "React",
        "Java",
    ]

    print("\n========== LLM VERIFIER TEST ==========\n")

    results = service.verify_unresolved_entities(
        entities=entities,
        resume_text=resume_text,
    )

    for result in results:
        print(
            f"Entity: {result['entity']}"
        )
        print(
            f"Status: {result['status']}"
        )
        print(
            f"Reason: {result['reason']}"
        )
        print("-" * 50)


if __name__ == "__main__":
    main()