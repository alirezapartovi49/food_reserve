from django.utils import timezone
from . import jalali


def numbers_converter(text):
    numbers = {
        "0":"۰",
        "1":"۱",
        "2":"۲",
        "3":"۳",
        "4":"۴",
        "5":"۵",
        "6":"۶",
        "7":"۷",
        "8":"۸",
        "9":"۹",
    }

    for key, value in numbers.items():
        text = text.replace(key, value)

    return text

def jalali_converter(time):
    jmonths = [
        "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
    ]

    time = timezone.localtime(time)

    str_time = f"{time.year},{time.month},{time.day}"
    list_time = list(jalali.Gregorian(str_time).persian_tuple())

    for index, month in enumerate(jmonths):
        if list_time[1] == index + 1:
            list_time[1] = month
            break

    out = f"{list_time[2]} {list_time[1]} {list_time[0]}, ساعت: {time.hour}:{time.minute}"

    return numbers_converter(out)