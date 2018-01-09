from django.contrib import admin
from app import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'author', 'pub_date']


@admin.register(models.Like)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']
