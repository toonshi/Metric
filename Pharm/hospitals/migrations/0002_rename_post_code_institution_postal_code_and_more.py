# Generated by Django 5.0.2 on 2024-02-17 04:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='institution',
            old_name='post_code',
            new_name='postal_code',
        ),
        migrations.AddField(
            model_name='institution',
            name='image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='images/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userreview',
            name='review_image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='images/'),
            preserve_default=False,
        ),
    ]