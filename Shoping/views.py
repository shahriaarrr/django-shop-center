from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_list_or_404
from django.http import Http404,HttpResponse
from django.urls.conf import path

# imports forms.py
from .forms import ContactForm,LoginForm,RegisterForm,ContactUsForm,UserNewOrderForm,EditProfileForm

# imports for user
from django.contrib.auth import authenticate,login,get_user_model,logout  # <-- register (get_user_model)

# class views
from django.views.generic import ListView
from django.views.generic import DetailView

# imports Product -> models.py
from .models import Product,Tag,Category,Slider,Gallery,ContactUsModel,AboutUs,OrderDetail,Order


import itertools

from zeep import Client


# -----------------------------

def Home_page(request): 
    name = 'yaisn esmaeili'
    sliders = Slider.objects.all()
    context = {
        'sliders':sliders
    }
    return render(request,'home.html',context)

# -----------------------------

# def contact_page(request):
#     contact_form = ContactForm(request.POST or None)
#     if contact_form.is_valid():
#         print(contact_form.cleaned_data)
#         print(contact_form.cleaned_data.get('content'))
#     # if request.method == 'POST':
#         # print(request.POST.get('fullname'))
#     context = {
#         'contactform':contact_form
#     }
#     return render(request,'view.html',context)

# -----------------------------

def login_page(request):

    # agar user login bood dige page login ro neshon nade!
    if request.user.is_authenticated:
        return redirect('Shoping:home')
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
            login_form.add_error('userName','??? User has not Found ???')

    return render(request,'login.html',context)

# -----------------------------

def logout_page(request):
    logout(request)
    return redirect('Shoping:home')


# -----------------------------

# baraye in ke az methodesh vaseye sakht user jadid estefate bshe bayad import beshe 
# from django.contrib.auth import get_user_model
#get_user_model.objects.create_user(username,email,password)
User = get_user_model()
def register_page(request):

    # agar user login bood dige page login ro neshon nade!
    if request.user.is_authenticated:
        return redirect('Shoping:home')

    register_form = RegisterForm(request.POST or None)
    context = {
        'registerform':register_form
    }

    # # baraye sakhtane user jadid 
    if register_form.is_valid():
        Username = register_form.cleaned_data.get('userName')
        Email = register_form.cleaned_data.get('email')
        Password = register_form.cleaned_data.get('password')
        User.objects.create_user(username=Username,email=Email,password=Password)
        return redirect('Shoping:login')

    return render(request,'register.html',context)

# -----------------------------
# def product_list_view(request):
#     products = Product.objects.all()
#     context = {
#         'products':products
#     }
#     return render(request,'product/product-list.html',context)
# -----------------------------

# class list
class ProductListView(ListView):
    # queryset = Product.objects.all()
    template_name = 'product/product-list.html'
    paginate_by = 4
    
    def get_queryset(self):
        return Product.objects.get_active_product()

# -----------------------------

# for searching products
class SearchView(ListView):
    template_name = 'product/product-list.html'
    paginate_by = 2

    def get_queryset(self):
        request = self.request

        #???????? ?????? ???? ???????? ?????? ???????? ?????? ?????????? ???? ???? ??????(q)
        qs = request.GET.get('question')
        if qs is not None:
            # ???????? ?????????? ???? ?????????? ?? ???? ?????????????? ???? ?????????? ?????? ?????? ???? ???????? ???? ?????????? ???? ?????????? ???????????? ?? ???? ???? ???? ?????????? ?????? ??????????
            return Product.objects.Search(qs)
        return Product.objects.get_active_product()

        # __icontains -> ???????? ???????? ???? ???????? ?????? ?????????? ??????
        # __iexact -> ???????? ???????? ???? ?????????? ?????????? ???? ?????????? ???????? ?????? ??????

