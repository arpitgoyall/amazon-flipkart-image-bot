from telegram import *
from telegram.ext import *
import re
from scraping import *
from message import Message

scrape = ImageScrape()

print("Bot Started...")

TOKEN = "Your Bot Token" # Your bot token here

bot = Bot(TOKEN)

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

def Find(string):
  
    # findall() has been used 
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)      
    return [x[0] for x in url]


msg_handler = MessageHandler(Filters.text, Message.send_message, run_async=True)
dispatcher.add_handler(msg_handler)


updater.start_polling()