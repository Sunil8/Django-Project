# Generated by Django 2.2 on 2019-06-19 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_petrol_detail_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petrol_detail',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
