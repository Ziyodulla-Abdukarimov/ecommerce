from django.contrib import admin
from model.models import *


# Register your models here.
class ProductInline(admin.StackedInline):
    model = ProductImages
    extra = 3


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductInline]


admin.site.register(CustomUser)
admin.site.register(AdminHod)
admin.site.register(Staffs)
admin.site.register(Client)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(Comment)
