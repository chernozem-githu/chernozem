from django.urls import path
from . import views
from .views import catalog_view, cart_view, add_to_cart, remove_from_cart
from .views import cart_page
from .views import add_perfume
from .views import catalog_view, perfume_detail
urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_page, name='profile'),
    path('confirm/', views.confirm_code, name='confirm_code'),
    path('catalog/', catalog_view, name='catalog'),
    path('cart/', cart_view, name='cart'),
    path('cart/', cart_page, name='cart'),
    path('cart/add/<int:perfume_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('add/', add_perfume, name='add_perfume'),
    path('catalog/<int:pk>/', perfume_detail, name='perfume_detail'),
]
