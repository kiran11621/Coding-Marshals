import datetime
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import *
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.views import View
from . import forms, models
from django.db import IntegrityError
from .models import Contact, ContestInformation, ContestUsers, LeaderBoard, Submissions
from users.models import QuestionMake, ContestQuestions
from users.filters import ProblemsFilter
import random
from datetime import *
import datetime
import os
import requests
import json
from django.template.defaulttags import register
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        return redirect('indexlogin')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('indexlogin')
            else:
                messages.info(request, 'User or Password is incorrect')

        context = {}
        return render(request, 'users/users_login.html', context)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('indexlogin')
    else:
        userForm = forms.UserForm()
        infoForm = forms.InfoForm()

        if request.method == 'POST':
            userForm = forms.UserForm(request.POST)
            infoForm = forms.InfoForm(request.POST, request.FILES)

            if userForm.is_valid() and infoForm.is_valid():
                user = userForm.save()
                user.set_password(user.password)
                user.save()

                users = infoForm.save(commit=False)
                users.user = user
                users.save()

                user_group = Group.objects.get_or_create(name='USERS')
                user_group[0].user_set.add(user)
                infoForm.save()

                messages.success(
                    request, 'Account was created successfully')

                subject = 'welcome to Code Marshals Family'
                n1='\n'
                message = f'Hi {user.username}, Thank You for registering in Code Marshals.{n1}Head on to Participate in Contests with your Friends in just few steps'
                email_from = settings.EMAIL_HOST_USER
                n1='\n'
                recipient_list = [user.email, ]
                send_mail(subject, message, email_from, recipient_list,fail_silently=False)
                return redirect('login')

        mydict = {'userForm': userForm, 'infoForm': infoForm}       
        return render(request, 'users/users_signup.html', context=mydict)


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url="login")
def user_profile(request, pk):
    users = models.UserInfo.objects.get(id=pk)
    submissions = models.Submissions.objects.all().filter(name_of_user=users.user.username)

    s = set()
    for i in submissions:
        s.add(i.name_of_contest)
    print(s)

    # Languages used 
    labels = ['CPP', 'JAVA', 'PYTHON']
    data = []

    try:
        allsubmissions = models.Submissions.objects.all().filter(name_of_user=users.user.username).count()
        cppsubmissions = data.append(models.Submissions.objects.all().filter(name_of_user=users.user.username, language='cpp').count()/allsubmissions*100)
        javasubmissions = data.append(models.Submissions.objects.all().filter(name_of_user=users.user.username, language='java').count()/allsubmissions*100)
        pythonsubmissions = data.append(models.Submissions.objects.all().filter(name_of_user=users.user.username, language='py').count()/allsubmissions*100)
        print(pythonsubmissions)
    except:
        pass


    # Verdict of submissions

    labels1 = ['Accepted','Wrong Answer']
    data1 =[]

    ac_submissions = models.Submissions.objects.all().filter(name_of_user=users.user.username,status=True).count()
    wa_submissions = models.Submissions.objects.all().filter(name_of_user=users.user.username,status=False).count()

    data1.append(ac_submissions)
    data1.append(wa_submissions)


    context = {
        'pk': pk,
        'users': users,
        's': s,
        'labels': labels,
        'data': data,
        'labels1':labels1,
        'data1':data1,
    }
    return render(request, 'users/user_profile.html',context)


@login_required(login_url="login")
def user_profile_update(request, pk):
    users = models.UserInfo.objects.get(id=pk)
    user = models.User.objects.get(id=users.user_id)
    userForm = forms.UserForm(instance=user)
    infoForm = forms.InfoForm(request.FILES, instance=users)


    mydict = {
        'userForm': userForm,
        'infoForm': infoForm,
        'user': user,
        'users': users
    }

    if request.method == 'POST':
        userForm = forms.UserForm(request.POST, instance=user)
        infoForm = forms.InfoForm(request.POST, request.FILES, instance=users)

        if userForm.is_valid() and infoForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            users = infoForm.save(commit=False)
            users.user = user
            users.save()

            return redirect('user_profile', pk)
    return render(request, 'users/user_profile_update.html', context=mydict)


def index(request):
    return render(request, 'index.html')


def navbar(request):
    return render(request, 'navbar.html')


def about(request):
    return render(request, 'users/about.html')


