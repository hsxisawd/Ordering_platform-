# Generated by Django 2.2.12 on 2022-03-24 09:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0002_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_id', models.IntegerField()),
                ('category_id', models.IntegerField()),
                ('cover_pic', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('status', models.IntegerField(default=1)),
                ('create_at', models.DateTimeField(default=datetime.datetime.now)),
                ('update_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'product',
            },
        ),
    ]