# Generated by Django 3.1.3 on 2022-01-13 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enquiry', '0011_auto_20220113_1342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enquiry',
            name='attachment',
        ),
    ]
