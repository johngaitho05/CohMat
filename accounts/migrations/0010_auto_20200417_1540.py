# Generated by Django 2.2.6 on 2020-04-17 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_userprofile_school'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_photo',
            field=models.FileField(default='C:\\Users\\John YK\\PycharmProjects\\CohMat\\media\\profile_photos/default_profile_pic.png', upload_to='profile_photos'),
        ),
    ]