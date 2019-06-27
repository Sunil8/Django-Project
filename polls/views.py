from django.shortcuts import render,redirect
from .forms import loginForm, bill_submit, employForm,modify_request,modify_bill
from .models import worker,HR,supervisor,Account,bill,petrol_detail
from django.http import HttpResponse
from django.contrib import messages
import datetime
from datetime import datetime
import xlwt



# Create your views here.
def index(request):
	return render(request,'polls/index.html')

def worker_login(request):
	if request.method == 'POST':
	#will handle the request 
		# form=loginForm(request.POST)
			name=request.POST['username']
			password=request.POST['password']
			if worker.objects.filter(username=name).exists():
				user=worker.objects.get(username=name)
				if password==user.password:
					request.session[user.username]=user.username
					return redirect('employ_login',pk=user.id)
				else:
					messages.error(request,'Password not correct')
					return redirect('worker_redirect')
			else:
				messages.error(request,'Username not correct')
				return redirect('worker_redirect')
	else:
	#creating a new form
	#returning form 
		form=loginForm()
		return render(request,'polls/login.html',{'form':form})

def employee_login(request,pk):
	employee=worker.objects.get(id=pk)
	today=datetime.now()
	try:
		name=request.session[employee.username]
		if name in employee.username:
			try:
				# return HttpResponse(pk)
				pet=petrol_detail.objects.get(date__month=today.month,worker_id=employee)
				# return HttpResponse(pk)
			except:
				# return HttpResponse(pk)
				pet=petrol_detail.objects.create(worker_id=employee,date=today)
				# return HttpResponse(pk)
				# pet.save()
			# return HttpResponse(pet.request_accept_status)
			return render(request, 'polls/employee.html',{'data':employee,'data2':pet})
		else:
			messages.error(request,"please login first..")
			return redirect('worker_redirect')
	except:
		messages.error(request,"please login first..")
		return redirect('worker_redirect')

def employ(request,pk):
	employee=worker.objects.get(id=pk)
	today=datetime.now()
	if request.method == 'POST':
		pet=petrol_detail.objects.get(date__month=today.month,worker_id=employee)
		pet.request_message=request.POST['reason']
		pet.request_petrol_liter=request.POST['request']
		pet.request_date=datetime.now()
		pet.request_status='yes'
		pet.request_accept_status='-'
		pet.bill_status='-'
		pet.bill_accept_status='-'
		pet.paid_status='-'
		# return HttpResponse(employee.name)
		pet.save()
		messages.success(request,'YOUR REQUEST HAS BEEN SUBMITTED')
		return redirect('employ_login',pk=pk)
	else:
		try:
			if employee.username in request.session[employee.username]:
				form = employForm()
				return render(request, 'polls/employ.html', {'form': form})
		# 	return HttpResponse(request.session[employee.username])
		except:
			messages.error(request,'please login first..')
			return redirect('worker_redirect')

def submit_bill(request,pk):
	user=worker.objects.get(id=pk)
	hr=HR.objects.get(id=1)
	today=datetime.now()
	pet=petrol_detail.objects.get(worker_id=user,date__month=today.month)
	if request.method=='POST':
		form=bill_submit(request.POST,request.FILES)
		if form.is_valid():
			pet.petrol_liter=request.POST['petrol']
			pet.date_of_submit=datetime.now()
			pet.bill_status='yes'
			pet.bill_accept_status='no'
			pet.bill_month=request.POST['month']
			pet.bill_paid_month=form.cleaned_data.get('bill_month')
			pet.nepali_month=form.cleaned_data.get(' nepali_month')
			pet.save()
			pet.total_price=float(pet.petrol_liter)*hr.petrol_price*float(pet.bill_month)
			pet.save()
			for fields in request.FILES.keys():
				for formFile in request.FILES.getlist(fields):
					image=bill.objects.create(worker_name=user,bill_image=formFile,date=datetime.now())
				messages.success(request, 'YOUR BILL HAS BEEN SUBMITTED')
				request.session[user.username]=user.username
				return redirect('employ_login',pk=pk)
	else:
		try:
			name=request.session[user.username]
			if name in user.username:
				del request.session[user.username]
				request.session[user.username]=user.username
				form = bill_submit()
				# return HttpResponse(pet.date)
				return render(request, 'polls/bill_submit.html',{'data':user,'form': form,'data2':pet})
			else:
				messages.error(request,'please login first..')
				return redirect('worker_redirect')
		except:
			messages.error(request,'please login first..')
			return redirect('worker_redirect')

