# Generated by Django 3.0 on 2020-01-12 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0017_stu_signup_emial_verify'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stu_signup',
            old_name='emial_verify',
            new_name='email_verify',
        ),
    ]
