from django.shortcuts import render, redirect
from .models import *

# Create your views here.

default_data = {}

login_page_link = 'quiz_manage/login_page.html'
register_page_link = 'quiz_manage/register_page.html'
profile_page_link = 'quiz_manage/profile_page.html'
otp_page_link = 'quiz_manage/otp_page.html'
forgot_pwd_page_link = 'quiz_manage/forgot_pwd_page.html'

#### START: VIEWS FOR PAGES ONLY ####

def index(request): # refer it as login_page
    return render(request, login_page_link)

# register_page
def register_page(request):
    return render(request, register_page_link)

# forgot_pwd_page
def forgot_pwd_page(request):
    return render(request, forgot_pwd_page_link)

# profile_page
def profile_page(request):
    # calling load_profile
    if 'email' in request.session:
        load_profile(request)
        return render(request, profile_page_link, default_data)
    
    return redirect(index)

#### END: VIEWS FOR PAGES ONLY ####

#### FUNCTIONALITY VIEWS ONLY ####

# START: REGISTRATION FUNCTIONALITY

def registration(request):
    master = Master.objects.create(Email=request.POST['email'], Password=request.POST['password'])
    UserProfile.objects.create(Master=master)

    return redirect(index)

# END: REGISTRATION FUNCTIONALITY

# START: LOGIN FUNCTIONALITY

def login(request):
    try:
        master = Master.objects.get(Email = request.POST['email'])
        if master.Password == request.POST['password']:
            request.session['email'] = master.Email

            return redirect(profile_page)
        else:
            print('incorrect password')
    
    except Master.DoesNotExist as err:
        print('account does not exist.')

    return redirect(index)

# END: LOGIN FUNCTIONALITY


# START: GET PROFILE DATA
def load_profile(request):
    master = Master.objects.get(Email = request.session['email'])

    user = UserProfile.objects.get(Master=master)

    user.BirthDate = user.BirthDate.strftime('%Y-%m-%d')


    default_data['user_profile'] = user

# END: GET PROFILE DATA



# profile_update_functionality
def profile_update(request):
    print(request.POST)
    
    master = Master.objects.get(Email=request.session['email'])

    print('master', master, master.Email)

    user = UserProfile.objects.get(Master = master)
    user.FullName=request.POST['full_name']
    user.Mobile=request.POST['mobile']
    user.Gender = request.POST['gender']
    user.BirthDate = request.POST['birth_date']
    user.City = request.POST['city']
    user.State = request.POST['state']
    user.Country = request.POST['country']
    user.Pincode = request.POST['pincode']
    
    user.save()

    
    return redirect(profile_page)

# LOGOUT
def logout(request):
    if 'email' in request.session:
        del request.session['email']
    return redirect(index)