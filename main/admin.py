from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Custom admin class
class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserModel)