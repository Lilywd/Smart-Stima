from django.db import models
from django.conf import settings
from django.shortcuts import reverse


# Create your models here.
CATEGORY_CHOICES = {
    ('A', 'Accessories'),
    ('C', 'Cameras'),
    ('L', 'Laptops'),
    ('S', 'Smartphones'),
    

  
}

LABEL_CHOICES = {
    ('N', 'new'),
    ('S', 'sale')
  
  
}

COUNTRY_CHOICES = {
    ('K', ' kenya'),
    ('U', 'uganda'),
    ('T', 'tanzania')
  
}


COUNTRY_CHOICES ={
    ('K', 'kenya'),
    ('U', 'uganda'),
    ('T', 'tanzania'),

}
#product
class Item(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField()
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    label = models.CharField(choices=LABEL_CHOICES,max_length=1, blank=True,null=True)
    slug = models.SlugField()
    description = models.TextField()
    
    
    def __str__(self):
       return self.title

    
    def get_absolute_url(self):
        return reverse("Store:product", kwargs= {
            'slug': self.slug
        })
    def get_add_to_cart_url(self):
        return reverse("Store:add-to-cart", kwargs= {
            'slug': self.slug
        })

    
    def get_remove_from_cart_url(self):
        return reverse("Store:remove-from-cart", kwargs= {
            'slug': self.slug
        })

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
       return f"{self.quantity} of {self.item.title}"

    
    def get_total_item_price(self):
        return self.quantity * self.item.price


    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()



# product in cart
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=30)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_method = models.IntegerField(default=1)
    delivery_address = models.ForeignKey('DeliveryAddress', on_delete=models.SET_NULL,blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL,blank=True, null=True)
    
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL,blank=True, null=True)

   # order status 
    delivery = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    refund_not_granted = models.BooleanField(default=False)
    total = models.FloatField(default=0)

    def __str__(self):
       return self.user.username
       

    def get_total(self):
        self.total = 0
        for order_item in self.items.all():
            self.total += order_item.get_final_price()
        # if self.coupon:
        #     total -= self.coupon.amount
    
        return self.total

    


class DeliveryAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    apartment = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
  

    country = models.CharField(max_length=1, choices=COUNTRY_CHOICES)

    
   
    zip = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.user.username



class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()
    
    def __str__(self):
        return self.code
