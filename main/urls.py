from django.urls import path
from . import views

urlpatterns = [
    path('login', views.doLogin, name='login'),
    path('logout', views.doLogout, name='logout'),
    path('addAdmin', views.addAdmin, name='addAdmin'),
    path('admin_api', views.admin_api, name='admin_api'),
    path('admin_api/<str:pk>', views.admin_api, name='admin_api'),
]