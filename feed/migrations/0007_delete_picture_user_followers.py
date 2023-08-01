# Generated by Django 4.2.1 on 2023-06-20 11:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0006_alter_user_profile_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Picture',
        ),
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]
