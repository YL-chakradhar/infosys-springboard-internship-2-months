from django.contrib import admin
from .models import *
admin.site.register(Customer)
admin.site.register(Cake)
admin.site.register(Cart)
admin.site.register(Order)