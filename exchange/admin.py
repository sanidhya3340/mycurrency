from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .admin_views import currency_converter_view
from .models import Currency, CurrencyExchangeRate, Provider

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'symbol']
    search_fields = ['code', 'name']
    def currency_converter_link(self, obj):
        url = reverse('admin:currency_converter')
        return format_html('<a href="{}">Currency Converter</a>', url)

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('currency-converter/', self.admin_site.admin_view(currency_converter_view))
        ]
        return custom_urls + urls

@admin.register(CurrencyExchangeRate)
class CurrencyExchangeRateAdmin(admin.ModelAdmin):
    list_display = ['source_currency', 'exchanged_currency', 'valuation_date', 'rate_value']
    list_filter = ['source_currency', 'exchanged_currency']
    search_fields = ['source_currency__code', 'exchanged_currency__code']

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'priority']
    list_editable = ['is_active', 'priority']
    ordering = ['priority']
