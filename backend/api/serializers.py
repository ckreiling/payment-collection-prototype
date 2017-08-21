from rest_framework import serializers
from .models import *

"""
For more serializer relations information, visit http://www.django-rest-framework.org/api-guide/relations/
"""


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PayerSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Payer
        exclude = ('user_profile',)


class PaymentPlanOptionSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = PaymentPlanOption
        exclude = ('user_profile',)


class UserProfileSerializer(serializers.ModelSerializer):
    payers = PayerSerializer(many=True, read_only=True)
    payment_plans = PaymentPlanOptionSerializer(many=True)

    class Meta:
        model = UserProfile
        exclude = ('venmo_auth_token', 'venmo_refresh_token',)
