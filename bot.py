import os
import threading
from datetime import datetime, timedelta, timezone

from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# Render Web Service-এর জন্য
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Sujon Signal AI Bot is running!"

@web_app.route("/health")
def health():
    return "OK"


# Statistics
wins = 0
losses = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Sujon Signal AI Bot চালু আছে!\n\n"
        "📊 Signal system প্রস্তুত করা হচ্ছে।\n"
        "⏱️ Timeframe: 1 Minute\n"
        "📈 Real + OTC scanner: Data connection required"
    )


async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔎 MARKET SCANNING...\n\n"
        "⚠️ Live Quotex Real/OTC candle data এখনো connected নয়।\n\n"
        "তাই এখন কোনো fake UP/DOWN signal দেওয়া হচ্ছে না।"
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total = wins + losses

    if total > 0:
        win_rate = (wins / total) * 100
    else:
        win_rate = 0

    await update.message.reply_text(
        f"📊 SIGNAL STATS\n\n"
        f"✅ WIN: {wins}\n"
        f"❌ LOSS: {losses}\n"
        f"📈 Win Rate: {win_rate:.1f}%"
    )


def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)


def main():
    threading.Thread(
        target=run_web_server,
        daemon=True
    ).start()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("stats", stats))

    print("Telegram bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
