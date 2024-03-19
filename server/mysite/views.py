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
    print(favicon_path)
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