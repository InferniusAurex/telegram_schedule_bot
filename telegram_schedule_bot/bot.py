import os
import pytz
from datetime import datetime, timedelta, time

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from message_builder import build_message_for_date
from timetable import TIMETABLE


# ===== CONFIG =====

TOKEN = os.getenv("TOKEN")
GROUP_ID = -5107345082   # your group id

IST = pytz.timezone("Asia/Kolkata")


# ===== DAILY MESSAGE =====

async def send_daily(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(IST)
    msg = build_message_for_date(now, "Everyone")
    await context.bot.send_message(chat_id=GROUP_ID, text=msg, parse_mode="HTML")
    print("Daily message sent at:", now)


# ===== COMMANDS =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Schedule Bot Running.")


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    now = datetime.now(IST)
    msg = build_message_for_date(now, name)
    await update.message.reply_text(msg, parse_mode="HTML")


async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = datetime.now(IST) + timedelta(days=1)
    day = target.strftime("%A").upper()

    if day not in TIMETABLE:
        await update.message.reply_text("Tomorrow is Weekend – No Classes.")
        return

    name = update.effective_user.first_name
    msg = build_message_for_date(target, name)
    await update.message.reply_text(msg, parse_mode="HTML")


async def week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "📅 Weekly Schedule (Mon–Fri)\n\n"

    for day in ["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY"]:
        text += f"{day}\n"

        for s, t in TIMETABLE[day]["morning"]:
            text += f"• {s} – {t}\n"

        for s, t in TIMETABLE[day]["afternoon"]:
            text += f"• {s} – {t}\n"

        text += "\n"

    await update.message.reply_text(text)


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(str(update.effective_chat.id))


# ===== APP =====

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("today", today))
app.add_handler(CommandHandler("tomorrow", tomorrow))
app.add_handler(CommandHandler("week", week))
app.add_handler(CommandHandler("id", get_id))


# ===== DAILY SCHEDULER (5:00 AM IST MON–FRI) =====

app.job_queue.run_daily(
    send_daily,
    time=time(5, 0, tzinfo=IST),
    days=(0, 1, 2, 3, 4)
)


print("Bot running...")
app.run_polling()
