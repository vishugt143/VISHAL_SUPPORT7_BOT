# bot.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
import asyncio

from database import add_user, add_group, all_users, all_groups, users
from configs import cfg


app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

BOT_ID = str(cfg.BOT_TOKEN.split(":")[0])


# ━━━━━━━━━ JOIN REQUEST (NO AUTO APPROVE) ━━━━━━━━━
@app.on_chat_join_request()
async def join_request(client, m):

    user = m.from_user
    chat = m.chat

    add_user(user.id)
    add_group(chat.id)

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ Approve",
                    callback_data=f"approve|{chat.id}|{user.id}"
                ),
                InlineKeyboardButton(
                    "❌ Reject",
                    callback_data=f"reject|{chat.id}|{user.id}"
                )
            ]
        ]
    )

    for admin in cfg.SUDO:

        try:

            await client.send_message(
                admin,
                f"📥 New Join Request\n\n"
                f"User : {user.mention}\n"
                f"User ID : `{user.id}`\n"
                f"Group : {chat.title}",
                reply_markup=keyboard
            )

        except:
            pass


# ━━━━━━━━━ CALLBACK BUTTON ━━━━━━━━━
@app.on_callback_query()
async def callback(client, cq):

    if cq.from_user.id not in cfg.SUDO:
        return await cq.answer("Not allowed", show_alert=True)

    data = cq.data.split("|")

    action = data[0]
    chat_id = int(data[1])
    user_id = int(data[2])

    try:

        if action == "approve":

            await client.approve_chat_join_request(
                chat_id,
                user_id
            )

            await cq.edit_message_text(
                "✅ User Approved"
            )

        elif action == "reject":

            await client.decline_chat_join_request(
                chat_id,
                user_id
            )

            await cq.edit_message_text(
                "❌ User Rejected"
            )

    except Exception as e:

        await cq.answer(str(e), show_alert=True)


# ━━━━━━━━━ START COMMAND ━━━━━━━━━
@app.on_message(filters.private & filters.command("start"))
async def start(client, m: Message):

    add_user(m.from_user.id)

    await m.reply_text(
        "Hello 👋\n\nI am Join Request Manager Bot"
    )


# ━━━━━━━━━ SAVE USER ON ANY MESSAGE ━━━━━━━━━
@app.on_message(filters.private)
async def save_user(client, m: Message):

    add_user(m.from_user.id)


# ━━━━━━━━━ USERS COUNT ━━━━━━━━━
@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def users_count(client, m):

    u = all_users()
    g = all_groups()

    await m.reply_text(

        f"👤 Users : {u}\n"
        f"👥 Groups : {g}\n"
        f"📊 Total : {u+g}"

    )


# ━━━━━━━━━ BROADCAST ━━━━━━━━━
@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def broadcast(client, m):

    if not m.reply_to_message:
        return await m.reply("Reply to message with /bcast")

    status = await m.reply("Broadcasting...")

    ok = 0
    fail = 0

    all_user = users.find({"bot_id": BOT_ID})

    for user in all_user:

        try:

            await m.reply_to_message.copy(
                int(user["user_id"])
            )

            ok += 1

            await asyncio.sleep(0.07)

        except FloodWait as e:

            await asyncio.sleep(e.value)

        except:

            fail += 1

    await status.edit(

        f"✅ Broadcast Done\n\n"
        f"Success : {ok}\n"
        f"Failed : {fail}"

    )


print("🤖 Bot Started")
app.run()
