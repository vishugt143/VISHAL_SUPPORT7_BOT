# database.py
from pymongo import MongoClient
from configs import cfg

# connect
client = MongoClient(cfg.MONGO_URI)
users = client['main']['users']
groups = client['main']['groups']

# Bot ka ID token se nikal rahe hain (string, same as tumhara config expects)
BOT_ID = str(cfg.BOT_TOKEN.split(":")[0])

def already_db(user_id):
    try:
        user = users.find_one({"user_id": str(user_id), "bot_id": BOT_ID})
        return bool(user)
    except Exception:
        return False

def already_dbg(chat_id):
    try:
        group = groups.find_one({"chat_id": str(chat_id), "bot_id": BOT_ID})
        return bool(group)
    except Exception:
        return False

def add_user(user_id):
    try:
        if already_db(user_id):
            return None
        return users.insert_one({"user_id": str(user_id), "bot_id": BOT_ID})
    except Exception:
        return None

def remove_user(user_id):
    try:
        if not already_db(user_id):
            return None
        return users.delete_one({"user_id": str(user_id), "bot_id": BOT_ID})
    except Exception:
        return None

def add_group(chat_id):
    try:
        if already_dbg(chat_id):
            return None
        return groups.insert_one({"chat_id": str(chat_id), "bot_id": BOT_ID})
    except Exception:
        return None

def all_users():
    try:
        return users.count_documents({"bot_id": BOT_ID})
    except Exception:
        return 0

def all_groups():
    try:
        return groups.count_documents({"bot_id": BOT_ID})
    except Exception:
        return 0
