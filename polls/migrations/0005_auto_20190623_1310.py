# Generated by Django 2.2 on 2019-06-23 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20190619_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petrol_detail',
            name='HR_valid',
            field=models.CharField(default='-', max_length=20),
        ),
        migrations.AlterField(
            model_name='petrol_detail',
            name='bill_status',
            field=models.CharField(default='-', max_length=20),
        ),
        migrations.AlterField(
            model_name='petrol_detail',
            name='paid_status',
            field=models.CharField(default='-', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='petrol_detail',
            name='request_accept_status',
            field=models.CharField(default='-', max_length=30),
        ),
    ]
