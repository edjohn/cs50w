# Generated by Django 3.2.7 on 2021-10-14 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(default='Anonymous', max_length=100)),
                ('description', models.CharField(max_length=4000)),
                ('stars', models.IntegerField(default=5)),
            ],
        ),
    ]