# Generated by Django 3.0 on 2019-12-20 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0013_auto_20191220_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='in_req',
            name='branch',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='in_req',
            name='req_acceped_by',
            field=models.CharField(max_length=320),
        ),
        migrations.AlterField(
            model_name='in_req',
            name='year',
            field=models.CharField(max_length=2),
        ),
    ]
