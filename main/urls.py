from django.urls import path
from . import views

urlpatterns = [
    path('login', views.doLogin, name='login'),
    path('logout', views.doLogout, name='logout'),
    path('admin_add', views.admin_add, name='admin_add'),
    path('admin_api', views.admin_api, name='admin_api'),
    path('admin_detail/<int:pk>', views.admin_detail, name='admin_detail'),
    path('lecturer_add', views.lecturer_add, name='lecturer_add'),
    path('lecturer_api', views.lecturer_api, name='lecturer_api'),
    path('lecturer_detail/<int:pk>', views.lecturer_detail, name='lecturer_detail'),
    path('student_add', views.student_add, name='student_add'),
    path('student_api', views.student_api, name='student_api'),
    path('student_detail/<int:pk>', views.student_detail, name='student_detail'),
]