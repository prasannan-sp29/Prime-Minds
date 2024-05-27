from django.urls import path
from accounts import views

urlpatterns = [
    path('',views.index,name = 'index'),
    # path('register/',views.register_details,name='register'),
    path('profile/',views.profile,name='profile'),
]