from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, HttpResponseRedirect

from app import forms, models


class UserAlreadyExist(Exception):
    pass


class CouldNotAuthenticate(Exception):
    pass


class UserNotActive(Exception):
    pass


def user_registration(request):
    if request.method == 'POST':
        form = forms.RegisterUser(request.POST)
        if form.is_valid():
            username = form.data.get('username')
            password = form.data.get('password')
            email = form.data.get('email')
            is_superuser = (True if form.data.get('is_superuser') == 'on'
                            else False)
            try:
                user = User.objects.create(username=username, email=email,
                                           is_superuser=is_superuser)
                user.set_password(password)
                user.save()
                login(request, user)
            except IntegrityError:
                raise UserAlreadyExist('User Already Exists')
            return HttpResponseRedirect('/app/home/')
    else:
        form = forms.RegisterUser()

    return render(request, 'app/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.data.get('username')
            password = form.data.get('password')
            user = authenticate(username=username, password=password)
            if not user:
                raise CouldNotAuthenticate('Given Credentials are wrong')
            if not user.is_active:
                raise UserNotActive('User is not active')
            login(request, user)
            return HttpResponseRedirect('/app/home/')
    else:
        form = forms.LoginForm()
    return render(request, 'app/login.html/', {'form': form})


@login_required
def user_logout(request):
    if request.user:
        logout(request)
        return HttpResponseRedirect('/app/login/')
    else:
        return HttpResponse('Already Logged out')


@login_required
def home(request):
    queryset = models.Post.objects.all()
    for post in queryset:
        post.is_liked = get_like_or_unlike(request.user, post)
        post.total_likes = get_total_like(post)
    return render(request, 'app/home.html', {'post_list': queryset})


@login_required
def create(request):
    if request.method == 'POST':
        form = forms.CreatePost(request.POST)
        if form.is_valid():
            title = form.data.get('title')
            description = form.data.get('description')
            models.Post.objects.create(
                title=title, description=description, author=request.user)
            return HttpResponseRedirect('/app/home/')
    else:
        form = forms.CreatePost()
    return render(request, 'app/create_post.html/', {'form': form})


@login_required
def delete(request, pk):
    post = models.Post.objects.get(pk=pk)
    if request.user == post.author or request.user.is_superuser:
        post.delete()
        return HttpResponseRedirect('/app/home/')
    else:
        return HttpResponse('Not Authorized')


@login_required
def like_post(request, pk):
    post = models.Post.objects.get(pk=pk)
    models.Like.objects.get_or_create(post=post, user=request.user)
    return HttpResponseRedirect('/app/home/')


@login_required
def unlike_post(request, pk):
    post = models.Post.objects.get(pk=pk)
    models.Like.objects.get(post=post, user=request.user).delete()
    return HttpResponseRedirect('/app/home/')


def get_like_or_unlike(user, post):
    try:
        like = models.Like.objects.get(post=post, user=user)
        if like:
            return True
    except models.Like.DoesNotExist:
        return False


def get_total_like(post):
    return post.like.count()
