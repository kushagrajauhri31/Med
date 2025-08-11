from django.urls import path,include
from .import views

urlpatterns = [
    path("",views.home,name="home"),
    path("test_details/",views.test_details,name="test_details"),
    path("feedback/",views.feedback,name="feedback"),
    path("ambulance/",views.ambulance,name="ambulance"),
    path("doctors/",views.doctors,name="doctors"),
    path("contactus/",views.contactus,name="contact"),
    path("appointment/",views.appointment,name="appointment"),
    path("upload_csv_report/",views.upload_csv_report,name="upload_csv_report"),
    

    
    
]
