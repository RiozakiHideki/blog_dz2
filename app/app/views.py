from lib2to3.fixes.fix_input import context

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm, RegisterForm
from .models import Post
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
import requests


def create_post(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                form.save()
                return redirect('post_list')
        else:
            form = PostForm()
    else:
        form = PostForm()

    return render(request, 'app/create_post.html', {'form': form})

def post_list(request):
    posts = Post.objects.all()  # Получаем все посты

    rub_cur = requests.get('https://api.nbrb.by/exrates/rates/456').json()['Cur_OfficialRate']
    usd_cur = requests.get('https://api.nbrb.by/exrates/rates/431').json()['Cur_OfficialRate']
    eur_cur = requests.get('https://api.nbrb.by/exrates/rates/451').json()['Cur_OfficialRate']
    pln_cur = requests.get('https://api.nbrb.by/exrates/rates/452').json()['Cur_OfficialRate']

    return render(request, 'app/post_list.html',{'posts': posts,
                   'rub_cur': rub_cur, 'usd_cur': usd_cur, 'eur_cur': eur_cur, 'pln_cur': pln_cur})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm()  # Пустая форма для отображения при GET-запросе

    if request.method == 'POST':  # Проверяем, если это POST-запрос
        if request.user.is_authenticated:
            form = CommentForm(request.POST)  # Создаем форму с данными из POST
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post  # Привязываем комментарий к текущему посту
                comment.author = request.user
                comment.save()
                return redirect('post_detail', post_id=post.id)  # Перезагружаем страницу
        else:
            form.add_error(None, "Чтобы оставить комментарий, вам нужно войти в систему.")
    # Передаем пост и форму в шаблон
    return render(request, 'app/post_detail.html', {'post': post, 'form': form})


@login_required(login_url='login')
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('post_list')

@login_required(login_url='login')
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        # Создаем форму с данными POST и привязываем её к посту
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        # Если GET-запрос, передаем данные поста в форму
        form = PostForm(instance=post)


    return render(request, 'app/post_edit.html', {'form': form, 'post': post})


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm

    return render(request, 'app/registration.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('post_list')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = AuthenticationForm()

    return render(request, 'app/login.html', {'form': form})


