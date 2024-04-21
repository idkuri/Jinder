from django.shortcuts import render
from django.http import HttpResponse
from django.http import FileResponse
from django.conf import settings

import os
import mimetypes

# Create your views here.
def serveRoot(request):
    return render(request, 'index.html')

def serveFavicon(request):
    favicon_path = os.path.join(settings.STATIC_ROOT, 'favicon.ico')
    with open(favicon_path, 'rb') as f:
        return HttpResponse(f.read(), content_type='image/x-icon')

def serveImage(request):
    url_param = request.GET.get('url', '')  
    if url_param.startswith('/'):
        url_param = url_param[1:]
    image_path = os.path.join(settings.STATIC_ROOT, url_param)
    mime_type, _ = mimetypes.guess_type(image_path)
    with open(image_path, 'rb') as f:
        return HttpResponse(f.read(), content_type=mime_type)
    
def serveMedia(request):
    url_param = request.path
    if url_param.startswith('/media'):
        url_param = url_param[7:]
    image_path = os.path.join(settings.MEDIA_ROOT, url_param)
    mime_type, _ = mimetypes.guess_type(image_path)
    with open(image_path, 'rb') as f:
        print("Hello")
        return HttpResponse(f.read(), content_type=mime_type)

def serveLoginPage(request):
    return render(request, 'login.html')

def serveChatRoom(request):
    return render(request, 'chat.html')

def serveRegisterPage(request):
    return render(request, 'register.html')

def serveRSC(request):
    url_param = request.path
    if url_param.startswith('/'):
        url_param = url_param[1:]
    rsc_path = os.path.join(settings.STATIC_ROOT, url_param)
    with open(rsc_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='text/plain')
        return response

def serveStatic(request):
    url_param = request.path
    if url_param.startswith('/'):
        url_param = url_param[1:]
    file_path = os.path.join(settings.STATIC_ROOT, url_param)
    mime_type, _ = mimetypes.guess_type(file_path)
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type=mime_type)
        return response
