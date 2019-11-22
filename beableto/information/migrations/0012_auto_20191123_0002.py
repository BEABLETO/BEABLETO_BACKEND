# Generated by Django 2.2.6 on 2019-11-23 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0011_seoulelevator'),
    ]

    operations = [
        migrations.CreateModel(
            name='Elevator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line', models.IntegerField()),
                ('station', models.CharField(max_length=100)),
                ('x_axis', models.FloatField()),
                ('y_axis', models.FloatField()),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='SeoulElevator',
        ),
    ]