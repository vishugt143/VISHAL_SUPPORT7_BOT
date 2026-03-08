# database.py

from pymongo import MongoClient
from configs import cfg

# Mongo connection
client = MongoClient(cfg.MONGO_URI)

db = client["main"]

users = db["users"]
groups = db["groups"]

# bot id
BOT_ID = str(cfg.BOT_TOKEN.split(":")[0])


# ━━━━━━━━━ USER CHECK ━━━━━━━━━
def user_exists(user_id):
    return users.find_one({
        "user_id": str(user_id),
        "bot_id": BOT_ID
    })


# ━━━━━━━━━ ADD USER ━━━━━━━━━
def add_user(user_id):

    try:

        if user_exists(user_id):
            return

        users.insert_one({
            "user_id": str(user_id),
            "bot_id": BOT_ID
        })

    except:
        pass


# ━━━━━━━━━ REMOVE USER ━━━━━━━━━
def remove_user(user_id):

    try:

        users.delete_one({
            "user_id": str(user_id),
            "bot_id": BOT_ID
        })

    except:
        pass


# ━━━━━━━━━ GROUP CHECK ━━━━━━━━━
def group_exists(chat_id):

    return groups.find_one({
        "chat_id": str(chat_id),
        "bot_id": BOT_ID
    })


# ━━━━━━━━━ ADD GROUP ━━━━━━━━━
def add_group(chat_id):

    try:

        if group_exists(chat_id):
            return

        groups.insert_one({
            "chat_id": str(chat_id),
            "bot_id": BOT_ID
        })

    except:
        pass


# ━━━━━━━━━ COUNT USERS ━━━━━━━━━
def all_users():

    try:
        return users.count_documents({
            "bot_id": BOT_ID
        })

    except:
        return 0


# ━━━━━━━━━ COUNT GROUPS ━━━━━━━━━
def all_groups():

    try:
        return groups.count_documents({
            "bot_id": BOT_ID
        })

    except:
        return 0
