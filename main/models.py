from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
def upload_path(instance, filename):
    file_type = filename.split('.')[-1]
    return '/'.join(['profile_pic', str(instance.admin.username), str(instance.admin.username + '.' + file_type)])

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
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    lecturer_id = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to=upload_path, default='profile_pic/default.png')
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

#lecture able to chat with student. so create chat model here
class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.TextField()
    sender_id = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    receiver_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

#lecture able to mark attendence of students. so create attendence model here
class Attendence(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    lecture_id = models.ForeignKey(Lecturer, on_delete=models.DO_NOTHING)
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

#lecture able to give lecture material(lecture pdfs videos) to students under the course. so create lecture material model here
class LectureMaterial(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='files/')
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

#lecture able to give assignment to students under the course. so create assignment model here
class Assignment(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='files/')
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

#student able to submit assignment to lecture under the course. so create assignment submission model here
class AssignmentSubmission(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='files/')
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

#student able to view availability of lecturers. lecturers mark their abalaibility by clicking on available or not available button. so create availability model here
class LecturerAvailability(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    status = models.CharField(max_length=255)
    lecture_id = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

#students able to use and find knowladge using integrated chatGPT via API. so I need to store those data for each student. so create chatGPT model here
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