# Generated by Django 3.0.5 on 2020-07-06 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0022_auto_20200706_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]