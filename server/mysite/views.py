from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

# Create your views here.
def serveRoot(request):
    return render(request, 'index.html')

def serveFavicon(request):
    return render(request, 'favicon.ico')