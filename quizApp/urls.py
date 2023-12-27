from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='login_page'),
    path('login/', login, name='login'),
    path('register_page/', register_page, name='register_page'),
    path('registration/', registration, name='registration'),

    path('forgot_pwd_page/', forgot_pwd_page, name='forgot_pwd_page'),
    path('profile_page/', profile_page, name='profile_page'),
    path('profile_update/', profile_update, name='profile_update'),
    
    path('logout/', logout, name='logout'),
]