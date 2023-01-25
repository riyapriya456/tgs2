from Adarsh.utils.database import Database
from Adarsh.utils.shortener import short_link
from Adarsh.vars import Var
from Adarsh.bot import StreamBot
from Adarsh.utils.human_readable import humanbytes
from Adarsh.utils.file_properties import get_file_ids
from Adarsh.server.exceptions import InvalidHash
import urllib.parse
import aiofiles
import logging
import aiohttp
db = Database(Var.DATABASE_URL, Var.name)

async def render_page(id, secure_hash):
    file_data=await get_file_ids(StreamBot, int(Var.BIN_CHANNEL), int(id))
    if file_data.unique_id[:6] != secure_hash:
        logging.debug(f'link hash: {secure_hash} - {file_data.unique_id[:6]}')
        logging.debug(f"Invalid hash for message with - ID {id}")
        raise InvalidHash

    # src = urllib.parse.urljoin(Var.URL, f'{secure_hash}/{str(id)}')
    src = f"{Var.URL}{id}/{urllib.parse.quote_plus(file_data.file_name)}?hash={secure_hash}"
    custom_player_link = f"intent:video.vidbox://{src}#Intent;package=com.adsinc.SKplayer;end"

    # after shorting
    user_info = await db.get_user(list(Var.OWNER_ID)[0])
    src_short_link = await short_link(user_info["base_site"], user_info["shortener_api"] , src)
    custom_player_short_link = await short_link(user_info["base_site"], user_info["shortener_api"], custom_player_link)

    if str(file_data.mime_type.split('/')[0].strip()) == 'video':
        async with aiofiles.open('Adarsh/template/req.html') as r:
            heading = f'Watch {file_data.file_name}'
            tag = file_data.mime_type.split('/')[0].strip()
            html = (await r.read()).replace('tag', tag) % (heading, file_data.file_name, src, src_short_link, custom_player_short_link)
    elif str(file_data.mime_type.split('/')[0].strip()) == 'audio':
        async with aiofiles.open('Adarsh/template/req.html') as r:
            heading = f'Listen {file_data.file_name}'
            tag = file_data.mime_type.split('/')[0].strip()
            html = (await r.read()).replace('tag', tag) % (heading, file_data.file_name, src, src_short_link, custom_player_short_link)
    else:
        async with aiofiles.open('Adarsh/template/dl.html') as r:
            async with aiohttp.ClientSession() as s:
                async with s.get(src) as u:
                    heading = f'Download {file_data.file_name}'
                    file_size = humanbytes(int(u.headers.get('Content-Length')))
                    html = (await r.read()) % (heading, file_data.file_name, src, file_size)
    return html