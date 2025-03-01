from django.shortcuts import render,redirect,get_object_or_404
from .models import Coffee,Cart,Checkout,Orderp,Invoice
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
import smtplib
from email.mime.text import MIMEText
import razorpay
from datetime import datetime

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
# from razorpay import Client

# Client.set_app_details({"title" : "<YOUR_APP_TITLE>", "version" : "<YOUR_APP_VERSION>"})







@csrf_exempt

# Create your views here.

def registerform(request):
    return render(request,"register.html")

def register(request):
   
    c=""
    if request.method=='POST':
        uname=request.POST['username']
        # fname=request.POST['fname']
        # lname=request.POST['lname']
        email=request.POST['email']
        pwd=request.POST['psw']
        rpwd=request.POST['psw-repeat']
        if(pwd==rpwd):
                user = User.objects.create_user(uname, email, pwd)
                subject = "Registered"
                body = """Account Created Successfully"""
                sender = "Anshankolothumthodi@gmail.com"
                recipients = [email]
                password = "yhfiidhlffahefsy"


                def send_email(subject, body, sender, recipients, password):
                    msg = MIMEText(body)
                    msg['Subject'] = subject
                    msg['From'] = sender
                    msg['To'] = ', '.join(recipients)
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                        smtp_server.login(sender, password)
                        smtp_server.sendmail(sender, recipients, msg.as_string())
                    print("Message sent!")


                send_email(subject, body, sender, recipients, password)
                return redirect('/')
        else:
            c=True
            d={"message":c}
            return render(request,'register.html',d)
            
    user.save()
    return render(request,"login.html")

def loginform(request):
    return render(request,"login.html")

