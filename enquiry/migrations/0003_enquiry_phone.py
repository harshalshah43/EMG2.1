# Generated by Django 3.1.3 on 2021-09-26 11:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enquiry', '0002_auto_20210926_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='phone',
            field=models.CharField(default=None, max_length=10, null=True, validators=[django.core.validators.RegexValidator(message='Phone no must be entered in format: Up to 10 digits allowed.', regex='^\\ ?1?\\d{9,15}$')]),
        ),
    ]