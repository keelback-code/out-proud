# Generated by Django 3.2 on 2022-03-18 10:25

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('page_code', models.SlugField(max_length=8, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=250)),
                ('text_content', models.TextField()),
                ('photo', cloudinary.models.CloudinaryField(max_length=255)),
                ('video', cloudinary.models.CloudinaryField(max_length=255)),
                ('link', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, 'Draft'), (1, 'Ready to Send')], default=0)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fillthisin', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]