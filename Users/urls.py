from django.urls import path
from Users import views

app_name = 'Users'

urlpatterns = [
   
    path("contact", views.contact, name="contact"),
    path('register', views.register, name="register"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('profile', views.profile, name="profile"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('subscribe', views.subscribe, name='subscribe'),
    # path("newsletter", views.newsletter, name="newsletter"),
]