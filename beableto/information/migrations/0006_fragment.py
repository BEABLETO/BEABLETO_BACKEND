# Generated by Django 2.2.6 on 2019-11-06 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0005_road'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fragment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_x', models.FloatField()),
                ('start_y', models.FloatField()),
                ('end_x', models.FloatField()),
                ('end_y', models.FloatField()),
                ('middle_x', models.FloatField()),
                ('middle_y', models.FloatField()),
            ],
        ),
    ]