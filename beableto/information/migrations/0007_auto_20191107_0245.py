# Generated by Django 2.2.6 on 2019-11-06 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0006_fragment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='road',
            name='road',
            field=models.CharField(max_length=5000),
        ),
    ]