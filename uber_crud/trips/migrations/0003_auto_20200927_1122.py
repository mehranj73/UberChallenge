# Generated by Django 3.1.1 on 2020-09-27 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0002_auto_20200927_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='status',
            field=models.CharField(choices=[('CO', 'COMPLETED'), ('IP', 'IN_PROGRESS'), ('RQ', 'REQUESTED'), ('AC', 'ACCEPTED')], default='RQ', max_length=20),
        ),
    ]