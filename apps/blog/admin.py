 # From inside your project's urls.py file
from django.conf.urls import url, include
from django.contrib import admin

  # THIS SECTION IS NEW!
  # ********************
from models import User, Tag, Post, Comment

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)

class TagAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tag, TagAdmin)

class PostAdmin(admin.ModelAdmin):
    pass
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Comment, CommentAdmin)
