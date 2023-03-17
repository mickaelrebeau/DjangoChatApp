"""DjangoChatApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView,PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from user.views import HomePageView, SignupView
from .settings import LOGOUT_REDIRECT_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(HomePageView.as_view()), name='home'),
    path("chat/", include('user.urls', namespace="chat")),
    path('login/', LoginView.as_view(), {'registration': 'login.html'}, name ='login'),
    path('logout/', LogoutView.as_view(), {'next_page': LOGOUT_REDIRECT_URL}, name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path("__reload__/", include("django_browser_reload.urls")),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
