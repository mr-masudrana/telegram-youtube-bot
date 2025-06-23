from telegram.ext import Application, CommandHandler, MessageHandler, filters
from pytube import YouTube
import os

# BotFather থেকে পাওয়া API টোকেন বসান এখানে
BOT_TOKEN = '7765322122:AAEjbRlUemQA5DKPmNcg2sc5ntcLdxwb3-k'

# /start কমান্ড হ্যান্ডলার
async def start(update, context):
    await update.message.reply_text("👋 স্বাগতম! ইউটিউব লিংক পাঠান, আমি ভিডিও ডাউনলোড করে দিব।")

# ইউটিউব ভিডিও ডাউনলোড হ্যান্ডলার
async def download_video(update, context):
    url = update.message.text
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').get_lowest_resolution()
        filename = stream.download()

        # ভিডিও ফাইল পাঠানো
        await update.message.reply_video(video=open(filename, 'rb'), caption=yt.title)
        os.remove(filename)
    except Exception as e:
        await update.message.reply_text(f"❌ ত্রুটি: {str(e)}")

# মেইন ফাংশন
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.run_polling()

if __name__ == '__main__':
    main()
