from django.db import models

# Create your models here.
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    first_Name = models.CharField(max_length=100)
    last_Name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=100)
    birth_Date = models.DateField()
    contact = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class Lecturer(models.Model):
    id = models.AutoField(primary_key=True)
    first_Name = models.CharField(max_length=100)
    last_Name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)