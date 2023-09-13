import sqlite3


def create_table():
    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS Chats(chat_id INT PRIMARY KEY)')
    cur.execute('CREATE TABLE IF NOT EXISTS Videos(video_id TEXT PRIMARY KEY)')
    conn.commit()
    cur.close()
    conn.close()


def insert_chat_id(chat_id):
    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()

    cur.execute('INSERT OR IGNORE INTO Chats (chat_id) VALUES (?)', (chat_id,))
    conn.commit()
    cur.close()
    conn.close()


def get_chat_ids():
    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()

    cur.execute('SELECT * FROM Chats')
    chats = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return chats


def insert_video_id(video_id):
    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()

    cur.execute('INSERT OR IGNORE INTO Videos (video_id) VALUES (?)', (video_id,))
    conn.commit()
    cur.close()
    conn.close()


def remove_video_ids():
    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()

    cur.execute('DELETE FROM Videos')
    conn.commit()
    cur.close()
    conn.close()


def get_latest_video_id():
    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()

    cur.execute('SELECT * FROM Videos')
    videos = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return videos
