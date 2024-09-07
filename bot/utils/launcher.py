import os
import glob
import asyncio
import argparse
from itertools import cycle

from pyrogram import Client
from better_proxy import Proxy

from bot.config import settings
from bot.utils import logger
from bot.core.tapper import run_tapper
from bot.core.registrator import register_sessions

start_text = """

<y>███╗   ███╗ █████╗      ██╗ ██████╗ ██████╗ ██████╗  ██████╗ ████████╗
████╗ ████║██╔══██╗     ██║██╔═══██╗██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝
██╔████╔██║███████║     ██║██║   ██║██████╔╝██████╔╝██║   ██║   ██║   
██║╚██╔╝██║██╔══██║██   ██║██║   ██║██╔══██╗██╔══██╗██║   ██║   ██║   
██║ ╚═╝ ██║██║  ██║╚█████╔╝╚██████╔╝██║  ██║██████╔╝╚██████╔╝   ██║   
╚═╝     ╚═╝╚═╝  ╚═╝ ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝    ╚═╝   </y>

Select an action:

    1. Run clicker
    2. Create session
"""

global tg_clients


def get_session_names() -> list[str]:
    session_files = [f for f in os.listdir('sessions') if f.endswith('.session')]
    session_names = [
        os.path.join('sessions', os.path.splitext(session_file)[0]) for session_file in session_files
    ]

    return session_names


def get_proxies() -> list[Proxy]:
    if settings.USE_PROXY_FROM_FILE:
        with open(file="bot/config/proxies.txt", encoding="utf-8-sig") as file:
            proxies = [Proxy.from_str(proxy=row.strip()).as_url for row in file]
    else:
        proxies = []

    return proxies


async def process() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", type=int, help="Action to perform")

    logger.info(f"Detected {len(get_session_names())} sessions | {len(get_proxies())} proxies")

    action = parser.parse_args().action

    if not action:
        logger.info(start_text)

        while True:
            action = input("> ")

            if not action.isdigit():
                logger.warning("Action must be number")
            elif action not in ["1", "2"]:
                logger.warning("Action must be 1 or 2")
            else:
                action = int(action)
                break

    if action == 1:
        await run_tasks()

    elif action == 2:
        await register_sessions()




async def run_tasks():
    proxies = get_proxies()
    proxies_cycle = cycle(proxies) if proxies else None
    tasks = []
    for session_name in get_session_names():
        task = asyncio.create_task(run_tapper(session_name, next(proxies_cycle) if proxies_cycle else None))
        tasks.append(task)

    await asyncio.gather(*tasks)
