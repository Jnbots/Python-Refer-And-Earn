import asyncio
import importlib
from config import START_IMG,OWNER_ID
from pyrogram import idle
from Plugins import LOGGER, JN
from Plugins.modules import ALL_MODULES


async def smm_start():
    try:
        await JN.start()
    except Exception as ex:
        LOGGER.error(ex)
        quit(1)

    for all_module in ALL_MODULES:
        importlib.import_module("Plugins.modules." + all_module)

    LOGGER.info(f"@{JN.username} Started.")
    # await JN.send_photo(OWNER_ID,START_IMG,"I am Alive")
    await idle()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(smm_start())
    LOGGER.info("Stopping smm bot")