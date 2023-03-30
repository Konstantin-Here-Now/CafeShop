from django.contrib import admin
from .models import Coffee, Cheque


class CoffeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'photo', 'exist')
    list_display_links = ('id', 'name')
    list_editable = ('price',)
    list_filter = ('exist',)
    search_fields = ('name',)


admin.site.register(Coffee, CoffeeAdmin)


class ChequeAdmin(admin.ModelAdmin):
    list_display = ('date_printed', 'number', 'total_price')
    list_display_links = ('date_printed',)
    search_fields = ('date_printed',)


admin.site.register(Cheque, ChequeAdmin)