def loginpage(request):
    c=""
    username = request.POST["username"]
    password = request.POST["psw"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/home/')
    else:
        c=True
        d={"message":c}
        return render(request,"login.html",d)
    
def log_out(request):
    logout(request)
    return redirect("/")

    
@login_required


def home(request):
    d={"user":request.user}
    return render(request,"home.html",d)

@login_required

def store(request):
    p=Coffee.objects.all()
    d={"coffee": p}
    return render(request,"store.html",d)

@login_required


def addsuccess(request):
    return render(request,"addsuccess.html")

@login_required


def items(request):
    p=Coffee.objects.all()
    d={"coffee": p}
    return render(request,"items.html",d)

@login_required


def updatesuccess(request):
    return render(request,"updatesuccess.html")

@login_required


def removed(request):
    return render(request,"removed.html")

@login_required


    
def buy(request, id):
    p = Coffee.objects.get(id=id)
    
    if request.method == 'POST':
        quantity = int(request.POST["qnt"])
        im=request.POST['ima']
        userid = request.user
        
        # Check if the item already exists in the cart for this user
        k = Cart.objects.filter(itemname=p.name, userid=userid).first()
        
        totall = quantity * int(p.price)
        
        if k:
            # If the item already exists, update the quantity and total
            k.itemqnt += quantity
            k.total += totall
            k.save()
        else:
            # If it's a new item in the cart, create a new cart entry
            x= Cart(
                itemname=p.name,
                itemquantity=p.quantity,
                itemprice=p.price,
                itemqnt=quantity,
                userid=userid,
                total=totall,
                imag=im
            )
            x.save()
        
        return redirect('/showcart/')    

@login_required

def addtocart(request, id):
    p = Coffee.objects.get(id=id)
    
    if request.method == 'POST':
        quantity = int(request.POST["qnt"])
        im=request.POST['ima']
        userid = request.user
        
        # Check if the item already exists in the cart for this user
        k = Cart.objects.filter(itemname=p.name, userid=userid).first()
        
        totall = quantity * int(p.price)
        
        if k:
            # If the item already exists, update the quantity and total
            k.itemqnt += quantity
            k.total += totall
            k.save()
        else:
            # If it's a new item in the cart, create a new cart entry
            x= Cart(
                itemname=p.name,
                itemquantity=p.quantity,
                itemprice=p.price,
                itemqnt=quantity,
                userid=userid,
                total=totall,
                imag=im
            )
            x.save()
        
        return redirect('/store/')

@login_required



@login_required


def mycart(request):
    return render(request,"cart.html")

@login_required


def showcart(request):

    totalp=0

    p=Cart.objects.all().filter(userid=request.user)
    
    for x in p:
            
            totalp=totalp+x.total
    check=Checkout(totalprice=totalp)
    check.save()
    d={"coffee":p,
           "checkout":check}

    return render(request,"showcart.html",d)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart

def remove_cart_item(request, itemname, userid):
    # Filter Cart items based on itemname and userid
    cart_items = Cart.objects.filter(itemname=itemname, userid=userid)
    
    if cart_items.exists():
        cart_item = cart_items.first()  # Get the first matching item (or logic for choosing one)
        
        # Decrease the quantity by 1
        if cart_item.itemqnt > 1:
            cart_item.itemqnt -= 1
            cart_item.total -= cart_item.itemprice  # Decrease total by price
            cart_item.save()
        else:
            # If quantity is 1, delete the item
            cart_item.delete()
    
    return redirect('/showcart/')  # Redirect back to the showcart view

    
@login_required


def purchased(request,paymentid,orderid):
    order=Orderp.objects.get(razorpay_order_id=orderid)
    order.ispaid=True
    order.razorpay_payment_id=paymentid
    order.save()

    return render(request,"purchased.html")


def payfail(request):


    return render(request,"payfail.html")



@login_required


def buyform(request,id):
    p=Coffee.objects.get(id=id)
    d={"coffee":p}
    return render(request,"buyform.html",d)

@login_required


def buyform1(request,id):
    p=Coffee.objects.get(id=id)
    d={"coffee":p}
    return render(request,"buyform1.html",d)

@login_required



def addform(request):
    return render(request,"addform.html")

@login_required


def updateform(request,id):
    p=Coffee.objects.get(id=id)
    d={"coffee":p}
    return render(request,"updateform.html",d)

@login_required


def add(request):
    if request.method == "POST":
        name = request.POST['name']
        quantity = request.POST['quantity']
        price = request.POST['price']
        image = request.FILES.get('img')  
        x = Coffee(name=name, quantity=quantity, price=price, image=image)
        x.save()

    return render(request, "addsuccess.html")

@login_required

def update(request,id):
    p=Coffee.objects.get(id=id)
    if request.method=="POST":
        name=request.POST['name']
        quantity=request.POST['quantity']
        price=request.POST['price']
        image = request.FILES.get('img')
    p.name=name
    p.quantity=quantity
    p.price=price
    p.image=image
    p.save()
    return redirect('/items/')

@login_required

def remove(request,id):
    p=Coffee.objects.get(id=id)
    p.delete()
    return render(request,"removed.html")

@login_required


def cartremove(request,itemname,userid):
    p=Cart.objects.all().filter(itemname=itemname)
    p.delete()
    q=Cart.objects.all().filter(userid=request.user)
    d={"coffee":q}
    return redirect('/showcart/')

@login_required

def checkout(request):
    # client = razorpay.Client(auth=("rzp_test_1j5JxKhdrgP8gG", "6PCwTzdEeazNErFK6mDlCRL4"))

    # data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" }
    # payment = client.order.create(data=data)
    
    totalp=0

    cart=Cart.objects.all().filter(userid=request.user)
    
    for cartitem in cart:
            
            totalp=totalp+cartitem.total
    tax=float(f'{(totalp)*0.05:.2f}')
    check=Checkout(totalprice=totalp+tax,subtotal=totalp,tax=tax,userids=request.user)
    check.save()
    d={"coffee":cart,
           "checkout":check}
    return render(request,"checkout.html",d)

@login_required

def ordernow(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        address=request.POST['address']
        email=request.POST['email']
        phone=request.POST['phone']
        city=request.POST['city']
        state=request.POST['state']
        zipcode=request.POST['zipcode']
        userid=request.user
        
    totalprice=0
   
    
    p=Orderp.objects.all().filter(userid=request.user)
    q=Cart.objects.all().filter(userid=request.user)
    check=Checkout.objects.all().filter(userids=request.user)

    for x in check:
            
            totalprice=x.totalprice
    # tax=float(f'{totalp*0.05:.2f}')
    # check=Checkout(totalprice=totalp)

    
    # check.save()
        # for x in q:
            
        #     totalp=totalp+x.total
        # subject = "Oredered"
        # body = """Order Placed Successfully
                

                # """
        # for t in q:
        #     body=body+f"{t.itemname}-{t.itemquantity}-{t.itemprice}-{t.itemqnt}-{t.itemqnt*t.itemprice}\n"
        # body=body+f"Total= ₹{totalp}"    

        # sender = "Anshankolothumthodi@gmail.com"
        # recipients = [email]
        # password = "yhfiidhlffahefsy"


        # def send_email(subject, body, sender, recipients, password):
        #             msg = MIMEText(body)
        #             msg['Subject'] = subject
        #             msg['From'] = sender
        #             msg['To'] = ', '.join(recipients)
        #             with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        #                 smtp_server.login(sender, password)
        #                 smtp_server.sendmail(sender, recipients, msg.as_string())
        #             print("Message sent!")


        # send_email(subject, body, sender, recipients, password)

      

#     return render(request,"purchased.html")

# @login_required

# def myorder(request):
    client = razorpay.Client(auth=("rzp_test_6LPRQFPLbqHgqV", "szGpp0XUNPYsHyeW1iaajHt7"))

    DATA = {
            "amount": totalprice*100,
            "currency": "INR",
            "receipt": "receipt#1",
            "notes": {
                "key1": fname+" "+lname,
                "key2": email,
                "key3":phone
            }
        }
    payment=client.order.create(data=DATA)
    y = Orderp(fname=fname, lname=lname,address=address,email=email,phone=phone,city=city,state=state,zipcode=zipcode,userid=userid,razorpay_order_id=payment['id'])
    y.save()
    print("*****************************************************************")
    print(payment)
    print("*****************************************************************")

    
    d={"coffee":q,
        #    "checkout":check,
            "totalprice":totalprice,
           "order":p,
           "payment":payment}
    
    return render(request,"myorder.html",d)

@login_required

def ordercancel(request):
 p=Orderp.objects.all().filter(userid=request.user)
 p.delete()
 return redirect('/home/')


@login_required

def yourorder(request):
    totalp=0

    p=Orderp.objects.all().filter(userid=request.user)
    q=Cart.objects.all().filter(userid=request.user)

    for x in q:
            
            totalp=totalp+x.total
    totalp=totalp+float(f'{totalp*0.05:.2f}')
    check=Checkout(totalprice=totalp)
    check.save()
    client = razorpay.Client(auth=("rzp_test_6LPRQFPLbqHgqV", "szGpp0XUNPYsHyeW1iaajHt7"))

    DATA = {
            "amount": totalp*100,
            "currency": "INR",
            "receipt": "receipt#1",
            }
        
    payment=client.order.create(data=DATA)
    y = Orderp(razorpay_order_id=payment['id'])
    y.save()


    d={"coffee":q,
           "checkout":check,
           "order":p,
           "payment":payment,
           }
    invoice=Invoice(iuserids=request.user,iamount=totalp,irazorpay_order_id=y.razorpay_order_id)
    invoice.save()
    
    
    
    return render(request,"yourorder.html",d)

def clearcart(request):
    q=Cart.objects.all().filter(userid=request.user)
    q.delete()
    return redirect('/home/')


import qrcode
from io import BytesIO
from django.core.files.storage import default_storage
from django.conf import settings
from django.shortcuts import render
from datetime import datetime

def generate_qr_code(order_data):
    # Data to encode in the QR code
    # qr_data = f"Order ID: {order_data['order_id']}\nCustomer: {order_data['customer_name']}\nTotal: ₹{order_data['total']}"
    qr_data="test data"
    # Generate the QR code
    qr = qrcode.make(qr_data)

    # Save the QR code to a temporary file
    qr_code_image = BytesIO()
    qr.save(qr_code_image, 'PNG')
    qr_code_image.seek(0)

    # Save the image to a file
    file_path = f"qr_codes/{order_data['order_id']}.png"
    with default_storage.open(file_path, 'wb') as f:
        f.write(qr_code_image.read())

    # Return the file path or URL to access the image
    qr_code_url = settings.MEDIA_URL + file_path
    return qr_code_url



def testr(request,userid):
    q=Cart.objects.all().filter(userid=request.user)
    p=Orderp.objects.all().filter(userid=request.user)

    itemssall=[]
    order_id=''
    customer_address= ''
    customer_email=''
    for orderc in p:
        order_id=orderc.razorpay_order_id
        customer_address=orderc.address+ ","+ orderc.city+","+ orderc.state+","+ orderc.zipcode
        customer_email=orderc.email
        
        
    
    for itemm in q:
        itemssall.append({'name': itemm.itemname+" - "+itemm.itemquantity+"ml", 'quantity': itemm.itemqnt, 'price': itemm.itemprice, 'total': itemm.total})

    # Example data for the invoice (replace this with actual data fetching from your database)
    order_data = {
        'order_id': order_id,
        'customer_name': userid,
        'customer_address': customer_address,
        'customer_email': customer_email,
        # 'items': [
        #     {'name': 'Espresso', 'quantity': 2, 'price': 2.50, 'total': 5.00},
        #     {'name': 'Latte', 'quantity': 1, 'price': 3.00, 'total': 3.00},
        #     {'name': 'Cappuccino', 'quantity': 1, 'price': 3.50, 'total': 3.50},
        # ],
        'items': itemssall,
        'tax_rate': 0.05,  # 7% sales tax
        'payment_terms': 'Due upon receipt.',
    }

    # Company information
    company_info = {
        'name': 'Your Company Name',
        'address': '456 Business Ave, Suite 100, Business City, BC 98765',
        'phone': '(123) 456-7890',
        'email': 'contact@yourcompany.com',
        'website': 'www.yourcompany.com'
    }

    # Calculate totals
    subtotal = sum(item['total'] for item in order_data['items'])
    tax = float(f"{(subtotal * order_data['tax_rate']):.2f}")
    total = subtotal + tax
    qr_code_url = generate_qr_code(order_data)
    # Get current date for the invoice
    current_date = datetime.now().strftime("%B %d, %Y")
    order_data.update({"subtotal":subtotal})
    order_data.update({'tax':tax})
    order_data.update({'total':total})
    order_data.update({'current_date':current_date})
    order_data.update({'qr_code_url':qr_code_url})


    return render(request,'inv.html',order_data)


# from django.http import HttpResponse
# from reportlab.lib.pagesizes import A4
# from reportlab.lib import colors
# from reportlab.pdfgen import canvas
# import os
# from django.conf import settings
# import qrcode
# from io import BytesIO
# import tempfile


# def testr(request,userid):
#     q=Cart.objects.all().filter(userid=request.user)
#     p=Orderp.objects.all().filter(userid=request.user)

#     itemssall=[]
#     order_id=''
#     customer_address= ''
#     customer_email=''
#     for orderc in p:
#         order_id=orderc.razorpay_order_id
#         customer_address=orderc.address+ ","+ orderc.city+","+ orderc.state+","+ orderc.zipcode
#         customer_email=orderc.email
        
        
    
#     for itemm in q:
#         itemssall.append({'name': itemm.itemname+" - "+itemm.itemquantity+"ml", 'quantity': itemm.itemqnt, 'price': itemm.itemprice, 'total': itemm.total})

#     # Example data for the invoice (replace this with actual data fetching from your database)
#     order_data = {
#         'order_id': order_id,
#         'customer_name': userid,
#         'customer_address': customer_address,
#         'customer_email': customer_email,
#         # 'items': [
#         #     {'name': 'Espresso', 'quantity': 2, 'price': 2.50, 'total': 5.00},
#         #     {'name': 'Latte', 'quantity': 1, 'price': 3.00, 'total': 3.00},
#         #     {'name': 'Cappuccino', 'quantity': 1, 'price': 3.50, 'total': 3.50},
#         # ],
#         'items': itemssall,
#         'tax_rate': 0.05,  # 7% sales tax
#         'payment_terms': 'Due upon receipt.',
#     }

#     # Company information
#     company_info = {
#         'name': 'Your Company Name',
#         'address': '456 Business Ave, Suite 100, Business City, BC 98765',
#         'phone': '(123) 456-7890',
#         'email': 'contact@yourcompany.com',
#         'website': 'www.yourcompany.com'
#     }

#     # Calculate totals
#     subtotal = sum(item['total'] for item in order_data['items'])
#     tax = subtotal * order_data['tax_rate']
#     total = subtotal + tax

#     # Get current date for the invoice
#     current_date = datetime.now().strftime("%B %d, %Y")

#     # Create HTTP response for PDF
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'inline; filename="invoice_{order_data["order_id"]}.pdf"'

#     # Create a PDF object using ReportLab
#     pdf = canvas.Canvas(response, pagesize=A4)

#     # Adjust the placement of logo and QR code

#     # Add company logo at the top-left (adjusted position)
#     logo_path = os.path.join(settings.BASE_DIR, 'ansh', 'static', 'img', 'tea.png')
#     pdf.drawImage(logo_path, 40, 730, width=90, height=60)  # Logo Y-position: 740

#     # Add QR code at the top-right containing order details (adjusted position)
#     qr_data = f"Order ID: {order_data['order_id']}\nCustomer: {order_data['customer_name']}\nTotal: ${total:.2f}"
#     qr = qrcode.make(qr_data)

#     # Save the QR code as a temporary file
#     temp_qr_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
#     qr.save(temp_qr_file)
#     temp_qr_path = temp_qr_file.name  # Get the path to the temporary file

#     # Add QR code at the top-right (adjusted position)
#     pdf.drawImage(temp_qr_path, 400, 735, width=100, height=100)  # QR code Y-position: 740

#     # Set font for the document
#     pdf.setFont("Helvetica", 10)

#     # Add company information to the header
#     pdf.setFont("Helvetica-Bold", 16)
#     pdf.drawString(100, 710, company_info['name'])  # Adjusted Y-position to 710
#     pdf.setFont("Helvetica", 10)
#     pdf.drawString(100, 695, company_info['address'])  # Adjusted Y-position to 695
#     pdf.drawString(100, 680, f"Phone: {company_info['phone']}")  # Adjusted Y-position to 680
#     pdf.drawString(100, 665, f"Email: {company_info['email']}")  # Adjusted Y-position to 665
#     pdf.drawString(100, 650, f"Website: {company_info['website']}")  # Adjusted Y-position to 650

#     # Add invoice title
#     pdf.setFont("Helvetica-Bold", 16)
#     pdf.drawString(400, 710, f"INVOICE #{order_data['order_id']}")  # Adjusted Y-position to 710

#     # Add invoice date
#     pdf.setFont("Helvetica", 12)
#     pdf.drawString(400, 695, f"Date: {current_date}")  # Adjusted Y-position to 695

#     # Add customer details
#     pdf.setFont("Helvetica-Bold", 12)
#     pdf.drawString(100, 590, "Bill To:")  # Adjusted Y-position to 590
#     pdf.setFont("Helvetica", 10)
#     pdf.drawString(100, 575, f"{order_data['customer_name']}")  # Adjusted Y-position to 575
#     pdf.drawString(100, 560, order_data['customer_address'])  # Adjusted Y-position to 560
#     pdf.drawString(100, 545, order_data['customer_email'])  # Adjusted Y-position to 545

#     # Add table headers for items
#     y_position = 510  # Adjusted Y-position for the table headers
#     pdf.setFont("Helvetica", 10)
#     pdf.drawString(100, y_position, "Item Description")
#     pdf.drawString(300, y_position, "Quantity")
#     pdf.drawString(400, y_position, "Price")
#     pdf.setFont("Helvetica-Bold", 16)

#     pdf.drawString(500, y_position, "Total")

#     # Draw a line under the headers
#     pdf.setStrokeColor(colors.black)
#     pdf.line(100, y_position - 5, 500, y_position - 5)

#     # Add items in the table
#     y_position -= 20
#     pdf.setFont("Symbol", 10)
#     for item in order_data['items']:
#         pdf.drawString(100, y_position, item['name'])
#         pdf.drawString(300, y_position, str(item['quantity']))
#         pdf.drawString(400, y_position, f"\u20B9 {item['price']:.2f}")
#         pdf.drawString(500, y_position, f"₹{item['total']:.2f}")
#         y_position -= 20

#     # Add subtotal, tax, and total at the bottom of the table
#     pdf.setFont("Symbol", 12)
#     pdf.drawString(400, y_position - 20, f"Subtotal: ₹{subtotal:.2f}")
#     pdf.drawString(400, y_position - 35, f"Tax: ₹{tax:.2f}")
#     pdf.drawString(400, y_position - 50, f"Total: ₹{total:.2f}")

#     # Add payment terms
#     pdf.setFont("Helvetica", 10)
#     pdf.drawString(100, y_position - 80, f"Payment Terms: {order_data['payment_terms']}")

#     # Add footer with legal information
#     pdf.setFont("Helvetica", 8)
#     pdf.drawString(100, 100, "Thank you for your business ₹!")
#     pdf.drawString(100, 90, "This is a computer-generated document and does not require a signature.")

#     # Save the PDF and return the response
#     pdf.showPage()
#     pdf.save()

#     return response