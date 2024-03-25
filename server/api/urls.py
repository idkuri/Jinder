from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'register/?$', views.register_user),
    re_path(r'login/?$', views.user_login, ),
    re_path(r'authenticate/?$', views.authenticate, ),
    re_path(r'logout/?$', views.logout, ),
    re_path(r'createPOST/?$', views.createPOST, ),
    re_path(r'getPOST/?$', views.getPOST, ),
    re_path(r'like/?$', views.like, ),
    re_path(r'getLike/?$', views.checkLike, ),
]

