"""
config.py

Centralized configuration for the RAG project.
Loads environment variables and exposes typed constants used across
ingest.py, retrieve.py, prompt.py, and app.py.
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load variables from .env into the process environment.
# This must happen before we read any os.getenv() calls below.
load_dotenv()


def _require_env(key: str) -> str:
    """
    Fetch a required environment variable or raise a clear error.

    Why a helper function instead of os.getenv(key) directly:
    If OPENAI_API_KEY is missing, we want the program to fail
    immediately and explicitly, not three files later inside an
    OpenAI SDK call with a cryptic 401 error.
    """
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(
            f"Missing required environment variable: '{key}'. "
            f"Did you create a .env file from .env.example?"
        )
    return value


@dataclass(frozen=True)
class Config:
    """
    Immutable configuration object.

    Why a frozen dataclass instead of plain module-level variables:
    - frozen=True prevents accidental mutation at runtime (e.g. some
      other file doing `config.CHUNK_SIZE = 9999` by mistake).
    - Grouping related settings into one object makes it easy to pass
      a single `cfg` argument around instead of importing a dozen
      loose names everywhere.
    """

    # --- Secrets ---
    openai_api_key: str

    # --- Model configuration ---
    embedding_model: str
    chat_model: str
    chat_temperature: float

    # --- Chunking configuration ---
    chunk_size: int
    chunk_overlap: int

    # --- Retrieval configuration ---
    top_k: int

    # --- Paths ---
    data_path: str
    vectorstore_dir: str


def load_config() -> Config:
    """
    Build and return a Config instance from environment variables,
    falling back to sensible defaults where appropriate.
    """
    return Config(
        openai_api_key=_require_env("OPENAI_API_KEY"),

        embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
        chat_model=os.getenv("CHAT_MODEL", "gpt-4o-mini"),
        chat_temperature=float(os.getenv("CHAT_TEMPERATURE", "0.0")),

        chunk_size=int(os.getenv("CHUNK_SIZE", "1000")),
        chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "200")),

        top_k=int(os.getenv("TOP_K", "4")),

        data_path=os.getenv("DATA_PATH", "data/knowledge.txt"),
        vectorstore_dir=os.getenv("VECTORSTORE_DIR", "vectorstore"),
    )


# Module-level singleton so other files can simply do:
#   from config import settings
settings: Config = load_config()