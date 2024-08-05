from django.conf import settings
from django.contrib import messages

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.db.models import Q
#from razorpay import Client
#import razorpay # type: ignore
#from app.ec import settings # type: ignore
from . models import Cart, Customer, OrderPlaced, Payment, Product
from .forms import AddToCartForm, CustomerProfileForm, CustomerRegistrationForm
# Create your views here.
def home(request):
    return render(request,"app/home.html")
def about(request):
    return render(request,"app/about.html")
def contact(request):
    return render(request,"app/contact.html")
class CategoryView(View):
    def get(self,request,val):
        product=Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')
        return render(request,'app/category.html',locals())
class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, 'app/category.html', {'product': product, 'title': title})
class ProductDetail(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        return render(request,'app/productiondetail.html',locals())

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',locals())
    def post(self,request):
        form =CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Registered Successfully")
        else:
            messages.error(request,"Invalid input data")
        return render(request,'app/customerregistration.html',locals())

class ProfileView(View):
    def get(self,request):
        form =CustomerProfileForm()
        return render(request,'app/profile.html',locals())  
    def post(self,request):
        form =CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, "Profile updated successfully!")
        else:
             messages.warning(request, "Error updating profile. Please correct the errors below.")
        return render(request,'app/profile.html',locals())  
    
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',locals())

class updateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form =CustomerProfileForm(instance=add)
        return render(request,'app/updateAddress.html',locals())  
    def post(self,request,pk):
        form =CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            #add.reg=Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            add.save()
            messages.success(request, "Profile updated successfully!")
        else:
             messages.warning(request, "Error updating profile. Please correct the errors below.")
        return redirect("address")



def show_cart(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to view your cart.")
        return redirect('login')  # Redirect to login page if user is not authenticated

    cart_items = Cart.objects.filter(user=request.user)
    amount = sum(item.product.discounted_price * item.quantity for item in cart_items)
    totalamount = amount + 40  # Adding fixed shipping cost

    return render(request, 'app/cart.html', {
        'cart': cart_items,
        'amount': amount,
        'totalamount': totalamount,
    })

def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    form = AddToCartForm(initial={'product_id': product_id})

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            try:
                product = Product.objects.get(pk=product_id)
                # Add product to cart logic here
                messages.success(request, f'{product.title} added to cart.')
                return redirect('cart')  # Redirect to cart page
            except Product.DoesNotExist:
                messages.error(request, 'Product does not exist.')
                return redirect('productiondetail', product_id=product_id)

    return render(request, 'app/productiondetail.html', {'product': product, 'form': form})

#def addtocart(request, product_id):
    #product = get_object_or_404(Product, pk=product_id)
    
    #if request.method == 'POST':
        # Assuming you have a Cart model with user and product fields
        #cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        #if not created:
            #cart_item.quantity += 1
            #cart_item.save()
        
        #messages.success(request, f'{product.title} added to cart.')
        #return redirect('showcart')  # Redirect to cart page

    #return render(request, 'app/cart.html', {'product': product})
def addtocart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        # Assuming you have a Cart model with user and product fields
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item.quantity = 1  # Set initial quantity to 1 for new items
            cart_item.save()
        
        messages.success(request, f'{product.title} added to cart.')
        return redirect('showcart')  # Redirect to cart page

    # If it's not a POST request, render the product details page
    return render(request, 'app/product_detail.html', {'product': product})

def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        a.quantity+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount+=value
        totalamount=amount+40
        print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
    return JsonResponse(data)

def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id)&Q(user=request.user))
        a.quantity-=1
        c.delete()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount+=value
        totalamount=amount+40
        print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
    return JsonResponse(data)

class checkout(View):
    def get(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
    
        if not cart_items.exists():
            return render(request, "app/home.html")
        
        amount = sum(item.product.discounted_price * item.quantity for item in cart_items)
        shipping = 40.00  # Example shipping cost
        totalamount = amount + shipping

        context = {
            'cart': cart_items,
            'amount': amount,
            'totalamount': totalamount,
        }

        # Assuming you have set up Razorpay client in your Django settings
        razoramount = int(totalamount * 100)
        #client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {
            "amount": razoramount,
            "currency": "INR",
            "receipt": "order_rcptid_11"
        }
        
        # Create a Razorpay order
        #payment_response = client.order.create(data=data)
        #order_id = payment_response['id']
        #order_status = payment_response['status']
        
        #if order_status == 'created':
            #payment = Payment(
                #user=user,
                #amount=totalamount,
               # razorpay_order_id=order_id,
                #razorpay_payment_status=order_status
           # )
           # payment.save()

        return render(request, 'app/checkout.html', context)
    #der(request,'app/checkout.html',locals())

def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    user=request.user
    customer=Customer.objects.get(id=cust_id)
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid=True
    payment.razorpay_order_id=payment_id
    payment.save()
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.adelete()
    return redirect("orders")