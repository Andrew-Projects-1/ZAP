# Generated by Django 4.1.1 on 2022-09-22 14:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionmodel',
            name='pub_date',
            field=models.DateTimeField(default=datetime.date.today),
        ),
    ]
