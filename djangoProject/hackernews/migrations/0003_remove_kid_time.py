# Generated by Django 4.0.6 on 2022-07-16 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hackernews', '0002_kid_story_kids'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kid',
            name='time',
        ),
    ]
