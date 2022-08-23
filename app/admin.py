from django.contrib import admin
from app.models import *

# Register your models here.
admin.site.register(District)
admin.site.register(City)
admin.site.register(Customer)
admin.site.register(Unit)
admin.site.register(Item)
admin.site.register(Distributor)
admin.site.register(Customer_Items)
admin.site.register(Distributor_Items)