# Generated by Django 2.2.9 on 2020-11-04 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='isOpen',
            field=models.BooleanField(default=True),
        ),
    ]
