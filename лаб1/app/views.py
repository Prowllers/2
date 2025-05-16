"""Definition of views."""

from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, Http404
from django.contrib.auth import login
from .forms import AnketaForm, CustomRegisterForm, CommentForm, BlogForm
from .models import Blog, Comment

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Главная',
            'year': datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Контакты',
            'message': 'Страница с нашими контактами',
            'year': datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'О нас',
            'message': 'Сведения о нас',
            'year': datetime.now().year,
        }
    )

def blog(request):
    """Renders the blog page with list of posts."""
    posts = Blog.objects.all().order_by('-posted')
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Блог',
            'posts': posts,
            'year': datetime.now().year,
        }
    )

def blogpost(request, pk):
    """Renders a single blog post page with comments."""
    post = get_object_or_404(Blog, id=pk)
    comments = Comment.objects.filter(post=post).order_by('date')
    
    if request.method == "POST" and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blogpost', pk=post.id)
    else:
        form = CommentForm()
    
    return render(
        request,
        'app/blogpost.html',
        {
            'post': post,
            'comments': comments,
            'form': form,
            'year': datetime.now().year,
        }
    )

def register(request):
    """Handles user registration."""
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomRegisterForm()
    
    return render(
        request,
        'app/registration.html',
        {
            'form': form,
            'title': 'Регистрация',
            'year': datetime.now().year,
        }
    )

def anketa(request):
    """Handles survey form submission."""
    data = None
    gender = {'1': 'Мужчина', '2': 'Женщина'}
    internet = {
        '1': 'Каждый день',
        '2': 'Несколько раз в день',
        '3': 'Несколько раз в неделю',
        '4': 'Несколько раз в месяц'
    }

    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            data = {
                'name': cleaned['name'],
                'city': cleaned['city'],
                'job': cleaned['job'],
                'gender': gender.get(cleaned['gender'], ''),
                'internet': internet.get(cleaned['internet'], ''),
                'notice': 'Да' if cleaned.get('notice') else 'Нет',
                'email': cleaned['email'],
                'message': cleaned['message'],
            }
            form = None
    else:
        form = AnketaForm()

    return render(
        request,
        'app/anketa.html',
        {
            'form': form,
            'data': data,
            'year': datetime.now().year,
        }
    )

def newpost(request):
    """Handles creation of new blog posts."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_post = blogform.save(commit=False)
            blog_post.posted = datetime.now()
            blog_post.author = request.user
            blog_post.save()
            return redirect('blog')
    else:
        blogform = BlogForm()
    
    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Новая статья',
            'year': datetime.now().year,
        }
    )

def links(request):
    """Renders the useful resources page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title': 'Полезные ресурсы',
            'message': 'Список полезных ссылок',
            'year': datetime.now().year,
        }
    )

def videopost(request):
    """Renders the video page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title': 'Видео',
            'message': 'Видеоматериалы',
            'year': datetime.now().year,
        }
    )