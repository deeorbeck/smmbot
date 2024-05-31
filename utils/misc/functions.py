import asyncio
import pytz
from datetime import datetime

async def get_time_in_tashkent():
    tz_tashkent = pytz.timezone('Asia/Tashkent')
    current_time = datetime.now(tz=tz_tashkent)
    return current_time
