# -*- coding: utf-8 -*-
import os, re, logging, requests, time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8950639235:AAHXj6ssUt9zlGqTDZ1u3VGMWyZqIH3S8-U"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KILISHA = "💀 شهم الدكتاتوري | بسم شهم الإله والرب الأعلى 💀"

def extract_url(text):
    """استخراج أي رابط TikTok من النص"""
    patterns = [
        r'https?://(?:www\.)?tiktok\.com/@[\w.-]+/video/\d+',
        r'https?://(?:www\.)?tiktok\.com/t/\w+',
        r'https?://vm\.tiktok\.com/\w+',
        r'https?://vt\.tiktok\.com/\w+',
        r'https?://(?:m\.)?tiktok\.com/v/\d+',
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return m.group()
    if "tiktok" in text.lower():
        return text.strip()
    return None

def download_tiktok(url):
    """تحميل فيديو TikTok"""
    try:
        api_url = f"https://www.tikwm.com/api/?url={url}"
        headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15"}
        resp = requests.get(api_url, headers=headers, timeout=30)
        data = resp.json()
        
        if data.get("code") == 0 and data.get("data"):
            vd = data["data"]
            return {
                "ok": True,
                "video": vd.get("play", vd.get("hdplay", "")),
                "music": vd.get("music", ""),
                "title": vd.get("title", "بدون عنوان"),
                "author": vd.get("author", {}).get("nickname", "غير معروف"),
            }
        
        api2 = f"https://api.tikmate.app/api/download?url={url}"
        resp2 = requests.get(api2, headers=headers, timeout=30)
        data2 = resp2.json()
        
        if data2.get("success"):
            return {
                "ok": True,
                "video": data2.get("video", ""),
                "title": data2.get("title", "بدون عنوان"),
                "author": data2.get("author", "غير معروف"),
            }
        
        return {"ok": False, "error": "تعذر التحميل"}
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"{KILISHA}\n\n"
        "🎬 <b>بوت تحميل تيك توك</b>\n\n"
        "📝 <b>طريقة الاستخدام:</b>\n"
        "• افتح TikTok\n"
        "• اضغط مشاركة → نسخ الرابط\n"
        "• أرسل الرابط هنا\n\n"
        "👑 <b>شهم الدكتاتوري القائد المجنح</b>",
        parse_mode='HTML'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    url = extract_url(text)
    
    if not url:
        await update.message.reply_text(
            f"❌ <b>لم يتم العثور على رابط TikTok!</b>\n\n"
            f"📝 أرسل رابط مثل:\n"
            f"<code>https://www.tiktok.com/@user/video/123456</code>\n"
            f"<code>https://vm.tiktok.com/abc123/</code>\n\n"
            f"{KILISHA}",
            parse_mode='HTML'
        )
        return
    
    msg = await update.message.reply_text(f"⏳ <b>جاري تحميل الفيديو...</b>\n{KILISHA}", parse_mode='HTML')
    result = download_tiktok(url)
    
    if result["ok"]:
        try:
            await msg.delete()
            caption = f"🎬 <b>{result['title'][:100]}</b>\n👤 @{result['author']}\n{KILISHA}"
            await update.message.reply_video(
                video=result["video"],
                caption=caption,
                parse_mode='HTML',
                supports_streaming=True
            )
        except Exception as e:
            await msg.edit_text(
                f"📥 <b>رابط التحميل المباشر:</b>\n\n{result['video']}\n\n"
                f"🎬 {result['title'][:100]}\n"
                f"{KILISHA}",
                parse_mode='HTML',
                disable_web_page_preview=False
            )
    else:
        await msg.edit_text(
            f"❌ <b>فشل التحميل!</b>\n\n"
            f"السبب: {result.get('error', 'خطأ غير معروف')}\n\n"
            f"🔗 الرابط: {url}\n\n"
            f"{KILISHA}",
            parse_mode='HTML'
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Error: {context.error}")
    if update and update.message:
        await update.message.reply_text(f"❌ حدث خطأ!\n{KILISHA}")

def main():
    print(KILISHA)
    print("[✓] SHAHEM BOT STARTING...")
    
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)
    
    print("[✓] بسم الإله والرب الأعلى")
    print("[✓] البوت شغال ✅\n")
    
    app.run_polling()

if __name__ == "__main__":
    main()

