# Generated by Django 4.2.2 on 2023-06-14 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketitem',
            name='status',
            field=models.CharField(choices=[('N', 'New'), ('SD', 'Sold'), ('CD', 'Canceled')], default='N', max_length=2),
        ),
    ]
