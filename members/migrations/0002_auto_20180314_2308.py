# Generated by Django 2.0.3 on 2018-03-14 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='registration_date',
        ),
        migrations.RemoveField(
            model_name='member',
            name='registration_upto',
        ),
    ]