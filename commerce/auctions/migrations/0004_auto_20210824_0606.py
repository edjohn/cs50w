# Generated by Django 3.2.5 on 2021-08-24 06:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='listing_bids', to='auctions.listing'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_bids', to=settings.AUTH_USER_MODEL),
        ),
    ]
