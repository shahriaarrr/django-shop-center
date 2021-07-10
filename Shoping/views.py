import django
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django import forms

# imports forms.py
from .forms import ContactForm,LoginForm

# imports for user
from django.contrib.auth import authenticate,login


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
def register_page(request):
    return render(request,'register.html',{})