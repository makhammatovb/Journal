# Generated by Django 5.0.4 on 2024-05-21 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tuit', '0009_publications_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewers',
            name='first_name',
            field=models.CharField(default=2, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reviewers',
            name='last_name',
            field=models.CharField(default=2, max_length=255),
            preserve_default=False,
        ),
    ]
