from django.urls import path
from department import views

urlpatterns = [
    path('addDepartment',views.add_department,name='addDepartment'),
    path('del_department/<int:pk>/',views.del_department,name='del_department'),
    path('department_view/<int:pk>/',views.department_view,name='department_view'),
]