from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from auth_project import settings
from django.core.mail import send_mail
#from django.contrib.sites.shortcuts import get_current_site
#from django.template.loader import render_to_string
#from django.utils.http import urlsafe_base64_encode
#from django.utils.encoding import force_bytes, force_text
#from .tokens import generate_token

# Create your views here.
def home(request):
    return render(request,"index.html")

def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request,'Username already exist Please try some other user name!')
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.error(request, 'Email already registered Please try other email address!')
            return redirect('signup')

        if len(username)>10:
            messages.error(request, 'username must be under 10 characters!')

        if pass1 != pass2:
            messages.error(request, 'Password did not match!')

        if not username.isalnum():
            messages.error(request, 'username must be alphanumeric!')
            return redirect('signup')

        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        #myuser.is_active = False 

        myuser.save()

        messages.success(request, "Your account has been successfully created please Login!!")

        # Welcome Email
        #subject = "Welcome to the Django Authentication System."
        #message = "Hello" + myuser.first_name + "!!\n" + "Welcome to Django!! \n Thank you for visiting our website \n We have also sent you a confirmation email, please confirm your email address to activate your account."
        #from_email = settings.EMAIL_HOST_USER
        #to_list = [myuser.email]
        #send_mail(subject, message, from_email, to_list, fail_silently=True)

        #Email Confirmation
        #current_site=get_current_site(request)
        #email_subject =  "Confirm your Email"
       # message2 = render_to_string('email_confirmation.html',{
           # 'name':myuser.first_name,
            #'domain':current_site.domain,
            #'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
            #'token':generate_token.make_token(myuser)
        #})
        return redirect('signin')

    return render(request,'signup.html')

def signin(request):

    if request.method=="POST":
        username=request.POST['username']
        pass1=request.POST['pass1']

        user=authenticate(username=username, password=pass1)

        if user is not None:
            login(request,user)
            fname=user.first_name
            return render(request,"index.html",{'fname':fname})
        else:
            messages.error(request, "Bad Creadentials please login again!")
            return redirect('signin')


    return render(request,'signin.html')

def signout(request):
    logout(request)
    messages.success(request,"Logged Out Succesfully!")
    return redirect('home')

