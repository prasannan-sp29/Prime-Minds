# urls.py
from django.urls import path
from .views import fetch_and_store_email_data

urlpatterns = [
    path('fetch-emails/', fetch_and_store_email_data, name='fetch_emails'),
]
