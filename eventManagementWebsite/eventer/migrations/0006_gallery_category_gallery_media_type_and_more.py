# Generated by Django 5.0.6 on 2024-09-15 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventer', '0005_gallery'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='category',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='gallery',
            name='media_type',
            field=models.CharField(choices=[('image', 'Image'), ('video', 'Video')], default='image', max_length=10),
        ),
        migrations.AddField(
            model_name='gallery',
            name='video_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
