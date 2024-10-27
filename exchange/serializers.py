from rest_framework import serializers
from .models import Currency, CurrencyExchangeRate

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['code', 'name', 'symbol']

class CurrencyExchangeRateSerializer(serializers.ModelSerializer):
    source_currency = serializers.CharField(source='source_currency.code')
    exchanged_currency = serializers.CharField(source='exchanged_currency.code')

    class Meta:
        model = CurrencyExchangeRate
        fields = ['source_currency', 'exchanged_currency', 'valuation_date', 'rate_value']

class CurrencyRateRequestSerializer(serializers.Serializer):
    source_currency = serializers.CharField(required=True, max_length=3)
    target_currency = serializers.CharField(required=True, max_length=3)
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)

    def validate(self, data):
        #source and target currencies should't be same
        if data['source_currency'] == data['target_currency']:
            raise serializers.ValidationError("Source and target currencies must be different.")

        date_from = data.get("date_from")
        date_to = data.get("date_to")
        if date_from and date_to and date_from > date_to:
            raise serializers.ValidationError("'date_from' must be before 'date_to'.")
        
        return data

class CurrencyConvertRequestSerializer(serializers.Serializer):
    source_currency = serializers.CharField(required=True, max_length=3)
    target_currency = serializers.CharField(required=True, max_length=3)
    amount = serializers.FloatField(required=True, min_value=0.01)

    def validate(self, data):
        if data['source_currency'] == data['target_currency']:
            raise serializers.ValidationError("Source and target currencies must be different.")
        return data
