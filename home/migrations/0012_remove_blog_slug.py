# Generated by Django 4.0.1 on 2022-01-23 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_blog_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='slug',
        ),
    ]
