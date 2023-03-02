from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Orders,OrdersUpdate
from math import ceil
import json
# Create your views here.
def index(request):
    # product =Product.objects.all()
    # print(product)
    # n= len(product)
    # nSlides =n//4 + ceil((n/4)-(n//4))

    allProds =[]                 #3rd method
    carprods = Product.objects.values('catagory','id')
    cats = {item['catagory'] for item in carprods}
    # print(cats)

    for cat in cats:
        prod = Product.objects.filter(catagory__icontains = cat)
        # print(prod)
        n= len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nSlides),nSlides])
    params = {'allProds': allProds}
    
    return render(request, 'shop/index.html', params)

    # params ={'no_of_slides':nSlides,'range':range(1,nSlides),'product':product}  // 1st method
    # allProds =[[product,range(1,nSlides),len(product)],                    // 2nd method
    #            [product,range(1,nSlides),len(product)]]
def searchMatch(query,item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.catagory.lower():
        return True
    else:
        return False
def search(request):
        query = request.GET.get('search')
        allProds =[]                 #3rd method
        carprods = Product.objects.values('catagory','id')
        cats = {item['catagory'] for item in carprods}

        for cat in cats:
            prodtemp = Product.objects.filter(catagory = cat)
            prod = [item for item in prodtemp if searchMatch(query,item)]  
            n= len(prod)
            nSlides = n//4 + ceil((n/4)-(n//4))
            if len(prod)!= 0:
                allProds.append([prod,range(1,nSlides),nSlides])
        params = {'allProds': allProds,"msg":""}
        print(len(allProds))

        if len(allProds) ==4 or len(query)<=2:
          params ={'msg':"please make sure you enter the revelent search query"}
       
    
        return render(request,'shop/search.html',params)

def about(request):
    return render(request,'shop/about.html')
    # return render(request,'shop/index.html')
def contact(request):
    thank = False
    if request.method == "POST":
        name =request.POST.get('name',"")
        email =request.POST.get('email',"")
        subject =request.POST.get('subject',"")
        message =request.POST.get('message',"")
        contact = Contact(name=name,email =email,subject=subject,message=message)
        contact.save()
        thank = True
    return render(request,'shop/contact.html',{"thank":thank})

def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId',"")
        email = request.POST.get('email',"")
        try:
            order =Orders.objects.filter(order_id=orderId,email=email)
            if len(order)>0:
                update =OrdersUpdate.objects.filter(order_id=orderId)
                updates =[]
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response= json.dumps({"status":"success","updates":updates,"itemJson":order[0].items_json},default=str)
                return HttpResponse(response)

            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request,'shop/tracker.html')



def product(request,myid):
    products = Product.objects.filter(id = myid)
    return render(request,'shop/prodView.html',{'product':products[0]})

def checkout(request):
    if request.method == "POST":
        items_json =request.POST.get('itemsJson','')
        print(items_json)
        name = request.POST.get('name','')
        amount = request.POST.get('amount','')
        email = request.POST.get('email','')
        address = request.POST.get('address1','') + " " + request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')
        phone = request.POST.get('phone','')
        order = Orders(items_json = items_json,name=name,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone,amount=amount)
        order.save()
        id =order.order_id
        update = OrdersUpdate(order_id=order.order_id ,update_desc="the order has been placed successfully")
        update.save()
        thank = True
        return render(request,'shop/checkout.html',{'thank':thank,'id': id})

    # return HttpResponse("i am checkout page")
    return render(request,'shop/checkout.html')