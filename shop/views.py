from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Order,OrderUpdate
from django.contrib import messages
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from .paytm import Checksum
# Create your views here.
MERCHANT_KEY = 'Your-Merchant-Key-Here'

def index(request):
    allprods =[]
    catprods = Product.objects.values('category','id')
    cats ={item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslide = n//4 + ceil((n/4)-(n//4))
        allprods.append([nslide,range(1,nslide),prod])
        msg = 'Products : Recommended for You!'

    dictionary = {'allprods': allprods, 'massage': msg}
    return render(request,'shop/index.html',dictionary)

def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '0')
        email = request.POST.get('email', '')
        desc = request.POST.get('desc', '')
        cont = Contact(name=name, phone=phone, email=email, desc=desc)
        cont.save()
        messages.success(request, 'Successfully Submitted!')
    return render(request, 'shop/contact.html')
def query(product,prod):
    if product.lower() in prod.Desc.lower() or product.lower() in prod.product_name.lower() or product.lower() in prod.category.lower():
        return True
    else:
        return False
def search(request):
    product = request.POST.get('search','')
    allprods = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    msg = ""
    if len(product)<3:
        return render(request, 'shop/search.html',{'massage':msg})

    for cat in cats:
        prod = Product.objects.filter(category=cat)
        schproduct = [item for item in prod if query(product,item)]
        n = len(schproduct)
        nslide = n // 4 + ceil((n / 4) - (n // 4))
        if len(schproduct) != 0 :
            allprods.append([nslide, range(1, nslide), schproduct])
            msg = 'Search Results Are :'

    dictionary = {'allprods': allprods, 'massage': msg}
    return render(request, 'shop/search.html', dictionary)

def productView(request,myid):
    product = Product.objects.filter(id=myid)
    dic={'product':product[0]}
    return render(request, 'shop/productView.html',dic)

def checkout(request):
    if request.method=="POST":
        itemsJson = request.POST.get('itemsJson','')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " , " + request.POST.get('address2', '')
        state = request.POST.get('state', '')
        city = request.POST.get('city', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Order(item_json=itemsJson,name=name,email=email,address=address,state=state,city=city,zip_code=zip_code,phone=phone,amount=amount)
        order.save()
        orderid = order.order_id
        order_update = OrderUpdate(order_id=orderid ,update_desc=f"Hi! {name}.Your order Is Placed Successfully!")
        order_update.save()
        # thank = True
        # return render(request, 'shop/checkout.html', {'thank': thank, 'id': orderid})
        # request paytm to transfer the amount to your account after payment by user
        param_dict = {

            'MID': 'Your-Merchant-Id-Here',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})

    return render(request, 'shop/checkout.html')

def tracker(request):
    if request.method =='POST':
        order_id = request.POST.get('orderId', '')
        email = request.POST.get('email', '')

        try:
            costmer = Order.objects.filter(order_id=order_id, email=email)
            if len(costmer)>0:
                update = OrderUpdate.objects.filter(order_id=order_id)
                updates =[]
                for item in update:
                    updates.append({'text': item.update_desc,'time': item.timestamp})
                response = json.dumps( [updates ,costmer[0].item_json] , default=str)
                print(response)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})

