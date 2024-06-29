import os
import shutil
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from backend import settings

# Create your models here.
def upload_path(instance, filename):
    file_type = filename.split('.')[-1]
    return '/'.join(['profile_pic', str(instance.id), str(instance.id) + '.' + file_type])

def upload_path_course(instance, filename):
    file_type = filename.split('.')[-1]
    return '/'.join(['course_images', str(instance.name), str(instance.name) + '.' + file_type])

def upload_path_materials(instance, filename):
    file_type = filename.split('.')[-1]
    return '/'.join(['lecture_materials', str(instance.title), str(instance.filename) + '.' + file_type])

class CustomUser(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "Lecturer"), (3, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to=upload_path, default='profile_pic/default.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def delete(self, *args, **kwargs):
        default_file_path = os.path.join(settings.MEDIA_ROOT, 'profile_pic', 'default.png')

        if self.profile_pic and self.profile_pic.path != default_file_path:
            file_path = self.profile_pic.path
            if os.path.isfile(file_path):
                os.remove(file_path)

        directory_path = os.path.join(settings.MEDIA_ROOT, 'profile_pic', str(self.id))
        if os.path.isdir(directory_path):
            shutil.rmtree(directory_path)

        super().delete(*args, **kwargs)

class Lecturer(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to=upload_path, default='profile_pic/default.png')
    degree = models.CharField(max_length=255, null=True)
    role = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def delete(self, *args, **kwargs):
        default_file_path = os.path.join(settings.MEDIA_ROOT, 'profile_pic', 'default.png')

        if self.profile_pic and self.profile_pic.path != default_file_path:
            file_path = self.profile_pic.path
            if os.path.isfile(file_path):
                os.remove(file_path)

        directory_path = os.path.join(settings.MEDIA_ROOT, 'profile_pic', str(self.id))
        if os.path.isdir(directory_path):
            shutil.rmtree(directory_path)

        super().delete(*args, **kwargs)

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255)
    degree = models.CharField(max_length=255, null=True)
    profile_pic = models.ImageField(upload_to=upload_path, default='profile_pic/default.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def delete(self, *args, **kwargs):
        default_file_path = os.path.join(settings.MEDIA_ROOT, 'profile_pic', 'default.png')

        if self.profile_pic and self.profile_pic.path != default_file_path:
            file_path = self.profile_pic.path
            if os.path.isfile(file_path):
                os.remove(file_path)

        directory_path = os.path.join(settings.MEDIA_ROOT, 'profile_pic', str(self.id))
        if os.path.isdir(directory_path):
            shutil.rmtree(directory_path)

        super().delete(*args, **kwargs)

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_path_course, default='course_images/default.png')
    degree = models.CharField(max_length=255, null=True)
    description = models.TextField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def delete(self, *args, **kwargs):
        default_file_path = os.path.join(settings.MEDIA_ROOT, 'course_images', 'default.png')

        if self.image and self.image.path != default_file_path:
            file_path = self.image.path
            if os.path.isfile(file_path):
                os.remove(file_path)

        directory_path = os.path.join(settings.MEDIA_ROOT, 'course_images', str(self.name))
        if os.path.isdir(directory_path):
            shutil.rmtree(directory_path)

        super().delete(*args, **kwargs)

class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.TextField()
    lecturer_id = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    sender_id = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class LectureMaterial(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    filename = models.CharField(max_length=255, null=True)
    file = models.FileField(upload_to=upload_path_materials, null=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def delete(self, *args, **kwargs):
        if self.file:
            file_path = self.file.path
            if os.path.isfile(file_path):
                os.remove(file_path)

        directory_path = os.path.join(settings.MEDIA_ROOT, 'lecture_materials', str(self.title))
        if os.path.isdir(directory_path):
            shutil.rmtree(directory_path)

        super().delete(*args, **kwargs)

class ChatGPT(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.TextField()
    response = models.TextField()
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Lecturer.objects.create(admin=instance)
        if instance.user_type == 3:
            Student.objects.create(admin=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.lecturer.save()
    if instance.user_type == 3:
        instance.student.save()