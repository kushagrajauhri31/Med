import csv
from django.shortcuts import get_object_or_404, render,HttpResponse

from .models import FeedBack, TestDetails,Contact,Appointment,Report,report_file
from django.contrib import messages
from django.http import HttpResponseRedirect


# Create your views here.
def home(request):
    return render(request,'pathology/html/home.html')

def test_details(request):
    testdetail_objects=TestDetails.objects.all()    
    testdetail_dict={
        "testdetail_key":testdetail_objects
    }

    return render(request,'pathology/html/Test_Details.html',testdetail_dict)


def feedback(request):
    if request.method=="POST":
        name=request.POST["txtname"]
        email=request.POST["txtemail"]
        feedback=request.POST["txtfeedback"]
        rating=request.POST["cmbrating"]

        f=FeedBack(Name=name,Email=email,Feedbacktext=feedback,Rating=rating)
        f.save()
        print("feedback saved successfully")
        messages.success(request,"Thank you for your feedback")
        return render(request,'pathology/html/feedback.html')


    return render(request,'pathology/html/feedback.html')    





def ambulance(request):
    return render(request,'pathology/html/ambulance.html')    


def doctors(request):
    return render(request,'pathology/html/doctors.html')


def appointment(request):
    if request.method=="GET":
        testdetail_obj=TestDetails.objects.all()    
        testdetail_dict={
            "testdetail_key":testdetail_obj
             }
        return render(request,'pathology/html/appointment.html',testdetail_dict)


    if request.method =="POST":
        user_name= request.POST["username"]            
        user_email= request.POST["useremail"]
        user_phone= request.POST["userphone"]  
        user_test= request.POST["cmb_tname"]
        
        user_adate=request.POST["usertime"]

        if len(user_phone)>10 or len(user_phone)<10 or int(user_phone)<0:
            messages.error(request,"Please enter a valid phone number")
            return render(request,'pathology/html/appointment.html')

        user_test = get_object_or_404(TestDetails, Test_name=user_test)

        a=Appointment(Name=user_name,Phone=user_phone,Email=user_email,Test_Name=user_test,Date=user_adate) #object creation
        a.save()    
        messages.success(request,"Appointment booked successfully.")
        return render(request,'pathology/html/appointment.html')
        
            
            
def contactus(request):
    if request.method=="GET":
        return render(request,'pathology/html/contact.html')


    if request.method =="POST":
        user_name= request.POST["txtname"]  #request.POST.get("txtname")    can  also be used          
        user_email= request.POST["txtemail"]
        user_phone= request.POST["txtphone"]  #request.POST is dictionary and control names are keys here
        user_query= request.POST["txtquery"]

        if len(user_phone)>10 or len(user_phone)<10 or int(user_phone)<0:
          messages.error(request,"Please enter a valid phone number")
          return render(request,'pathology/html/contact.html')

        else:
          c=Contact(Name=user_name,Email=user_email,Phone=user_phone,Your_Query=user_query) #object creation
          c.save()    ###ORM concept  and it will store data into contact table using ORM
          print("Contact saved successfully")
          messages.success(request,"Thankyou for contacting us, we will reach you soon.")
          return render(request,'pathology/html/contact.html')        




def upload_csv_report(request, report_id):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        # Process the CSV file (you may need to adjust this based on your CSV structure)
        csv_data = csv.reader(csv_file)
        for row in csv_data:
            # Assume the CSV has a column 'file_path' containing file paths of PDFs
            file_path = row[0]
            report_file = report_file(report=Report.objects.get(report_id=report_id), file_content=file_path)
            report_file.save()

        return HttpResponseRedirect('/success/')

    return render(request, 'pathology/html/upload_csv.html') 






        
