from django.contrib import admin

# Register your models here.
from blogs.models import Blogs


@admin.register(Blogs)
class BlogsAdmin(admin.ModelAdmin):
    list_display = (
    'blog_name', 'blogger_fullname', 'blogger_username', 'content', 'date')