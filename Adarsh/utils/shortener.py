import contextlib
from shortzy import Shortzy


async def short_link(base_site, api_key, link):
    if api_key and base_site:
        shortzy = Shortzy(api_key, base_site) 
        with contextlib.suppress(Exception):
            link = link.replace("http://", "https://")
            link = await shortzy.convert(link)
    return link
