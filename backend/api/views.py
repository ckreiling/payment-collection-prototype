from rest_framework import mixins, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser

from .models import UserProfile
from . import models, serializers


class UserProfileDetail(APIView):
    """
    We write our own view here so the User, authenticated
    through the Token passed in the request's header, can get their
    information implicitly. Otherwise, user info would have to be
    passed through the URL, which is redundant since they must already be
    authenticated with a token to access this information.
    """

    def get(self, request, format=None):
        """
        Return the serialized information for the user in the request.
        """
        user_profile = models.UserProfile.objects.get(user=request.user)
        serializer = serializers.UserProfileSerializer(data=user_profile)
        # Check that the serialized information is valid!
        serializer.is_valid()
        return Response(serializer.validated_data)


class CreatePayer(mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """
    This view needs to be accessed by anyone - however, a new payer
    won't be created if they do not provide the unique survey code
    that will attach the payer information to the corresponding
    User.
    """

    def get_queryset(self):
        user_profile = models.UserProfile.objects.get(user=self.request.user)
        return models.Payer.objects.filter(user_profile=user_profile)

    serializer_class = serializers.PayerSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        user_profile = models.UserProfile.objects.get(user=self.request.user)
        serializer.save(user_profile=user_profile)

    def post(self, request, *args, **kwargs):
        if type(request.user) == AnonymousUser:
            # If the user isn't authenticated, find the user associated with the given survey code
            user_profile = models.UserProfile.objects.get(survey_code=request.data['survey_code'])
            user = user_profile.user
            request.user = user
        return self.create(request, *args, **kwargs)


class PayerDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        return models.Payer.objects.filter(user_profile=user_profile)

    serializer_class = serializers.PayerSerializer


class CreateTransaction(generics.CreateAPIView):
    def get_queryset(self):
        user_profile = models.UserProfile.objects.get(user=self.request.user)
        return models.Transaction.objects.filter(payer__user_profile=user_profile)

    serializer_class = serializers.TransactionSerializer


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        user_profile = models.UserProfile.objects.get(user=self.request.user)
        return models.Transaction.objects.filter(payer__user_profile=user_profile)

    serializer_class = serializers.TransactionSerializer


class CreatePaymentPlanOption(generics.CreateAPIView):
    def get_queryset(self):
        user_profile = models.UserProfile.objects.get(user=self.request.user)
        return models.PaymentPlanOption.objects.filter(user_profile=user_profile)

    serializer_class = serializers.PaymentPlanOptionSerializer

    def perform_create(self, serializer):
        user_profile = models.UserProfile.objects.get(user=self.request.user)
        serializer.save(user_profile=user_profile)


class PaymentPlanOptionDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        user_profile = models.UserProfile.objects.get(user=self.request.user)
        return models.PaymentPlanOption.objects.filter(user_profile=user_profile)

    serializer_class = serializers.PaymentPlanOptionSerializer


class CreatePayment(generics.CreateAPIView):
    def get_queryset(self):
        user_profile = models.UserProfile.objects.get(user=self.request.user)
        return models.Payment.objects.filter(payment_plan__user_profile=user_profile)

    serializer_class = serializers.PaymentSerializer


class PaymentDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        user_profile = models.UserProfile.objects.get(user=self.request.user)
        return models.Payment.objects.filter(payment_plan__user_profile=user_profile)

    serializer_class = serializers.PaymentSerializer
