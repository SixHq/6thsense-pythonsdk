import datetime
import time
import pytz


def get_time_now():
    tz = pytz.timezone('Africa/Lagos')
    today = datetime.datetime.now(tz=tz)
    return time.mktime(today.timetuple())


def get_todays_start():
    tz = pytz.timezone('Africa/Lagos')
    today = datetime.datetime.now(tz=tz).date()
    return time.mktime(today.timetuple())    

def get_day_from_now(days):
    tz = pytz.timezone('Africa/Lagos')
    today = datetime.datetime.now(tz=tz).date()  + datetime.timedelta(days=days)
    return time.mktime(today.timetuple())   


def get_min_offset_from_now(min):
    now = get_time_now()
    delta = min*60
    min = now+delta

    offset = min - now
    return offset


def get_offset_from_nine_am():
    now = get_time_now()
    start_date = get_todays_start()
    delta = 9*60*60
    nine_am = start_date+delta

    offset = nine_am - now
    return offset


def get_offset_from_twleve_fiteen():
    now = get_time_now()
    start_date = get_todays_start()
    delta = 12*60*60 + 57*60
    nine_am = start_date+delta
    offset = nine_am - now
    return offset


def get_offset_from_six_pm():
    now = get_time_now()
    start_date = get_todays_start()
    delta = 18*60*60
    six_am = start_date+delta

    offset = six_am - now
    return offset

def get_next_nine_am_day():
    next_date = get_day_from_now(1)
    return next_date + 9*60*60
    
def get_readable_date_from_time_stamp(ts):
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    
def get_day_from_time_stamp(time_stamp):
    time_stamp = datetime.datetime.fromtimestamp(time_stamp)
    day = time_stamp.strftime("%A")
    return day


def get_a_week_time(timestamp):
    return timestamp + 7*24*60*60

    