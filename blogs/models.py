from django.db import models


# Create your models here.
class Blogs(models.Model):
    blog_name = models.CharField(max_length=500)
    blogger_fullname = models.CharField(max_length=500)
    blogger_username = models.CharField(max_length=500)
    content = models.TextField(max_length=50000)
    date = models.DateTimeField(auto_now=True)
    profile_pic = models.ImageField(null=True, blank=True)
    emailid = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    college = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
