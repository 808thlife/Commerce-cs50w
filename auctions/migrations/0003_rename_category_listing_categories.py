# Generated by Django 4.1.4 on 2023-02-09 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_listing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='category',
            new_name='categories',
        ),
    ]
