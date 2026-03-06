# Don't Remove Credit @teacher_slex
# Subscribe YouTube ƈɦǟռռɛʟ For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters, Client, errors
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users
from configs import cfg
import asyncio
import aiohttp

app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

BOT_ID = str(cfg.BOT_TOKEN.split(":")[0])

#━━━━━━━━━━━━━━━━━━━━ HELPER ━━━━━━━━━━━━━━━━━━━━
def parse_post_link(link: str):
    parts = link.split("/")
    chat = parts[-2]
    msg_id = int(parts[-1])
    return chat, msg_id

#━━━━━━━━━━━━━━━━━━━━ 30-SEC KEEP ALIVE PING ━━━━━━━━━━━━━━━━━━━━
async def keep_alive_ping():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://localhost:8000/") as resp:
                    pass
        except Exception:
            pass
        await asyncio.sleep(30)

#━━━━━━━━━━━━━━━━━━━━ JOIN REQUEST (NO APPROVE, ONLY DM) ━━━━━━━━━━━━━━━━━━━━
@app.on_chat_join_request(filters.group | filters.channel)
async def approve(_, m: Message):
    op = m.chat
    kk = m.from_user
    try:
        add_group(op.id)
        await app.approve_chat_join_request(op.id, kk.id)

        mention = kk.mention  
        welcome = (
            f"👋 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 {mention}\n\n"
            "𝗬𝗼𝘂𝗿 𝗷𝗼𝗶𝗻 𝗿𝗲𝗾𝘂𝗲𝘀𝘁 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗿𝗲𝗰𝗲𝗶𝘃𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝗳𝘂𝗹𝗹𝘆.\n\n"
            "⏳ 𝗣𝗹𝗲𝗮𝘀𝗲 𝘄𝗮𝗶𝘁 𝘄𝗵𝗶𝗹𝗲 𝗼𝘂𝗿 𝗮𝗱𝗺𝗶𝗻 𝗿𝗲𝘃𝗶𝗲𝘄𝘀 𝗮𝗻𝗱 𝗮𝗽𝗿𝗼𝘃𝗲𝘀 𝘆𝗼𝘂𝗿 𝗿𝗲𝗾𝘂𝗲𝘀𝘁.\n\n"
            "🤑 𝗔𝗽𝗸𝗮 𝘃𝗶𝗽 𝗻𝘂𝗺𝗯𝗲𝗿 𝗽𝗮𝗻3𝗹 𝗻𝗶𝗰𝗵𝗲 𝗱𝗶𝗬𝗲 𝗴𝗮𝘆𝗲 𝗵𝗮𝗶𝗻 — 𝗨𝘀𝗲 𝗸𝗮𝗿𝗻𝗲 𝗸𝗲 𝗹𝗶𝗲 𝘀𝗲𝘁𝘂𝗽 𝘃𝗶𝗱𝗲𝗼 𝗱𝗵𝘆𝗮𝗮𝗻 𝘀𝗲 𝗱𝗲𝗸𝗵𝗲𝗶𝗻."
        )
        await app.send_message(kk.id, welcome, parse_mode="markdown")
        add_user(kk.id)
        
    except errors.PeerIdInvalid:
        print("user isn't start bot(means group)")
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as err:
        print(str(err))

#━━━━━━━━━━━━━━━━━━━━ START COMMAND ━━━━━━━━━━━━━━━━━━━━
@app.on_message(filters.private & filters.command("start"))
async def start(_, m: Message):
    add_user(m.from_user.id)

    if m.from_user.id not in cfg.SUDO:
        await m.reply_text("𝐁𝐇𝐀𝐈 𝐇𝐀𝐂𝐊 𝐒𝐄 𝐏𝐋𝐀𝐘 𝐊𝐑𝐎\n\n💸𝐏𝐑𝐎𝐅𝐈𝐓 𝐊𝐑𝐎🍻")
        for link in cfg.POSTS:
            try:
                chat_id, msg_id = parse_post_link(link)
                await app.copy_message(
                    chat_id=m.from_user.id,
                    from_chat_id=chat_id,
                    message_id=msg_id
                )
                await asyncio.sleep(1)
            except:
                pass
        return

    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("🗯 ƈɦǟռռɛʟ", url="https://t.me/lnx_store"),
            InlineKeyboardButton("💬 Support", url="https://t.me/teacher_slex")
        ]]
    )

    await m.reply_photo(
        photo="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhsaR6kRdTPF2ZMEgmgSYjjXU6OcsJhkBe1EWtI1nfbOziINTYzxjlGCMSVh-KoH05Z8MpRWhVV9TIX_ykpjdeGqJ1atXy1TUqrVkohUxlykoZyl67EfMQppHoWYrdHmdi6FMcL9v-Vew2VtaWHWY_eGZt-GN057jLGvYj7UV49g0rXVxoDFXQAYxvaX1xP/s1280/75447.jpg",
        caption=(
            f"**🦊 Hello {m.from_user.mention}!**\n\n"
            "I'm an auto approve bot.\n"
            "I handle join requests & DM users.\n\n"
            "📢 Broadcast : /bcast\n"
            "📊 Users : /users\n\n"
            "__Powered By : @teacher_slex__"
        ),
        reply_markup=keyboard
    )

#━━━━━━━━━━━━━━━━━━━━ USERS COUNT ━━━━━━━━━━━━━━━━━━━━
@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def users_count(_, m: Message):
    u = all_users()
    g = all_groups()
    await m.reply_text(f"🙋 Users : `{u}`\n👥 Groups : `{g}`\n📊 Total : `{u+g}`")

#━━━━━━━━━━━━━━━━━━━━ BROADCAST COPY ━━━━━━━━━━━━━━━━━━━━
@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m: Message):
    if not m.reply_to_message:
        return await m.reply("⚠️ Bhai, kisi message ko reply karke /bcast use karo.")
        
    status = await m.reply("⚡ Fast Broadcasting started...")
    ok = fail = 0
    
    bot_users = users.find({"bot_id": BOT_ID})
    
    for u in bot_users:
        try:
            await m.reply_to_message.copy(u["user_id"])
            ok += 1
            await asyncio.sleep(0.05) 
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await m.reply_to_message.copy(u["user_id"])
                ok += 1
            except:
                fail += 1
        except Exception:
            fail += 1
            
    await status.edit(f"✅ **Broadcast Complete!**\n\n👤 Success: {ok}\n❌ Failed: {fail}")

#━━━━━━━━━━━━━━━━━━━━ 🚫 AUTO DELETE ILLEGAL BOT MSG ━━━━━━━━━━━━━━━━━━━━
@app.on_message(filters.me)
async def auto_delete_illegal(_, m: Message):
    try:
        content = ""
        if m.text:
            content = m.text.lower()
        elif m.caption:
            content = m.caption.lower()

        for word in cfg.ILLEGAL_WORDS:
            if word.lower() in content:
                await asyncio.sleep(0.1)
                await m.delete()
                return
    except:
        pass

print("🤖 Bot is Alive!")
app.loop.create_task(keep_alive_ping())
app.run()
