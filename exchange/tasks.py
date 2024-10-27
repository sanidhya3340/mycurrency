from celery import shared_task
from .providers import ProviderFactory
from .models import Currency, CurrencyExchangeRate
from datetime import timedelta, date

@shared_task
def load_historical_data(source_currency_code, target_currency_code, start_date, end_date):
    try:
        # Fetch the Currency objects based on the provided codes
        source_currency = Currency.objects.get(code=source_currency_code)
        target_currency = Currency.objects.get(code=target_currency_code)
    except Currency.DoesNotExist as e:
        print(f"Currency not found: {e}")
        return
    
    provider = ProviderFactory()
    current_date = start_date

    while current_date <= end_date:
        try:
            # Fetch rate for each date
            rate = provider.get_exchange_rate(source_currency.code, target_currency.code, current_date)
            
            # Save rate to DB using the actual Currency IDs
            if rate > 0:
                CurrencyExchangeRate.objects.update_or_create(
                    source_currency=source_currency,
                    exchanged_currency=target_currency,
                    valuation_date=current_date,
                    defaults={'rate_value': rate}
                )
                print(f"Successfully stored rate for {current_date}: {rate}")
            else:
                print(f"No rate found for {current_date}. Skipping...")
        except Exception as e:
            print(f"Failed to load rate for {current_date}: {e}")

        # Move to the next day
        current_date += timedelta(days=1)
    
    print(f"Historical data loaded from {start_date} to {end_date} for {source_currency_code} to {target_currency_code}")
