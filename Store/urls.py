from django.urls import path
from Store import views

from Store.views import  ItemDetailView,CartSummaryView,BillingView, PaymentView,  add_to_cart, remove_from_cart, remove_single_item_from_cart, AddCouponView
app_name = 'Store'


# url paths to the pages
urlpatterns = [
    path('add-to-cart/<slug>/', add_to_cart, name="add-to-cart"),
    path('add-coupon/', AddCouponView.as_view(), name="add-coupon"),
    path('billing', BillingView.as_view(), name="billing"),
    path('cart', CartSummaryView.as_view(), name="cart"),
    path('', views.home, name="index"),
    path('payment/', PaymentView.as_view(), name="payment"),
    path('product/<slug>/', ItemDetailView.as_view(), name="product"),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove_single_item_from_cart/<slug>/',remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('shipping', views.shipping, name="shipping"),
    # path('shop', ItemsView.as_view(), name="shop"),
    path('shop', views.shop, name="shop"),
    path('wishlist', views.wishlist, name="wishlist"),
    # path('daraja/stk-push', views.stk_push_callback, name='mpesa_stk_push_callback'),
]