from pymongo import MongoClient
from configs import cfg

client = MongoClient(cfg.MONGO_URI)

db = client["main"]
users = db["users"]
groups = db["groups"]
requests = db["requests"]

BOT_ID = str(cfg.BOT_TOKEN.split(":")[0])


# ---------------- USERS ---------------- #

def add_user(user_id):
    try:
        users.update_one(
            {"user_id": str(user_id), "bot_id": BOT_ID},
            {"$set": {"user_id": str(user_id), "bot_id": BOT_ID}},
            upsert=True
        )
    except:
        pass


def remove_user(user_id):
    try:
        users.delete_one({"user_id": str(user_id), "bot_id": BOT_ID})
    except:
        pass


def get_users():
    return users.find({"bot_id": BOT_ID})


def all_users():
    try:
        return users.count_documents({"bot_id": BOT_ID})
    except:
        return 0


# ---------------- GROUPS ---------------- #

def add_group(chat_id):
    try:
        groups.update_one(
            {"chat_id": str(chat_id), "bot_id": BOT_ID},
            {"$set": {"chat_id": str(chat_id), "bot_id": BOT_ID}},
            upsert=True
        )
    except:
        pass


def all_groups():
    try:
        return groups.count_documents({"bot_id": BOT_ID})
    except:
        return 0


# ---------------- JOIN REQUESTS ---------------- #

def add_request(user_id, chat_id):
    try:
        requests.update_one(
            {"user_id": str(user_id), "chat_id": str(chat_id)},
            {"$set": {"user_id": str(user_id), "chat_id": str(chat_id)}},
            upsert=True
        )
    except:
        pass


def get_requests():
    return requests.find()


def clear_requests():
    try:
        requests.delete_many({})
    except:
        pass
