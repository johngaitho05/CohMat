# Generated by Django 3.0.5 on 2020-07-06 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_remove_userprofile_user_cohorts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_photo',
            field=models.FileField(default='C:\\Users\\John YK\\PycharmProjects\\CohMat\\media\\profile_photos/default_profile_pic.png', upload_to='profile_photos'),
        ),
    ]