def supervisor_login(request):
	if request.method == 'POST':
	#will handle the request 
		# form=loginForm(request.POST)
		name=request.POST['username']
		password=request.POST['password']
		if supervisor.objects.filter(username=name).exists():
			user=supervisor.objects.get(username=name)
			if password==user.password:
				# employee=worker.objects.all().filter(supervisor_link=user)
				request.session[user.username]=user.username
				# return render(request, 'polls/supervisor.html',{'data':employee})
				return redirect('supervisorLogin',pk=user.id)
			else:
				messages.error(request,'Password not correct')
				return redirect('supervisor_redirect')
		else:
			messages.error(request,'Username not correct')
			return redirect('supervisor_redirect')
			# return HttpResponse('wrong form')
	else:
	#creating a new form
	#returning form 
		form=loginForm()
		return render(request,'polls/login.html',{'form':form})

def supervisorLogin(request,pk):
	user=supervisor.objects.get(id=pk)
	today=datetime.now()
	if request.method =='POST': # If the form is submitted
		search_query = request.POST['Search']
		if worker.objects.filter(name=search_query).exists():
			# employee=worker.objects.filter(name=search_query)
			pet=petrol_detail.objects.filter(date__month=today.month,worker_id__name=search_query)
			return render(request, 'polls/supervisor.html',{'pk':pk,'data2':pet})
		elif worker.objects.filter(branch=search_query).exists():
			pet=petrol_detail.objects.filter(worker_id__branch=search_query,date__month=today.month)
			return render(request, 'polls/supervisor.html',{'data2':pet})
		elif worker.objects.filter(department=search_query).exists():
			pet=petrol_detail.objects.filter(worker_id__department=search_query,date__month=today.month)
			return render(request, 'polls/supervisor.html',{'data2':pet})
		else:
			messages.error(request,'Result not found.Please type correctly...')
			# employee=worker.objects.all()
			return redirect('supervisorLogin',pk=user.id)
	else:
		try:
			name=request.session[user.username]
			employee=worker.objects.filter(supervisor_link=user)

			for data in employee:
				try:
					petrol_detail.objects.get(worker_id=data,date__month=today.month)
				except:
					petrol_detail.objects.create(worker_id=data,date=today)
			pet=petrol_detail.objects.filter(date__month=today.month,worker_id__supervisor_link=user)
			return render(request,'polls/supervisor.html',{'data':employee,'data2':pet,'pk':pk})
		except:
			messages.error(request,"please login first..")
			return redirect('supervisor_redirect')

def Supervisor_detail(request,pk,value):
	employee=worker.objects.get(id=value)
	today=datetime.now()
	pet=petrol_detail.objects.get(worker_id=employee,date__month=today.month)
	user=supervisor.objects.get(id=pk)
	if request.method=='POST':
		if 'accept' in request.POST:
			pet.request_status='no'
			pet.accepted_petrol_liter=pet.request_petrol_liter
			pet.request_petrol_liter='0'
			pet.request_accept_status='yes'
			pet.request_accept_date=datetime.now()
			# employee.bill_accept_date=datetime.now()
			pet.save()
			messages.info(request,'Bill reqeust for {0} has been accepted..'.format(employee.name))
		if 'reject' in request.POST:
			pet.request_status='no'
			pet.request_petrol_liter='0'
			pet.request_accept_status='rejected'
			pet.request_reject_date=datetime.now()
			pet.accepted_petrol_liter='0'
			pet.save()
			messages.info(request,'Bill reqeust for {0} has been rejected..'.format(employee.name))
		if 'modify' in request.POST:
			request.session['modify']='modify'
			return redirect('request_modify',pk=pk,value=value)
		# employ=worker.objects.all().filter(supervisor_link=employee.supervisor_link)
		return redirect('supervisorLogin',pk=pk)
	else:
		try:
			# name=request.session[user.name]
			if request.session[user.username] in user.username:
				return render(request, 'polls/Supervisor_detail.html',{'data':employee,'pk':pk,'value':value,'data2':pet})
			else:
				messages.error(request,'please login first..')
				return redirect('supervisor_redirect')
		except:
			messages.error(request,'please login first..')
			return redirect('supervisor_redirect')

