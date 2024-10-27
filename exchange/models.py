from django.db import models

class CurrencyExchangeRate(models.Model):
    source_currency = models.ForeignKey('Currency', related_name='exchanges', on_delete=models.CASCADE)
    exchanged_currency = models.ForeignKey('Currency', on_delete=models.CASCADE)
    valuation_date = models.DateField(db_index=True)
    rate_value = models.DecimalField(db_index=True, decimal_places=6, max_digits=18)

    def __str__(self):
        return f"{self.source_currency.code} to {self.exchanged_currency.code} on {self.valuation_date} - Rate: {self.rate_value}"

class Currency(models.Model):   
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.code} - {self.name}"
    
class Provider(models.Model):
    PROVIDER_CHOICES = [
        ('currencybeacon', 'CurrencyBeacon'),
        ('mock', 'MockProvider'),
    ]
    
    name = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
    is_active = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(default=1)  # Lower numbers mean higher priority

    def __str__(self):
        return f"{self.get_name_display()} - {'Active' if self.is_active else 'Inactive'} (Priority: {self.priority})"