from django.contrib import admin
from .models import Product, Variation

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["empty_label"] = "None"  # Change placeholder text to "None"
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    list_display = ('product_name', 'price', 'stock', 'created_date', 'updated_date', 'is_available')
    prepopulated_fields = {'slug':('product_name',)}
    
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable =('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')
    

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)