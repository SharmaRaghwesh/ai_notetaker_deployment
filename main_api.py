from fastapi import FastAPI, BackgroundTasks
import asyncio
from meetbot import run_bot

app = FastAPI(title="AI Notetaker API")

@app.get("/")
def root():
    return {"message": "AI Notetaker API is running"}

@app.post("/start_meeting/")
async def start_meeting(
    meet_url: str,
    output_wav: str = "output.wav",
    device_name: str = None,
    max_minutes: int = 60,
    check_interval: int = 10,
    leave_grace: int = 5,
    args: dict = {}
):
    """
    Starts the Google Meet bot in the background.
    """
    loop = asyncio.get_event_loop()
    background_task = loop.create_task(
        run_bot(meet_url, output_wav, device_name, max_minutes, check_interval, leave_grace, args)
    )
    return {"status": "Meeting bot started. Check logs for progress."}
