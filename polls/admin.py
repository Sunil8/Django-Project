from django.contrib import admin

# Register your models here.
from .models import worker,bill,supervisor,Account,HR

admin.site.register(worker)
admin.site.register(bill)
admin.site.register(supervisor)
admin.site.register(Account)
admin.site.register(HR)