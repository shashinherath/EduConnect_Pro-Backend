# Generated by Django 5.0.6 on 2024-07-01 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_rename_lecturer_id_announcement_lecturer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='announcement',
            old_name='lecturer',
            new_name='lecturer_id',
        ),
    ]
