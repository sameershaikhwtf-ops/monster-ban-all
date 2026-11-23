# File: c:\Users\sameer\CodeGPT\banallbot\BANALLBOT.py
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import (
    ChannelParticipantsKicked,
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
)
from telethon.tl.functions.channels import GetParticipantRequest

# ====== CREDENTIALS (already added) ======
API_ID = 33414948
API_HASH = "9460fc00b82faab0c73e9966b3884e4d"
BOT_TOKEN = "9209848556:AAEqGABvZXraqsV48maYSixGcCuce5tRkL8"
# =========================================

client = TelegramClient("bot_session", API_ID, API_HASH)


async def is_admin(chat, user_id):
    try:
        p = await client(GetParticipantRequest(chat, user_id))
        return isinstance(p.participant, (ChannelParticipantAdmin, ChannelParticipantCreator))
    except Exception:
        return False


async def ban_all(event):
    if not event.is_group:
        return await event.reply("Ye command sirf group me chalegi.")
    if not await is_admin(event.chat_id, event.sender_id):
        return await event.reply("Sirf admin ye command use kar sakta hai.")

    msg = await event.reply("Ban shuru ho raha hai...")
    done = failed = 0
    async for user in client.iter_participants(event.chat_id):
        if user.bot or user.id == event.sender_id:
            continue
        try:
            await client.edit_permissions(event.chat_id, user.id, view_messages=False)
            done += 1
            await asyncio.sleep(0.5)  # flood se bachne ke liye
        except Exception:
            failed += 1  # admins/owner ban nahi honge
    await msg.edit(f"Ho gaya. Banned: {done}, Failed: {failed}")


async def unban_all(event):
    if not event.is_group:
        return await event.reply("Ye command sirf group me chalegi.")
    if not await is_admin(event.chat_id, event.sender_id):
        return await event.reply("Sirf admin ye command use kar sakta hai.")

    msg = await event.reply("Unban shuru ho raha hai...")
    done = failed = 0
    async for user in client.iter_participants(event.chat_id, filter=ChannelParticipantsKicked):
        try:
            await client.edit_permissions(event.chat_id, user.id, view_messages=True)
            done += 1
            await asyncio.sleep(0.5)
        except Exception:
            failed += 1
    await msg.edit(f"@wtf_monster owner of bot: {done}, Failed: {failed}")


async def main():
    await client.start(bot_token=BOT_TOKEN)
    me = await client.get_me()
    print(f"Bot chal rha hai ab chudh gaye tum log: @{me.username}")

    client.add_event_handler(ban_all, events.NewMessage(pattern=r"^/banall"))
    client.add_event_handler(unban_all, events.NewMessage(pattern=r"^/unbanall"))

    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
