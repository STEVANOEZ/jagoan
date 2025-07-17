import os, logging, requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("BOT_TOKEN")

def generate(base):
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    res = set()
    for i in range(len(base)+1):
        for c in alpha:
            res.add(base[:i]+c+base[i:])
    return sorted(res)

def is_taken(u):
    try:
        return requests.get(f"https://t.me/{u}", timeout=5).status_code == 200
    except:
        return True

async def handle(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    t = update.message.text.lower().strip()
    if not t.isalpha():
        return await update.message.reply_text("Masukkan hanya huruf saja.")
    await update.message.reply_text(f"Mencari variasi untuk: {t}")
    lines = []
    for u in generate(t)[:30]:
        lines.append(f"@{u} {'✅' if is_taken(u) else '❎'}")
    await update.message.reply_text("\n".join(lines))

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()

if __name__ == "__main__":
    main()
