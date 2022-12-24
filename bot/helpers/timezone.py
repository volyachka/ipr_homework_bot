from datetime import datetime
import pytz


def get_msk_time():
    tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz)
    msk_time = now.strftime('%H:%M:%S')
    return msk_time
