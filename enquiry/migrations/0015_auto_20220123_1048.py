# Generated by Django 3.1.3 on 2022-01-23 05:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('enquiry', '0014_auto_20220113_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquiry',
            name='date_posted',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
