from django.conf.urls import url, include
from django.contrib import admin


from models import User, Like, Post, Comment

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)

class LikeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Like, LikeAdmin)

class PostAdmin(admin.ModelAdmin):
    pass
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Comment, CommentAdmin)
