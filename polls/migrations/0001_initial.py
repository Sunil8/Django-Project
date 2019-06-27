# Generated by Django 2.2 on 2019-06-17 06:35

from django.db import migrations, models
import django.db.models.deletion
import polls.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='HR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('petrol_price', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='supervisor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='worker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('name_of_supervisor', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('worker_type', models.CharField(choices=[('insource', 'Insource'), ('outsource', 'Outsource')], default='insource', max_length=20)),
                ('department', models.CharField(max_length=50)),
                ('Account_link', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='polls.Account')),
                ('HR_link', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='polls.HR')),
                ('supervisor_link', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='polls.supervisor')),
            ],
        ),
        migrations.CreateModel(
            name='petrol_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_petrol_liter', models.IntegerField(default=0)),
                ('accepted_petrol_liter', models.IntegerField(default=0)),
                ('request_message', models.CharField(default='-', max_length=1000)),
                ('request_status', models.CharField(default='-', max_length=20)),
                ('request_accept_status', models.CharField(default='', max_length=30)),
                ('request_date', models.DateField(null=True)),
                ('request_accept_date', models.DateField(null=True)),
                ('request_reject_date', models.DateField(null=True)),
                ('bill_status', models.CharField(default='no', max_length=20)),
                ('date_of_submit', models.DateField(null=True)),
                ('bill_accept_status', models.CharField(default='-', max_length=30, null=True)),
                ('bill_accept_date', models.DateField(null=True)),
                ('bill_reject_date', models.DateField(null=True)),
                ('petrol_liter', models.IntegerField(default=0)),
                ('bill_month', models.IntegerField(default=1)),
                ('HR_valid', models.CharField(default='no', max_length=20)),
                ('paid_status', models.CharField(default=None, max_length=20, null=True)),
                ('paid_date', models.DateField(null=True)),
                ('total_price', models.FloatField(null=True)),
                ('bill_paid_month', models.DateField(null=True)),
                ('worker_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='polls.worker')),
            ],
        ),
        migrations.CreateModel(
            name='bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_image', models.ImageField(blank=True, upload_to=polls.models.user_directory_path)),
                ('date', models.DateField(null=True)),
                ('worker_name', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='polls.worker')),
            ],
        ),
    ]
