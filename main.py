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

#dogs #dogs_airdrop #dogsclaim\n
📅 **{d}**
'''


async def send_report():
    TonAirdropClaim.url = 'https://ethsign-common.s3.us-east-1.amazonaws.com/cms/ton-airdrop-claim.json'
    
    is_already_pin: bool = False

    while True:
        await asyncio.sleep(CHECK_TIME)
        logger.info('Checking Airdrop...')
        res = await TonAirdropClaim.check_airdrop()
        logger.info(res)

        if isinstance(res, list):
            
            for x in res:
                is_dogs_airdrop: bool = True if x.get('data', {}).get('slug') == 'dogs' else False

                if is_dogs_airdrop:
                    is_busy: str = x.get('data', {}).get('isBusy', 'true')
                    is_busy: bool = False if is_busy == 'false' else True

                    timenow = datetime.now()

                    message: str = REPORT_MESSAGE(s=is_busy, d=timenow)

                    try:
                        msg: types.Message = await bot.send_message(CHANNEL, message)

                        if not is_busy and not is_already_pin:
                            is_already_pin = True
                            await msg.pin()

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