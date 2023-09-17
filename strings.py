import json


start_str = 'Вас приветствует бот Штабов Навального! Я буду сообщать вам статистику видео с канала популярной политики через час после её выхода 😇'
help_str = 'Это бот для Штабов Навального, который собирает статистику с видео канала "Популярная политика". Для начала напишите /start'
channel_str = 'Откройте канал "Популярная политика" на YouTube по этой ссылке:\nhttps://www.youtube.com/@Popularpolitics'

def generate_statistics_string(video_name, view_count, like_count, comment_count):
    return f""" Статистика по видео на данный момент:
Название видео: {video_name}

Количество просмотров видео: {view_count}🙈 
Количество лайков: {like_count}👍
Количество комментариев: {comment_count}🗣"""


def string_to_json(msg):
    msg = msg.replace("'", "\"")
    result = json.loads(msg)
    return result
