from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime, timedelta
import pytz
from datetime import time


from message_builder import build_message_for_date
from timetable import TIMETABLE

TOKEN = "8388895720:AAFczzuwqyDCcz2-SjAF_6wJQFq0pA-rWJw"
GROUP_ID = -5107345082   # your group id

async def send_daily(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now()
    msg = build_message_for_date(now, "Inferno")
    await context.bot.send_message(chat_id=GROUP_ID, text=msg, parse_mode="HTML")



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Schedule Bot Running.")


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    msg = build_message_for_date(datetime.now(), name)
    await update.message.reply_text(msg, parse_mode="HTML")


async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = datetime.now() + timedelta(days=1)
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



app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("today", today))
app.add_handler(CommandHandler("tomorrow", tomorrow))
app.add_handler(CommandHandler("week", week))
app.add_handler(CommandHandler("id", get_id))

ist = pytz.timezone("Asia/Kolkata")
app.job_queue.run_daily(
    send_daily,
    time=time(5, 0, tzinfo=ist),
    days=(0, 1, 2, 3, 4)  # Monday-Friday
)


print("Bot running...")
app.run_polling()
