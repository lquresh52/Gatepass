# Generated by Django 2.2.5 on 2019-09-29 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='stu_signup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid', models.CharField(max_length=8)),
                ('username', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('mobile_no', models.BigIntegerField()),
                ('year', models.CharField(max_length=2)),
                ('branch', models.CharField(max_length=100)),
                ('roll_no', models.IntegerField()),
                ('gfm', models.CharField(max_length=200)),
                ('icard_img', models.ImageField(upload_to='profile_img')),
                ('user_img', models.ImageField(upload_to='profile_img')),
            ],
        ),
    ]