def navbar_contest(request):
    return render(request, 'users/navbar_contest.html')



@login_required(login_url="login")
def contact(request):
    if request.method == 'POST':
        Firstname = request.POST.get('Firstname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')


        contact = Contact(Firstname=Firstname, email=email,
                          phone=phone, message=message)
        contact.save()

        subject = 'Contacted Code Marshals'
        n1='\n'
        message = f'Hi {Firstname}, Thank You for Contacting Us.{n1}We wil reach out to you soon'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list,fail_silently=False)
        return redirect('indexlogin')

    return render(request, 'users/contact.html')



@login_required(login_url="login")
def blogs(request):
    return render(request, 'users/blogs.html')


@login_required(login_url="login")
def information(request):
    return render(request, 'users_contest_display/information.html')



@login_required(login_url="login")
def indexlogin(request):

    current_user = request.user.id

    user = models.User.objects.get(id=current_user)

    if request.user.username != 'admin':
        userinfo = models.UserInfo.objects.get(user=user)

        return render(request, 'users/indexlogin.html', {'pk': userinfo.id})
    return render(request, 'users/indexlogin.html')

def questionmake(request, uname, pk):
    contest = ContestInformation.objects.get(pk=pk)
    context = {
        'name': contest.cname,
        'uname': contest.username,
        'prim_key': contest.pk,
    }

    if request.method == 'POST':
        problem_name = request.POST.get('problem')
        authorname = request.POST.get('authorname')
        problem_statement = request.POST.get('problem_statement')
        input_format = request.POST.get('input_format')
        constraints = request.POST.get('constraints')
        output_format = request.POST.get('output_format')
        tags = request.POST.get('tags')
        sample_input = request.POST.get('sample_input')
        sample_output = request.POST.get('sample_output')
        explanation=request.POST.get('explanation')
        hidden_input = request.FILES['hidden_input']
        hidden_output = request.FILES['hidden_output']
        difficulty = request.POST.get('difficulty')

        question = QuestionMake(problem_name=problem_name, authorname=authorname, problem_statement=problem_statement,
                                input_format=input_format, constraints=constraints, output_format=output_format,
                                tags=tags, sample_input=sample_input, sample_output=sample_output,explanation=explanation,
                                hidden_input=hidden_input, hidden_output=hidden_output, difficulty=difficulty)

        try:
            question.save()

        except:
            messages.error(request, 'Question Name Already taken')
            return render(request, 'users/Question_making_page.html', context)

        redirect('question', uname=uname, pk=pk)

    return render(request, 'users/Question_making_page.html', context)

@login_required(login_url="login")
def create_contest(request):
    if request.method == 'POST':
        cname = request.POST.get('cname')
        username = request.POST.get('username')
        date = request.POST.get('date')
        starttime = request.POST.get('starttime')
        endtime = request.POST.get('endtime')
        description = request.POST.get('description')
        rules = request.POST.get('rules')
        prizes = request.POST.get('prizes')

        characters = list('abcdefghijklmnopqrstuvwxyz')

        length = 6

        passcode = ""

        passcode += str(username[0:2])
        passcode += str(cname[0:2])
        for x in range(length):
            passcode += random.choice(characters)

        user = models.User.objects.get(id=request.user.id)

        contest_info = ContestInformation(cname=cname, username=username, passcode=passcode, description=description,
                                          date=date, starttime=starttime, endtime=endtime, rules=rules,
                                          prizes=prizes)

        subject = 'Contest Created'
        n1='\n'
        message = f'Hi {username}, Your contest named {cname} was created.{n1}Passcode for your contest is {passcode}.{n1}Share with your friends to invite them for participating in contest'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail(subject, message, email_from, recipient_list,fail_silently=False)

        try:
            contest_info.save()
            return redirect('contestquestions', uname=contest_info.username, pk=contest_info.pk)
        except:
            messages.error(request, 'Contest Name Already taken')
        
    return render(request, 'users/create_contest.html')


def contestquestions(request, uname, pk):
    contest = ContestInformation.objects.get(pk=pk)

    context = {
        'name': contest.cname,
        'uname': contest.username,
        'prim_key': contest.pk,
        'passcode': contest.passcode,
    }
    return render(request, 'users/contest_questions_selected.html', context)


