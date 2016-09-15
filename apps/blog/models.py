from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import bcrypt, re

PASS_REGEX = re.compile(r'\d.*[A-Z]|[A-Z].*\d')

class UserManager(models.Manager):
    def validateReg(self, request):
        errors = []
        if len(request.POST['username']) < 1:
            errors.append('Username can not be empty')

        try:
            user = User.objects.get(username = request.POST['username'])
            errors.append('This username is already being used')
        except ObjectDoesNotExist:
            pass

        if len(errors) > 0:
            return (False, errors)
        return (True, errors)

    def validateRegPass(self, request):
        errors = []
        if len(request.POST['password']) < 1:
            errors.append('Password can not be empty')
        elif len(request.POST['password']) < 8:
            errors.append('Password should be more than 7 characters')
        elif not PASS_REGEX.match(request.POST['password']):
            errors.append('Password should contain at least one apper case letter and one number')
        if request.POST['password'] != request.POST['repeat']:
            errors.append('Password repeat did not match the password')

        if len(errors) > 0:
            return (False, errors)
        return (True, errors)

    def validateLogin(self, request):
        from bcrypt import hashpw, gensalt
        errors = []
        try:
	        user = self.get(username=request.POST['username'])
	        password = user.pw_hash.encode()
	        loginpass = request.POST['password'].encode()
	        print password
	        print hashpw(loginpass, password)
	        if hashpw(loginpass, password) == password:
	            return (True, user)
	        else:
	            errors.append("Sorry, no password match. Please try again.")
	            return (False, errors)
        except ObjectDoesNotExist:
            pass
        errors.append("Sorry, no email found. Please try again.")
        return (False, errors)


class User(models.Model):
      username = models.CharField(max_length=45)
      image = models.ImageField(upload_to='blog/images/user/', default='blog/images/post/anonym.png')
      about = models.TextField(default = "")
      pw_hash = models.CharField(max_length=255)
      created_at = models.DateTimeField(auto_now_add = True)
      updated_at = models.DateTimeField(auto_now = True)

      objects = models.Manager()
      manager = UserManager()

class Tag(models.Model):
      name = models.CharField(max_length=45)
      use = models.PositiveIntegerField(default = 0)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)

class Post(models.Model):
      title = models.CharField(max_length=100)
      post = models.TextField()
      image = models.ImageField(upload_to='blog/images/post/', default='blog/images/post/no.png')
      user_id = models.ForeignKey(User)
      tags = models.ManyToManyField(Tag, related_name='post_tag')
      like = models.PositiveIntegerField(default = 0)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
      comment = models.TextField(max_length=1000)
      user_id = models.ForeignKey(User)
      post_id = models.ForeignKey(Post)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
