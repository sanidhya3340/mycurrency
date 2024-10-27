from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from datetime import timedelta
from .models import Currency
from .providers import ProviderFactory
from .serializers import (
    CurrencySerializer,
    CurrencyRateRequestSerializer,
    CurrencyConvertRequestSerializer
)

# Unified Currency CRUD API
class CurrencyAPIView(APIView):
    """
    Handles full CRUD operations for Currency:
    - GET (list all or retrieve one)
    - POST (create)
    - PUT (update)
    - DELETE (remove)
    """

    def get(self, request, code=None):
        if code:
            # Retrieve a specific currency by code
            currency = get_object_or_404(Currency, code=code)
            serializer = CurrencySerializer(currency)
            return Response(serializer.data)
        else:
            # List all currencies
            currencies = Currency.objects.all()
            serializer = CurrencySerializer(currencies, many=True)
            return Response(serializer.data)

    def post(self, request):
        # Create a new currency
        serializer = CurrencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, code):
        # Update an existing currency
        currency = get_object_or_404(Currency, code=code)
        serializer = CurrencySerializer(currency, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, code):
        # Delete an existing currency
        currency = get_object_or_404(Currency, code=code)
        currency.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Currency Exchange Rate API
class CurrencyExchangeRateAPIView(APIView):
    """
    Handles retrieving the latest exchange rate or rates for a specific date range.
    """
    def get(self, request):
        # Validate query parameters
        serializer = CurrencyRateRequestSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        source_currency = validated_data.get("source_currency")
        target_currency = validated_data.get("target_currency")
        date_from = validated_data.get("date_from")
        date_to = validated_data.get("date_to")

        provider = ProviderFactory()

        # Handle rate fetching for a specific date range
        if date_from and date_to:
            if date_from > date_to:
                return Response({"error": "'date_from' must be before 'date_to'."}, status=status.HTTP_400_BAD_REQUEST)

            current_date = date_from
            rates = []
            while current_date <= date_to:
                rate = provider.get_exchange_rate(source_currency, target_currency, current_date)
                
                # Validate and handle missing rate
                if rate is None:
                    return Response({"error": f"Could not retrieve rate for {current_date}."}, status=status.HTTP_404_NOT_FOUND)

                rates.append({
                    "date": current_date,
                    "rate": float(rate)
                })
                current_date += timedelta(days=1)

            return Response({
                "source_currency": source_currency,
                "target_currency": target_currency,
                "rates": rates
            })

        # Fetch single latest rate if no date range is specified
        latest_rate = provider.get_exchange_rate(source_currency, target_currency)
        if latest_rate is None:
            return Response({"error": "Could not retrieve the latest exchange rate."}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "source_currency": source_currency,
            "target_currency": target_currency,
            "rate": float(latest_rate)
        })

# Currency Conversion API
class CurrencyConversionAPIView(APIView):
    """
    Handles currency conversion using the latest available exchange rates.
    """
    def get(self, request):
        # Validate query parameters
        serializer = CurrencyConvertRequestSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        source_currency = validated_data.get("source_currency")
        target_currency = validated_data.get("target_currency")
        amount = validated_data.get("amount")

        provider = ProviderFactory()
        rate = provider.get_exchange_rate(source_currency, target_currency)
        
        # Validate and handle missing rate
        if rate is None:
            return Response({"error": "Could not retrieve the exchange rate for conversion."}, status=status.HTTP_404_NOT_FOUND)

        converted_amount = amount * float(rate)

        return Response({
            "source_currency": source_currency,
            "target_currency": target_currency,
            "amount": amount,
            "converted_amount": converted_amount,
            "rate": float(rate)
        })
