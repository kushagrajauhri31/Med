from django.contrib import admin
from .models import FeedBack, TestDetails,Appointment,Contact,Order,Cart,report_file,Report

# Register your models here.
admin.site.register(TestDetails)
admin.site.register(FeedBack)
# admin.site.register(Job)
# admin.site.register(Health_Campaign)
admin.site.register(Appointment)
admin.site.register(Contact)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(report_file)
admin.site.register(Report)



