# Generated by Django 3.2 on 2022-04-16 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('out_app', '0014_alter_page_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.SlugField(max_length=12, primary_key=True, serialize=False, unique=True, verbose_name='Page code'),
        ),
    ]
