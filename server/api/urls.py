from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'register/?$', views.register_user),
    re_path(r'login/?$', views.user_login, ),
    re_path(r'authenticate/?$', views.authenticate, ),
    re_path(r'logout/?$', views.logout, ),
]

