# Generated by Django 5.0.4 on 2024-06-28 10:12

import main.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_remove_assignmentsubmission_assignment_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturematerial',
            name='file',
            field=models.FileField(null=True, upload_to=main.models.upload_path_materials),
        ),
    ]
