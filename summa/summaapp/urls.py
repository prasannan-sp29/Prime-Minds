from django.urls import path
from .views import *

urlpatterns = [
    path('', my_form_view, name='my_form_view'),
    path('food/',create_food_item,name='food')
]