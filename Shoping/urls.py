from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name = 'Shoping'


urlpatterns = [
    path('',views.Home_page,name='home'),
    path('view/',views.contact_page,name='contact'),
    path('login/',views.login_page,name='login'),
    path('register/',views.register_page,name='register')
]