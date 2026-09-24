import os
from dotenv import load_dotenv

load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-3.5-flash-lite"

MAX_CHUNK_CHARACTERS = 12000
MIN_CHUNK_CHARACTERS = 4000