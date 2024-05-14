from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as django_logout
from django.contrib.auth.decorators import login_required  

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect

from app.forms import BlogForm, CommentForm
from app.models import Blog


def welcome(request):
    """Render the welcome page."""
    return render(request, 'welcome.html')

def login(request):
    """Log in a user."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('/home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    """Log out a user."""
    django_logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('welcome') 

def signup(request):
    """Render the signup page."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully. Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'There was an error creating your account. Please try again.')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def home(request):
    """Render the home page."""
    blog_posts = Blog.objects.all().order_by('-created_at')
    paginator = Paginator(blog_posts, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'page_obj': page_obj})

@login_required
def create_blog(request):
    """Create a new blog post."""
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'Blog post created successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Error creating blog post. Please correct the errors below.')
    else:
        form = BlogForm()
    return render(request, 'create_blog.html', {'form': form})

def blogs(request):
    """Render all blog posts wihtout log in"""
    all_posts = Blog.objects.all()
    paginator = Paginator(all_posts, 5) 
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'blogs.html', {'page_obj': page_obj})

def view_blogs(request, blog_id): 
    """Render a single blog post."""
    blog_post = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'view_blogs.html', {'blog_post': blog_post})

@login_required
def view_blog(request, blog_id): 
    """Render a single blog post."""
    blog_post = get_object_or_404(Blog, pk=blog_id)
    comments = blog_post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.blog = blog_post
            new_comment.user = request.user
            new_comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()
    return render(request, 'view_blog.html', {'blog_post': blog_post, 'comments': comments, 'form': form})

@login_required
def like_blog(request, blog_id):
    """Like a blog post."""
    if request.user.is_authenticated:
        blog = Blog.objects.get(pk=blog_id)
        if request.user not in blog.likes.all():
            blog.likes.add(request.user)
            messages.success(request, 'You liked the blog post.')
        else:
            messages.warning(request, 'You have already liked this blog post.')
        return redirect('home')  
    else:
        messages.error(request, 'Please log in to like the blog post.')
        return redirect('login') 

@login_required
def dislike_blog(request, blog_id):
    """Dislike a blog post."""
    if request.user.is_authenticated:
        blog = Blog.objects.get(pk=blog_id)
        if request.user not in blog.dislikes.all():
            blog.dislikes.add(request.user)
            messages.success(request, 'You disliked the blog post.')
        else:
            messages.warning(request, 'You have already disliked this blog post.')
        return redirect('home') 
    else:
        messages.error(request, 'Please log in to dislike the blog post.')
        return redirect('login') 
    
@login_required
def edit_blog(request, blog_id):
    """Edit a blog post."""
    blog_post = get_object_or_404(Blog, pk=blog_id)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog_post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully.')
            return redirect('view_blog', blog_id=blog_id)
        else:
            messages.error(request, 'Error updating blog post. Please correct the errors below.')
    else:
        form = BlogForm(instance=blog_post)  
    return render(request, 'edit_blog.html', {'form': form, 'blog_post': blog_post})

def view_blogs_by_tag(request):
    # Get the tag(s) from the URL parameters
    tags = request.GET.get('tag', '').split(',')
    print(tags)
    # Filter blogs based on the tag(s)
    if tags:
        blogs = Blog.objects.filter(tags__name__in=tags).distinct()
        print(blogs.query)
    else:
        blogs = Blog.objects.all()
        print(blogs.query)
    return render(request, 'blogs_by_tag.html', {'blogs': blogs})
#http://127.0.0.1:8000/blogs/tag?tag=%27funny%27
