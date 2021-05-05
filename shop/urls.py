
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='shop home'),
    path('about/',views.about,name='About Us'),
    path('contact/',views.contact,name='Contact'),
    path('tracker/',views.tracker,name='Tracker'),
    path('search/',views.search,name='Search'),
    path('productView/<int:myid>',views.productView,name='ProductView'),
    path('checkout/',views.checkout,name='Checkout'),
    path('handlerequest/',views.handlerequest,name='HandleRequest'),

]