# Generated by Django 3.1.1 on 2020-09-29 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200918_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.FileField(blank=True, null=True, upload_to='my_images'),
        ),
    ]
