# Generated by Django 4.2.2 on 2023-06-10 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_name_profile_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='discount',
            field=models.IntegerField(default=0),
        ),
    ]