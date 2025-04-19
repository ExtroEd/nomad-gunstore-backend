from django.contrib import admin
from django import forms
from .models import Category, Product, ProductAttribute
from ckeditor.widgets import CKEditorWidget


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['details'].widget = CKEditorWidget()
        self.fields['features'].widget = CKEditorWidget()

        if not self.instance.pk:
            self.fields['attributes'].initial = {
                "color": "black",
                "weight": "1.5kg"
            }


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = (
        'name', 'category', 'price', 'brand', 'stock', 'is_deal_of_the_day'
    )
    list_filter = (
        'category', 'brand', 'is_clearance', 'is_deal_of_the_day', 'stock'
    )
    search_fields = ('name', 'description', 'brand')
    inlines = [ProductAttributeInline]
    autocomplete_fields = ['category']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Общая информация', {
            'fields': (
                'name', 'category', 'brand', 'price', 'image'
            )
        }),
        ('Описание', {
            'fields': (
                'details', 'features',
            )
        }),
        ('Дополнительно', {
            'fields': (
                'stock', 'is_clearance', 'is_deal_of_the_day', 'created_at'
            )
        }),
        ('Атрибуты', {
            'fields': ('attributes',)
        }),
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    autocomplete_fields = ['parent']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
