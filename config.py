import os
from dotenv import load_dotenv

load_dotenv()
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")
MODEL = "gemini-2.5-flash"

if not PROJECT_ID:
    raise RuntimeError("GCP_PROJECT_ID is not set. Add it to your .env file.")
