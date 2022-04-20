# Generated by Django 3.2 on 2022-04-20 13:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('out_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allowed_page', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ViewerAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shown_name', models.CharField(max_length=100, verbose_name='My name (as it will appear to viewer)')),
                ('viewer_name', models.CharField(max_length=100)),
                ('viewer_email', models.EmailField(max_length=100)),
                ('allowed_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='out_app.page', verbose_name='Page code - this can be found on your profile page')),
            ],
        ),
    ]
