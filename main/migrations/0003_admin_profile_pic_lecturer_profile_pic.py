# Generated by Django 5.0.4 on 2024-06-18 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_admin_email_remove_admin_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='profile_pic',
            field=models.ImageField(default='images/default.png', upload_to='images/'),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='profile_pic',
            field=models.ImageField(default='images/default.png', upload_to='images/'),
        ),
    ]
