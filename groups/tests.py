from django.test import TestCase

# Create your tests here.


from datetime import datetime, timedelta

week_list = ("MON", "TUE", "WHE", "THU", "FRI", "SAT", "SUN")

a = "WHE"

print(week_list.index(a))

dt = datetime(2020, 4, 22)
temp = 7 - dt.weekday()
td = timedelta(days=(temp - 7))

print(dt)
print(td)
print(dt + td)


def cal_deadline(today, c_weekday):
    weekday = today.weekday()
    if c_weekday > weekday:
        print("A")
        between_day = c_weekday - weekday
        td = timedelta(days=(between_day + 7))
        return today + td
    else:
        print("B")
        between_day = c_weekday - weekday
        td = timedelta(days=(7 - between_day))
        return today + td


print()
print(cal_deadline(dt, 3))
