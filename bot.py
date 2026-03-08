# bot.py
import asyncio
from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, PeerIdInvalid

from configs import cfg
from database import add_user, add_group, remove_user, all_users, all_groups, users

app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

BOT_ID = str(cfg.BOT_TOKEN.split(":")[0])  # same format as DB


# ------- helper: parse public post link (expects t.me/channel/msgid or @channel/msgid) -------
def parse_post_link(link: str):
    parts = link.rstrip("/").split("/")
    if len(parts) >= 2:
        chat = parts[-2]
        try:
            msg_id = int(parts[-1])
        except Exception:
            msg_id = None
        return chat, msg_id
    return None, None

def flood_wait_seconds(e):
    return getattr(e, "value", getattr(e, "x", getattr(e, "wait", 1))) or 1


# ---------------- JOIN REQUEST (no auto-approve) ----------------
@app.on_chat_join_request()
async def on_join_request(_, m: Message):
    try:
        chat = m.chat
        user = m.from_user

        # Save group & user in DB (so broadcast and counts include them)
        try:
            add_group(chat.id)
        except:
            pass
        try:
            add_user(user.id)
        except:
            pass

        # Forward configured POSTS (if any) to the user as intro (best-effort)
        for link in getattr(cfg, "POSTS", []):
            try:
                from_chat, msg_id = parse_post_link(link)
                if from_chat and msg_id:
                    await app.copy_message(chat_id=user.id, from_chat_id=from_chat, message_id=msg_id)
                    await asyncio.sleep(0.7)
            except Exception:
                # ignore if DM fails
                pass

        # Send short intro DM to the user (best-effort)
        try:
            await app.send_message(
                user.id,
                f"👋 {user.first_name or 'Friend'}, your join request to *{chat.title or chat.id}* has been received.\nAdmins will review it manually.",
                parse_mode="markdown"
            )
        except Exception:
            pass

        # Notify SUDO admins with Approve/Reject buttons
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ Approve", callback_data=f"approve|{chat.id}|{user.id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject|{chat.id}|{user.id}")
        ]])

        admin_text = (
            f"📥 New Join Request\n\n"
            f"User: {user.mention}\n"
            f"User ID: `{user.id}`\n"
            f"Group: {chat.title or chat.id}\n"
            f"Group ID: `{chat.id}`\n"
            f"Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"
        )

        for admin in cfg.SUDO:
            try:
                await app.send_message(admin, admin_text, reply_markup=keyboard, parse_mode="markdown")
            except Exception:
                pass

    except Exception as e:
        print("join_request error:", e)


# ---------------- CALLBACK: Approve / Reject ----------------
@app.on_callback_query()
async def on_callback(_, cq):
    try:
        if not cq.data:
            return await cq.answer()

        # Only SUDO allowed
        if cq.from_user.id not in cfg.SUDO:
            return await cq.answer("You are not allowed.", show_alert=True)

        parts = cq.data.split("|")
        if len(parts) != 3:
            return await cq.answer()

        action, chat_id_s, user_id_s = parts
        try:
            chat_id = int(chat_id_s)
            user_id = int(user_id_s)
        except:
            return await cq.answer("Invalid data.", show_alert=True)

        if action == "approve":
            try:
                await app.approve_chat_join_request(chat_id, user_id)
                try:
                    await app.send_message(user_id, f"✅ Your request to join `{chat_id}` has been approved.")
                except:
                    pass
                await cq.edit_message_text("✅ Request Approved")
                await cq.answer("Approved!")
            except FloodWait as e:
                await asyncio.sleep(flood_wait_seconds(e))
                try:
                    await app.approve_chat_join_request(chat_id, user_id)
                    await cq.edit_message_text("✅ Request Approved")
                    await cq.answer("Approved!")
                except Exception as ex:
                    await cq.answer(f"Failed: {ex}", show_alert=True)
            except Exception as ex:
                await cq.answer(f"Failed: {ex}", show_alert=True)

        elif action == "reject":
            try:
                # decline if available; otherwise just inform
                try:
                    await app.decline_chat_join_request(chat_id, user_id)
                except:
                    pass
                try:
                    await app.send_message(user_id, f"❌ Your request to join `{chat_id}` was rejected.")
                except:
                    pass
                await cq.edit_message_text("❌ Request Rejected")
                await cq.answer("Rejected!")
            except Exception as ex:
                await cq.answer(f"Failed: {ex}", show_alert=True)

    except Exception as e:
        print("callback error:", e)
        try:
            await cq.answer("Internal error", show_alert=True)
        except:
            pass