def request_modify(request,pk,value):
	employee=worker.objects.get(id=value)
	user=supervisor.objects.get(id=pk)
	today=datetime.now()
	req=petrol_detail.objects.get(worker_id=value,date__month=today.month)
	if request.method=='POST':
		req.accepted_petrol_liter=request.POST['petrol']
		req.request_status='no'
		req.request_petrol_liter='0'
		req.request_accept_status='yes'
		req.request_accept_date=datetime.now()
		req.save()
		messages.info(request,'Bill request for {0} has been modified..'.format(employee.name))
		return redirect('supervisorLogin',pk=pk)
	else:
		try:
			if user.username in request.session[user.username]:
				form=modify_request()
				return render(request,'polls/modify_request.html',{'form':form,'data':employee,'data2':req})
		except:
			messages.error(request,'Please login first...')
			return redirect('supervisor_redirect')

def HR_login(request):
	today=datetime.now()
	if request.method == 'POST':
	#will handle the request 
		# form=loginForm(request.POST)
		if 'modify' in request.POST:
			try:
				user=HR.objects.get(id=1)
				name=request.session.get(user.username)
				data =request.POST['petrol']
				user.petrol_price=request.POST['petrol']
				user.save()
				return render(request, 'polls/hr.html',{'data':user})
			except:
				messages.error(request,'Please fill the rate input box...')
				return render(request,'polls/hr.html')

		if 'login' in request.POST:
			name=request.POST['username']
			password=request.POST['password']
			if HR.objects.filter(username=name).exists():
				user=HR.objects.get(username=name)
				if password==user.password:
					request.session[user.username]=user.username
					employee=worker.objects.all()
					for employ in employee:
						try:
							petrol_detail.objects.get(worker_id=employ,date__month=today.month)
						except:
							petrol_detail.objects.create(worker_id=employ,date=today)
					return render(request, 'polls/hr.html',{'data':user})
				else:
					messages.error(request,'Password not correct')
					return redirect('HR_redirect')
			else:
				messages.error(request,'Username not correct')
				return redirect('HR_redirect')
				# return HttpResponse('wrong form')
	else:
	#creating a new form
	#returning form 
		form=loginForm()
		return render(request,'polls/login.html',{'form':form})

def bill_request(request):
	today=datetime.now()
	user=HR.objects.get(id=1)
	if request.method =='POST': # If the form is submitted
		search_query = request.POST['Search']
		if worker.objects.filter(name=search_query).exists():
			if petrol_detail.objects.filter(worker_id__name=search_query,request_accept_status='yes',date__month=today.month).exists():
				data=petrol_detail.objects.filter(worker_id__name=search_query,request_accept_status='yes',date__month=today.month)
				return render(request, 'polls/bill_request.html',{'data2':data})
			else:
				messages.error(request,'No any employee with name {0} have request accepted...'.format(search_query))
				return redirect('bill_request')
		elif worker.objects.filter(branch=search_query).exists():
			pet=petrol_detail.objects.filter(worker_id__branch=search_query,date__month=today.month)
			return render(request, 'polls/bill_request.html',{'data2':pet})
		elif worker.objects.filter(department=search_query).exists():
			pet=petrol_detail.objects.filter(worker_id__department=search_query,date__month=today.month)
			return render(request, 'polls/bill_request.html',{'data2':pet})
		else:
			messages.error(request,'Result not found.Please type correctly...')
			return redirect('bill_request')
	else:
		try:
			if user.username in request.session[user.username]:
				if petrol_detail.objects.filter(request_accept_status='yes',date__month=today.month).exists():
					pet=petrol_detail.objects.filter(request_accept_status='yes',date__month=today.month)
					employee=worker.objects.all()
					return render(request,'polls/bill_request.html',{'data':employee,'data2':pet})
				else:
					messages.info(request,'No any employee have their petrol request accepted...')
					return render(request,'polls/bill_request.html')
		except:
			messages.error(request,'Please login first..')
			return redirect('HR_redirect')

def bill_upload(request):
	today=datetime.now()
	user=HR.objects.get(id=1)
	if request.method =='POST': # If the form is submitted
		search_query = request.POST['Search']
		if worker.objects.filter(name=search_query).exists():
			# employee=worker.objects.filter(name=search_query)
			pet=petrol_detail.objects.filter(worker_id__name=search_query,date__month=today.month)
			return render(request, 'polls/bill_upload.html',{'data2':pet})
		elif worker.objects.filter(branch=search_query).exists():
			pet=petrol_detail.objects.filter(worker_id__branch=search_query,date__month=today.month)
			return render(request, 'polls/bill_upload.html',{'data2':pet})
		elif worker.objects.filter(department=search_query).exists():
			pet=petrol_detail.objects.filter(worker_id__department=search_query,date__month=today.month)
			return render(request, 'polls/bill_upload.html',{'data2':pet})
		else:
			messages.error(request,'Result not found.Please type correctly...')
			return redirect('bill_upload')
	else:
		try:
			if user.username in request.session[user.username]:
				employee=worker.objects.all()
				pet=petrol_detail.objects.filter(date__month=today.month)
				return render(request,'polls/bill_upload.html',{'data':employee,'data2':pet})
		except:
			messages.error(request,'Please login first..')
			return redirect('HR_redirect')


