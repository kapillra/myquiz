from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from random import randint
from django.db import IntegrityError

# Create your views here.

default_data = {}

login_page_link = 'quiz_manage/login_page.html'
register_page_link = 'quiz_manage/register_page.html'
profile_page_link = 'quiz_manage/profile_page.html'
otp_page_link = 'quiz_manage/otp_page.html'
forgot_pwd_page_link = 'quiz_manage/forgot_pwd_page.html'

# email function
def send_otp(request):
    otp = randint(1000, 9999)
    request.session['otp'] = otp

    send_to = [request.session['reg_data']['email']]
    send_from = settings.EMAIL_HOST_USER
    subject = 'Login Attempt'
    message = f'Hello! We noticed someone entered your account. OTP is: {otp}'
    
    print(otp)
    print('done')

    send_mail(subject, message, send_from, send_to)

## Email Verification
def verify_otp(request):
    if int(request.POST['otp']) == request.session['otp']:
        master = Master.objects.create(Email=request.session['reg_data']['email'], Password=request.session['reg_data']['pwd'])
        UserProfile.objects.create(Master=master)
        print('account created successfully.')
        return redirect(index)
    else:
        print('invalid otp.')
    
    return redirect(otp_page_link)

#### START: VIEWS FOR PAGES ONLY ####

def index(request): # refer it as login_page
    if 'email' in request.session:
        load_profile(request)
        return render(request, profile_page_link, default_data)
    return render(request, login_page_link)

# register_page
def register_page(request):
    return render(request, register_page_link)

# forgot_pwd_page
def forgot_pwd_page(request):
    return render(request, forgot_pwd_page_link)

# otp_page
def otp_page(request):
    return render(request, otp_page_link)

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
    try:
        master = Master.objects.get(Email=request.POST['email'])
        print("Account exist. Please login.")
    except Master.DoesNotExist as err:
        print(err)
        print('account not found')

        request.session['reg_data'] = {'email': request.POST['email'], 'pwd': request.POST['password']}
        send_otp(request)
        return redirect(otp_page)
    

    return redirect(index)

# END: REGISTRATION FUNCTIONALITY

# START: LOGIN FUNCTIONALITY

def login(request):
    try:
        master = Master.objects.get(Email = request.POST['email'])
        if master.Password == request.POST['password']:
            request.session['email'] = master.Email

            # send_otp(request)

            return redirect(profile_page)
        else:
            print('incorrect password')
    
    except Master.DoesNotExist as err:
        print('account does not exist.')

    return redirect(index)

# END: LOGIN FUNCTIONALITY

for gc in gender_choices:
    {
        'm': 'male',
        'f': 'female'
    }
    print(gc)

# START: GET PROFILE DATA
def load_profile(request):
    master = Master.objects.get(Email = request.session['email'])

    user = UserProfile.objects.get(Master=master)

    user.BirthDate = user.BirthDate.strftime('%Y-%m-%d')


    default_data['user_profile'] = user
    
    default_data['gender_choices'] = dict()
    
    for gc in gender_choices:
        default_data['gender_choices'].setdefault(gc[0], gc[1])
    

    default_data['quiz_preset_data'] = {
        'categories': QuizCategory.objects.all(),
        'subjects': Subject.objects.all(),
    }
    
    myquizes = Quiz.objects.filter(UserProfile=user)
    
    for myquiz in myquizes:
        myquiz.TotalQuestions = len(QuesAns.objects.filter(Quiz=myquiz))

    default_data['my_quizes'] = myquizes

# END: GET PROFILE DATA

import os
# profile image update
def upload_profile_image(request):
    master = Master.objects.get(Email=request.session['email'])
    user = UserProfile.objects.get(Master = master)

    image_name = request.FILES['profile_image'].name
    img_ext = image_name.split('.')[-1]

    image_new_name = f"{master.Email.split('@')[0]}_{user.Mobile}.{img_ext}"
    print(image_new_name)

    image = request.FILES['profile_image']
    image.name = image_new_name

    image_path = os.path.join(settings.MEDIA_ROOT, 'profile_images')
    
    for file in os.scandir(image_path):
        if file.name == image.name:
            del_file = os.path.join(image_path, file.name)
            os.remove(del_file)
        
        print(file.name)

    user.ProfileImage = image
    user.save()

    # print(request.FILES['profile_image'])

    return redirect(profile_page)

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


# CHANGE PASSWORD
def change_password(request):
    master = Master.objects.get(Email=request.session['email'])
    if master.Password == request.POST['current_pwd']:
        if request.POST['new_pwd'] == request.POST['re_new_pwd']:
            master.Password = request.POST['new_pwd']
            master.save()
            print('password has been changed.')
        else:
            print('new password and repeat password must be same.')
    else:
        print('current password not matched.')
    
    return redirect(profile_page)

# CREATE NEW QUIZ
def create_quiz(request):
    master = Master.objects.get(Email=request.session['email'])
    user = UserProfile.objects.get(Master=master)
    
    subject = Subject.objects.get(pk=int(request.POST['subject']))
    category = QuizCategory.objects.get(pk=int(request.POST['category']))

    Quiz.objects.create(
        UserProfile = user,
        Category = category,
        Subject = subject,
        Title = request.POST['quiz_title'],
        Duration = request.POST['duration'],
        DifficultyLevel = request.POST['difficulty_level'],
        TotalScore = request.POST['total_score'],
    )

    return redirect(profile_page)

# ADD OPTIONS TO QUIZES
def add_options(request, id):
    master = Master.objects.get(Email=request.session['email'])
    user = UserProfile.objects.get(Master=master)

    quiz = Quiz.objects.get(
        id = id,
        UserProfile = user
    )

    options = []
    for d in request.POST:
        if d.startswith('option'):
            options.append(request.POST[d])
    options = '|'.join(options)

    QuesAns.objects.create(
        Quiz = quiz,
        Question = request.POST['question'],
        Options = options,
        Answer = request.POST['set_answer'],
    )

    return redirect(profile_page)

# FETCH QUESTIONS
def fetch_questions(request, id):
    quiz = Quiz.objects.get(id=id)
    questions = QuesAns.objects.filter(Quiz=quiz)

    dic = {'ques_ans': []}
    for ques in questions:
        dic['ques_ans'].append({'question': ques.Question, 'options': ques.Options, 'answer': ques.Answer})

    return JsonResponse(dic)

# LOGOUT
def logout(request):
    if 'email' in request.session:
        del request.session['email']
    return redirect(index)