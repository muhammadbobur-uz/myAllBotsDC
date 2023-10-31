
from dotenv import dotenv_values
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters
import pyqrcode
import png
from gtts import gTTS

config = dotenv_values(".env")


STATE_QRCODE = 0
STATE_WORD_TO_SOUND = 1

def start(update:Update,context:CallbackContext):
    update.message.reply_html("🟢 <b>Привет через этого бота</b> \n\n1️⃣ Вы можете создать QR code"
                              "\n2️⃣ И вы можете передавать текст в голосовое сообщение.\n\n"
                              "Для этого нажмите кнопку <b>Mеню</b>")

def sound(txt):
    t = f"{txt}"
    m = gTTS(text = t, lang = 'ru', slow = False)
    return m.save("sound/sound.mp3")

def QRC(txt):
    u =pyqrcode.create(txt)
    return u.png('QR/qr.png', scale=6)

def qrcode(update:Update,context:CallbackContext):
    update.message.reply_html("✳️ Введите текст, который будет написан в QRcod\n\n<b>текст...</b>")
    return STATE_QRCODE

def qr_text(update:Update, context:CallbackContext):
    msg = update.message.text
    QRC(msg)
    context.bot.send_photo(chat_id= update.message.chat_id, photo = open("QR/qr.png", 'rb'), caption="Ваш QR code" )
    return ConversationHandler.END

def word_to_sound(update:Update, context:CallbackContext):
    update.message.reply_html("✳️ Введите текст, который будет голосового сообщения \n\n<b>text...</b>")
    return STATE_WORD_TO_SOUND

def send_sound(update:Update, context:CallbackContext):
    msg = update.message.text
    sound(msg)
    context.bot.send_audio(chat_id = update.message.chat_id, audio = open("sound/sound.mp3", 'rb'), caption = 'Вот ваш текст')
    return ConversationHandler.END

def hlp(update:Update, context:CallbackContext):
    update.message.reply_html(f"/start - Начинать \n/qrcode - Cоздать QR code\n/word_to_sound - Перенести текст в голосовое сообщение")

updater = Updater(config['TOKEN'], use_context = True)

conv_handler = ConversationHandler(
    entry_points = [
        CommandHandler('qrcode', qrcode)
    ],
    states = {
        STATE_QRCODE: [
            MessageHandler(Filters.all, qr_text)
        ],
    },
    fallbacks= []
)

convw_handler = ConversationHandler(
    entry_points=[
        CommandHandler('word_to_sound', word_to_sound)
    ],
    states= {
        STATE_WORD_TO_SOUND: [
            MessageHandler(Filters.all, send_sound)
        ],
    },
    fallbacks= []
)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(convw_handler)
updater.dispatcher.add_handler(conv_handler)
updater.dispatcher.add_handler(MessageHandler(Filters.all, hlp))

updater.start_polling()
updater.idle()
