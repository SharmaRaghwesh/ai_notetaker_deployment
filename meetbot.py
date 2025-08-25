import os, asyncio, time, threading
from playwright.async_api import async_playwright
from summarizer import transcribe_and_summarize

# Only import recorder if running locally
RUNNING_LOCALLY = os.getenv("RUNNING_LOCALLY", "true").lower() == "true"
if RUNNING_LOCALLY:
    from recorder import record_audio

# ---------- Bot Checks participants ----------
async def get_participant_count(page):
    """
    Robustly fetch participant count from Google Meet UI.
    Handles different labels: People / Participants / In the meeting.
    """
    try:
        await page.click("button[aria-label*='Show everyone']", timeout=2000)
    except:
        pass  # Already open

    selectors = ["text=People", "text=Participants", "text=In the meeting"]

    for sel in selectors:
        try:
            element = await page.query_selector(sel)
            if element:
                text = await element.inner_text()
                match = re.search(r"\d+", text)
                if match:
                    return int(match.group())
        except:
            continue

    try:
        people_nodes = await page.query_selector_all("div[role='listitem']")
        return len(people_nodes)
    except:
        return 0
    ...

# ---------- Meet Bot ----------
async def run_bot(meet_url, output_wav, device_name, max_minutes, check_interval, leave_grace, args):
    bot_email = os.getenv("BOT_EMAIL")
    bot_password = os.getenv("BOT_PASSWORD")
    if not bot_email or not bot_password:
        raise RuntimeError("Set BOT_EMAIL and BOT_PASSWORD in your environment.")

    stop_flag = threading.Event()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Login
        print("🔐 Logging into Google…")
        await page.goto("https://accounts.google.com/")
        await page.fill('input[type="email"]', bot_email)
        await page.click('button:has-text("Next")')
        await page.wait_for_timeout(1500)
        await page.fill('input[type="password"]', bot_password)
        await page.click('button:has-text("Next")')
        await page.wait_for_timeout(3000)

        # Go to Meet link
        print(f"🌐 Opening Meet: {meet_url}")
        await page.goto(meet_url)
        await page.wait_for_timeout(4000)

        # Pre-join
        try:
            if await page.locator('text="Continue without microphone and camera"').count():
                await page.click('text="Continue without microphone and camera"')
                print("✅ Continued without mic/cam")
        except:
            pass

        # Join (Ask first, then Join now)
        if await page.locator('button:has-text("Ask to join")').count():
            await page.click('button:has-text("Ask to join")')
            print("🛎️ Requested to join")
        elif await page.locator('button:has-text("Join now")').count():
            await page.click('button:has-text("Join now")')
            print("✅ Joined immediately")
        else:
            print("❌ Could not join")
            await browser.close()
            return

        # Start recording thread
        recorder = threading.Thread(target=record_audio, args=(stop_flag, output_wav, device_name))
        recorder.start()

        start_time = time.time()
        max_seconds = max_minutes * 60
        empty_rounds = 0

        # Monitor meeting
        while True:
            if time.time() - start_time > max_seconds:
                print("⏰ Max meeting duration reached")
                break

            count = await get_participant_count(page)
            print(f"👥 Detected {count} participant(s)")
            if count <= 1:
                empty_rounds += 1
                if empty_rounds >= 3:
                    print("🚪 No participants 3 times in a row. Leaving meeting...")
                    await asyncio.sleep(leave_grace)
                    break
                # if count <= 1:
                #     print("✅ Everyone left. Exiting meeting…")
                #     break

            await asyncio.sleep(check_interval)

        # Leave
        try:
            await page.click('button[aria-label*="Leave call"]')
        except:
            print("⚠️ Couldn’t click leave")

        stop_flag.set()
        recorder.join()
        await browser.close()

    # After meeting → Summarize
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Set GEMINI_API_KEY environment variable")

    print("🎙️ Sending audio to Gemini for transcription + summarization...")
    notes = transcribe_and_summarize(output_wav,api_key,args)
    print("📄 Summarization complete!")

    with open("meeting_notes.md", "w") as f:
        f.write(notes)
    print("📝 Notes saved to meeting_notes.md")
