from django.urls import path
from .views import CurrencyAPIView, CurrencyExchangeRateAPIView, CurrencyConversionAPIView
from .admin_views import currency_converter_view

urlpatterns = [
    path('currencies/', CurrencyAPIView.as_view(), name='currency-list-create'),
    path('currencies/<str:code>/', CurrencyAPIView.as_view(), name='currency-detail-update-delete'),
    path('rates/', CurrencyExchangeRateAPIView.as_view(), name='currency-rates'),
    path('convert/', CurrencyConversionAPIView.as_view(), name='currency-convert'),
    path('admin/currency-converter/', currency_converter_view, name='currency_converter'),
]
