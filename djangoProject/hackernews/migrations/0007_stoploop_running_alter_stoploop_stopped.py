# Generated by Django 4.0.6 on 2022-07-16 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackernews', '0006_comment_remove_story_kids_delete_kid_delete_story'),
    ]

    operations = [
        migrations.AddField(
            model_name='stoploop',
            name='running',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='stoploop',
            name='stopped',
            field=models.BooleanField(default=True),
        ),
    ]
