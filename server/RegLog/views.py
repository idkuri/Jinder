from django.shortcuts import render
from django.http import HttpResponse
from django.conf import global_settings
import psycopg2
# Create your views here.
dbsettings = global_settings.DATABASES['default']
connector = psycopg2.connect(
    dbname=dbsettings['NAME'],
    user=dbsettings['USER'],
    password=dbsettings['PASSWORD'],
    host=dbsettings['HOST'],
    port=dbsettings['PORT']
)
cursor = connector.cursor()


def register_user(request):
    return HttpResponse('hello world')


cursor.close()
connector.close()