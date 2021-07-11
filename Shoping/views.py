import django
from django.db import reset_queries
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django import forms

# imports forms.py
from .forms import ContactForm,LoginForm,RegisterForm

# imports for user
from django.contrib.auth import authenticate,login,get_user_model  # <-- register (get_user_model)





# -----------------------------
def Home_page(request):
    name = 'yaisn esmaeili'
    context = {
        'name':name
    }
    return render(request,'home.html',context)
# -----------------------------
def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        print(contact_form.cleaned_data.get('content'))
    # if request.method == 'POST':
        # print(request.POST.get('fullname'))
    context = {
        'contactform':contact_form
    }
    return render(request,'view.html',context)
# -----------------------------
def login_page(request):
    login_form = LoginForm(request.POST or None)

    context = {
        'loginform':login_form
    }

    if login_form.is_valid():

        # get username and password and checking for login and redirect user to home page!
        Username = login_form.cleaned_data.get('userName')
        Password = login_form.cleaned_data.get('password')
        user = authenticate(request,username=Username,password=Password)

        if user is not None:
            login(request,user)

            # baAd az inke form post shop text dakhel pak beshe
            context['loginform'] = LoginForm()
            return redirect('Shoping:home')
        else:
            print('User has not exists!')
        

    # if request.user.is_authenticated:
    #     print('Yes')
    # else:
    #     return redirect('Shoping:contact')


    return render(request,'login.html',context)

# -----------------------------

# baraye in ke az methodesh vaseye sakht user jadid estefate bshe bayad import beshe 
# from django.contrib.auth import get_user_model
#get_user_model.objects.create_user(username,email,password)

# User = get_user_model()
def register_page(request):
    register_form = RegisterForm(request.POST or None)
    context = {
        'registerform':register_form
    }

    # # baraye sakhtane user jadid 
    # if register_form.is_valid():
    #     Username = register_form.cleaned_data.get('userName')
    #     Email = register_form.cleaned_data.get('email')
    #     Password = register_form.cleaned_data.get('password')
    #     User.objects.create_user(username=Username,email=Email,password=Password)
    #     return redirect('Shoping:home')



    return render(request,'register.html',context)