class AddQuestionsToContest(View):
    def get(self, request, uname, pk, *args, **kwargs):
        questions = QuestionMake.objects.all()
        myFilter = ProblemsFilter(request.GET, queryset=questions)
        questions = myFilter.qs
        context = {'questions': questions, 'uname': uname, 'myFilter': myFilter}
        return render(request, 'users/Questions_list.html', context)

    def post(self, request, uname, pk, *args, **kwargs):
        question_items = {
            'items': []
        }
        print('ijfrejfierjeui')
        items = request.POST.getlist('items[]')
        a1 = ContestInformation.objects.get(pk=pk)
        quest = ContestQuestions.objects.create(contest_name=a1)
        quest.questions.add(*items)
        return redirect('contestquestionsafterselection', uname=uname, pk=quest.pk)

        return render(request, 'users/contest_questions_selected.html')

def contest_questions_selected(request):
    return render(request, 'users/contest_questions_selected.html')
    
class update_question_list(View):
    def get(self, request, uname, pk, *args, **kwargs):
        questions = QuestionMake.objects.all()
        myFilter = ProblemsFilter(request.GET, queryset=questions)
        questions = myFilter.qs
        context = {'questions': questions, 'uname': uname, 'myFilter': myFilter}
        return render(request, 'users/Questions_list.html', context)

    def post(self, request, uname, pk, *args, **kwargs):
        question_items = {
            'items': []
        }
        items = request.POST.getlist('items[]')
        a1 = ContestInformation.objects.get(pk=pk)
        quest = ContestQuestions.objects.get(contest_name=a1)

        try:
            quest.questions.add(*items)
        except:
            return redirect('contestquestionsafterselection', uname=uname, pk=quest.pk)
        return redirect('contestquestionsafterselection', uname=uname, pk=quest.pk)
        return render(request, 'users/contestquestionsafterselection.html')


def contestquestionsafterselection(request, uname, pk):
    ques = ContestQuestions.objects.get(pk=pk)
    cname = ques.contest_name,
    pointer = ContestInformation.objects.get(cname=cname[0])
    context = {
        'Contest_name': ques.contest_name,
        'uname': uname,
        'q': ques.questions,
        'pk': cname[0].pk,
        'passcode': pointer.passcode,

    }
    return render(request, 'users/contestquestionsafterselection.html', context)


# view for contest_list_view

