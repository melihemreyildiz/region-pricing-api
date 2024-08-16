from rest_framework import serializers


class AveragePriceSerializer(serializers.Serializer):
    day = serializers.DateField()
    average_price = serializers.IntegerField(allow_null=True)


class RateQuerySerializer(serializers.Serializer):
    date_from = serializers.DateField(required=True, format='%Y-%m-%d')
    date_to = serializers.DateField(required=True, format='%Y-%m-%d')
    origin = serializers.CharField(required=True)
    destination = serializers.CharField(required=True)