# Generated by Django 5.0.4 on 2024-04-30 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
