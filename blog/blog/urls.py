"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path
from articles import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.archive, name='archive'),
    path('article/<int:article_id>', views.get_article, name='get_article'),
    path('article/new/', views.create_post, name='create_post'),
    path('register/', views.create_user, name='register'),
    path('login/', views.input_user, name='login'),
    path('logout/', LogoutView.as_view(next_page='http://127.0.0.1:8000/'), name='logout'),
]

