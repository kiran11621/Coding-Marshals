from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import datetime

from blogs import models
from blogs.models import Blogs
from users import models as umodels


@login_required(login_url="login")
def display_blogs(request):
    blogs = models.Blogs.objects.all().order_by('-date')
    return render(request, "blogs/display_blogs.html", {'blogs': blogs})


@login_required(login_url="login")
def create_blog(request):
    if request.method == 'POST':
        blog_name = request.POST.get('blog_name')
        blogger_fullname = request.POST.get('blogger_fullname')
        blogger_username = request.POST.get('blogger_username')
        content = request.POST.get('content')
        date = datetime.datetime.now()
        user = umodels.User.objects.get(username=blogger_username)
        userinfo = umodels.UserInfo.objects.get(user=user)
        print(userinfo)
        print(user)
        print(userinfo.profile_pic)
        print(blog_name)
        print(blogger_username)
        print(content)
        profile_pic = userinfo.profile_pic
        college = userinfo.college
        emailid = user.email
        print(emailid)
        city = userinfo.city
        country = userinfo.country
        print(country)
        print(city)

        blog = Blogs(blog_name=blog_name, blogger_fullname=blogger_fullname, blogger_username=blogger_username,
                     content=content, date=date, profile_pic=profile_pic, college=college, emailid=emailid, city=city, country=country)
        blog.save()
        return redirect('display_blogs')

    return render(request, "blogs/create_blog.html")