def hr_detail(request,value):
	employee=worker.objects.get(id=value)
	hr=HR.objects.get(id=1)
	today=datetime.now()
	pet=petrol_detail.objects.get(worker_id=employee,date__month=today.month)
	if request.method=='POST':
		if 'accept' in request.POST:
			pet.paid_status='no'
			pet.HR_valid='yes'
			pet.bill_status='no'
			pet.bill_accept_status='yes'
			pet.bill_accept_date=datetime.now()
			pet.save()
			messages.success(request,'Petrol bill for {0} has been accepted..'.format(employee.name))
			# return redirect('bill_upload')
		if 'reject' in request.POST:
			pet.HR_valid='no'
			pet.bill_status='-'
			pet.bill_accept_status='rejected'
			pet.paid_status='-'
			pet.bill_reject_date=datetime.now()
			pet.save()
			messages.success(request,'Petrol bill for {0} has been rejected..'.format(employee.name))
			# return redirect('bill_upload'	
		return redirect('bill_upload')
	else:
		try:
			if hr.username in request.session[hr.username]:
				return render(request,'polls/hr_detail.html',{'data':employee,'data2':pet})
		except:
			messages.error(request,'please login first..')
			return redirect('HR_redirect')

def account_login(request):
	today=datetime.now()
	if request.method == 'POST':
	#will handle the request 
		# form=loginForm(request.POST)
		name=request.POST['username']
		password=request.POST['password']
		if Account.objects.filter(username=name).exists():
			user=Account.objects.get(username=name)
			if password==user.password:
				request.session[user.username]=user.username
				employee=worker.objects.all()
				for employ in employee:
					try:
						petrol_detail.objects.get(worker_id=employ,date__month=today.month)
					except:
						petrol_detail.objects.create(worker_id=employ,date=today)
				return redirect('account_employee')
			else:
				messages.error(request,'Password not correct')
				return redirect('account_redirect')
		else:
			messages.error(request,'Username not correct')
			return redirect('account_redirect')
			# return HttpResponse('wrong form')
	else:
	#creating a new form
	#returning form 
		form=loginForm()
		return render(request,'polls/login.html',{'form':form})

def account_employee_detail(request):
	today=datetime.now()
	user=Account.objects.get(id=1)
	if request.method =='POST': # If the form is submitted
		search_query = request.POST['Search']
		# return HttpResponse(search_query)
		if worker.objects.filter(name=search_query).exists():
			# employee=worker.objects.filter(name=search_query)
			pet=petrol_detail.objects.filter(worker_id__name=search_query,date__month=today.month)
			return render(request, 'polls/account.html',{'data2':pet})
		elif worker.objects.filter(branch=search_query).exists():
			pet=petrol_detail.objects.filter(worker_id__branch=search_query,date__month=today.month)
			return render(request, 'polls/account.html',{'data2':pet})
		elif worker.objects.filter(department=search_query).exists():
			pet=petrol_detail.objects.filter(worker_id__department=search_query,date__month=today.month)
			return render(request, 'polls/account.html',{'data2':pet})
		else:
			messages.error(request,'Result not found.Please type correctly...')
			return redirect('account_employee')
	else:
		try:
			if user.username in request.session[user.username]:
				employee=worker.objects.all()
				pet=petrol_detail.objects.filter(date__month=today.month)
				return render(request, 'polls/account.html',{'data':employee,'data2':pet})
		except:
			messages.error(request,'Please login first..')
			return redirect('account_redirect')


