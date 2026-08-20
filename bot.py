import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# Render-এর জন্য ছোট web server
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Sujon Signal AI Bot is running!"

@web_app.route("/health")
def health():
    return "OK"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Sujon Signal AI Bot চালু আছে!\n\n"
        "1 মিনিটের signal system প্রস্তুত করা হচ্ছে।"
    )

def main():
    # Web server আলাদা thread-এ চালু
    threading.Thread(
        target=run_web_server,
        daemon=True
    ).start()

    # Telegram bot
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("Telegram bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
