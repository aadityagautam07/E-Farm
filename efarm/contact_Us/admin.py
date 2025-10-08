from django.contrib import admin
from .models import *

# Register your models here.
class Contact_MailAdmin(admin.ModelAdmin):
    # Overwriting the list.
    list_display = ('subject', 'name', 'email', )
    list_display_links = ('name', 'email', 'subject', )



admin.site.register(Contact_Mail, Contact_MailAdmin)