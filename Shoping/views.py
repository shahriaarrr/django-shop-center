import django
from django.db import reset_queries
from django.db.models.signals import pre_save
from django.shortcuts import render,redirect,get_list_or_404
from django.http import Http404, request
from django import forms

# imports forms.py
from .forms import ContactForm,LoginForm,RegisterForm

# imports for user
from django.contrib.auth import authenticate,login,get_user_model,logout  # <-- register (get_user_model)

# class views
from django.views.generic import ListView
from django.views.generic import DetailView

# imports Product -> models.py
from .models import Product,Tag,Category,Slider,Gallery


import itertools

# -----------------------------

def Home_page(request): 
    name = 'yaisn esmaeili'
    sliders = Slider.objects.all()
    context = {
        'sliders':sliders
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
            login_form.add_error('userName','❌ User has not Found ❌')

    return render(request,'login.html',context)

# -----------------------------

def logout_page(request):
    if request.method == 'POST':
        logout(request)
        
        return redirect('Shoping:home')
    return render(request, 'logout.html',{})

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

        #میگه اگر حر وارد شده برای سرچ برابر ود با کیو(q)
        qs = request.GET.get('question')
        if qs is not None:
            # برای اینکه هم عنوان و هم توضیحات را بتوان سرچ کرد در مودل یک تابعی در منجرش ساختیم و آن را به اینجا پاس دادیم
            return Product.objects.Search(qs)
        return Product.objects.get_active_product()

        # __icontains -> فیلد هایی که شامل این مقدار هست
        # __iexact -> فیلد هایی که دقیقا برابر با مقدار وارد شده است

# -----------------------------
def group_list_image_gallery(num,list_show):
    args = [iter(list_show)] * num
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def product_detail_view(request,pk):
    # handel error 404
    product = get_list_or_404(Product,id=pk)
    product = Product.objects.get(id=pk)

    # list tag haei eke vase har product set shode ro neshon mide
    # print(product.tag_set.all())

    # برای اینکه اگر محصولی اکتیو نبود توی دیتیل ویو هم در یو ار ال نمایش داده نشود.
    if product is None or not product.active:
        raise Http404('محصول مورد نظر یافت نشد')

    # برای ساختن قسمت محصولات پیشنهادی در هر صفحه
    mahsolat_pisnahadi = Product.objects.get_queryset().filter(categories__product=product).distinct()
    grouped_mahsolat_pisnahadi = group_list_image_gallery(3,mahsolat_pisnahadi)

    gallery = Gallery.objects.filter(product_id=product)
    gallery_list = list(group_list_image_gallery(3,gallery))
    print(gallery)
    context = {
        'product':product,
        'gallery':gallery_list,
        'mahsolat_pisnahadi':grouped_mahsolat_pisnahadi
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
            raise Http404('صفحه ی مورد نظر یافت نشد!')

        return Product.objects.get_category(caegory)


def product_category(request):
    category = Category.objects.all()
    context = {
        'category':category
        }
    return render(request,'product-list.html',context)