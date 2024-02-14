from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='login_page'),
    path('login/', login, name='login'),
    path('register_page/', register_page, name='register_page'),
    path('registration/', registration, name='registration'),
    path('otp_page/', otp_page, name='otp_page'),
    path('verify_otp/', verify_otp, name='verify_otp'),

    path('forgot_pwd_page/', forgot_pwd_page, name='forgot_pwd_page'),
    path('profile_page/', profile_page, name='profile_page'),
    path('profile_update/', profile_update, name='profile_update'),
    path('upload_profile_image/', upload_profile_image, name='upload_profile_image'),
    path('change_password/', change_password, name='change_password'),
    
    
    path('create_quiz/', create_quiz, name='create_quiz'),
    path('add_options/<int:id>/', add_options, name='add_options'),
    
    path('fetch_questions/<int:id>/', fetch_questions, name='fetch_questions'),
    
    
    path('logout/', logout, name='logout'),
]