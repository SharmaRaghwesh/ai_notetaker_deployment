import argparse, asyncio
from meetbot import run_bot

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("meet_url")
    parser.add_argument("--out", default="meeting.wav")
    parser.add_argument("--style", choices=["minimal","business","advanced"], default="business")
    args = parser.parse_args()

    asyncio.run(run_bot(
        args.meet_url,
        args.out,
        device_name="Meet Aggregate",
        max_minutes=90,
        check_interval=20,
        leave_grace=10,
        style=args.style
    ))
