# Generated by Django 3.1.7 on 2021-06-19 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_posts_total_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
