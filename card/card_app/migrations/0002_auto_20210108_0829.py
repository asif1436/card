# Generated by Django 3.0.4 on 2021-01-08 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='father_name',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='inter_marks',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='mother_name',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='nationality',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='ssc_marks',
        ),
    ]
