# Generated by Django 5.0.6 on 2024-09-15 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventer', '0003_registration'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='tickets_sold',
            field=models.IntegerField(default=0),
        ),
    ]
