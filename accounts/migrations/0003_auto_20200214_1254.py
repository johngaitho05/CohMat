# Generated by Django 2.2.6 on 2020-02-14 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200211_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_groups',
            field=models.TextField(default='[]'),
        ),
    ]