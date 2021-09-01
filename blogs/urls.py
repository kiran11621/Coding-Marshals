from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('display_blogs/', views.display_blogs, name='display_blogs'),
    path('create_blog/', views.create_blog, name='create_blog'),
]
