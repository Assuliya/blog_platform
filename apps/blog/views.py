from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from models import User, Post, Comment,Tag
import bcrypt

def index(request):
    return render(request, 'blog/index.html')

def login(request):
    return render(request, 'blog/login.html')

def register(request):
    return render(request, 'blog/register.html')

def show(request, user_id):
    if not 'user' in request.session:
        return redirect(reverse('index'))
    user = User.manager.get(id=user_id)
    posts = Post.objects.filter(user_id=user_id)
    comments = Comment.objects.all()
    context = {'user':user, 'posts':posts, 'comments': comments}
    return render(request, 'blog/show.html', context)

def edit(request, user_id):
    user = User.objects.get(id = user_id)
    context = {'user':user}
    return render(request, 'blog/edit.html', context)

def dashboard(request):
    users = User.objects.all()
    context = {'users':users}
    return render(request, 'blog/dashboard.html', context)

def deletion_page(request):
    return render(request, 'blog/delete.html')

def register_process(request):
    result = User.manager.validateReg(request)
    resultPass = User.manager.validateRegPass(request)
    if result[0] == False or resultPass[0] == False:
        errors = result[1]+resultPass[1]
        print_messages(request, errors)
        return redirect(reverse('register'))
    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.manager.create(username=request.POST['username'], pw_hash=pw_hash)
    return log_user_in(request, user)

def login_process(request):
    result = User.manager.validateLogin(request)
    if result[0] == False:
        print_messages(request, result[1])
        return redirect(reverse('login'))
    return log_user_in(request, result[1])

def print_messages(request, message_list):
    for message in message_list:
        messages.add_message(request, messages.ERROR, message)

def log_user_in(request, user):
    request.session['user'] = user.id
    return redirect(reverse('show', kwargs={'user_id':request.session['user']}))

def update(request):
    user = User.manager.get(id=request.session['user'])
    if user.username != request.POST['username']:
        result = User.manager.validateReg(request)
        if result[0] == False:
            print_messages(request, result[1])
            return redirect(reverse('edit', kwargs={'user_id':request.session['user']}))
    update = User.objects.get(id = request.session['user'])
    update.username = request.POST['username']
    update.image = request.POST['image']
    update.save(update_fields=None)
    return redirect(reverse('show', kwargs={'user_id':request.session['user']}))

def update_pass(request):
    result = User.manager.validateRegPass(request)
    result2 = User.manager.validateLogin(request)
    if result[0] == False or result2[0] == False:
        if result2[0] != False:
            print_messages(request, result[1])
        else:
            print_messages(request, result2[1])
        return redirect(reverse('edit', kwargs={'user_id':request.session['user']}))
    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    update = User.objects.get(id = request.session['user'])
    update.pw_hash = pw_hash
    update.save(update_fields=None)
    return redirect(reverse('dashboard_show', kwargs={'user_id':request.session['user']}))

def logout(request):
    user = User.manager.get(id=request.session['user'])
    user.user_level = 0
    user.save(update_fields=None)
    request.session.pop('user')
    return redirect(reverse('index'))

def delete(request):
    User.objects.filter(id = request.session['user']).delete()
    request.session.pop('user')
    return redirect(reverse('index'))

def add_post(request):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user'])
        Post.objects.create(title = request.POST['title'], message = request.POST['message'], user_id = user)
        return redirect(reverse('show', kwargs={'user_id':request.session['user']}))
    else:
	    return redirect(reverse('show'))

def add_comment(request, post_id):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user'])
        message = Message.objects.get(id=message_id)
        page = message.user_id_to.id
        Comment.objects.create(comment = request.POST['comment'], user_id = user, message_id = message)
        return redirect(reverse('show', kwargs={'user_id':page}))
    else:
	    return redirect(reverse('show'))
