# Generated by Django 5.0.4 on 2024-06-22 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_rename_phoen_number_lecturer_phone_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='address',
            new_name='phone_number',
        ),
        migrations.RemoveField(
            model_name='student',
            name='course_id',
        ),
        migrations.AddField(
            model_name='student',
            name='course_id',
            field=models.ManyToManyField(to='main.course'),
        ),
    ]
