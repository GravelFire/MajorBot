import asyncio
import random
from urllib.parse import unquote

import aiohttp
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from telethon.tl.functions.messages import RequestAppWebViewRequest
from telethon.tl.types import InputBotAppShortName, InputPeerNotifySettings, InputNotifyPeer
from telethon import TelegramClient, functions, types
from telethon import errors
import json
from .agents import generate_random_user_agent
import socks
from bot.config import settings
from typing import Any, Callable
import functools
from bot.utils import logger
from bot.exceptions import InvalidSession
from .headers import headers


def error_handler(func: Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            await asyncio.sleep(1)
    return wrapper


def proxy_to_dict(proxy: Proxy) -> dict:
    proxy_type_map = {
        'http': socks.HTTP,
        'socks': socks.SOCKS5
    }

    proxy_dict = {
        'proxy_type': proxy_type_map.get(proxy.protocol, socks.HTTP),
        'addr': proxy.host,
        'port': proxy.port,
    }

    if proxy.login:
        proxy_dict['username'] = proxy.login
    if proxy.password:
        proxy_dict['password'] = proxy.password

    return proxy_dict



class Tapper:
    
    def __init__(self, session_name: str, proxy: str):
        self.proxy = proxy
        if self.proxy:
            proxy = Proxy.from_str(proxy)
            proxy_dict = proxy_to_dict(proxy)
        else:
            proxy_dict = None
        self.tg_client = TelegramClient(session_name, api_id=settings.API_ID, api_hash=settings.API_HASH, proxy=proxy_dict)
        self.session_name = session_name
        self.tg_client_id = 0

    async def get_tg_web_data(self) -> str:
        await self.tg_client.connect()
        ref_id = settings.REF_ID if random.randint(0, 100) <= 85 else "339631649"
        app_info = await self.tg_client(RequestAppWebViewRequest(
            'me',
            InputBotAppShortName(await self.tg_client.get_input_entity('major'), 'start'),
            'android',
            start_param=ref_id
        ))
        web_data = unquote(string=unquote(string=app_info.url.split('tgWebAppData=', maxsplit=1)[1].split('&tgWebAppVersion', maxsplit=1)[0]))
        get_me = await self.tg_client.get_me()
        self.tg_client_id = get_me.id
            
        await self.tg_client.disconnect()
        
        return ref_id, web_data
        
        
    async def join_and_mute_tg_channel(self, link: str):
        link = link if 'https://t.me/+' in link else link[13:]
        async with self.tg_client as client:

            if 'https://t.me/+' in link:
                try:
                    invite_hash = link.split('/+')[-1]
                    result = await client(functions.messages.ImportChatInviteRequest(hash=invite_hash))
                    logger.info(f"{self.session_name} | Joined to channel: <y>{result.chats[0].title}</y>")
                    await asyncio.sleep(random.randint(10, 20))

                except Exception as e:
                    logger.error(f"{self.session_name} | (Task) Error while join tg channel: {e}")
            else:
                try:
                    await client(functions.channels.JoinChannelRequest(channel='@'+link))
                    logger.info(f"{self.session_name} | Joined to channel: <y>{link}</y>")
                except Exception as e:
                    logger.error(f"{self.session_name} | (Task) Error while join tg channel: {e}")
    
    @error_handler
    async def make_request(self, http_client, method, endpoint=None, url=None, **kwargs):
        full_url = url or f"https://major.glados.app/api{endpoint or ''}"
        response = await http_client.request(method, full_url, **kwargs)
        response.raise_for_status()
        return await response.json()
    
    @error_handler
    async def login(self, http_client, init_data, ref_id):
        response = await self.make_request(http_client, 'POST', endpoint="/auth/tg/", json={"init_data": init_data})
        if response and response.get("access_token", None):
            return response
        return None
    
    @error_handler
    async def get_daily(self, http_client):
        return await self.make_request(http_client, 'GET', endpoint="/tasks/?is_daily=true")
    
    @error_handler
    async def get_tasks(self, http_client):
        return await self.make_request(http_client, 'GET', endpoint="/tasks/?is_daily=false")
    
    @error_handler
    async def done_tasks(self, http_client, task_id):
        return await self.make_request(http_client, 'POST', endpoint="/tasks/", json={"task_id": task_id})
    
    @error_handler
    async def claim_swipe_coins(self, http_client):
        response = await self.make_request(http_client, 'GET', endpoint="/swipe_coin/")
        if response and response.get('success') is True:
            logger.info(f"{self.session_name} | Start game <y>SwipeCoins</y>")
            coins = random.randint(settings.SWIPE_COIN[0], settings.SWIPE_COIN[1])
            payload = {"coins": coins }
            await asyncio.sleep(55)
            response = await self.make_request(http_client, 'POST', endpoint="/swipe_coin/", json=payload)
            if response and response.get('success') is True:
                return coins
            return 0
        return 0

    @error_handler
    async def claim_hold_coins(self, http_client):
        response = await self.make_request(http_client, 'GET', endpoint="/bonuses/coins/")
        if response and response.get('success') is True:
            logger.info(f"{self.session_name} | Start game <y>HoldCoins</y>")
            coins = random.randint(settings.HOLD_COIN[0], settings.HOLD_COIN[1])
            payload = {"coins": coins }
            await asyncio.sleep(55)
            response = await self.make_request(http_client, 'POST', endpoint="/bonuses/coins/", json=payload)
            if response and response.get('success') is True:
                return coins
            return 0
        return 0

    @error_handler
    async def claim_roulette(self, http_client):
        response = await self.make_request(http_client, 'GET', endpoint="/roulette/")
        if response and response.get('success') is True:
            logger.info(f"{self.session_name} | Start game <y>Roulette</y>")
            await asyncio.sleep(10)
            response = await self.make_request(http_client, 'POST', endpoint="/roulette/")
            if response:
                return response.get('rating_award', 0)
            return 0
        return 0
    
    @error_handler
    async def visit(self, http_client):
        return await self.make_request(http_client, 'POST', endpoint="/user-visits/visit/?")
        
    @error_handler
    async def streak(self, http_client):
        return await self.make_request(http_client, 'POST', endpoint="/user-visits/streak/?")
    
    @error_handler
    async def get_detail(self, http_client):
        detail = await self.make_request(http_client, 'GET', endpoint=f"/users/{self.tg_client_id}/")
        
        return detail.get('rating') if detail else 0
    
    @error_handler
    async def join_squad(self, http_client):
        return await self.make_request(http_client, 'POST', endpoint="/squads/2237841784/join/?")
    
    @error_handler
    async def get_squad(self, http_client, squad_id):
        return await self.make_request(http_client, 'GET', endpoint=f"/squads/{squad_id}?")

    @error_handler
    async def check_proxy(self, http_client: aiohttp.ClientSession) -> None:
        response = await self.make_request(http_client, 'GET', url='https://httpbin.org/ip', timeout=aiohttp.ClientTimeout(5))
        ip = response.get('origin')
        logger.info(f"{self.session_name} | Proxy IP: {ip}")
    
    #@error_handler
    async def run(self) -> None:
        if settings.USE_RANDOM_DELAY_IN_RUN:
                random_delay = random.randint(settings.RANDOM_DELAY_IN_RUN[0], settings.RANDOM_DELAY_IN_RUN[1])
                logger.info(f"{self.session_name} | Bot will start in <y>{random_delay}s</y>")
                await asyncio.sleep(random_delay)
                
        proxy_conn = ProxyConnector().from_url(self.proxy) if self.proxy else None
        http_client = aiohttp.ClientSession(headers=headers, connector=proxy_conn)
        ref_id, init_data = await self.get_tg_web_data()
        
        if not init_data:
            if not http_client.closed:
                await http_client.close()
            if proxy_conn:
                if not proxy_conn.closed:
                    proxy_conn.close()
                    
        if self.proxy:
            await self.check_proxy(http_client=http_client)
            
        if settings.FAKE_USERAGENT:            
            http_client.headers['User-Agent'] = generate_random_user_agent(device_type='android', browser_type='chrome')
        
        while True:
            try:
                if http_client.closed:
                    if proxy_conn:
                        if not proxy_conn.closed:
                            proxy_conn.close()

                    proxy_conn = ProxyConnector().from_url(self.proxy) if self.proxy else None
                    http_client = aiohttp.ClientSession(headers=headers, connector=proxy_conn)
                    if settings.FAKE_USERAGENT:            
                        http_client.headers['User-Agent'] = generate_random_user_agent(device_type='android', browser_type='chrome')
                
                user_data = await self.login(http_client=http_client, init_data=init_data, ref_id=ref_id)
                if not user_data:
                    logger.info(f"{self.session_name} | <r>Failed login</r>")
                    sleep_time = random.randint(settings.SLEEP_TIME[0], settings.SLEEP_TIME[1])
                    logger.info(f"{self.session_name} | Sleep <y>{sleep_time}s</y>")
                    await asyncio.sleep(delay=sleep_time)
                    continue
                http_client.headers['Authorization'] = "Bearer " + user_data.get("access_token")
                logger.info(f"{self.session_name} | <y>⭐ Login successful</y>")
                user = user_data.get('user')
                squad_id = user.get('squad_id')
                rating = await self.get_detail(http_client=http_client)
                logger.info(f"{self.session_name} | ID: <y>{user.get('id')}</y> | Points : <y>{rating}</y>")
                
                if squad_id is None:
                    await self.join_squad(http_client=http_client)
                    squad_id = "2237841784"
                    await asyncio.sleep(1)
                    
                data_squad = await self.get_squad(http_client=http_client, squad_id=squad_id)
                if data_squad:
                    logger.info(f"{self.session_name} | Squad : <y>{data_squad.get('name')}</y> | Member : <y>{data_squad.get('members_count')}</y> | Ratings : <y>{data_squad.get('rating')}</y>")    
                
                data_visit = await self.visit(http_client=http_client)
                if data_visit:
                    await asyncio.sleep(1)
                    logger.info(f"{self.session_name} | Daily Streak : <y>{data_visit.get('streak')}</y>")
                
                await self.streak(http_client=http_client)
                
                
                hold_coins = await self.claim_hold_coins(http_client=http_client)
                if hold_coins:
                    await asyncio.sleep(1)
                    logger.info(f"{self.session_name} | Reward HoldCoins: <y>{hold_coins}</y>")
                await asyncio.sleep(10)
                
                
                swipe_coins = await self.claim_swipe_coins(http_client=http_client)
                if swipe_coins:
                    await asyncio.sleep(1)
                    logger.info(f"{self.session_name} | Reward SwipeCoins: <y>{swipe_coins}</y>")
                await asyncio.sleep(10)
                
                
                roulette = await self.claim_roulette(http_client=http_client)
                if roulette:
                    await asyncio.sleep(1)
                    logger.info(f"{self.session_name} | Reward Roulette : <y>{roulette}</y>")
                await asyncio.sleep(10)
                
                
                data_daily = await self.get_daily(http_client=http_client)
                if data_daily:
                    for daily in reversed(data_daily):
                        await asyncio.sleep(10)
                        id = daily.get('id')
                        title = daily.get('title')
                        #if title not in ["Donate rating", "Boost Major channel", "TON Transaction"]:
                        data_done = await self.done_tasks(http_client=http_client, task_id=id)
                        if data_done and data_done.get('is_completed') is True:
                            await asyncio.sleep(1)
                            logger.info(f"{self.session_name} | Daily Task : <y>{daily.get('title')}</y> | Reward : <y>{daily.get('award')}</y>")
                
                data_task = await self.get_tasks(http_client=http_client)
                if data_task:
                    for task in data_task:
                        await asyncio.sleep(10)
                        id = task.get('id')
                        if task.get('type') == 'subscribe_channel':
                            if not settings.TASKS_WITH_JOIN_CHANNEL:
                                continue
                            await self.join_and_mute_tg_channel(link=task.get('payload').get('url'))
                            await asyncio.sleep(5)
                        
                        data_done = await self.done_tasks(http_client=http_client, task_id=id)
                        if data_done and data_done.get('is_completed') is True:
                            await asyncio.sleep(1)
                
                            logger.info(f"{self.session_name} | Task : <y>{task.get('title')}</y> | Reward : <y>{task.get('award')}</y>")
                await http_client.close()
                if proxy_conn:
                    if not proxy_conn.closed:
                        proxy_conn.close()
            
            except InvalidSession as error:
                raise error

            except Exception as error:
                logger.error(f"{self.session_name} | Unknown error: {error}")
                await asyncio.sleep(delay=3)
                
                   
            sleep_time = random.randint(settings.SLEEP_TIME[0], settings.SLEEP_TIME[1])
            logger.info(f"{self.session_name} | Sleep <y>{sleep_time}s</y>")
            await asyncio.sleep(delay=sleep_time)    
            
        

async def run_tapper(session_name: str, proxy: str | None):
    try:
        await Tapper(session_name=session_name, proxy=proxy).run()
    except InvalidSession:
        logger.error(f"{session_name} | Invalid Session")