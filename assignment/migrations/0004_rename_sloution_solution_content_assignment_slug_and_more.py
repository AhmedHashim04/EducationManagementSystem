# Generated by Django 5.1.1 on 2025-04-24 05:55

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0003_grade'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solution',
            old_name='sloution',
            new_name='content',
        ),
        migrations.AddField(
            model_name='assignment',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='grade',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='solution',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
