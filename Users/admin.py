from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,SubscribedUsers
# Register your models here.

class CustomUserAdmin(UserAdmin):
   list_display = ('email', 'username', 'date_joined','last_login','is_staff','is_admin')
   search_fields = ('email', 'username',)
   readonly_fields =('date_joined','last_login' )
   
   fieldsets = ()
   filter_horizontal = ()
   list_filter = ()

class SubscribedUsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_date')

 
 
# Now register the new UserAdmin...
admin.site.register(User, CustomUserAdmin)
admin.site.register(SubscribedUsers, SubscribedUsersAdmin)
