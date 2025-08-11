from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from account.models import Profile
from pathology.models import TestDetails,Cart
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from pathology.models import Order,report_file,Report
from django.contrib.auth import login,authenticate
# Create your views here.

# def Register(request):
#     if request.method=="POST":
#         fname=request.POST["fname"]
#         lname=request.POST["lname"]
#         username=request.POST["unm"]
#         email=request.POST["email"]
#         password=request.POST["password"]
#         confirmpass=request.POST["confirmpass"]
#         contact=request.POST["contact"]

#         if password==confirmpass:
#             usr=User.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=password)
#             usr.save()
#             prof=Profile(user=usr,contact=contact)
#             prof.save()

#             login(request, usr)
#             return redirect("home")
#         else:
#             return redirect("account:register")
#     return render(request,"account/register.html")

def Register(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        username = request.POST["unm"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmpass = request.POST["confirmpass"]
        contact = request.POST["contact"]

         # Check if the passwords match
        if password == confirmpass:
            # Check if the user already exists
            if User.objects.filter(username=username).exists():
                # If the user exists, redirect to the login page
                return redirect("login")
            else:
                # If the user doesn't exist, create a new user
                usr = User.objects.create_user(
                    first_name=fname,
                    last_name=lname,
                    username=username,
                    email=email,
                    password=password,
                    is_superuser=False
                )
                usr.save()

                prof = Profile(user=usr, contact=contact)
                prof.save()

                # Redirect to the login page
                return redirect("login")
        
        # Handle password mismatch or other errors
        return redirect("account:register")

    return render(request, "account/register.html")


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        pas = request.POST["pwd"]

        user = auth.authenticate(request, username=username, password=pas)
        if user is not None:
            auth.login(request, user) 
            return redirect("home")
        else:
            messages.error(request, "INVALID CREDENTIALS!")
            return redirect("login")
    return render(request, "account/login.html")

def logout(request):
    auth.logout(request)
    return redirect("home")

def cart(request):
    context = {}


    if request.user.is_authenticated:
        tid = request.POST.get("t_id")
        test = TestDetails.objects.filter(id=tid).last()
        user = request.user
        # Get only active cart objects (not yet removed or proceeded to checkout)
        cart_obj = Cart.objects.filter(user=request.user, is_active=True)
        # breakpoint()
        context['cart_obj'] = cart_obj
        
        if test is not None:
            
            if not Cart.objects.filter(TestDetails=test, user=user).exists():
                test_price = test.Charge
                crt = Cart(TestDetails=test, total_price=test_price, user=user,is_active=True)
                crt.save()
            elif Cart.objects.filter(TestDetails=test, user=user,is_active=False).exists():
                # breakpoint()
                crt_obj = Cart.objects.filter(TestDetails=test, user=user, is_active=False).first()
                if crt_obj:
                    crt_obj.is_active = True
                    crt_obj.save()
            else:
                messages.info(request, f"{test.Test_name} is already in your cart")


        else:
            messages.info(request, "Selected test not found")

    else:
        messages.error(request, "Please Login first")
        return redirect('login')
    cart_tot=Cart.objects.filter(user=request.user,is_active=True)
    sale,service_charge,tax,total=0,0,0,0
    for i in cart_tot:
        sale += i.TestDetails.Charge 
        service_charge+=sale*i.service_charge /100
        tax+=sale*i.gst /100
        total+=(sale+service_charge+tax)
    context['cart_tot']=total
    context['service_charges']=service_charge
    context['tax']=tax
    context['price']=sale
    return render(request, "account/cart.html", context)


def view_profile(request):
    
    context = {}
    user_data = request.user
    try:
        profile_data = Profile.objects.get(user=user_data)
        context['profile_data'] = profile_data
    except Profile.DoesNotExist:
        context['message'] = "Please create your profile."


    report_order = Order.objects.filter(user=user_data)
    context['rep_odr'] = report_order
    report_files_dict={}
    
    
    # report_files_list = []
    for order in report_order:
        # Get the corresponding report for each order
        report = Report.objects.filter(order=order).first()
        # Check if the report exists
        if report:
            # Get report files for the report
            report_files = report_file.objects.filter(report=report)

            # Create a key based on the order number
            key = f'order_{order.order_id}'
            # Add report files to the dictionary under the corresponding key
            report_files_dict[key] = list(report_files)
        else:
            # If the report does not exist, set an empty list for the key
            key = f'order_{order.order_id}'
            report_files_dict[key] = [] 
         
    file_paths_dict = {}
    for key, files in report_files_dict.items():
        file_paths = [file.file_content.url for file in files]
        file_paths_dict[key] = file_paths
    context ['file_paths_dict']= file_paths_dict

    
    return render(request, 'account/profile.html', context)




def profile_Update(request):
    context={}
    user_data=request.user
    Profile_data=get_object_or_404(Profile,user=user_data)
    context['profile_data']=Profile_data
    # context['']
    if request.method=="POST":
        username=request.POST["username"]
        contact=request.POST['contact']
        bloodgroup=request.POST['bloodgroup']
        Profile_data.contact=contact
        Profile_data.bloodGroup=bloodgroup
        user_data.username=username
        
        user_data.save()
        Profile_data.save()
        return redirect("view_profile")
    return render(request,'account/profile_Update.html', context)
# def get_CartData(request):
#     cart_item = Cart.objects.filter( user=request.user,is_active=True)



from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse

def remove_cart_item(request):
    if  "delete_cart" in request.GET:
        id=request.GET['delete_cart']
        cart_item=get_object_or_404(Cart,id=id)
        # Mark the Cart item as inactive
        cart_item.is_active = False
        cart_item.save()
    return HttpResponse(1)


import paypalrestsdk
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse

paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})

def execute_payment(request):
    cartitem=Cart.objects.filter( user=request.user,is_active=True)
    for i in cartitem:
        sale += i.TestDetails.Charge 
        service_charge+=sale*i.service_charge /100
        tax+=sale*i.gst /100
        total+=(sale+service_charge+tax)
    
    payment_id = total/84
    payer_id = get_object_or_404(User,id=id)

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payment_id": payment_id}):
        return render(request, 'payment_success.html')
    else:
        return render(request, 'payment_failed.html')

def payment_checkout(request):
    return render(request, 'checkout.html')

def create_payment(request):
    payment = paypalrestsdk.Payment({
        "intent": "sale",        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_payment')),
            
        },
        "transactions": [
            {
                "amount": {
                    "total": "10.00",  # Total amount in USD
                    "currency": "USD",
                },
                "description": "Payment for Product/Service",
            }
        ],
    })

    if payment.create():
        return redirect(payment.links[1].href)  # Redirect to PayPal for payment
    else:
        return render(request, 'payment_failed.html')
    


