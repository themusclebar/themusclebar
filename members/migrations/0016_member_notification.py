# Generated by Django 2.0.3 on 2018-04-02 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0015_auto_20180402_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='notification',
            field=models.IntegerField(default=0),
        ),
    ]
