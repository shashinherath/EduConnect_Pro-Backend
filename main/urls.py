from django.urls import path
from . import views

urlpatterns = [
    path('login', views.doLogin, name='login'),
    path('logout', views.doLogout, name='logout'),
    path('admin_add', views.admin_add, name='admin_add'),
    path('admin_api', views.admin_api, name='admin_api'),
    path('admin_detail/<int:pk>', views.admin_detail, name='admin_detail'),
]