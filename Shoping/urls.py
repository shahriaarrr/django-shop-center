from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name = 'Shoping'


urlpatterns = [
    path('',views.Home_page,name='home'),
    # path('view/',views.contact_page,name='contact'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_page,name='logout'),
    path('register/',views.register_page,name='register'),

    # products
    # path('product-list/',views.product_list_view,name='ProductList'),  #--> with function base
    path('Product-list/',views.ProductListView.as_view(),name='ProductList'),

    path('product-detail/<int:pk>',views.product_detail_view,name='ProductDetail'), 
    # path('Product-detail/',views.ProductDetailView.as_view(),name='ProductDetail')

    # path('404-error/',views.page_404,name='page-404')
    path('Product-list/search/',views.SearchView.as_view()),

    #category
    path('Product-list/<category_name>',views.ProductListViewByCategory.as_view()),
    
    path('category/',views.product_category,name='category'),

    path('contact-us/',views.ContactPage,name='contact'),
    path('about-us/',views.AboutPage,name='about'),

    # order
    path('add-user-order',views.add_user_order),

    # user open order
    path('user-open-order/',views.user_open_order,name='openOrder'), 
    
    # dargah pardakht
    path('request/',views.send_request,name='request'),
    path('verify/',views.verify,name='verify'),

    #profile
    path('profile/',views.profile_user,name='profile'),
    path('profile/edit',views.edit_profile,name='edit-profile'),

]