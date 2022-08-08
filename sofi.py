import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ExtBot, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

# this represents the token thats connected to sofi bot
# todo: it should be kept private in env variables
SOFI_TOKEN = "1669004254:AAG4lcu6CBtOOoS2RcrQMVc0uway1WKJ8oo"
# the sofi updater object is of the class updater which is provided by the
# python-telegram-bot package integrated in this project
# it's main function is to read the messages that gets sent to SOFI
sofi_updater = Updater(token=SOFI_TOKEN, use_context=True)
# the sofi dispatcher is allows to connect responses based on updates observed by sofi_updater
# in other words the dispatcher calls a functions based on what the user types to the bot
sofi_dispatcher = sofi_updater.dispatcher
# to get an instance of SOFI and control its actions we will make use of
# the sofi_instance
sofi_instance = ExtBot(token=SOFI_TOKEN)


# MOVIE ENDPOINTS
BASE_URL = "https://pan-da.herokuapp.com/api/"
SEARCH = BASE_URL + "search/"
GET = BASE_URL + "get/"




# UTILITIES
def convertToMessageTemplate(watchable_json):
    image = watchable_json['image']
    identifier = watchable_json['identifier']
    description = watchable_json['description']
    return identifier + "\n" + image + "\n" + description


# BOT FUNCTIONS
def search(update, context):
    chat_id = update.effective_chat.id
    query = update.message.text.lower()
    try:
        search_query = query.split('d-')[1]
        if search_query is not None:
            request = requests.get(SEARCH + search_query)
            watchable_list = request.json()
            for watchable in watchable_list:
                print(watchable)
                sofi_instance.send_message(chat_id, convertToMessageTemplate(watchable))
            #sofi_instance.send_message(chat_id, result)
            pass
    except:
        pass



keyboard = [
    [
        InlineKeyboardButton("Option 1", callback_data='1'),
        InlineKeyboardButton("Option 2", callback_data='2'),
    ],
    [InlineKeyboardButton("Option 3", callback_data='3')],
]



# BOT HANDLERS 
search_handler = MessageHandler(Filters.text, search)


# run code
sofi_dispatcher.add_handler(search_handler)
sofi_updater.start_polling()
