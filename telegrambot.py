import logging
from telegram import Update , InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext,  CallbackQueryHandler, Filters , MessageHandler
import translators
import os


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, callback: CallbackContext):
    update.message.reply_text('welcom to translation bot')
    
    keyboard = [[
            InlineKeyboardButton("english", callback_data='en'),
            InlineKeyboardButton("french", callback_data='fr'),
            ],
            [InlineKeyboardButton("chinese", callback_data='zh'),
            InlineKeyboardButton("arabic", callback_data='ar'),
            ],
            [InlineKeyboardButton("russian", callback_data='ru'),
            InlineKeyboardButton("espanish", callback_data='es'),
            ],
            [InlineKeyboardButton("portuguese", callback_data='pt'),
            InlineKeyboardButton("italian", callback_data='it'),
            ],
            [InlineKeyboardButton("japanese", callback_data='ja'),
            InlineKeyboardButton("hindi", callback_data='hi'),
            ],
            [InlineKeyboardButton("persian", callback_data='fa'),]
    ]

    reply_markup =  InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose your imported language', reply_markup=reply_markup)
    

def target(update: Update, callback: CallbackContext):
  keyboard = [[
            InlineKeyboardButton("english", callback_data='@en'),
            InlineKeyboardButton("french", callback_data='@fr'),
            ],
            [InlineKeyboardButton("chinese", callback_data='@zh'),
            InlineKeyboardButton("arabic", callback_data='@ar'),
            ],
            [InlineKeyboardButton("russian", callback_data='@ru'),
            InlineKeyboardButton("espanish", callback_data='@es'),
            ],
            [InlineKeyboardButton("portuguese", callback_data='@pt'),
            InlineKeyboardButton("italian", callback_data='@it'),
            ],
            [InlineKeyboardButton("japanese", callback_data='@ja'),
            InlineKeyboardButton("hindi", callback_data='@hi'),
            ],
            [InlineKeyboardButton("persian", callback_data='@fa'),]
    ]

  reply_markup =  InlineKeyboardMarkup(keyboard)
  update.message.reply_text('Please choose your choosen language', reply_markup=reply_markup)

f = ''
t = ''
def button(update: Update, context: CallbackContext):
    global f , t
    query = update.callback_query
    query.answer()
    if query.data.isalpha() == True:
      query.edit_message_text("Your input language selected successfully")
      update.effective_chat.send_message('enter /target to choose your target language')
      f = str(query.data)
    elif query.data[0] == '@':
      query.edit_message_text(text=f"Your target language selected successfully")
      update.effective_chat.send_message('enter your sentence')
      t = str(query.data[1:])

def translate(update:Update , callback:CallbackContext):
  global f , t
  text = update.message.text
  tr = translators.google(text , from_language= f , to_language= t)
  update.effective_chat.send_message(tr)


def main() :
    TOKEN = "1886012278:AAGnOW0j8LQ1cYck98ul2MjZQGawGuTG75g"
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    PORT = int(os.environ.get('PORT', '8443'))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("target", target))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command , translate))
    

    updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN,
                        webhook_url = 'https://translationproje.herokuapp.com/' + TOKEN)

    updater.idle()

if __name__ == '__main__':
    main()