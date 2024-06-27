# Generated by Django 5.0.4 on 2024-06-26 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_rename_sender_id_chat_lecturer_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lecturer',
            old_name='phone_number',
            new_name='degree',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='level',
            new_name='degree',
        ),
        migrations.AddField(
            model_name='course',
            name='degree',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
