# Generated by Django 5.1.5 on 2025-02-07 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fields', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='lat',
            field=models.FloatField(default=None, null=None),
        ),
        migrations.AddField(
            model_name='field',
            name='long',
            field=models.FloatField(default=None, null=None),
        ),
    ]
