# AI Meet Bot

🤖 A bot that joins Google Meet, records audio in chunks, merges them, and sends to Gemini for transcription + summary.

## Setup

1. Clone repo
2. Create `.env` file (DO NOT commit it):


BOT_EMAIL=your_google_bot_email@gmail.com

BOT_PASSWORD=your_google_bot_password

GEMINI_API_KEY=your_gemini_api_key

3. Install dependencies:

4. Run:
python main.py

## Deploy on Railway
- Push repo to GitHub
- Create new Railway project
- Add Environment Variables in Dashboard:
- `BOT_EMAIL`
- `BOT_PASSWORD`
- `GEMINI_API_KEY`
- Deploy 🚀

✅ Flow will be:

Local: .env → load via dotenv
GitHub: .env ignored (safe)
Railway: you set env vars in dashboard → bot runs with them
