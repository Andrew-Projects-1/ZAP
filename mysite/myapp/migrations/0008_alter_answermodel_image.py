# Generated by Django 4.1.1 on 2022-10-13 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_answermodel_image_answermodel_image_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answermodel',
            name='image',
            field=models.ImageField(max_length=144, null=True, upload_to='uploads/answers/%Y/%m/%d/'),
        ),
    ]