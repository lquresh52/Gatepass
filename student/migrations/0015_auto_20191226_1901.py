# Generated by Django 3.0 on 2019-12-26 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0014_auto_20191220_2303'),
    ]

    operations = [
        migrations.AddField(
            model_name='in_req',
            name='first_name',
            field=models.CharField(default='a', max_length=200),
        ),
        migrations.AddField(
            model_name='in_req',
            name='last_name',
            field=models.CharField(default='a', max_length=200),
        ),
    ]
