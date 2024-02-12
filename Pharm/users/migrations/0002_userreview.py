# Generated by Django 5.0.1 on 2024-02-10 17:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userprofile')),
            ],
        ),
    ]
