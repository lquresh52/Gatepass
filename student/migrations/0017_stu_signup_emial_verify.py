# Generated by Django 3.0 on 2020-01-12 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0016_stu_signup_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='stu_signup',
            name='emial_verify',
            field=models.CharField(default='accepted', max_length=10),
            preserve_default=False,
        ),
    ]