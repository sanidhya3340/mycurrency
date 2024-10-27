from django.shortcuts import render
from django import forms
from .providers import ProviderFactory
from .models import Currency

class CurrencyConversionForm(forms.Form):
    source_currency = forms.ModelChoiceField(queryset=Currency.objects.all(), label="Source Currency")
    amount = forms.DecimalField(decimal_places=2, max_digits=18, label="Amount")
    target_currencies = forms.ModelMultipleChoiceField(queryset=Currency.objects.all(), label="Target Currencies")

def currency_converter_view(request):
    conversion_results = None
    if request.method == "POST":
        form = CurrencyConversionForm(request.POST)
        if form.is_valid():
            source_currency = form.cleaned_data['source_currency']
            amount = form.cleaned_data['amount']
            target_currencies = form.cleaned_data['target_currencies']

            provider = ProviderFactory()
            conversion_results = []
            for target_currency in target_currencies:
                if source_currency == target_currency:
                    continue
                rate = provider.get_exchange_rate(source_currency.code, target_currency.code)
                converted_amount = amount * rate
                conversion_results.append({
                    "source": source_currency.code,
                    "target": target_currency.code,
                    "rate": rate,
                    "converted_amount": converted_amount
                })
    else:
        form = CurrencyConversionForm()

    return render(request, "admin/currency_converter.html", {
        "form": form,
        "conversion_results": conversion_results
    })
