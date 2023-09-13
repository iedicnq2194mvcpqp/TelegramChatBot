import json


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
