# Generated by Django 2.1.1 on 2018-10-08 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radiusadmin', '0003_radcheck_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='radcheck',
            name='mac_address',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='radcheck',
            name='phone_number',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
