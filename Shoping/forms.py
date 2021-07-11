from django import forms
from django.forms.fields import CharField
from django.forms.forms import Form
from django.utils.html import WRAPPING_PUNCTUATION
from django.contrib.auth import get_user_model

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
        widget=forms.TextInput(attrs={'class':'form-control text-center','placeholder':'Enter Your name'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control text-center','placeholder':'Enter You password'})
    )


# baraye ijad form register dar safheye register.html
class RegisterForm(forms.Form):
    userName = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class':'form-control text-center','placeholder':'Enter Your name'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class':'form-control w-100 text-center','placeholder':'Enter Your Email'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class':'form-control text-center','placeholder':'Enter password'})
    )
    confirm_password = forms.CharField(
        label='Confirm',
        widget=forms.PasswordInput(attrs={'class':'form-control text-center','placeholder':'Enter password again'})
    )

    # baraye check kardan username tekrari.
    def clean_userName(self):
        userName = self.cleaned_data.get('userName')
        filter_name = User.objects.filter(username=userName)
        if filter_name.exists():
            raise forms.ValidationError('User is taken')
        return userName

    # baraye check kardane email tekrari.
    def clean_email(self):
        email = self.cleaned_data.get('email')
        filter_email = User.objects.filter(email=email)
        if filter_email.exists():
            raise forms.ValidationError('Email is taken')
        return email


    # # baraye check kardan password tekrari
    # def clean(self):
    #     data = self.cleaned_data
    #     pass1 = self.cleaned_data.get('password')
    #     pass2 = self.cleaned_data.get('confirm_password')

    #     if len(pass1) < 6:
    #         raise forms.ValidationError('length is small')
    #         if pass1 != pass2:
    #             raise forms.ValidationError('Password must match')
    #     return data
