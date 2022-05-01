"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from home.views import works_list, check_name, check_email, check_subject

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls'))
]


htmx_urlpatterns = [
    path('works_list/<str:category>', works_list, name='works-list'),
    path('check-name', check_name, name="check-name"),
    path('check-email', check_email, name="check-email"),
    path('check-subject', check_subject, name="check-subject"),
]

urlpatterns += htmx_urlpatterns