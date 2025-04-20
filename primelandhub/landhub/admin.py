from django.contrib import admin
from .models import reg_form,property,Reviews, interested,Notification,Buyer

# Register your models here.
admin.site.register(reg_form)
admin.site.register(property)
admin.site.register(Reviews)
admin.site.register(interested)
admin.site.register(Notification)

admin.site.register(Buyer)