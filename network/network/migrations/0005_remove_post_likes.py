# Generated by Django 3.2.5 on 2021-09-30 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_alter_followerrelation_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]
