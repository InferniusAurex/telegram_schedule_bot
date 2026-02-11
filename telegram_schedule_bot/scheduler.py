import asyncio
import pytz
from datetime import datetime
from message_builder import build_message_for_date

IST = pytz.timezone("Asia/Kolkata")

async def daily_job(app, chat_id):
    last_sent = None

    while True:
        now = datetime.now(IST)

        # Run only Monday–Friday at 5:00 AM IST
        if now.weekday() < 5 and now.hour == 5 and now.minute == 0:
            today = now.strftime("%Y-%m-%d")

            if today != last_sent:
                msg = build_message_for_date(now, "Everyone")
                await app.bot.send_message(chat_id, msg, parse_mode="HTML")
                last_sent = today

            await asyncio.sleep(60)

        await asyncio.sleep(20)
