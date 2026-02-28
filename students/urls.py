from django.urls import path
from . import views
from .views import student_list,student_detail

urlpatterns = [
    path('students/', views.student_list),
    path('students/<int:id>/',student_detail),
    path('',views.student_list,name='student_list'),
    path('add/',views.add_student,name='add_student'),
    path('update/<int:id>/', views.update_student, name='update_student'),
    path('delete/<int:id>/', views.delete_student, name='delete_student'),
]
