import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # vLLM Server
    VLLM_BASE_URL: str = os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1")
    VLLM_API_KEY: str = os.getenv("VLLM_API_KEY", "sk-no-key-required")
    VLLM_MODEL_NAME: str = os.getenv("VLLM_MODEL_NAME", "Qwen/Qwen2.5-Math-7B-Instruct")

    # FastAPI Server
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8080"))

    # CORS
    CORS_ORIGINS: list[str] = os.getenv(
        "CORS_ORIGINS", "http://localhost:3000,http://localhost:5173"
    ).split(",")

    # Mode
    MOCK_MODE: bool = os.getenv("MOCK_MODE", "true").lower() == "true"


settings = Settings()
