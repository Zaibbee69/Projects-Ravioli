# Generated by Django 5.0.6 on 2024-09-28 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companer', '0004_companyoverview_companyvalue'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('summary', models.TextField()),
                ('description', models.TextField()),
                ('icon', models.CharField(max_length=64)),
            ],
        ),
    ]
