__version__ = '0.1'

import logging
import os
import asyncio

from colorama import init
from colorama import Fore as Color
from dotenv import load_dotenv
from telethon.sync import TelegramClient, events, types
from datetime import datetime

from utils import TonAirdropClaim

shandler = logging.StreamHandler()
shandler.setFormatter(logging.Formatter(f'{Color.GREEN} %(asctime)s{Color.RESET} | {Color.LIGHTCYAN_EX}%(name)s{Color.RESET} | {Color.MAGENTA}%(levelname)s{Color.RESET} | %(message)s'))
shandler.setLevel(logging.INFO)

logging.basicConfig(level=logging.NOTSET,handlers=[shandler])
logger = logging.getLogger(__name__)

init(autoreset=True)
load_dotenv()

API_ID: int = int(os.environ.get('API_ID'))
API_HASH: str = os.environ.get('API_HASH')
BOT_TOKEN: str = os.environ.get('BOT_TOKEN')
CHECK_TIME: int = int(os.environ.get('CHECK_TIME', 60))
CHANNEL: str = os.environ.get('CHANNEL')

bot: TelegramClient = TelegramClient(None, API_ID, API_HASH)


REPORT_MESSAGE: str = lambda s, d: f'''
**[ {"🟢 Open" if s == False else "🔴 Close"} ]** Token withdrawal status
**[ {"🟢 открыть" if s == False else "🔴 Закрыто"} ]** Статус вывода токена
**[ {"🟢 باز " if s == False else "🔴 بسته "} ]** وضعیت برداشت توکن 

#dogs #dogs_airdrop #dogsclaim #tokentable_bot #tokentable\n
📅 **{d}**
'''


async def send_report():
    TonAirdropClaim.url = 'https://withdrawal.onetime.dog/withdrawal/2cd43l72TvK_W5wt9LvXFg'
    
    while True:
        await asyncio.sleep(CHECK_TIME)
        logger.info('Checking Airdrop...')
        res = await TonAirdropClaim.check_airdrop()
        logger.info(res)

        if isinstance(res, dict):
            is_withdrawal_busy: bool = False if res.get('error') == 'No choose option' and res.get('ok') == False else True
            
            timenow = datetime.now()
            message: str = REPORT_MESSAGE(s=is_withdrawal_busy, d=timenow)

            try:
                msg: types.Message = await bot.send_message(CHANNEL, message)
            except Exception as e:
                logger.error(f'{Color.RED} Send Report Error : {e}')



async def main():
    await bot.start(bot_token=BOT_TOKEN)
    me = await bot.get_me()
    logger.info(f'connceted to @{me.username}')
    
    bot.loop.create_task(send_report())
    await bot.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())