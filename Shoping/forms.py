from django import forms
from django.forms.fields import CharField
from django.forms.forms import Form
from django.utils.html import WRAPPING_PUNCTUATION

class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control w-100 text-center','placeholder':'Enter Your FullName'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control w-100 text-center','placeholder':'Enter Your Email'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control w-100 text-center','placeholder':'Enter content'}))


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if 'yasin' in email:
            raise forms.ValidationError('Yasin in email Field')


class LoginForm(forms.Form):
    userName = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control text-center','placeholder':'Enter Your name'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control text-center','placeholder':'Enter You password'})
    )
