from django.urls import path
from .views import index, blog_detail

app_name = 'home'

urlpatterns = [
    path('', index, name='index'),
    path('blog/<slug:slug>', blog_detail, name='blog_detail'),
]