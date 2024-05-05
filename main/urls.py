from django.urls import path
from . import views

urlpatterns = [
    path('lecturer/', views.LecturerList.as_view()),
    path('lecturer/<int:pk>/', views.LecturerDetail.as_view()),
]