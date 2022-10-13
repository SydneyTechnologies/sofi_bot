import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ExtBot, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

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
    print("hi")
    image = watchable_json['image']
    identifier = watchable_json['identifier']
    description = watchable_json['description']
    return [identifier + "\n" + image + "\n", identifier]


# BOT FUNCTIONS

def download(identifier):
    request = requests.get(GET + identifier)
    result = request.json()
    print(result)
    return result

def search(update, context):
    chat_id = update.effective_chat.id
    query = update.message.text.lower()

    try:
        search_query = query.split('d-')[1]
        if search_query is not None:
            request = requests.get(SEARCH + search_query)
            watchable_list = request.json()
            message = convertToMessageTemplate(watchable_list[0])
            idenfier = message[1]
            context.user_data["target"] = idenfier
            keyboard = [
        [
            InlineKeyboardButton("Download", callback_data="1"),
        ],
    ]
           
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(message[0], reply_markup=reply_markup)
    except:
        print(search_query)
        pass


def buttonFunc(update, context):
    chat_id = update.effective_chat.id
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    downloadId = context.user_data["target"]
    downloadLink = download(downloadId)["download-link"].replace("'", "")
    query.edit_message_text(text=f"Selected option: {downloadId}")
    # query = update.callback_query
    # query.answer()
    # download_link = download(query.data)
    # print(query.data)
    print(downloadLink)
    # sofi_instance.send_message(chat_id=chat_id, document=f'{downloadLink}')
    sofi_instance.send_message(chat_id, downloadLink)





# BOT HANDLERS 
search_handler = MessageHandler(Filters.text, search)
button_handler = CallbackQueryHandler(buttonFunc)


# run code
sofi_dispatcher.add_handler(search_handler)
sofi_dispatcher.add_handler(button_handler)
sofi_updater.start_polling()
