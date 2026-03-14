#views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post
from .forms import UserRegisterForm, PostForm

def home(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'title': 'Главная'
    }
    return render(request, 'blog/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form, 'title': 'Регистрация'})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    
    return render(request, 'blog/login.html', {'title': 'Вход'})

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('home')

@login_required
def profile(request):
    # Показываем только посты текущего пользователя
    user_posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/profile.html', {
        'posts': user_posts,
        'title': 'Мой профиль'
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Пост успешно создан!')
            return redirect('home')
    else:
        form = PostForm()
    
    return render(request, 'blog/post_form.html', {
        'form': form,
        'title': 'Создать пост'
    })

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Проверяем, что автор - текущий пользователь
    if post.author != request.user:
        messages.error(request, 'Вы не можете редактировать чужие посты')
        return redirect('home')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пост успешно обновлен!')
            return redirect('home')
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_form.html', {
        'form': form,
        'title': 'Редактировать пост'
    })

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if post.author != request.user:
        messages.error(request, 'Вы не можете удалить чужой пост')
        return redirect('home')
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Пост успешно удален!')
        return redirect('home')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'title': post.title
    })