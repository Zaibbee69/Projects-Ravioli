# Generated by Django 5.0.6 on 2024-07-22 15:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auctionlisting_category_auctionlisting_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='auction_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='highest_bid',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist_auction', to='auctions.auctionlisting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]