# Generated by Django 2.2.5 on 2019-10-01 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_in_req_request_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='in_req',
            old_name='email',
            new_name='gmail',
        ),
    ]
