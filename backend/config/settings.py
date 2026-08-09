from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
load_dotenv()
class Settings:
    RAPID_API_KEY = os.getenv("RAPID_API_KEY")      
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    MONGODB_URL = os.getenv("MONGODB_URL")
    DATABASE_NAME= os.getenv("DATABASE_NAME")
    JWT_SECRET_KEY= os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",30))
    REFRESH_TOKEN_EXPIRE_DAYS=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS",7))

    PINECONE_INDEX_NAME = os.getenv(
        "PINECONE_INDEX_NAME",
        "careercopilot"
    )

    GROQ_MODEL = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-120b"
    )
    TEMPERATURE = float(
        os.getenv("TEMPERATURE", 0)
    )
    @property
    def llm(self):
        return ChatGroq(
            api_key=self.GROQ_API_KEY,
            model=self.GROQ_MODEL,
            temperature=self.TEMPERATURE,
        )
settings = Settings()

