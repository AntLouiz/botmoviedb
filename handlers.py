import telegram
import tmdbsimple as tmdb
from telegram.ext import (
  Filters,
  CommandHandler,
  RegexHandler,
  MessageHandler
)
from emoji import emojize
from decouple import config


def start(bot, update):
  """
    Show a welcome message
  """

  msg = "Hi, send a message like \"*find* Thor: Ragnarok\" to see the movie overview."
  bot.send_message(
    chat_id=update.message.chat_id,
    text=msg,
    parse_mode=telegram.ParseMode.MARKDOWN
  )

def get_movie(bot, update, groups):
  """
    Shows the movie overview
  """

  def send_movie_message(matched_movie, bot, chat_id):
    title = matched_movie['title']
    overview = matched_movie['overview']

    # print("Title: {}\nOverview: \n{}".format(title, overview))
    bot.send_message(chat_id=chat_id, text=title)

    if(matched_movie['poster_path']):
      image_link = image_url+matched_movie['poster_path']
      # print("Image Link: {}".format(image_link))
      bot.send_photo(chat_id=chat_id, photo=image_link)

    bot.send_message(chat_id=chat_id, text=overview)
    # print("\n")
    pass

  def send_movies_message_keyboard(matched_movies, bot, chat_id):
    kb = []
    msg = "I found that movies, check if your movie is in the keyboard options."

    for movie in matched_movies:
      title = movie['title']
      kb.append([telegram.KeyboardButton("find {}".format(title))])

    kb_markup = telegram.ReplyKeyboardMarkup(kb)
    bot.send_message(
      chat_id=chat_id,
      text=msg,
      reply_markup=kb_markup
    )
    pass


  movie_name = groups[0]
  chat_id = update.message.chat_id

  if not movie_name:
    bot.send_message(
      text="Please insert a movie name after \"*find*\".",
      parse_mode=telegram.ParseMode.MARKDOWN
    )
    return True

  tmdb.API_KEY = config('MOVIE_DB_TOKEN')
  search = tmdb.Search()

  image_url = "https://image.tmdb.org/t/p/w185"
  response = search.movie(query=movie_name)
  results = search.results
  num_results = len(results)

  if num_results > 1:
    movies = results
    send_movies_message_keyboard(movies, bot, chat_id)

  elif num_results == 1:
    movie = results[0]
    send_movie_message(movie, bot, chat_id)

  else:
    msg = "Movie not found, please try again."
    bot.send_message(chat_id=chat_id, text=msg)

def support(bot, update):
  """
    Shows a help message.
  """

  msg = "Send \"*find* <my_movie>\" to get the film overview."

  bot.send_message(
    chat_id= update.message.chat_id,
    text=msg,
    parse_mode=telegram.ParseMode.MARKDOWN
  )

def default(bot, update):
  """
    A default message to unknown command messages.
  """

  msg = "Sorry, i don\'t understanding that command. Send [/help] to show a help message."
  msg += emojize(':pensive:', use_aliases= True)

  bot.send_message(
    chat_id=update.message.chat_id,
    text=msg,
    parse_mode=telegram.ParseMode.MARKDOWN
  )


start_handler = CommandHandler('start', start)
help_handler = CommandHandler('support', support)

get_movie_handler = RegexHandler(r"find\s+(.*)$", get_movie, pass_groups=True)
default_handler = MessageHandler(Filters.command, default)