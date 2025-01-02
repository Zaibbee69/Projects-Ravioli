# Generated by Django 5.0.6 on 2024-10-01 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companer', '0010_user_blog'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='confirmation',
            field=models.CharField(default=21, max_length=64),
            preserve_default=False,
        ),
    ]