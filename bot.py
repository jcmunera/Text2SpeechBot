from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from gtts import gTTS
from langdetect import detect
import os

TOKEN = 'TOKEN_TELEGRAM'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Envíame un texto en cualquier idioma y te lo convertiré en un mensaje de voz.")

async def text_to_speech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    try:
        lang = detect(text)
        tts = gTTS(text=text, lang=lang, slow=False)
        filename = f"voice_{update.message.from_user.id}.mp3"
        tts.save(filename)

        with open(filename, 'rb') as audio_file:
            await update.message.reply_document(document=audio_file, filename="voz.mp3")

        os.remove(filename)
    except Exception as e:
        await update.message.reply_text(f"Error al generar la voz: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_to_speech))

    print("Bot corriendo...")
    app.run_polling()
