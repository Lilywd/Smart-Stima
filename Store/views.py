from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, View

from requests import request
from Store.models import Coupon, Item, OrderItem, Order, DeliveryAddress, Payment
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from Store.forms import CouponForm,BillingForm
from django.http import HttpResponse

from django.conf import settings
# Create your views here.

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

PAYMENT_CHOICES = (
    ('M','Mpesa'),
    ('P', 'PayPal')
)

def home(request):
    items = Item.objects.all()
    context = {'items':items}
    return render(request, 'Store/index.html',context)


class CartSummaryView(LoginRequiredMixin,View):
    login_url = '/signin'
    redirect_field_name = 'signin'
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            
            context = {
                'object': order
                
            }
            return render(self.request, 'Store/cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")
   

class ItemDetailView(DetailView):
    model = Item
    
    template_name = 'Store/product.html'


@login_required
def shop(request):
    items = Item.objects.all()
    context = {'items':items}
    return render(request, 'Store/shop.html',context)

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item  quantity was updated ")
            return redirect("Store:cart")
        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
    return redirect("Store:cart")

@login_required   
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("Store:cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("Store:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("Store:product", slug=slug)
@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("Store:cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("Store:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("Store:product", slug=slug)
        
class BillingView(View):
    def get(self, request, *args, **kwargs):
        user= request.user
        try:
            delivery = DeliveryAddress.objects.get(user=user)
        except:
            delivery = ""
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
           
            form = BillingForm()
            context = {
                'form': form,
                'couponform' : CouponForm(),
                'order' : order,
                "delivery":delivery
               
                }
            return render(self.request, 'Store/billing.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'you do not have an active order')
            return redirect('Store:billing')   
    
    def post(self, request, *args, **kwargs):
        user= request.user
        order = Order.objects.get(user=self.request.user, ordered=False)
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        address = request.POST["address"]
        apartment = request.POST["apartment"]
        city = request.POST["city"]
        country = request.POST["country"]
        zip = request.POST["zip"]
        phone = request.POST["phone"]
        # payment_option = "M"
        delivery_address = DeliveryAddress(user= self.request.user, first_name=first_name,
        last_name= last_name, address=address, city=city, apartment=apartment,country=country,
        zip=zip, phone=phone, email=email)
        delivery = DeliveryAddress.objects.filter(user=self.request.user).exists()
        if delivery:
            DeliveryAddress.objects.filter(user=user).update(user= self.request.user, first_name=first_name,
        last_name= last_name, address=address, city=city, apartment=apartment,country=country,zip = zip, phone=phone, email=email)

        else:
            delivery_address.save()
        try:
            Order.objects.filter(user=self.request.user, ordered=False).update(delivery_address = delivery_address)
        except:
            pass
        return redirect('Store:shipping')


def shipping(request):
    if request.method == "POST":
        shipping = request.POST["shipping"]
        order = Order.objects.get(user=request.user, ordered=False)
        if shipping == "1":
            total = order.get_total()
            Order.objects.filter(user=request.user, ordered=False).update(shipping_method = 1)
        elif shipping == "2":
            total = order.get_total() + 19.99
            Order.objects.filter(user=request.user, ordered=False).update(shipping_method = 2)
        elif shipping == "3":
            total = order.get_total() + 29.99
            Order.objects.filter(user=request.user, ordered=False).update(shipping_method = 3)
        # print(total)
        return redirect('Store:payment')
    user= request.user
    try:
        delivery = DeliveryAddress.objects.get(user=user)
    except:
        delivery = ""
    context ={"user":user, "delivery":delivery}
    return render(request, 'Store/shipping.html', context)

class PaymentView(View):
    def get(self, request,*args, **kwargs):
        user = request.user
        order = Order.objects.get(user=request.user, ordered=False)
        try:
            delivery = DeliveryAddress.objects.get(user=user)
        except:
            delivery = ""
        context ={"user":user, "delivery":delivery, "order":order}
        print(order.items.count())
        if order.delivery_address:
            return render(self.request, 'Store/payment.html', context)
        else:
            messages.error(self.request, 'you have not added your delivery information ')
            return redirect('Store:billing') 

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount= int(order.get_total() * 100)
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
                
            )
            payment=Payment()
            payment.stripe_charge_id = charge['id']
            payment.user =self.request.user
            payment.amount = order.get_total()
            payment.save()
            
            order_items = order.items.all
            order_items.update(ordered=True)
            for item in order_items:
                item.save()



            order.ordered = True
            order.payment = payment
            order.save()
            
            messages.success(self.request, "Your order was successful!")
            return redirect("/")

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
            messages.warning(self.request, "Rate limit error")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
            print(e)
            messages.warning(self.request, "Invalid parameters")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
            messages.warning(self.request, "Not authenticated")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
            messages.warning(self.request, "Network error")
            return redirect("/")

        except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
            messages.warning(
                self.request, "Something went wrong. You were not charged. Please try again.")
            return redirect("/")

        except Exception as e:
                # send an email to ourselves
            messages.warning(
                self.request, "A serious error occurred. We have been notifed.")
            return redirect("/")
        
    
            
def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, 'coupon does not exist')
        return redirect('Store:billing')  
       
class AddCouponView(View):
    def post(self, request, *args, **kwargs):
        coupon_code = request.POST["coupon"]
        order = Order.objects.filter(user=request.user,ordered=False).exists()
        if order == False:
            messages.info(request, 'you do not have an active order')
            return redirect('Store:billing')
        
        coupon = Coupon.objects.filter(code=coupon_code).exists()
        if coupon == False:
            messages.info(request, 'the coupon code you entered is invalid')
            return redirect('Store:billing')
        coupon = Coupon.objects.get(code = coupon_code)
        Order.objects.filter(user=request.user, ordered=False).update(coupon = coupon)
        order = Order.objects.get(user=request.user, ordered=False)
        total = order.get_total()
        total -= coupon.amount
        Order.objects.filter(user=request.user, ordered=False).update(total = total)
        messages.success(self.request, 'Coupon successfully added')
        return redirect('Store:billing')
        

            # form =  CouponForm(self.request.POST or None)
            # if form.is_valid():

            #     try:
            #         code = form.cleaned_data.get('code')
            #         order = Order.objects.get(user=self.request.user,ordered=False)
            #         order.coupon = get_coupon(self.request, code)
            #         order.save()
            #         messages.success(self.request, 'Coupon successfully added')
            #         return redirect('Store:billing')  

            #     except ObjectDoesNotExist:
            #         messages.info(self.request, 'you do not have an active order')
            #         return redirect('Store:billing')  
            # messages.info(self.request, 'you do not have an active order')
            # return redirect('Store:cart') 
        
        




def wishlist(request):
    return render(request, 'Store/wishlist.html')




