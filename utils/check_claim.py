import aiohttp
import logging

logger = logging.getLogger(__name__)

class TonAirdropClaim:
    url: str = None

    @classmethod
    async def check_airdrop(cls) -> dict | None:
        async with aiohttp.ClientSession() as http_client:
            try:
                res = await http_client.get(cls.url)
                res.raise_for_status()
                response_json = await res.json()
                return response_json
            
            except Exception as e:
                logger.error(f'check airdrop error : {e}')
                return None
            

