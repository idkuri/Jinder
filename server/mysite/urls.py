from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.conf.urls import url

urlpatterns = [
    path('', views.serveRoot, name="serveRoot"),
    path('favicon.ico/', views.serveFavicon, name="serveFavicon"),
    path('_next/image/', views.serveImage, name="serveImage"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

