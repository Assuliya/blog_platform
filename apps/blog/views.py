from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count
from models import User, Post, Comment, Like
# from forms import UserForm
import bcrypt


def index(request):
    return render(request, 'blog/index.html')

def login(request):
    context = random_users(request)
    return render(request, 'blog/login.html', context)

def post(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post_id=post_id)
    user_like = Like.objects.filter(post_id=post_id)
    likes = Like.objects.filter(post_id=post_id).values('post_id').annotate(count=Count('post_id'))
    before = False
    for x in user_like:
        if x.user_id.id == request.session['user']:
            before = True
    context = {'post':post, 'comments':comments, 'likes':likes, 'before':before}
    return render(request, 'blog/post.html', context)

def user(request, user_id):
    user = User.manager.get(id=user_id)
    posts = Post.objects.filter(user_id=user_id).order_by('-created_at')
    comments = Comment.objects.all()
    count = Like.objects.all().values('post_id').annotate(count=Count('post_id'))
    likes = Like.objects.all().values('post_id').annotate(count=Count('post_id'))
    print likes
    context = {'user':user, 'posts':posts, 'comments': comments, 'count': count, 'likes': likes}
    return render(request, 'blog/user.html', context)

def edit(request):
    user = User.objects.get(id = request.session['user'])
    random = random_users(request)
    context = {'user':user}
    context.update(random)
    return render(request, 'blog/edit.html', context)

def main(request):
    extra = User.objects.all()
    latest = Post.objects.all().order_by('-created_at')[:4]
    posts = Post.objects.all()
    count = Like.objects.all().values('post_id').annotate(count=Count('post_id')).order_by('-count')[:4]
    liked = []
    for x in posts:
        for y in count:
            if x.id == y['post_id']:
                liked.append([x,y['count']])
    random = random_users(request)
    context = {'latest':latest, 'liked':liked, 'count':count}
    context.update(random)
    return render(request, 'blog/main.html', context)

def deletion_page(request):
    return render(request, 'blog/delete.html')

def random_users(request):
    import random
    order = ['-created_at', 'created_at', '-username', 'username']
    rnd_order = (random.choice(order))
    raw_users = User.objects.all().order_by(rnd_order)
    x = (random.choice(raw_users)).id
    if x > len(raw_users) - 3:
        x -= 3
    users = raw_users[x:x+3]

    num_like = Like.objects.all().values('post_id__user_id').annotate(count=Count('post_id__user_id'))
    num_post = Post.objects.all().values('user_id').annotate(count=Count('user_id')).order_by('-count')
    context = {'users':users, 'num_like':num_like, 'num_post':num_post}
    return context

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
    return redirect(reverse('user', kwargs={'user_id':request.session['user']}))

def update(request):
    user = User.manager.get(id=request.session['user'])
    if user.username != request.POST['username']:
        result = User.manager.validateReg(request)
        if result[0] == False:
            print_messages(request, result[1])
            return redirect(reverse('edit', kwargs={'user_id':request.session['user']}))

    update = User.objects.get(id = request.session['user'])
    update.username = request.POST['username']
    if 'image' in request.FILES:
        request.FILES['image'].name = request.POST['username']
        update.image = request.FILES['image']
    update.save()
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
    return redirect(reverse('main', kwargs={'user_id':request.session['user']}))

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
        if 'image' in request.FILES:
            request.FILES['image'].name = user.username + "_" + request.POST['title'][:8]
            Post.objects.create(image = request.FILES['image'], title = request.POST['title'], post = request.POST['post'], user_id = user)
        else:
            Post.objects.create(title = request.POST['title'], post = request.POST['post'], user_id = user)
        return redirect(reverse('user', kwargs={'user_id':request.session['user']}))
    else:
	    return redirect(reverse('user'))

def add_comment(request, post_id):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user'])
        post = Post.objects.get(id=post_id)
        Comment.objects.create(comment = request.POST['comment'], user_id = user, post_id = post)
        return redirect(reverse('post', kwargs={'post_id':post_id}))
    else:
	    return redirect(reverse('user'))

def add_like(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        user = User.objects.get(id=request.session['user'])
        Like.objects.create(user_id = user, post_id = post)
        return redirect(reverse('post', kwargs={'post_id':post_id}))
    else:
	    return redirect(reverse('post'))
