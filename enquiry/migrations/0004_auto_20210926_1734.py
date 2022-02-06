# Generated by Django 3.1.3 on 2021-09-26 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enquiry', '0003_enquiry_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='address',
            field=models.CharField(default='No address', max_length=150),
        ),
        migrations.AddField(
            model_name='enquiry',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='description',
            field=models.TextField(default='No description', null=True),
        ),
    ]
