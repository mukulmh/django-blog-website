from django.contrib import admin

# Register your models here.
from .models import Comment, Featured, Like, Post,Category

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Featured)
admin.site.register(Like)
admin.site.register(Comment)
