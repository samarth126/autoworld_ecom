from django.contrib import admin
from django import forms
from mptt.admin import MPTTModelAdmin
from django.contrib.admin.filters import RelatedOnlyFieldListFilter

# Register your models here.
from .models import *

admin.site.register(Category, MPTTModelAdmin)

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Transaction)
admin.site.register(Message)
admin.site.register(shipping_address)
# admin.site.register(Order_status)
admin.site.register(Order)
admin.site.register(Order_item)
admin.site.register(Contact)
admin.site.register(Support)

# admin.site.register(Tri)




admin.site.register(TypeOfVehicle)






# admin.site.register(Manufacturer)
class CarModelInline(admin.TabularInline):
    model=CarModel
    inlines=[
        
    ]

@admin.register(Manufacturer)
class ManufactureAdmin(admin.ModelAdmin):
    inlines=[
        CarModelInline,
        
    ]
    list_display = ('name_of_Manufacturer', 'vehicaltype' )






class ProductImageInline(admin.TabularInline):
    model=ProductImage
    
@admin.register(Product)
class ProductInline(admin.ModelAdmin):
    
    inlines=[
        ProductImageInline,
    ]
    
   


class Producttest(admin.StackedInline):
    list_display = ('title', 'manufacturer', 'myear', 'vehicaltype','vmodel')
    model=Product 
  
@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    
    
   
    # list_filter = (
    #     ('manufacturer', RelatedOnlyFieldListFilter),
    #     ('vmodel', RelatedOnlyFieldListFilter),
        
    # )
    inlines=[
        
        # ProductImageInline,
        Producttest,
        
       
        
        
       
    ]
    
    # fields = ('myear', 'title', 'category', 'regular_price', 'descount_price')
    # list_display = ('title', 'manufacturer', 'myear', 'vehicaltype','vmodel')
    # list_editable = ('vehicaltype', 'manufacturer', 'vmodel', )


