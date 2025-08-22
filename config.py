from dotenv import load_dotenv
import os

# Load from .env (only for local dev)
load_dotenv()

BOT_EMAIL = os.getenv("BOT_EMAIL")
BOT_PASSWORD = os.getenv("BOT_PASSWORD")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Add safety check
if not BOT_EMAIL or not BOT_PASSWORD or not GEMINI_API_KEY:
    raise ValueError("❌ Missing environment variables. Please set BOT_EMAIL, BOT_PASSWORD, GEMINI_API_KEY")
