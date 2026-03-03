"""
Web authentication URLs (session-based).
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from apps.accounts.views.web_views import signup_view
from apps.accounts.views.auth_views import (
    user_login_view,
    admin_login_view,
    custom_logout_view,
    choose_user_type_view,
    set_user_type_view
)

urlpatterns = [
    path('login/', user_login_view, name='login'),
    path('admin/login/', admin_login_view, name='admin_login'),
    path('logout/', custom_logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('choose-type/', choose_user_type_view, name='choose_user_type'),
    path('set-type/', set_user_type_view, name='set_user_type'),
]