from django.conf.urls import url,include
from . import views
from django.conf import settings
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$',views.index),
    url(r'^employee/$',views.worker_login,name='worker_redirect'),
    url(r'^employee/(?P<pk>\d+)/$',views.employee_login,name='employ_login'),
    url(r'^supervisor/$',views.supervisor_login,name='supervisor_redirect'),
    url(r'^supervisor/(?P<pk>\d+)/$',views.supervisorLogin,name='supervisorLogin'),
    url(r'^HR/$',views.HR_login,name='HR_redirect'),
    url(r'^account/$',views.account_login,name='account_redirect'),
    url(r'^account/employee_detail/$',views.account_employee_detail,name='account_employee'),
    url(r'^employee/(?P<pk>\d+)/request_for_petrol/$', views.employ, name='employ'),
    url(r'^employee/(?P<pk>\d+)/bill_submit/$', views.submit_bill, name='bill_submit'),
    url(r'^supervisor/(?P<pk>(\d+))/(?P<value>(\d+))/$',views.Supervisor_detail, name='Supervisor_detail'),
    url(r'^supervisor/(?P<pk>(\d+))/(?P<value>(\d+))/modify/$',views.request_modify, name='request_modify'),
    url(r'^HR/bill_request/$', views.bill_request, name='bill_request'),
    url(r'^HR/bill_request/(?P<value>\d+)/$', views.bill_modify, name='bill_modify'),
    url(r'^HR/bill_upload/$', views.bill_upload, name="bill_upload"),
    url(r'^HR/bill_upload/hr_detail/(?P<value>\d+)/$', views.hr_detail, name='hr_detail'),
    url(r'^account/employee_detail/account_detail/(?P<value>\d+)/$', views.account_detail, name='account_detail'),
    url(r'^account/employee_detail/account_detail/(?P<value>\d+)/bill_image/$',views.bill_image, name='account_bill_image'),
    url(r'^HR/bill_upload/hr_detail/(?P<value>\d+)/bill_image/$',views.bill_image, name='hr_bill_image'),
    url(r'^HR/modify_petrol/$',views.modify_petrol,name='modify_petrol'),
    url(r'^excel/$',views.download_excel_data,name="excelsheet"),
]