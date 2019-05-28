import time
import datetime


# https://stackoverflow.com/questions/7703865/going-from-twitter-date-to-python-datetime-date
def convert_string_timestamp(time_str):
    ts = time.mktime(time.strptime(time_str, '%a %b %d %H:%M:%S +0000 %Y'))
    return ts

def get_year(time_str):
    return int(time_str.split()[-1])
