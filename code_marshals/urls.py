from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # all admin side features

    path('admin_login/', views.admin_login, name='admin_login'),
    path('logout/', views.logoutUser, name='logout'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('admin_navbar/', views.admin_navbar, name='admin_navbar'),
    path('admin_user_view/hwjhvqhvwgudvguesvyufy', views.admin_user_view, name='admin_user_view'),
    path('update_user_details/<int:pk>', views.update_user_details, name='update_user_details'),
    path('delete_user_details/<int:pk>', views.delete_user_details, name='delete_user_details'),
    path('admin_question_view/', views.admin_question_view, name='admin_question_view'),
    path('update_question_details/<int:pk>', views.update_question_details, name='update_question_details'),
    path('delete_question/<int:pk>', views.delete_question, name='delete_question'),
    path('admin_add_question/', views.admin_add_question, name='admin_add_question'),
    path('admin_contest_view/', views.admin_contest_view, name='admin_contest_view'),
    path('delete_contest/<int:pk>', views.delete_contest, name='delete_contest'),

]
