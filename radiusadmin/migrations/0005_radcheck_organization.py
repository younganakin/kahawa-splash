# Generated by Django 2.1.1 on 2018-10-08 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radiusadmin', '0004_auto_20181008_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='radcheck',
            name='organization',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
