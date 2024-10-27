import os
import requests
import random
from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal
from .provider_registry import register_provider, get_provider
from .models import Provider

# Abstract Interface for Currency Providers
class CurrencyProviderInterface(ABC):
    @abstractmethod
    def get_exchange_rate(self, source_currency: str, target_currency: str, valuation_date: date = None) -> Decimal:
        """Retrieve the exchange rate from source to target currency for a specific date or latest."""
        pass

# CurrencyBeacon Provider
class CurrencyBeaconProvider(CurrencyProviderInterface):
    API_URL = os.getenv("CURRENCY_BEACON_API_URL", "https://api.currencybeacon.com/v1")
    API_KEY = os.getenv("CURRENCY_BEACON_API_KEY", "LNhV0SbxfG4L1HeXaNGyX3SeZ1RIA6db")

    def get_exchange_rate(self, source_currency: str, target_currency: str, valuation_date: date = None) -> Decimal:
        if valuation_date is None:
            return self.get_latest_rate(source_currency, target_currency)
        else:
            return self.get_historical_rate(source_currency, target_currency, valuation_date)

    def get_latest_rate(self, source_currency: str, target_currency: str) -> Decimal:
        try:
            response = requests.get(
                f"{self.API_URL}/latest",
                params={"api_key": self.API_KEY, "base": source_currency, "symbols": target_currency}
            )
            data = response.json()
            rate = data.get("rates", {}).get(target_currency)
            return Decimal(rate) if rate else Decimal("0.0")
        except Exception as e:
            print(f"Error fetching latest rate from CurrencyBeacon: {e}")
            return Decimal("0.0")

    def get_historical_rate(self, source_currency: str, target_currency: str, valuation_date: date) -> Decimal:
        try:
            response = requests.get(
                f"{self.API_URL}/historical",
                params={
                    "api_key": self.API_KEY,
                    "base": source_currency,
                    "symbols": target_currency,
                    "date": valuation_date.strftime("%Y-%m-%d")
                }
            )
            data = response.json()
            rate = data.get("rates", {}).get(target_currency)
            return Decimal(rate) if rate else Decimal("0.0")
        except Exception as e:
            print(f"Error fetching historical rate from CurrencyBeacon: {e}")
            return Decimal("0.0")

# Register CurrencyBeaconProvider
register_provider('currencybeacon', CurrencyBeaconProvider)

# Mock Provider for Testing
class MockCurrencyProvider(CurrencyProviderInterface):
    def get_exchange_rate(self, source_currency: str, target_currency: str, valuation_date: date = None) -> Decimal:
        return Decimal(random.uniform(0.5, 1.5))

# Register MockCurrencyProvider
register_provider('mock', MockCurrencyProvider)

# Provider Factory
class ProviderFactory:
    def __init__(self):
        self.providers = self.load_providers()

    def load_providers(self):
        provider_objects = Provider.objects.filter(is_active=True).order_by('priority')
        providers = []

        for provider in provider_objects:
            try:
                provider_class = get_provider(provider.name)
                providers.append(provider_class())
            except ValueError as e:
                print(f"Error: {e}")

        return providers

    def get_exchange_rate(self, source_currency: str, target_currency: str, valuation_date: date = None) -> Decimal:
        for provider in self.providers:
            rate = provider.get_exchange_rate(source_currency, target_currency, valuation_date)
            if rate > 0:
                return rate
        raise ValueError("No valid exchange rate found from available providers")