# -----------------------------
def group_list_image_gallery(num,list_show):
    args = [iter(list_show)] * num
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def product_detail_view(request,pk):

    # handel error 404
    product = get_list_or_404(Product,id=pk)
    product = Product.objects.get(id=pk)

    new_order_form = UserNewOrderForm(request.POST or None,initial={'product_id':pk})
    
    # list tag haei eke vase har product set shode ro neshon mide
    # print(product.tag_set.all())

    # ???????? ?????????? ?????? ???????????? ?????????? ???????? ?????? ?????????? ?????? ???? ???? ???? ???? ???? ?????????? ???????? ????????.
    if product is None or not product.active:
        raise Http404('?????????? ???????? ?????? ???????? ??????')

    # ???????? ?????????? ???????? ?????????????? ???????????????? ???? ???? ????????
    mahsolat_pisnahadi = Product.objects.get_queryset().filter(categories__product=product).distinct()
    grouped_mahsolat_pisnahadi = group_list_image_gallery(3,mahsolat_pisnahadi)

    gallery = Gallery.objects.filter(product_id=product)
    gallery_list = list(group_list_image_gallery(3,gallery))
    # print(gallery)
    context = {
        'product':product,
        'gallery':gallery_list,
        'mahsolat_pisnahadi':grouped_mahsolat_pisnahadi,
        'new_order_form':new_order_form
        }
    return render(request,'product/produvt-detail.html',context)

        # return redirect('Shoping:page-404')

# -----------------------------

class ProductListViewByCategory(ListView):
    # queryset = Product.objects.all()
    template_name = 'product/product-list.html'
    paginate_by = 4
    
    def get_queryset(self):
        # print(self.kwargs)
        category_name = self.kwargs['category_name']
        caegory = Category.objects.filter(name__iexact=category_name).first()
        if caegory is None:
            raise Http404('???????? ?? ???????? ?????? ???????? ??????!')

        return Product.objects.get_category(caegory)


def product_category(request):
    category = Category.objects.all()
    context = {
        'category':category
        }
    return render(request,'product-list.html',context)


# ----- contact page ----
def ContactPage(request):

    contact_form = ContactUsForm(request.POST or None)
    if contact_form.is_valid():
        fullname = contact_form.cleaned_data.get('full_name')
        email = contact_form.cleaned_data.get('email')
        text = contact_form.cleaned_data.get('text')
        ContactUsModel.objects.create(full_name=fullname,email=email,text=text)
        contact_form = ContactUsForm()
        return redirect('Shoping:home')


    context = {
        'contactform':contact_form
    }

    return render(request,'contact.html',context)

def AboutPage(request):
    text = AboutUs.objects.first()
    context = {
        'text':text
    }

    return render(request,'aboutus.html',context)



#---- Order
# zamani mishe kharid kard ke user login bashe
@login_required(login_url='Shoping:login')
def add_user_order(request):
    new_order_form = UserNewOrderForm(request.POST or None)

    if new_order_form.is_valid():
        order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
        if order is None:
            order = Order.objects.create(owner_id=request.user.id,is_paid=False)
        product_id = new_order_form.cleaned_data.get('product_id')
        count = new_order_form.cleaned_data.get('count')
        if count < 0:
            count = 1
        product = Product.objects.get_queryset().filter(id=product_id).first()
        order.orderdetail_set.create(product_id=product.id,price=product.price, count=count)
            
        
        return redirect('Shoping:home')


# sabad kharid
def user_open_order(request):
    context = {
        'order':None,
        'details':None
    }
    open_order:Order = Order.objects.filter(owner_id=request.user.id,is_paid=False).first()
    if open_order is not None:
        context['order'] = open_order
        context['details'] = open_order.orderdetail_set.all()

    return render(request,'user-open-order.html',context)



# dargah pardakht
MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
amount = 1000  # Toman / Required
description = "?????????????? ?????????? ???? ???????????? ???? ???? ?????? ???????? ???????? ????????"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
CallbackURL = 'http://localhost:8000/verify/' # Important: need to edit for realy server.

def send_request(request):
    result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))

def verify(request):
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')




@login_required(login_url='Shoping:login')
def profile_user(request):

    context = {}
    return render(request,'profile.html',context)


@login_required(login_url='Shoping:login')
def edit_profile(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if user is None:
        raise Http404('?????????? ???????? ?????? ???????? ??????')

    edit_profile_form = EditProfileForm(request.POST or None,initial={'first_name':user.first_name,'last_name':user.last_name})
    if edit_profile_form.is_valid():
        first_name = edit_profile_form.cleaned_data.get('first_name')
        last_name = edit_profile_form.cleaned_data.get('last_name')
        user.first_name = first_name
        user.last_name = last_name
        user.save()

    context = {
        'edit_form':edit_profile_form
    }

    return render(request,'edit-profile.html',context)