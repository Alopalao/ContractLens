import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def _load_gemini_api_key() -> str:
	env_key = os.getenv("GEMINI_API_KEY")
	if env_key:
		return env_key

	key_path = Path(__file__).resolve().parents[2] / "gemini_key"
	if key_path.exists():
		return key_path.read_text(encoding="utf-8").strip()

	return ""

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "contract_analyzer")
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours
GEMINI_API_KEY = _load_gemini_api_key()