def display_past_contest_list(request):
    today = datetime.datetime.now()

    total_sec_today = (today.hour * 60 * 60) + (today.minute * 60) + (today.second)
    print(total_sec_today)

    l = []

    obj = ContestInformation.objects.order_by('date', 'starttime', 'endtime').reverse()

    for i in obj:
        if i.date.year < today.year:
            l.append(i)
        elif i.date.year == today.year and i.date.month < today.month:
            l.append(i)
        elif i.date.year == today.year and i.date.month == today.month and i.date.day < today.day:
            l.append(i)
        elif i.date.year == today.year and i.date.month == today.month and i.date.day == today.day:
            total_sec_till_starttime = (i.starttime.hour * 60 * 60) + (i.starttime.minute * 60) + (
                i.starttime.second)
            total_sec_till_endtime = (i.endtime.hour * 60 * 60) + (i.endtime.minute * 60) + (i.endtime.second)
            if total_sec_today > total_sec_till_endtime:
                l.append(i)

    paginator = Paginator(l, 8, orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users_contest_display/pastcontest.html', {'obj': page_obj})


def display_past_contest_leaderboard(request, cname):
    obj = models.Submissions.objects.all()


    obj1 = ContestInformation.objects.get(cname=cname)

    obj2 = ContestQuestions.objects.get(contest_name=obj1)

    filtered_contest = models.Submissions.objects.all().filter(name_of_contest=obj2)

    # dictionary of count of number of submissions of particular user
    d = {}

    for i in filtered_contest:
        if i.name_of_user in d:
            d[i.name_of_user] += 1
        else:
            d[i.name_of_user] = 1

    for keys, values in d.items():
        print(keys, values)

    cumulative_score_dict = {}
    point_dict = {}

    # Filtering user with contest

    for key in d:
        l1 = []
        print(key)
        filtered_contest_with_user = models.Submissions.objects.all().filter(name_of_contest=obj2, name_of_user=key,
                                                                             status=True)


        for i in filtered_contest_with_user:
            if i.name_of_user in cumulative_score_dict:
                if i.name_of_question not in l1:
                    cumulative_score_dict[i.name_of_user] += i.remaining_time_in_sec
                    point_dict[i.name_of_user] += 100
                    l1.append(i.name_of_question)


            else:
                cumulative_score_dict[i.name_of_user] = i.remaining_time_in_sec
                point_dict[i.name_of_user] = 100
                l1.append(i.name_of_question)


        user = models.User.objects.get(username=key)
        print(user)
        userinfo = models.UserInfo.objects.get(user=user)
        print(userinfo.college)

        try:
            con_name = obj2
            uname = key
            a = LeaderBoard.objects.get(con_name=obj2, uname=key)
            a.final_points = point_dict[uname]
            a.cumulative_score = cumulative_score_dict[uname]
            a.number_of_submissions = d[uname]
            a.successful_submissions = point_dict[uname] // 100
            a.college_name = userinfo.college
            a.save()

        except:
            con_name = obj2
            uname = key
            final_points = point_dict[uname]
            cumulative_score = cumulative_score_dict[uname]
            number_of_submissions = d[uname]
            successful_submissions = point_dict[uname] // 100
            college_name = userinfo.college
            leaderboard = LeaderBoard(con_name=con_name, uname=uname, final_points=final_points,
                                      cumulative_score=cumulative_score, number_of_submissions=number_of_submissions,
                                      successful_submissions=successful_submissions, college_name=college_name)
            leaderboard.save()

    board = models.LeaderBoard.objects.all().filter(con_name=obj2).order_by('-cumulative_score')
    print(board)

    context = {
        'board': board,
    }

    return render(request, "users_contest_display/past_leaderboard.html", context)


def display_future_contest_list(request):
    today = datetime.datetime.now()

    total_sec_today = (today.hour * 60 * 60) + (today.minute * 60) + (today.second)

    l = []

    obj = ContestInformation.objects.order_by('date', 'starttime', 'endtime')

    for i in obj:

        if i.date.year > today.year:
            l.append(i)
        elif i.date.year == today.year and i.date.month > today.month:
            l.append(i)
        elif i.date.year == today.year and i.date.month == today.month and i.date.day > today.day:
            l.append(i)
        elif i.date.year == today.year and i.date.month == today.month and i.date.day == today.day:
            total_sec_till_starttime = (i.starttime.hour * 60 * 60) + (i.starttime.minute * 60) + (i.starttime.second)
            total_sec_till_endtime = (i.endtime.hour * 60 * 60) + (i.endtime.minute * 60) + (i.endtime.second)
            if total_sec_today < total_sec_till_starttime and total_sec_today < total_sec_till_endtime:
                l.append(i)

    paginator = Paginator(l, 8, orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        passcode = request.POST.get('passcode')
        print(passcode)

    return render(request, 'users_contest_display/futurecontest.html', {'obj': page_obj})


def display_running_contest_list(request):
    today = datetime.datetime.now()

    total_sec_today = (today.hour * 60 * 60) + (today.minute * 60) + (today.second)
    print(total_sec_today)

    l = []

    obj = ContestInformation.objects.order_by('date', 'starttime', 'endtime')

    for i in obj:
        if i.date.year == today.year and i.date.month == today.month and i.date.day == today.day:
            total_sec_till_starttime = (i.starttime.hour * 60 * 60) + (i.starttime.minute * 60) + (i.starttime.second)
            total_sec_till_endtime = (i.endtime.hour * 60 * 60) + (i.endtime.minute * 60) + (i.endtime.second)
            if total_sec_today >= total_sec_till_starttime and total_sec_today <= total_sec_till_endtime:
                l.append(i)

    paginator = Paginator(l, 8, orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users_contest_display/runningcontest.html', {'obj': page_obj})


def checkpasscode(request, pk, cname):


    user = models.User.objects.get(id=request.user.id)

    users = models.UserInfo.objects.get(user=user)


    if request.method == 'POST':
        passfromuser = request.POST.get('pass')

        obj = ContestInformation.objects.get(pk=pk)

        obj1 = ContestQuestions.objects.get(contest_name=obj)


        if obj.passcode == passfromuser:

            user = models.UserInfo.objects.get(id=users.id)
           
            l1 = []
            l1.append(user)

            try:
                quest = ContestUsers.objects.get(contest_na=obj1)
                quest.username.add(*l1)
            except:
                quest = ContestUsers.objects.create(contest_na=obj1)
                print(quest)

                quest.username.add(*l1)

            return redirect("contest_landing_page", pk, cname, request.user.id)
        else:
            messages.info(request, "Wrong Passcode Try Again!")

    return render(request, "users_contest_display/enter_passcode_page.html")


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def contest_landing_page(request, pk, cname, current_user):
    cname = models.ContestInformation.objects.get(pk=pk)
    contest = ContestInformation.objects.get(pk=pk)
    question = models.ContestQuestions.objects.get(contest_name=cname)
    q = question.questions
    qlist = {}
    for i in q.all():
        qlist[i.problem_name] = "Not Accepted Yet"

    listq = []
    for i in q.all():
        listq.append(i.problem_name)


    obj1 = ContestInformation.objects.get(cname=cname)
    obj2 = ContestQuestions.objects.get(contest_name=obj1)
    user = models.User.objects.get(id=current_user)
    filtered_contest = models.Submissions.objects.all().filter(name_of_contest=obj2, name_of_user=user, status=True)

    for i in filtered_contest:
        if i.name_of_question in qlist.keys():
            qlist[i.name_of_question] = "Accepted"

    countques = {}
    for i in listq:
        filtered_questions = models.Submissions.objects.all().filter(name_of_contest=obj2, name_of_question=i,
                                                                     status=True).count()

        countques[i] = filtered_questions

    # -------------------------------------------------------------------------------------------------------------------
    obj = models.Submissions.objects.all()

    print(obj)

    obj1 = ContestInformation.objects.get(cname=cname)

    obj2 = ContestQuestions.objects.get(contest_name=obj1)

    filtered_contest = models.Submissions.objects.all().filter(name_of_contest=obj2)
    print(filtered_contest)

    # dictionary of count of number of submissions of particular user
    d = {}

    for i in filtered_contest:
        if i.name_of_user in d:
            d[i.name_of_user] += 1
        else:
            d[i.name_of_user] = 1

    for keys, values in d.items():
        print(keys, values)

    cumulative_score_dict = {}
    point_dict = {}

    # Filtering user with contest

    for key in d:
        l1 = []
        print(key)
        filtered_contest_with_user = models.Submissions.objects.all().filter(name_of_contest=obj2, name_of_user=key,
                                                                             status=True)
        print(filtered_contest_with_user)

        for i in filtered_contest_with_user:
            if i.name_of_user in cumulative_score_dict:
                if i.name_of_question not in l1:
                    cumulative_score_dict[i.name_of_user] += i.remaining_time_in_sec
                    point_dict[i.name_of_user] += 100
                    l1.append(i.name_of_question)


            else:
                cumulative_score_dict[i.name_of_user] = i.remaining_time_in_sec
                point_dict[i.name_of_user] = 100
                l1.append(i.name_of_question)



        user = models.User.objects.get(username=key)

        userinfo = models.UserInfo.objects.get(user=user)


        try:
            con_name = obj2
            uname = key
            a = LeaderBoard.objects.get(con_name=obj2, uname=key)
            a.final_points = point_dict[uname]
            a.cumulative_score = cumulative_score_dict[uname]
            a.number_of_submissions = d[uname]
            a.successful_submissions = point_dict[uname] // 100
            a.college_name = userinfo.college
            a.save()

        except:
            if len(point_dict)==0:
                break;
            con_name = obj2
            uname = key
            final_points = point_dict[uname]
            cumulative_score = cumulative_score_dict[uname]
            number_of_submissions = d[uname]
            successful_submissions = point_dict[uname] // 100
            college_name = userinfo.college
            leaderboard = LeaderBoard(con_name=con_name, uname=uname, final_points=final_points,
                                      cumulative_score=cumulative_score, number_of_submissions=number_of_submissions,
                                      successful_submissions=successful_submissions, college_name=college_name)
            leaderboard.save()

    board = models.LeaderBoard.objects.all().filter(con_name=obj2).order_by('-cumulative_score')[:5]
    print(board)
    # -------------------------------------------------------------------------------------------------------------------
    formatedtime = contest.endtime.strftime("%H:%M:%S")
    context = {
        'cname': cname,
        'pk': pk,
        'current_user': current_user,
        'question': question.questions,
        'description': contest.description,
        'rules': contest.rules,
        'prizes': contest.prizes,
        'date': contest.date,
        'start': contest.starttime,
        'end': contest.endtime,
        'username': contest.username,
        'qlist': qlist,
        'countques': countques,
        'board': board,
        'formatedtime': formatedtime,
    }
    return render(request, "users_contest_display/contest_landing_page.html", context=context)


def particular_question(request, current_user, cname, pk, problem_name):
    question = models.QuestionMake.objects.get(problem_name=problem_name)
    contest = ContestInformation.objects.get(pk=pk)

    total_sec_till_starttime = (contest.starttime.hour * 60 * 60) + (contest.starttime.minute * 60) + (
        contest.starttime.second)
    total_sec_till_endtime = (contest.endtime.hour * 60 * 60) + (contest.endtime.minute * 60) + (contest.endtime.second)
    time_left = total_sec_till_endtime - total_sec_till_starttime
    formatedtime = contest.endtime.strftime("%H:%M:%S")


    obj = models.Submissions.objects.all()



    obj1 = ContestInformation.objects.get(cname=cname)

    obj2 = ContestQuestions.objects.get(contest_name=obj1)

    filtered_contest = models.Submissions.objects.all().filter(name_of_contest=obj2)


    # dictionary of count of number of submissions of particular user
    d = {}

    for i in filtered_contest:
        if i.name_of_user in d:
            d[i.name_of_user] += 1
        else:
            d[i.name_of_user] = 1



    cumulative_score_dict = {}
    point_dict = {}

    # Filtering user with contest

    for key in d:
        l1 = []
 
        filtered_contest_with_user = models.Submissions.objects.all().filter(name_of_contest=obj2, name_of_user=key,
                                                                             status=True)


        for i in filtered_contest_with_user:
            if i.name_of_user in cumulative_score_dict:
                if i.name_of_question not in l1:
                    cumulative_score_dict[i.name_of_user] += i.remaining_time_in_sec
                    point_dict[i.name_of_user] += 100
                    l1.append(i.name_of_question)


            else:
                cumulative_score_dict[i.name_of_user] = i.remaining_time_in_sec
                point_dict[i.name_of_user] = 100
                l1.append(i.name_of_question)

     

        user = models.User.objects.get(username=key)
        userinfo = models.UserInfo.objects.get(user=user)


        try:
            con_name = obj2
            uname = key
            a = LeaderBoard.objects.get(con_name=obj2, uname=key)
            a.final_points = point_dict[uname]
            a.cumulative_score = cumulative_score_dict[uname]
            a.number_of_submissions = d[uname]
            a.successful_submissions = point_dict[uname] // 100
            a.college_name = userinfo.college
            a.save()

        except:
            if len(point_dict)==0:
                break;
            con_name = obj2
            uname = key
            final_points = point_dict[uname]
            cumulative_score = cumulative_score_dict[uname]
            number_of_submissions = d[uname]
            successful_submissions = point_dict[uname] // 100
            college_name = userinfo.college
            leaderboard = LeaderBoard(con_name=con_name, uname=uname, final_points=final_points,
                                      cumulative_score=cumulative_score, number_of_submissions=number_of_submissions,
                                      successful_submissions=successful_submissions, college_name=college_name)
            leaderboard.save()

    board = models.LeaderBoard.objects.all().filter(con_name=obj2).order_by('-cumulative_score')
    print(board)

    context = {
        'cname': cname,
        'pk': pk,
        'current_user': current_user,
        'question': question,
        'description': contest.description,
        'endtime': contest.endtime,
        'date': contest.date,
        'formatedtime': formatedtime,
        'problem_name': question.problem_name,
        'board': board,
    }
    return render(request, "users_contest_display/particular_question.html", context=context)



def submit_solution(request, current_user, cname, pk, problem_name):
    c = models.ContestInformation.objects.get(pk=pk)
    cname = models.ContestQuestions.objects.get(contest_name=c)
    obj = models.QuestionMake.objects.get(problem_name=problem_name)

    hidden_input = "media/" + str(obj.hidden_input)

    hidden_output = "media/" + str(obj.hidden_output)

    with open(hidden_input, 'r') as f:
        input_file = f.read()

    with open(hidden_output, 'r') as f:
        output_file = f.read()


    if request.method == "POST":

        name_of_contest = cname
        name_of_question = problem_name
        name_of_user = request.user
        code = request.POST.get('code')
        language = request.POST.get('language')
        dt = datetime.datetime.now()

        if judge_code(code, language, input_file, output_file):
            status = True
        else:
            status = False

        if status == True:
            points = 100
            total_sec_today = (dt.hour * 60 * 60) + (dt.minute * 60) + (dt.second)
            total_sec_till_endtime = (c.endtime.hour * 60 * 60) + (c.endtime.minute * 60) + (c.endtime.second)
            print(total_sec_today)
            print(total_sec_till_endtime)
            remaining_time_in_sec = total_sec_till_endtime - total_sec_today
        else:
            points = 0
            remaining_time_in_sec = 0

        submit = Submissions(name_of_contest=name_of_contest, name_of_question=name_of_question,
                             name_of_user=name_of_user, code=code, language=language, dt=dt, status=status,
                             points=points, remaining_time_in_sec=remaining_time_in_sec)
        submit.save()

        if status == True:
            result = True
        else:
            result = False

        context = {
            'result': result,
            'pk': pk,
            'cname': cname,
            'current_user': current_user
        }

        return render(request, "users_contest_display/submit_solution.html", context)
    contex = {
            'res':True,
            'pk': pk,
            'cname': cname,
            'current_user': current_user
        }

    return render(request, "users_contest_display/submit_solution.html",contex)





def judge_code(code, language, input_file, output_file):
    url = "https://codexweb.netlify.app/.netlify/functions/enforceCode"

    payload = {"code": code,
               "language": language,
               "input": input_file
               };

    json_data = json.dumps(payload)

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=json_data)


    result = response.json()


    useroutput = result["output"]

    if useroutput == output_file:
        return True
    else:
        return False


def leaderboard_display(request, cname, current_user):
    obj = models.Submissions.objects.all()

    obj1 = ContestInformation.objects.get(cname=cname)

    obj2 = ContestQuestions.objects.get(contest_name=obj1)

    filtered_contest = models.Submissions.objects.all().filter(name_of_contest=obj2)

    # dictionary of count of number of submissions of particular user 
    d = {}

    for i in filtered_contest:
        if i.name_of_user in d:
            d[i.name_of_user] += 1
        else:
            d[i.name_of_user] = 1


    cumulative_score_dict = {}
    point_dict = {}

    # Filtering user with contest

    for key in d:
        l1 = []
        filtered_contest_with_user = models.Submissions.objects.all().filter(name_of_contest=obj2, name_of_user=key,
                                                                             status=True)


        for i in filtered_contest_with_user:
            if i.name_of_user in cumulative_score_dict:
                if i.name_of_question not in l1:
                    cumulative_score_dict[i.name_of_user] += i.remaining_time_in_sec
                    point_dict[i.name_of_user] += 100
                    l1.append(i.name_of_question)


            else:
                cumulative_score_dict[i.name_of_user] = i.remaining_time_in_sec
                point_dict[i.name_of_user] = 100
                l1.append(i.name_of_question)


        user = models.User.objects.get(username=key)
        print(user)
        userinfo = models.UserInfo.objects.get(user=user)
        print(userinfo.college)

        try:
            con_name = obj2
            uname = key
            a = LeaderBoard.objects.get(con_name=obj2, uname=key)
            a.final_points = point_dict[uname]
            a.cumulative_score = cumulative_score_dict[uname]
            a.number_of_submissions = d[uname]
            a.successful_submissions = point_dict[uname] // 100
            a.college_name = userinfo.college
            a.save()

        except:
            if len(point_dict)==0:
                break;
            con_name = obj2
            uname = key
            final_points = point_dict[uname]
            cumulative_score = cumulative_score_dict[uname]
            number_of_submissions = d[uname]
            successful_submissions = point_dict[uname] // 100
            college_name = userinfo.college
            leaderboard = LeaderBoard(con_name=con_name, uname=uname, final_points=final_points,
                                      cumulative_score=cumulative_score, number_of_submissions=number_of_submissions,
                                      successful_submissions=successful_submissions, college_name=college_name)
            leaderboard.save()

    board = models.LeaderBoard.objects.all().filter(con_name=obj2).order_by('-cumulative_score')
    print(board)

    context = {
        'board': board,
    }

    return render(request, "users_contest_display/leaderboard.html", context)