# AstroDegen 🔮

A Telegram bot that gives you a Chinese Zodiac and Numerology reading based on your birth date. No sugarcoating. No bullshit.

## What it does

Send your birth date and get:
- **Chinese Zodiac sign** — who you really are
- **Full Date Number** — your life's core energy
- **Day Number** — what your birth day says about you
- **Day of the Year** — the final nail in the coffin

## Commands

| Command | Description |
|---|---|
| `/start` | Welcome message |
| `/readme YYYY-MM-DD` | Get your reading |

**Example:** `/readme 1990-07-15`

## Setup

1. Clone the repo
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file based on `.env.example` and add your Telegram bot token:
```
TOKEN=your_telegram_bot_token_here
```
4. Run:
```bash
python main.py
```

## Tech
- Python
- python-telegram-bot
- ephem
- python-dotenv
