from django.contrib import admin

# Register your models here.
from .models import Category, Product, Size, User, Status, Order, CustomerAddress, OrderDetail
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']


admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Size)
admin.site.register(Status)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(CustomerAddress)



