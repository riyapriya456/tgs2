from Adarsh.bot import StreamBot
from Adarsh.utils.database import Database
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters, Client
import time
import shutil, psutil
from Adarsh.vars import Var
from utils_bot import *
from Adarsh import StartTime

db = Database(Var.DATABASE_URL, Var.name)

START_TEXT = """ Your Telegram DC Is : `{}`  """


@StreamBot.on_message(filters.regex("DC"))
async def start(bot, update):
    text = START_TEXT.format(update.from_user.dc_id)
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        quote=True
    )

    
    
@StreamBot.on_message(filters.command("list"))
async def list(l, m):
    LIST_MSG = "Hi! {} Here is a list of all my commands \n \n 1 . `start⚡️` \n 2. `help📚` \n 3. `ping📡` \n 4. `status📊` \n 5. `DC` this tells your telegram dc \n 8. "
    await l.send_message(chat_id = m.chat.id,
        text = LIST_MSG.format(m.from_user.mention(style="md"))
        
    )
    
    
@StreamBot.on_message(filters.regex("ping📡"))
async def ping(b, m):
    start_t = time.time()
    ag = await m.reply_text("....")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await ag.edit(f"Pong!\n{time_taken_s:.3f} ms")
    
    
@StreamBot.on_message(filters.command("shortener_api") & filters.private )
async def shortener_api_handler(bot, m):
    user_id = (await bot.get_chat(Var.OWNER_USERNAME)).id

    user = await db.get_user(user_id)
    cmd = m.command
    if len(cmd) == 1:
        SHORTENER_API_MESSAGE = "To add or update your Shortner Website API,\n\nEx: `/shortener_api 6LZq851sXofffPHugiKQq`\n\nCurrent Shortener API: `{shortener_api}`"
        s = SHORTENER_API_MESSAGE.format(shortener_api=user["shortener_api"])

        return await m.reply(s)
    elif len(cmd) == 2:
        api = cmd[1].strip()
        await db.update_user_info(user_id, {"shortener_api": api})
        await m.reply(f"Shortener API updated successfully to {api}")

    
@StreamBot.on_message(filters.command("base_site") & filters.private & filters.user(Var.OWNER_USERNAME))
async def base_site_handler(bot: Client, m):

    user_id = (await bot.get_chat(Var.OWNER_USERNAME)).id
    user = await db.get_user(user_id)
    cmd = m.command
    if len(cmd) == 1:
        BASE_SITE_MESSAGE = "To add or update your Shortner Website,\n\nEx: `/base_site droplink.co`\n\nCurrent Base Site: `{base_site}`"
        s = BASE_SITE_MESSAGE.format(base_site=user["base_site"])

        return await m.reply(s)
    elif len(cmd) == 2:
        base_site = cmd[1].strip()
        # Updating the user's base site in the database.
        await db.update_user_info(user_id, {"base_site": base_site})
        await m.reply(f"Base Site updated successfully to {base_site}")


@StreamBot.on_message(filters.private & filters.regex("status📊"))
async def stats(bot, update):
  currentTime = readable_time((time.time() - StartTime))
  total, used, free = shutil.disk_usage('.')
  total = get_readable_file_size(total)
  used = get_readable_file_size(used)
  free = get_readable_file_size(free)
  sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
  recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
  cpuUsage = psutil.cpu_percent(interval=0.5)
  memory = psutil.virtual_memory().percent
  disk = psutil.disk_usage('/').percent
  botstats = f'<b>Bot Uptime:</b> {currentTime}\n' \
            f'<b>Total disk space:</b> {total}\n' \
            f'<b>Used:</b> {used}  ' \
            f'<b>Free:</b> {free}\n\n' \
            f'📊Data Usage📊\n<b>Upload:</b> {sent}\n' \
            f'<b>Down:</b> {recv}\n\n' \
            f'<b>CPU:</b> {cpuUsage}% ' \
            f'<b>RAM:</b> {memory}% ' \
            f'<b>Disk:</b> {disk}%'
  await update.reply_text(botstats)
