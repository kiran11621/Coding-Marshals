from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path
from users.views import AddQuestionsToContest, update_question_list
from . import views

urlpatterns = [

    # users authentication

    path('users_signup/', views.signup_view, name='users_signup'),
    path('users_login/', views.login_page, name='login'),
    path('logout/', views.logoutUser, name='logout'),


    path('user_profile/<int:pk>', views.user_profile, name='user_profile'),
    path('user_profile_update/<int:pk>', views.user_profile_update, name='user_profile_update'),


    path('indexlogin/', views.indexlogin, name='indexlogin'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('navbar_contest/', views.navbar_contest, name='navcon'),


    path('create_contest/', views.create_contest, name='create_contest'),
    path('contest_questions/<str:uname>/<int:pk>', views.contestquestions, name='contestquestions'),
    path('contestquestionafter/<str:uname>/<int:pk>', views.contestquestionsafterselection,
         name="contestquestionsafterselection"),
    path('question_list/<str:uname>/<int:pk>', AddQuestionsToContest.as_view()),
    path('update_question_list/<str:uname>/<int:pk>', update_question_list.as_view()),
    path('Questionmake/<str:uname>/<int:pk>', views.questionmake, name='question'),

    # urls for user contest display
    path('futurecontest/', views.display_future_contest_list, name="listofcontests"),
    path('pastcontest/', views.display_past_contest_list, name="pastcontest"),
    path('runningcontest/', views.display_running_contest_list, name="runningcontest"),
    path('runningcontest/<int:pk>/<str:cname>', views.checkpasscode, name="validatepasscode"),


    path('contest_landing_page/<int:pk>/<str:cname>/<str:current_user>', views.contest_landing_page,
         name="contest_landing_page"),
    path('particular_question/<str:current_user>/<str:cname>/<str:pk>/<str:problem_name>', views.particular_question,
         name="particular_question"),

         

    path('submit/<str:current_user>/<str:cname>/<str:pk>/<str:problem_name>',views.submit_solution,name="submitsoln"),
    path('leaderboard/<str:cname>/<str:current_user>',views.leaderboard_display,name="leaderboard"),
    path('past_leaderboard/<str:cname>',views.display_past_contest_leaderboard,name="past_leaderboard"),
    path('information/',views.information,name="information"),



    # reset password urls
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_form.html") ,name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_done.html"),name="password_reset_complete"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
