# database.py
from pymongo import MongoClient
from configs import cfg

# connect
client = MongoClient(cfg.MONGO_URI)

# using same db/collection names as your old file
users = client['main']['users']
groups = client['main']['groups']

def already_db(user_id):
    """Return True if user exists (stored as string)."""
    try:
        user = users.find_one({"user_id": str(user_id)})
        return bool(user)
    except Exception:
        return False

def already_dbg(chat_id):
    """Return True if group exists (stored as string)."""
    try:
        group = groups.find_one({"chat_id": str(chat_id)})
        return bool(group)
    except Exception:
        return False

def add_user(user_id):
    """Insert a user doc if not exists. Stored user_id as string."""
    if already_db(user_id):
        return None
    try:
        return users.insert_one({"user_id": str(user_id)})
    except Exception:
        return None

def remove_user(user_id):
    """Remove user if exists."""
    if not already_db(user_id):
        return None
    try:
        return users.delete_one({"user_id": str(user_id)})
    except Exception:
        return None

def add_group(chat_id):
    """Insert group doc if not exists. Stored chat_id as string."""
    if already_dbg(chat_id):
        return None
    try:
        return groups.insert_one({"chat_id": str(chat_id)})
    except Exception:
        return None

def all_users():
    """Return count of users."""
    try:
        return users.count_documents({})
    except Exception:
        return 0

def all_groups():
    """Return count of groups."""
    try:
        return groups.count_documents({})
    except Exception:
        return 0
