from django.db import models
import datetime

# Create your models here.
workerType= (
    ('insource','Insource'),
    ('outsource','Outsource'),
)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    now = datetime.datetime.now()
    date=now.strftime("%Y-%m-%d")
    return 'polls/{0}/{1}/{2}'.format(instance.worker_name.username,date, filename)

class worker(models.Model):
	name=models.CharField(max_length=50)
	name_of_supervisor=models.CharField(max_length=50)
	username=models.CharField(max_length=20,unique=True)
	password=models.CharField(max_length=100)
	worker_type=models.CharField(max_length=20,choices=workerType, default='insource')
	supervisor_link=models.ForeignKey('supervisor',default=1,on_delete=models.CASCADE)
	Account_link=models.ForeignKey('Account',default=1,on_delete=models.CASCADE)
	HR_link=models.ForeignKey('HR',default=1,on_delete=models.CASCADE)
	department=models.CharField(max_length=50)
	branch=models.CharField(max_length=50,null=True)
	def _str_(self):
		name=self.name
		return name

class petrol_detail(models.Model):
	nepali_month=models.CharField(max_length=30,null=True)
	date=models.DateField(null=True)

	worker_id=models.ForeignKey('worker',default=1,on_delete=models.CASCADE)
	request_petrol_liter=models.IntegerField(default=0)
	accepted_petrol_liter=models.IntegerField(default=0)
	request_message=models.CharField(max_length=1000,default='-')
	request_status=models.CharField(max_length=20,default='-')
	request_accept_status=models.CharField(max_length=30,default="-")
	request_date=models.DateField(null=True)
	request_accept_date=models.DateField(null=True)
	request_reject_date=models.DateField(null=True)

	bill_status=models.CharField(max_length=20,default='-')
	date_of_submit=models.DateField(null=True)
	bill_accept_status=models.CharField(max_length=30,default='-',null=True)
	bill_accept_date=models.DateField(null=True)
	bill_reject_date=models.DateField(null=True)
	petrol_liter=models.IntegerField(default=0)
	bill_month=models.IntegerField(default=1)
	HR_valid=models.CharField(max_length=20,default='-')

	paid_status=models.CharField(max_length=20,default='-',null=True)
	paid_date=models.DateField(null=True)
	total_price=models.FloatField(null=True)
	bill_paid_month=models.DateField(null=True)
	def date_month(self):
		if self.date:
			return self.date.strftime("%B")

	# def compare_date(self):
 #    	return datetime.now() > self.paid_month

class supervisor(models.Model):
	name=models.CharField(max_length=50)
	password=models.CharField(max_length=20)
	username=models.CharField(max_length=20,unique=True)
	def _str_(self):
		name=self.name
		return name


class HR(models.Model):
	username=models.CharField(max_length=50,unique=True)
	password=models.CharField(max_length=20)
	petrol_price=models.FloatField(null=True)

class Account(models.Model):
	username=models.CharField(max_length=50,unique=True)
	password=models.CharField(max_length=20)

class bill(models.Model):
	bill_image=models.ImageField(upload_to=user_directory_path,blank=True)
	worker_name=models.ForeignKey('worker',default=1,on_delete=models.CASCADE)
	date=models.DateField(null=True)
	def _str_(self):
		return str(bill_image)