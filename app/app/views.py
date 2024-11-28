from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm
from .models import Post


def index(request):
    return HttpResponse("Hello world")


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()

    return render(request, 'app/create_post.html', {'form': form})

def post_list(request):
    posts = Post.objects.all()  # Получаем все посты
    return render(request, 'app/post_list.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm()  # Пустая форма для отображения при GET-запросе

    if request.method == 'POST':  # Проверяем, если это POST-запрос
        form = CommentForm(request.POST)  # Создаем форму с данными из POST
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  # Привязываем комментарий к текущему посту
            comment.save()
            return redirect('post_detail', post_id=post.id)  # Перезагружаем страницу

    # Передаем пост и форму в шаблон
    return render(request, 'app/post_detail.html', {'post': post, 'form': form})


def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('post_list')

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



