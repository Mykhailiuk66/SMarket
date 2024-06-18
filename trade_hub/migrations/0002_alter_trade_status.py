# Generated by Django 4.2.2 on 2024-06-18 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_hub', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='status',
            field=models.CharField(choices=[('N', 'New'), ('RW', 'In Review'), ('DC', 'Declined'), ('CD', 'Canceled'), ('SC', 'Success')], default='N', max_length=2),
        ),
    ]
