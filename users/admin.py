from users.forms import UserForm
from django.contrib import admin
from .models import LeaderBoard, UserInfo, Contact, QuestionMake, ContestInformation, ContestQuestions, ContestUsers, \
    Submissions
from .forms import User


# Register your models here.

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'mobile', 'college']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'Firstname', 'email', 'phone', 'message']


@admin.register(QuestionMake)
class QuestionMakeAdmin(admin.ModelAdmin):
    list_display = ['id', 'problem_name', 'authorname', 'difficulty', 'tags']


@admin.register(ContestInformation)
class ContestInformationAdmin(admin.ModelAdmin):
    list_display = ['id', 'cname', 'username',
                    'passcode', 'date', 'starttime', 'endtime']


@admin.register(ContestQuestions)
class ContestQuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'contest_name',)


@admin.register(ContestUsers)
class ContestUsersAdmin(admin.ModelAdmin):
    list_display = ('contest_na',)


@admin.register(Submissions)
class SubmissionsAdmin(admin.ModelAdmin):
    list_display = ('name_of_contest', 'name_of_question', 'name_of_user', 'language', 'dt', 'status', 'points',
                    'remaining_time_in_sec')


@admin.register(LeaderBoard)
class LeaderBoardAdmin(admin.ModelAdmin):
    list_display = (
        'con_name', 'uname', 'final_points', 'cumulative_score', 'number_of_submissions', 'successful_submissions',
        'college_name')
