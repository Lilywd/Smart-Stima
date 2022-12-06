from django.contrib import admin
from.models import Coupon, DeliveryAddress, Item, OrderItem, Order, Payment
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered', 'delivery', 'received', 'refund_requested', 'refund_granted', 'refund_not_granted','delivery_address','payment','coupon']
    list_filter = ['ordered','delivery','received','refund_requested','refund_granted', 'refund_not_granted']
    list_display_links = ['user','delivery_address','payment','coupon']


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(DeliveryAddress)