# ---------------- /start ----------------
@app.on_message(filters.private & filters.command("start"))
async def start_cmd(_, m: Message):
    try:
        add_user(m.from_user.id)

        # If user is SUDO show owner intro with photo and admin options
        if m.from_user.id in cfg.SUDO:
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("🗯 Channel", url="https://t.me/lnx_store"),
                InlineKeyboardButton("💬 Support", url="https://t.me/teacher_slex")
            ]])
            await m.reply_photo(
                photo="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhsaR6kRdTPF2ZMEgmgSYjjXU6OcsJhkBe1EWtI1nfbOziINTYzxjlGCMSVh-KoH05Z8MpRWhVV9TIX_ykpjdeGqJ1atXy1TUqrVkohUxlykoZyl67EfMQppHoWYrdHmdi6FMcL9v-Vew2VtaWHWY_eGZt-GN057jLGvYj7UV49g0rXVxoDFXQAYxvaX1xP/s1280/75447.jpg",
                caption=(
                    f"**🦊 Hello {m.from_user.mention}!**\n\n"
                    "I'm a join-request manager bot (manual approval only).\n"
                    "I handle join requests & DM users.\n\n"
                    "📢 Broadcast : reply to any message with /bcast\n"
                    "📊 Users : /users\n\n"
                    "__Powered By : @teacher_slex__"
                ),
                reply_markup=keyboard
            )
            return

        # Normal user: short greeting + forward POSTS if configured
        await m.reply_text("𝐁𝐇𝐀𝐈 𝐇𝐀𝐂𝐊 𝐒𝐄 𝐏𝐋𝐀𝐘 𝐊𝐑𝐎\n\n💸𝐏𝐑𝐎𝐅𝐈𝐓 𝐊𝐑𝐎🍻")
        for link in getattr(cfg, "POSTS", []):
            try:
                from_chat, msg_id = parse_post_link(link)
                if from_chat and msg_id:
                    await app.copy_message(chat_id=m.from_user.id, from_chat_id=from_chat, message_id=msg_id)
                    await asyncio.sleep(0.7)
            except Exception:
                pass

    except Exception as e:
        print("start error:", e)


# ---------------- Save user on any private message ----------------
@app.on_message(filters.private)
async def save_on_private(_, m: Message):
    try:
        add_user(m.from_user.id)
    except:
        pass


# ---------------- /users command ----------------
@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def users_cmd(_, m: Message):
    try:
        u = all_users()
        g = all_groups()
        await m.reply_text(f"🙋 Users : `{u}`\n👥 Groups : `{g}`\n📊 Total : `{u+g}`")
    except Exception as e:
        await m.reply_text(f"Error: {e}")


# ---------------- /bcast command ----------------
@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast_cmd(_, m: Message):
    if not m.reply_to_message:
        return await m.reply("Reply to a message and use /bcast")

    status = await m.reply("⚡ Broadcasting started...")
    ok = 0
    fail = 0

    try:
        cursor = users.find({"bot_id": BOT_ID})
    except Exception as e:
        await status.edit(f"DB Error: {e}")
        return

    for doc in cursor:
        uid = doc.get("user_id")
        if not uid:
            fail += 1
            continue
        try:
            user_id = int(uid)
        except:
            fail += 1
            continue

        # ensure user saved
        try:
            add_user(user_id)
        except:
            pass

        try:
            await m.reply_to_message.copy(chat_id=user_id)
            ok += 1
            await asyncio.sleep(0.08)
        except FloodWait as e:
            await asyncio.sleep(flood_wait_seconds(e))
            try:
                await m.reply_to_message.copy(chat_id=user_id)
                ok += 1
            except Exception:
                fail += 1
        except PeerIdInvalid:
            # user unreachable -> remove from DB
            try:
                remove_user(user_id)
            except:
                pass
            fail += 1
        except Exception:
            fail += 1

    await status.edit(f"✅ Broadcast Complete!\n\n👤 Success: {ok}\n❌ Failed: {fail}")


# ---------------- run ----------------
if __name__ == "__main__":
    print("Bot is starting...")
    app.run()
