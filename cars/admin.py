# cars/admin.py
from django.contrib import admin
from .models import CarBrand, CarModel, Car, CarImage, CarFeature, CarFeatureRelation

@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'created_at')
    list_filter = ('brand',)
    search_fields = ('name', 'brand__name')
    ordering = ('brand__name', 'name')

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    max_num = 10

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'owner', 'price', 'status', 'views_count', 'created_at')
    list_filter = ('status', 'brand', 'body_type', 'fuel_type', 'condition', 'created_at')
    search_fields = ('brand__name', 'model__name', 'owner__email', 'description')
    ordering = ('-created_at',)
    inlines = [CarImageInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('owner', 'brand', 'model', 'year')
        }),
        ('Характеристики', {
            'fields': ('body_type', 'fuel_type', 'engine_volume', 'engine_power',
                      'transmission', 'drive_type', 'mileage', 'condition', 'color')
        }),
        ('Цена и продажа', {
            'fields': ('price', 'is_negotiable', 'status')
        }),
        ('Дополнительная информация', {
            'fields': ('vin', 'license_plate', 'description', 'location', 'contact_phone')
        }),
        ('Статистика', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        }),
    )

@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ('car', 'is_main', 'created_at')
    list_filter = ('is_main', 'created_at')
    search_fields = ('car__brand__name', 'car__model__name')

@admin.register(CarFeature)
class CarFeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('category', 'name')