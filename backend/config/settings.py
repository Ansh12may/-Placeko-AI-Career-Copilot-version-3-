from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
load_dotenv()
class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
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
