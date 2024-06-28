from django.urls import path
from . import views

urlpatterns = [
    path('login', views.doLogin, name='login'),
    path('logout', views.doLogout, name='logout'),
    path('current_user', views.current_user, name='current_user'),
    path('admin_add', views.admin_add, name='admin_add'),
    path('admin_api', views.admin_api, name='admin_api'),
    path('admin_detail/<int:pk>', views.admin_detail, name='admin_detail'),
    path('lecturer_add', views.lecturer_add, name='lecturer_add'),
    path('lecturer_api', views.lecturer_api, name='lecturer_api'),
    path('lecturer_detail/<int:pk>', views.lecturer_detail, name='lecturer_detail'),
    path('student_add', views.student_add, name='student_add'),
    path('student_api', views.student_api, name='student_api'),
    path('student_detail/<int:pk>', views.student_detail, name='student_detail'),
    path('course_add', views.course_add, name='course_add'),
    path('course_api', views.course_api, name='course_api'),
    path('course_detail/<int:pk>', views.course_detail, name='course_detail'),
    path('lecture_material_add', views.lecture_material_add, name='lecture_material_add'),
    path('lecture_material_api', views.lecture_material_api, name='lecture_material_api'),
    path('lecture_material_detail/<int:pk>', views.lecture_material_detail, name='lecture_material_detail'),
]