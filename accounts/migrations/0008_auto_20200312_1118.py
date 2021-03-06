# Generated by Django 2.2.6 on 2020-03-12 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_userprofile_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='current_interest',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_current_interest', to='mainapp.Cohort'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='study_field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.Cohort'),
        ),
    ]
