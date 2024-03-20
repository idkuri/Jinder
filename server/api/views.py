from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
import psycopg2
# Create your views here.
# dbsettings = settings.DATABASES['default']
# print("Flag " + str(dbsettings))
# connector = psycopg2.connect(
#     dbname=dbsettings['NAME'],
#     user=dbsettings['USER'],
#     password=dbsettings['PASSWORD'],
#     host=dbsettings['HOST'],
#     port=dbsettings['PORT']
# )
# cursor = connector.cursor()


def register_user(request):
    return HttpResponse("User Registration")

def user_login(request):
    return HttpResponse("User Login")


# cursor.close()
# connector.close()
