# Generated by Django 2.2.6 on 2020-03-12 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_reply_content'),
        ('accounts', '0005_remove_userprofile_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='current_interest',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.Cohort'),
        ),
    ]