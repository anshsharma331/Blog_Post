"""blog_application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from app import views
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.welcome, name='welcome'),
    path('blogs/', views.blogs, name='blogs'),
    path('login', views.login, name='login' ),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('view_blogs', views.view_blogs, name='view_blogs'),
    path('home', views.home, name= 'home'),
    path('create_blog', views.create_blog, name='create_blog'),
    path('edit_blog/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('blog/<int:blog_id>/', views.view_blog, name='view_blog'),
    path('blogs/<int:blog_id>/', views.view_blogs, name='view_blogs'),
    path('like/<int:blog_id>/', views.like_blog, name='like_blog'),
    path('dislike/<int:blog_id>/', views.dislike_blog, name='dislike_blog'),
    path('blogs/tag', views.view_blogs_by_tag, name='view_blogs_by_tag'),
]
