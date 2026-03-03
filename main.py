import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from datetime import datetime
import ephem
import os
from dotenv import load_dotenv
import data

load_dotenv()
TOKEN = os.getenv("TOKEN")


# ── Core Logic ────────────────────────────────────────────────────────────────

def chinese_newyear(year):
    solstice = ephem.previous_solstice(f'{year}/01/01')
    first_new_moon = ephem.next_new_moon(solstice)
    second_new_moon = ephem.next_new_moon(first_new_moon)
    return ephem.Date(second_new_moon).datetime()

def get_zodiac(date):
    year = date.year
    ny = chinese_newyear(year)
    zodiac_year = year - 1 if date < ny else year
    return data.zodiac[(zodiac_year - 4) % 12]

def reduce(n, stop_at=None):
    """Reduce n to single digit or master number."""
    masters = {11, 22, 28, 33}
    while len(str(n)) > 1:
        if n in masters:
            break
        if n == 20:
            n = 11
            break
        n = sum(int(d) for d in str(n))
    return n

def main_numbers(date):
    date_str = date.strftime('%Y%m%d')

    # Full date number
    full_lp = sum(int(d) for d in date_str)
    sum_all = reduce(full_lp)

    # Day number
    daynr = reduce(date.day)

    # Day of year
    doy_raw = date.timetuple().tm_yday
    doy = reduce(doy_raw)

    return sum_all, daynr, doy

# ── Handlers ──────────────────────────────────────────────────────────────────

logging.basicConfig(level=logging.WARNING)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 <b>Welcome to the AstroDegen!</b>\n\n"
        "Wanna get a reading? Use the /readme command.\n\n",
        parse_mode='HTML'
    )

async def read(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Dude... I don't read minds. Give me a date.\nExample: <code>/readme 1990-07-15</code>",
            parse_mode='HTML'
        )
        return

    try:
        date = datetime.strptime(context.args[0], '%Y-%m-%d')
    except ValueError:
        await update.message.reply_text(
            "Use the correct format: YYYY-MM-DD\n\nExample: <code>/readme 1990-07-15</code>",
            parse_mode='HTML'
        )
        return

    sign = get_zodiac(date)
    sum_all, daynr, doy = main_numbers(date)


    # Group labels by their final number value
    number_labels = {
        sum_all: [],
        daynr: [],
        doy: []
    }
    number_labels[sum_all].append("FULL DATE NUMBER")
    number_labels[daynr].append("DAY NUMBER")
    number_labels[doy].append("DAY OF THE YEAR")

    reply = (
        f"<b>Chinese Zodiac sign — {sign}</b>\n\n"
        f"{data.Animal.get(sign, '')}\n\n\n\n"
    )

    seen = set()
    for label_key in [sum_all, daynr, doy]:
        if label_key in seen:
            continue
        seen.add(label_key)
        labels = number_labels[label_key]
        merged_label = " & ".join(labels)
        reply += (
            f"<b>{merged_label} — {label_key}</b>\n"
            f"{data.Number_short.get(str(label_key), '—')}\n\n"
        )

    await update.message.reply_text(reply, parse_mode='HTML')
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "All I would do to you is a reading. Use the /readme command.",
        parse_mode='HTML'
    )

# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("readme", read))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling()