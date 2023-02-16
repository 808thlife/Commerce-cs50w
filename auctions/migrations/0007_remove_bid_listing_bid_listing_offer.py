# Generated by Django 4.1.4 on 2023-02-14 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_comments_remove_listing_bid_remove_listing_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='listing',
        ),
        migrations.AddField(
            model_name='bid',
            name='listing_offer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='auctions.listing'),
        ),
    ]
