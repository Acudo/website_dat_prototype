import datetime

now = datetime.datetime.now(datetime.UTC)

if now > datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=1):
    print("evil")
else:
    print("not evil")
