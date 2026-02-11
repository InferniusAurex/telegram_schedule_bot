import asyncio
import pytz
from datetime import datetime
from message_builder import build_message_for_date

IST = pytz.timezone("Asia/Kolkata")

async def daily_job(app, chat_id):
    last_sent = None

    print("Scheduler started...")

    while True:
        now = datetime.now(IST)

        print("Scheduler tick:", now.strftime("%Y-%m-%d %H:%M:%S"))

        # Monday–Friday only
        if now.weekday() < 5:

            # Time window (22:00–22:01 for testing)
            if now.hour == 22 and now.minute < 2:

                today = now.strftime("%Y-%m-%d")

                if today != last_sent:
                    print("DAILY JOB TRIGGERED")

                    msg = build_message_for_date(now, "Everyone")

                    await app.bot.send_message(
                        chat_id,
                        msg,
                        parse_mode="HTML"
                    )

                    last_sent = today

                    # prevent double send
                    await asyncio.sleep(120)

        await asyncio.sleep(20)
