from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.conf.urls import url

favicon_view = RedirectView.as_view(url='/templates/favicon.ico', permanent=True)

urlpatterns = [
    path('', views.serveRoot, name="serveRoot"),
    # url(r'^favicon\.ico$',RedirectView.as_view(url='/templates/favicon.ico')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

