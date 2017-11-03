import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from decouple import config
import tmdbsimple as tmdb


updater = Updater(token=config('TELEGRAM_BOT_TOKEN'))
dispatcher = updater.dispatcher


def start(bot, update):
  """
    Mostra a mensagem de bem-vindo
  """

  msg = "Hello, send /movie to see the movie overview."
  bot.send_message(
    chat_id=update.message.chat_id,
    text=msg
  )

def default(bot, update):
  '''
    A default message to unknown users messages.
  '''

  msg = 'Sorry, i don\'t understanding that command '
  msg += emojize(':pensive:', use_aliases= True)

  bot.send_message(
    chat_id= update.message.chat_id,
    text= msg
  )

default_handler = MessageHandler(Filters.command, default)
start_handler = CommandHandler('start', start)

dispatcher.add_handler(default_handler)
dispatcher.add_handler(start_handler)

updater.start_polling()

"""tmdb.API_KEY = config('MOVIE_DB_TOKEN')
# bot token 462659520:AAH8oMaK3NS2wvfBWPYLMUzvdt_TKlH-_Uc


search = tmdb.Search()

# movie_name = input("Insira o nome de um filme: ")
movie_name = "Batman vs Superman"

image_url = "https://image.tmdb.org/t/p/w185"
# bot.send_photo(chat_id=chat_id, photo='https://telegram.org/img/t_logo.png')

response = search.movie(query=movie_name)

for s in search.results:
  title = s['title']
  overview = s['overview']

  print("Title: {}\nOverview: \n{}".format(title, overview))

  if(s['poster_path']):
    image_link = image_url+s['poster_path']
    print("Image Link: {}".format(image_link))

  print("\n")"""