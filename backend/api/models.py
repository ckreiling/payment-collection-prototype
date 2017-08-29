from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
import random
import string


class SurveyCode:
    """
    Callable class for generating a UserProfile's survey code at instantiation
    """

    def __call__(self, *args, **kwargs):
        ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile_and_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Fun pub-sub for generating both a Token and UserProfile for each User creation
    """
    if created:
        Token.objects.create(user=instance)
        UserProfile.objects.create(user=instance)


class UserProfile(models.Model):
    """
    Extends Django's User object to create a profile for the user. This profile has all of the client-facing material
    attached to it:
        - Payers
        - Payment Plans
    It also has all of the non-client-facing material attached to it, specifically for Venmo's Oauth2.0 setup.
    These models are built for a Venmo developer API that has unfortunately been deprecated. Until
    there is a developer API available, the OAuth2.0 tokens will be left blank. This will clear up
    possible database migration issues when Venmo brings their API back online for new applications.
    """
    user = models.OneToOneField('auth.User', related_name='profile', on_delete=models.CASCADE)
    venmo_handle = models.CharField(max_length=50)
    venmo_auth_token = models.CharField(max_length=100, blank=True)
    venmo_refresh_token = models.CharField(max_length=100, blank=True)
    # Random code for the survey that retrieves the organization's users
    survey_code = models.CharField(unique=True, default=SurveyCode, max_length=10)
    """
    reverse model documentation
    payers = array of Payer
    payment_plans = array of PaymentPlanOption
    """

    def __str__(self):
        return self.user.username


class PaymentPlanOption(models.Model):
    """
    Defines a payment plan option, to be selected by a payer upon filling out the corresponding survey.
    """
    option_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='payment_plans')
    """
    reverse model documentation
    payments = array of Payment
    """

    class Meta:
        order_with_respect_to = 'user_profile'

    def __str__(self):
        return self.option_name


class Payment(models.Model):
    """
    Defines a single payment, with the date that it is due and the amount that is due on that date. A foreign key
    associates many of these with one PaymentPlanOption.
    """
    date_due = models.DateTimeField()
    amount_due = models.DecimalField(decimal_places=2, max_digits=10)
    # The PaymentPlanOption this payment is associated with
    payment_plan = models.ForeignKey(PaymentPlanOption, null=True, blank=True, on_delete=models.CASCADE,
                                     related_name='payments')

    class Meta:
        order_with_respect_to = 'payment_plan'

    def __str__(self):
        return self.date_due.__str__() + ', ' + self.amount_due.__str__()


class Payer(models.Model):
    """
    These represent a single payer in an organization. These are associated with a UserProfile so the collector
    can easily request funds from them based on their chosen payment plan.
    """
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    # The payment plan this user is on
    payment_plan = models.ForeignKey(PaymentPlanOption, on_delete=models.CASCADE, related_name='payers')
    venmo_username = models.CharField(max_length=50, blank=True, unique=True, verbose_name="payer's venmo username")
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    # Information regarding the last time the user had paid
    last_pay_date = models.DateTimeField(null=True, verbose_name="last date the payer paid")
    last_pay_amount = models.DecimalField(decimal_places=2, max_digits=10, null=True,
                                          verbose_name="last transaction amount")
    next_pay_date = models.DateTimeField(null=True)
    next_pay_amount = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # The user this Payer is identified with
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="payers")

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ': ' + self.payment_plan.__str__()

    class Meta:
        order_with_respect_to = 'user_profile'


class Transaction(models.Model):
    """
    A transaction made by the Payer. One of these is automatically generated whenever a Payer makes a Venmo transaction.
    """
    date = models.DateTimeField(verbose_name="date of transaction")
    amount = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="transaction amount")
    payer = models.ForeignKey(Payer, on_delete=models.CASCADE, related_name="transactions")

    class Meta:
        order_with_respect_to = 'payer'