def account_detail(request,value):
	employee=worker.objects.get(id=value)
	today=datetime.now()
	user=Account.objects.get(id=1)
	pet=petrol_detail.objects.get(worker_id=employee,date__month=today.month)
	if request.method=="POST":
		pet.paid_status='yes'
		pet.paid_date=datetime.now()
		pet.save()
		messages.success(request,'Bill for Employ: {0} has been paid..'.format(employee.name))
		request.session['account']='account'
		return redirect('account_employee')
	else:
		try:
			if user.username in request.session[user.username]:
				return render(request,'polls/account_detail.html',{'data':employee,'data2':pet})
		except:
			messages.error(request,'please login first..')
			return redirect('account_redirect')


def bill_image(request,value):
	employee=worker.objects.get(id=value)
	today=datetime.now()
	pet=petrol_detail.objects.get(worker_id=employee,date__month=today.month)
	images=bill.objects.filter(worker_name=employee,date=pet.date_of_submit)
	return render(request,'polls/bill_image.html',{'data':employee,'source':images})
	

def modify_petrol(request):
	try:
		if request.method=="POST":
			if data in request.POST['petrol']:
				user=HR.objects.get(id=1)
				user.petrol_price=request.POST['petrol']
				return render(request, 'polls/hr.html')
			else:
				messages.error(request,'Please fill the rate input box...')
				return render(request,'polls/hr.html')
	except:
		messages.error(request,'Please fill the rate input box...')
		return render(request,'polls/hr.html')

def bill_modify(request,value):
	employee=worker.objects.get(id=value)
	today=datetime.now()
	pet=petrol_detail.objects.get(worker_id=value,date__month=today.month)
	hr=HR.objects.get(id=1)
	if request.method=='POST':
		form=modify_bill(request.POST,request.FILES)
		if form.is_valid():
			pet.paid_status='no'
			pet.HR_valid='yes'
			pet.bill_status='no'
			pet.bill_accept_status='yes'
			pet.date_of_submit=datetime.now()
			pet.petrol_liter=request.POST['petrol']
			pet.save()
			pet.bill_paid_month=form.cleaned_data.get('bill_month')
			pet.bill_month=request.POST['month']
			# return HttpResponse(hr.petrol_price)
			# employee.total_price=employee.petrol_liter*hr.petrol_price*employee.bill_month
			pet.save()
			# return HttpResponse(employee.bill_month)
			pet.total_price=float(pet.petrol_liter)*hr.petrol_price*float(pet.bill_month)
			pet.save()
			for fields in request.FILES.keys():
				for formFile in request.FILES.getlist(fields):
					image=bill.objects.create(worker_name=employee,bill_image=formFile,date=datetime.now())
				messages.success(request, 'BILL of {0} HAS BEEN ACCEPTED'.format(employee.name))
				return redirect('bill_request')
	else:
		try:
			if hr.username in request.session[hr.username]:
				form=modify_bill()
				return render(request,'polls/bill_modify.html',{'data':employee,'form':form,'data2':pet})
		except:
			messages.error(request,'Please login first...')
			return redirect('HR_redirect')


def download_excel_data(request):
	today=datetime.now()
	# content-type of response
	response = HttpResponse(content_type='application/ms-excel')

	#decide file name
	response['Content-Disposition'] = 'attachment; filename="Excel Format For Fule Allowance.xls"'

	#creating workbook
	wb = xlwt.Workbook(encoding='utf-8')

	#adding sheet
	ws = wb.add_sheet("sheet1")

	# Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	# headers are bold
	font_style.font.bold = True

	#column header names, you can use your own headers here
	columns = ['S.N', 'Employee ID', 'Employee Name', 'Department','Rate/Perliter','Petrol Exp','Actual Payment','Grand Total','Months','Remarks' ]

	#write column headers in sheet
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	# Sheet body, remaining rows
	font_style = xlwt.XFStyle()

	#get your data, from database or from a text file...
	data = petrol_detail.objects.filter(date__month=today.month) #dummy method to fetch data.
	for my_row in data:
		row_num = row_num + 1
		ws.write(row_num, 0, row_num, font_style)
		ws.write(row_num, 1, my_row.worker_id.id, font_style)
		ws.write(row_num, 2, my_row.worker_id.name, font_style)
		ws.write(row_num, 3, my_row.worker_id.department, font_style)
		ws.write(row_num, 4, my_row.worker_id.HR_link.petrol_price, font_style)
		ws.write(row_num, 5, my_row.total_price, font_style)
		ws.write(row_num, 6, my_row.total_price, font_style)
		ws.write(row_num, 7, my_row.total_price, font_style)
		ws.write(row_num, 8, my_row.nepali_month, font_style)
		ws.write(row_num, 9,'-', font_style)
	
	wb.save(response)
	return response