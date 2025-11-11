from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price', 'quantity', 'subtotal')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'payment_status', 'total', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('order_number', 'user__email', 'user__username')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    list_editable = ('status', 'payment_status')
    
    fieldsets = (
        ('Order Info', {'fields': ('order_number', 'user', 'status', 'payment_status')}),
        ('Shipping Details', {'fields': ('shipping_address', 'shipping_city', 'shipping_state', 
                                          'shipping_country', 'shipping_postal_code', 'phone_number')}),
        ('Pricing', {'fields': ('subtotal', 'shipping_cost', 'tax', 'total')}),
        ('Additional', {'fields': ('notes', 'created_at', 'updated_at')}),
    )
