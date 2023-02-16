# Generated by Django 4.1.4 on 2023-02-14 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_listing_categories'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_offer', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='listing',
            name='img',
            field=models.ImageField(upload_to='auctions/media/images'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.AddField(
            model_name='listing',
            name='bid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid', to='auctions.bid'),
        ),
    ]
