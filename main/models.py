from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
def upload_path(instance, filename):
    file_type = filename.split('.')[-1]
    return '/'.join(['profile_pic', str(instance.id), str(instance.id) + '.' + file_type])

def upload_path_course(instance, filename):
    file_type = filename.split('.')[-1]
    return '/'.join(['course_images', str(instance.id), str(instance.name) + '.' + file_type])

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

class Lecturer(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to=upload_path, default='profile_pic/default.png')
    degree = models.CharField(max_length=255, null=True)
    role = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255)
    degree = models.CharField(max_length=255, null=True)
    profile_pic = models.ImageField(upload_to=upload_path, default='profile_pic/default.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_path_course, default='course_images/default.png')
    degree = models.CharField(max_length=255, null=True)
    description = models.TextField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

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
    file = models.FileField(upload_to='files/')
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

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