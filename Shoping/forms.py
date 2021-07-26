from django import forms
from django.forms import widgets
from django.forms.fields import CharField
from django.forms.forms import Form
from django.utils.html import WRAPPING_PUNCTUATION
from django.contrib.auth import get_user_model,authenticate
from django.core import validators

# baraye check kardan email va username tekrari bayad import beshe ta az mothode filteresh estefade bshe.
User = get_user_model()


# pass
class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control w-100 text-center','placeholder':'Enter Your FullName'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control w-100 text-center','placeholder':'Enter Your Email'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control w-100 text-center','placeholder':'Enter content'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if 'yasin' in email:
            raise forms.ValidationError('Yasin in email Field')


# baraye ijad form login dar safheye login.html
class LoginForm(forms.Form):
    userName = forms.CharField(
        widget=forms.TextInput(attrs={'class':'text-center','placeholder':'Enter your Name'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'text-center','placeholder':'Enter you Password'})
    )

    # def clean_userName(self):
    #     username = self.cleaned_data.get('userName')
    #     password = self.cleaned_data.get('password')
    #     user = authenticate(username=username,password=password)
    #     if user is None:
    #         raise forms.ValidationError('User has not exists!')


# baraye ijad form register dar safheye register.html
class RegisterForm(forms.Form):
    userName = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class':'text-center','placeholder':'Enter your name'}),
        validators=[
            validators.MaxLengthValidator(limit_value=20,message='تعداد کاراکتر ها نمیتواند بیشتر از 20 باشد'),
            validators.MinLengthValidator(limit_value=8,message='تعداد کاراکتر ها نمیتواند کم تر از 8 باشد')
            
            ]
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class':'text-center','placeholder':'Enter your Email'}),
        validators=[
            validators.EmailValidator(message='ایمیل وارد شده صحیح نمیباشد')
        ]
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class':'text-center','placeholder':'Enter your Password'})
    )
    confirm_password = forms.CharField(
        label='Confirm',
        widget=forms.PasswordInput(attrs={'class':'text-center','placeholder':'Enter your confirm Password'})
    )

    # remember = forms.BooleanField()

    # baraye check kardan username tekrari.
    def clean_userName(self):
        userName = self.cleaned_data.get('userName')
        filter_name = User.objects.filter(username=userName)
        if filter_name.exists():
            raise forms.ValidationError('این نام کاربری وجود دارد')
        return userName

    # baraye check kardane email tekrari.
    def clean_email(self):
        email = self.cleaned_data.get('email')
        filter_email = User.objects.filter(email=email)
        if filter_email.exists():
            raise forms.ValidationError('ایمیل وجود دارد')
        return email


    # baraye check kardan password tekrari
    def clean_confirm_password(self):
        data = self.cleaned_data
        pass1 = self.cleaned_data.get('password')
        pass2 = self.cleaned_data.get('confirm_password')

        if pass1 != pass2 :
            raise forms.ValidationError('پسورد مغایرت دارد')
        elif len(pass1) < 6:
            raise forms.ValidationError('پسورد زیادی کوچک است')
        return data



class ContactUsForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'لطفا نام و نام خانوادگی خود را وارد کنید'}),label='نام و نام خانوادگی',validators=[validators.MaxLengthValidator(150,message='نام و نام خانوادگی شما نمیتواند بیشتر از 150 کاراکتر باشد')])
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'ایمیل خودرا وارد کنید'}),label='ایمیل',validators=[validators.EmailValidator(message='ایمیل وارد شده اشتباه است')])
    text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'متن پیام خود را وارد کنید ...'}),label='متن پیام ')
    
