# Generated by Django 3.2 on 2022-05-03 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('out_app', '0007_alter_vieweraccess_allowed_page'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vieweraccess',
            old_name='email',
            new_name='viewer_email',
        ),
    ]