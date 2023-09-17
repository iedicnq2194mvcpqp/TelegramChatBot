import threading
import schedule
import telebot
from telebot import types
import yt_service
import db_service
import time
import strings
from dotenv import load_dotenv, dotenv_values

load_dotenv()

api_token = dotenv_values()['TELEGRAM_KEY']

bot = telebot.TeleBot(api_token)

db_service.create_table()

chats = db_service.get_chat_ids()
video = db_service.get_latest_video_id()
if not video:
    video = yt_service.get_channel_video_stats()


def write_statistics(video_id):
    time.sleep(3600)
    db_service.remove_video_ids()
    db_service.insert_video_id(video_id)
    msg = yt_service.get_latest_video_statistics()
    json_msg = strings.string_to_json(str(msg[1]))
    video_name = msg[0]
    res = strings.generate_statistics_string(video_name, json_msg['viewCount'], json_msg['likeCount'], json_msg['commentCount'])
    # Чтобы бот постил в ТГ канал:
    bot.send_message(dotenv_values()['CHANNEL_ID'], res)
    for c in chats:
        bot.send_message(c[0], res)


def check_update():
    global video
    video_id = yt_service.get_channel_video_stats()
    if video[0][0] != video_id:
        db_service.remove_video_ids()
        db_service.insert_video_id(video_id)
        video = db_service.get_latest_video_id()
        if not video:
            video = yt_service.get_channel_video_stats()
        write_statistics(video_id)


schedule.every().minutes.do(lambda: check_update())


def make_markup():
    markup = types.ReplyKeyboardMarkup()
    yt_channel = types.WebAppInfo("https://www.youtube.com/@Popularpolitics")
    btn1 = types.KeyboardButton('Открыть канал', web_app=yt_channel)
    btn2 = types.KeyboardButton('Посмотреть статистику последнего видео')
    markup.row(btn1, btn2)
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    db_service.insert_chat_id(message.chat.id)
    bot.send_message(message.chat.id, strings.start_str, reply_markup=make_markup())
    bot.register_next_step_handler(message, chat)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, strings.help_str)


@bot.message_handler(commands=['channel'])
def channel(message):
    msg = yt_service.get_channel_playlist_ids()
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['stats'])
def stats(message):
    msg = yt_service.get_latest_video_statistics()
    json_msg = strings.string_to_json(str(msg[1]))
    video_name = msg[0]
    res = strings.generate_statistics_string(video_name, json_msg['viewCount'], json_msg['likeCount'], json_msg['commentCount'])
    bot.send_message(message.chat.id, res)
    # Чтобы бот постил в ТГ канал:
    # bot.send_message(dotenv_values()['CHANNEL_ID'], res)


@bot.message_handler()
def chat(message):
    if message.text.lower() == 'открыть канал':
        bot.send_message(message.chat.id,strings.channel_str)
    if message.text.lower() == 'посмотреть статистику последнего видео':
        stats(message)


bot_polling_thread = threading.Thread(target=bot.infinity_polling)
bot_polling_thread.daemon = True
bot_polling_thread.start()

while True:
    schedule.run_pending()
    time.sleep(1)
