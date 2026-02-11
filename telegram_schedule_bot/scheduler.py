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

        # Debug heartbeat (every loop)
        print("Scheduler tick:", now.strftime("%Y-%m-%d %H:%M:%S"))

        # Monday–Friday only
        if now.weekday() < 5:

            # Allow small window (05:00–05:01)
          if now.hour == 22 and now.minute <= 25:

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

                    # Sleep 2 minutes so it never double sends
                    await asyncio.sleep(120)

        # Normal loop sleep
        await asyncio.sleep(20)
