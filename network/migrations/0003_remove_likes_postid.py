# Generated by Django 3.1.7 on 2021-06-17 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20210617_2305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likes',
            name='postid',
        ),
    ]
