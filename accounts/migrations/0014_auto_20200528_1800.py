# Generated by Django 2.2.6 on 2020-05-28 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20200527_1302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='messages_count',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='notifications_count',
        ),
    ]
