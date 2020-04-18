from blacklist.models import Blacklist

def my_job():

    b = Blacklist(ip="123456")
    b.save()
