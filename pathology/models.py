from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



# Create your models here.
class TestDetails(models.Model):
    id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    Test_name=models.CharField(max_length=100)
    Charge=models.IntegerField()
    test_img=models.FileField(upload_to="media/TestDetails",default="default\sample_testImg.jpg")
    Test_Condition=models.CharField(max_length=100,null=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)



class FeedBack(models.Model):
    Name=models.CharField(max_length=45,null=False)   
    Email=models.CharField(max_length=45,null=False)
    Feedbacktext=models.TextField(null=False)
    Rating=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


# class Job(models.Model):
#     PostName=models.CharField(max_length=50,null=False)    
#     NoOfSeats=models.IntegerField(null=False)
#     Lastdatetoapply=models.DateField(default=timezone.now)
#     Postdate=models.DateField(default=timezone.now)
#     Description=models.TextField()
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)



# class Health_Campaign(models.Model):
#     Campaign_Name=models.CharField(max_length=100,null=False)
#     Organizer_Name=models.CharField(max_length=50,null=False)
#     Venue=models.CharField(max_length=50,null=False)
#     Description=models.CharField(max_length=200,null=False)
#     Event_pic=models.FileField(max_length=100,upload_to="pathology/picture",default="")
#     Date=models.DateField(default=timezone.now)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)



class Contact(models.Model):
    Name=models.CharField(max_length=50,null=False)
    Email=models.EmailField(max_length=100,null=True)
    Phone=models.IntegerField(null=False)
    Your_Query=models.TextField(max_length=500,null=False)
    Date=models.DateField(default=timezone.now)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)



class Appointment(models.Model):
    Name=models.CharField(max_length=50,null=False)
    Phone=models.CharField(max_length=10,null=False)
    Email=models.EmailField(max_length=100,null=True)
    Test_Name=models.ForeignKey(TestDetails,on_delete=models.CASCADE)
    Date=models.DateField(default=timezone.now)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)  

class Cart(models.Model):
    TestDetails=models.ForeignKey(TestDetails,on_delete=models.CASCADE)
    total_price=models.FloatField(null=True,blank=True)    
    gst = models.FloatField(null=True, blank=True, default=18)
    service_charge = models.FloatField(null=True, blank=True, default=10)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    def __str__(self):
       return self.TestDetails.Test_name +"("+"id:" +str(self.user.id) +"; name:"+ self.user.username +")"
    def save(self, *args, **kwargs):
        # Call the parent class's save method to ensure the default save behavior
        super().save(*args, **kwargs)

     
        # # Calculate GST amount (18%)
        # gst_rate = 0.18
        # gst_amount = self.total_price * gst_rate

        # Update the values in the Cart model and save again
        self.total_price = self.total_price

        super().save(*args, **kwargs)
        

class Order(models.Model):
    order_id = models.CharField(max_length=15, unique=True)

    TestDetails=models.ForeignKey(TestDetails,on_delete=models.CASCADE)
    total_price=models.ForeignKey(Cart,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.order_id:
            # Generate a new order ID if it doesn't exist
            last_order = Order.objects.order_by('-id').first()
            if last_order:
                last_order_number = int(last_order.order_id.split('_')[-1])
                new_order_number = last_order_number + 1
            else:
                new_order_number = 1

            self.order_id = f'odr_path_test{new_order_number:03d}'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id+str(self.user.username)


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    report_date = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    report_status=models.BooleanField(default=False)
    def __str__(self):
        return str(self.order.id)+str(self.order.user.username)

class report_file(models.Model):
    file_id = models.AutoField(primary_key=True)
    report=models.ForeignKey(Report,on_delete=models.CASCADE)
    file_content = models.FileField(upload_to='report_files/pdf/')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the report_status of the associated Report
        self.report.report_status = True
        self.report.save()
    def __str__(self):
        return str(self.report.order.id)+str(self.report.order.user.username)+" "+str(self.file_content)







    






