# -*- coding: utf-8 -*-
import os, re, logging, requests, time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8950639235:AAHXj6ssUt9zlGqTDZ1u3VGMWyZqIH3S8-U"  # ⚠️ غير هذا

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KILISHA = "💀 شهم الدكتاتوري | بسم شهم الإله والرب الأعلى 💀"

def download_tiktok(url):
    try:
        api_url = f"https://www.tikwm.com/api/?url={url}"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(api_url, headers=headers, timeout=30)
        data = resp.json()
        if data.get("code") == 0 and data.get("data"):
            vd = data["data"]
            return {"ok": True, "video": vd.get("play", ""), "music": vd.get("music", ""), "title": vd.get("title", "")}
        return {"ok": False}
    except:
        return {"ok": False}

def extract_url(text):
    import re
    m = re.search(r'https?://(?:www\.)?tiktok\.com/@[\w.-]+/video/\d+|https?://vm\.tiktok\.com/\w+', text)
    return m.group() if m else None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"{KILISHA}\n\n🎬 أرسل رابط TikTok للتحميل")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = extract_url(update.message.text)
    if not url:
        await update.message.reply_text("📝 أرسل رابط TikTok")
        return
    msg = await update.message.reply_text("⏳ جاري التحميل...")
    result = download_tiktok(url)
    if result["ok"]:
        try:
            await msg.delete()
            await update.message.reply_video(video=result["video"], caption=f"{result['title']}\n{KILISHA}")
        except:
            await msg.edit_text(f"📥 {result['video']}")
    else:
        await msg.edit_text("❌ فشل التحميل")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print(f"{KILISHA}\n[✓] البوت شغال")
    app.run_polling()

if __name__ == "__main__":
    main()