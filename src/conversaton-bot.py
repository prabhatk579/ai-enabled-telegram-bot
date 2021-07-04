import logging
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from telegram import Bot, Update, ReplyKeyboardMarkup
from utils import get_reply, fetch_news, topics_keyboard

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN = '1333608087:AAH5RLQM7G_UUP2qPZpeUtGMIyBqCM7bDLM'
app = Flask(__name__)

@app.route('/')

def index():
    return "Hello!"

@app.route(f'/{TOKEN}', methods = ['GET','POST'])
def webhook():
    update = Update.de_json(request.get_json(),bot)
    dp.process_update(update)
    return "ok"


def start(update, context):
    print(update)
    """Send a message when the command /start is issued."""
    author = update.from_user.first_name
    update.message.reply_text("Hi! {}. \nThis is Prabhat's curiosity python project and you are one of the very first to try it and its a very small project. You just had a talk with my computer.\n\n\nTyping anything below to get a reply... It's an AI bot now. Start by typing 'Hi' or 'who are you' , 'get me tech news' or 'get me entertaintment news in hindi from India', but its still a dumb one (T_T).\n\n Type /help for Help and /news for all te news topic".format(author))

def help_command(update, context):
    print(update)
    update.message.reply_text("Can't help you bud!")


def reply_text(update, context):
    print("Name: ",update.message.from_user.first_name, update.message.from_user.last_name, "\t\tUsername: ", update.message.from_user.username)
    print("Input: ",update.message.text)
    intent , reply = get_reply(update.message.text, update.message.chat_id)
    print("Reply: ", reply)
    if intent == 'get_news':
        articles = fetch_news(reply)
        for article in articles:
            update.message.reply_text(article['link'])
    else:
        update.message.reply_text(reply)

def news(update, context):
    update.message.reply_text("Choose a category",
        reply_markup= ReplyKeyboardMarkup(keyboard= topics_keyboard , one_time_keyboard= True))
''' 
def echo(update, context):
    print(update)
    update.messahe.reply_text(update.message.text)

def echo_sticker(update,context):
    update.message.send_sticker(chat_id = update.message.chat_id, sticker = update.message.sticker.file_id)
'''
def error(update,context):
    logger.error("Say what... I don't see that command up there, Try anything from the above list")

if __name__ == '__main__':
    bot = Bot(TOKEN)
    bot.set_webhook("https://9957d42c27b6.ngrok.io/" + TOKEN)
    dp = Dispatcher(bot, None)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("News", news))
    #dp.add_handler(MessageHandler(Filters.text, reply_text))
    dp.add_handler(MessageHandler(Filters.text, reply_text))
    #dp.add_handler(MessageHandler(Filters.sticker &Filters.command, echo_sticker))
    dp.add_error_handler(error)
    app.run(port = 8443)
