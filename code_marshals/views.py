from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from users import models as umodels
from users import forms as uforms
from django.contrib.auth import authenticate, login, logout
from users.forms import UserForm, InfoForm
from users.models import QuestionMake, ContestInformation


# Create your views here.

# admin login
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('username')

            user = authenticate(request, username=username, password=password)

            # if username == 'admin' and password == 'admin':
            #     login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            #     return redirect('admin_home')
            if user is not None:
                login(request, user)
                return redirect('admin_home')

    

        context = {}
        return render(request, 'code_marshals/admin_login.html', context)

    


# admin logout
def logoutUser(request):
    logout(request)
    return redirect('admin_login')


# home page
@login_required(login_url='admin_login')
def admin_home(request):
    dict = {
        'total_user': umodels.UserInfo.objects.all().count(),
        'total_contest_organized': umodels.ContestInformation.objects.all().count(),
        'total_questions': umodels.ContestInformation.objects.all().count()
    }
    return render(request, 'code_marshals/admin_home.html', context=dict)


# navbar page
def admin_navbar(request):
    return render(request, 'code_marshals/admin_navbar.html')


# index page
def index(request):
    return render(request, 'index.html')


# user details view and change

@login_required(login_url='admin_login')
def admin_user_view(request,):
    users = umodels.UserInfo.objects.all()
    return render(request, 'code_marshals/user_details.html', {'users': users})


@login_required(login_url='admin_login')
def update_user_details(request, pk):
    users = umodels.UserInfo.objects.get(id=pk)
    user = umodels.User.objects.get(id=users.user_id)
    userForm = uforms.UserForm(instance=user)
    infoForm = uforms.InfoForm(request.FILES, instance=users)

    mydict = {
        'userForm': userForm,
        'infoForm': infoForm
    }

    if request.method == 'POST':
        userForm = uforms.UserForm(request.POST, instance=user)
        infoForm = uforms.InfoForm(request.POST, request.FILES, instance=users)

        if userForm.is_valid() and infoForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            users = infoForm.save(commit=False)
            users.user = user
            users.save()

            return redirect('admin_user_view')
    return render(request, 'code_marshals/update_user_details.html', context=mydict)


@login_required(login_url='admin_login')
def delete_user_details(request, pk):
    users = umodels.UserInfo.objects.get(id=pk)
    user = umodels.User.objects.get(id=users.user_id)
    print(users)
    print(user)
    user.delete()
    users.delete()

    return HttpResponseRedirect('admin_user_view')


# question view, add, delete and update question

@login_required(login_url='admin_login')
def admin_question_view(request):
    question = umodels.QuestionMake.objects.all()
    return render(request, 'code_marshals/question_details.html', {'question': question})


@login_required(login_url='admin_login')
def update_question_details(request, pk):
    if request.method == 'POST':
        obj = QuestionMake.objects.get(pk=pk)
        obj.problem_name = request.POST.get('problem')
        obj.authorname = request.POST.get('authorname')
        obj.problem_statement = request.POST.get('problem_statement')
        obj.input_format = request.POST.get('input_format')
        obj.constraints = request.POST.get('constraints')
        obj.output_format = request.POST.get('output_format')
        obj.tags = request.POST.get('tags')
        obj.sample_input = request.POST.get('sample_input')
        obj.sample_output = request.POST.get('sample_output')
        obj.hidden_input = request.FILES['hidden_input']
        obj.hidden_output = request.FILES['hidden_output']
        obj.difficulty = request.POST.get('difficulty')

        obj.save()

        return redirect('admin_question_view')
    return render(request, 'code_marshals/update_question_details.html')


@login_required(login_url='admin_login')
def delete_question(request, pk):
    question = umodels.QuestionMake.objects.get(id=pk)

    question.delete()
    return HttpResponseRedirect('code_marshals/admin_question_view')

@login_required(login_url='admin_login')
def admin_add_question(request):
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
                                tags=tags, sample_input=sample_input, sample_output=sample_output,
                                explanation=explanation,hidden_input=hidden_input, hidden_output=hidden_output, difficulty=difficulty)
        try:
            question.save()
        except:
            messages.error(request, 'Contest Name Already taken')

    return render(request, 'code_marshals/add_question.html')


@login_required(login_url='admin_login')
def admin_contest_view(request):
    contest = umodels.ContestInformation.objects.all()

    return render(request, 'code_marshals/contest_details.html', {'contest': contest})


@login_required(login_url='admin_login')
def delete_contest(request, pk):
    contest = umodels.ContestInformation.objects.get(id=pk)

    contest.delete()
    return redirect('admin_contest_view')