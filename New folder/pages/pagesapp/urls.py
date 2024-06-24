from django.urls import path
from pagesapp import views

urlpatterns = [
    path("",views.index,name='index'),
    path('user_view/<str:name>', views.user_view, name='user_view'),
    # path('download-pdf/', views.download_pdf, name='download_pdf'),
]
