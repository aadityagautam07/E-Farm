from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth.models import Group
from django.utils.html import format_html


# Register your models here.

class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'number', )


class CustomUserAdmin(UserAdmin, admin.ModelAdmin):
    model = CustomUser

    list_display = ('email', 'username', 'staff', 'date_joined', 'superuser', 'account_verification', 'phone')
    # list_editable = ( )

    # Verified or not
    def account_verification(self, obj):
        if obj.is_verified == False:  
            return format_html('<i class="fa fa-close" style="font-size:20px;color:red"></i>')
        else:
            return format_html('<i class="fa fa-check" style="font-size:20px;color:green"></i>')

    def superuser(self, obj):
        if obj.is_superuser == False:  
            return format_html('<i class="fa fa-close" style="font-size:20px;color:red"></i>')
        else:
            return format_html('<i class="fa fa-check" style="font-size:20px;color:green"></i>')
    
    def staff(self, obj):
        if obj.is_staff == False:  
            return format_html('<i class="fa fa-close" style="font-size:20px;color:red"></i>')
        else:
            return format_html('<i class="fa fa-check" style="font-size:20px;color:green"></i>')


admin.site.unregister(Group)
admin.site.register(OtpCode, OtpCodeAdmin)
admin.site.register(CustomUser, CustomUserAdmin)