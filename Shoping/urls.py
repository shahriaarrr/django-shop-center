from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name = 'Shoping'


urlpatterns = [
    path('',views.Home_page,name='home'),
    path('view/',views.contact_page,name='contact'),
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
    
    path('category/',views.product_category,name='category')
]