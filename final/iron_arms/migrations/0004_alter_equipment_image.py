# Generated by Django 3.2.7 on 2021-10-21 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iron_arms', '0003_alter_equipment_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='image',
            field=models.ImageField(upload_to='static/iron_arms/images/equipment'),
        ),
    ]