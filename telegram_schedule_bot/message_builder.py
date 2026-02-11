import random
from timetable import TIMETABLE
from weather import get_weather
from holidays import get_holiday

MONO = {
    "a":"𝚊","b":"𝚋","c":"𝚌","d":"𝚍","e":"𝚎","f":"𝚏","g":"𝚐","h":"𝚑",
    "i":"𝚒","j":"𝚓","k":"𝚔","l":"𝚕","m":"𝚖","n":"𝚗","o":"𝚘","p":"𝚙",
    "q":"𝚚","r":"𝚛","s":"𝚜","t":"𝚝","u":"𝚞","v":"𝚟","w":"𝚠","x":"𝚡",
    "y":"𝚢","z":"𝚣",
    "A":"𝙰","B":"𝙱","C":"𝙲","D":"𝙳","E":"𝙴","F":"𝙵","G":"𝙶","H":"𝙷",
    "I":"𝙸","J":"𝙹","K":"𝙺","L":"𝙻","M":"𝙼","N":"𝙽","O":"𝙾","P":"𝙿",
    "Q":"𝚀","R":"𝚁","S":"𝚂","T":"𝚃","U":"𝚄","V":"𝚅","W":"𝚆","X":"𝚇",
    "Y":"𝚈","Z":"𝚉"
}

def mono(text):
    return "".join(MONO.get(c, c) for c in text)

def get_quote():
    with open("quotes.txt", "r", encoding="utf-8") as f:
        quotes = [line.strip() for line in f if line.strip()]
    return random.choice(quotes)

def build_message_for_date(target_date, username=""):
    iso_date = target_date.strftime("%Y-%m-%d")
    holiday = get_holiday(iso_date)

    # Holiday check
    if holiday:
        return f"🎉 <b>Today is Holiday</b>\n{holiday}"

    day_name = target_date.strftime("%A").upper()
    date_str = target_date.strftime("%d %b | %a")

    if day_name not in TIMETABLE:
        return "<b>No Classes.</b>"

    data = TIMETABLE[day_name]
    uname = mono(username)

    # Greeting logic
    hour = target_date.hour

    if 5 <= hour < 12:
        greet = "Morning"
        emoji = "🌞"
    elif 12 <= hour < 17:
        greet = "Afternoon"
        emoji = "🌤️"
    elif 17 <= hour < 21:
        greet = "Evening"
        emoji = "🌆"
    else:
        greet = "Night"
        emoji = "🌙"

    temp, _ = get_weather()
    weather_text = f" | 🌡️ {temp}" if temp else ""

    msg = f"{emoji} {greet}, {uname} ☀️ | {date_str}{weather_text}\n\n"

    msg += "<blockquote>🍀 Morning Schedule:</blockquote>\n"
    for s, t in data["morning"]:
        msg += f"• <b><i>{s}</i></b> – {t}\n"

    msg += "\n<blockquote>🍀 Afternoon Schedule:</blockquote>\n"
    for s, t in data["afternoon"]:
        msg += f"• <b><i>{s}</i></b> – {t}\n"

    msg += "\n<blockquote>☁️ Must Carry:</blockquote>\n"
    for item in data["must_carry"]:
        msg += f"🔵 {item}\n"

    msg += "\n📖 Quote for the day:\n"
    msg += f"<span class='tg-spoiler'>{get_quote()}</span>"

    return msg
