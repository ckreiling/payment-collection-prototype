from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extends Django's User object to create a profile for the user. This profile has all of the client-facing material
    attached to it:
        - Payers
        - Payment Plans
    It also has all of the non-client-facing material attached to it, specifically for Venmo's Oauth2.0 setup.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    venmo_handle = models.CharField()
    venmo_auth_token = models.CharField()
    venmo_refresh_token = models.CharField()
    # Random code for the survey that retrieves the organization's users
    survey_code = models.CharField(unique=True)

    def __str__(self):
        return self.user.username


class PaymentPlanOption(models.Model):
    """
    Defines a payment plan option, to be selected by a payer upon filling out the corresponding survey.
    """
    option_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        order_with_respect_to = 'user'

    def __str__(self):
        return self.option_name


class Payment(models.Model):
    """
    Defines a single payment, with the date that it is due and the amount that is due on that date. A foreign key
    associates many of these with one PaymentPlanOption.
    """
    date_due = models.DateTimeField()
    amount_due = models.DecimalField(decimal_places=2)
    # The PaymentPlanOption this payment is associated with
    payment_plan = models.ForeignKey(PaymentPlanOption, on_delete=models.CASCADE)

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
    payment_plan = models.ForeignKey(PaymentPlanOption)
    venmo_username = models.CharField(blank=True, unique=True, verbose_name="payer's venmo username")
    email = models.EmailField()
    phone_number = models.CharField()
    date_created = models.DateTimeField(auto_now_add=True)
    # Information regarding the last time the user had paid
    last_pay_date = models.DateTimeField(null=True, verbose_name="last date the payer paid")
    last_pay_amount = models.DecimalField(decimal_places=2, null=True, verbose_name="last transaction amount")
    next_pay_date = models.DateTimeField(null=True)
    next_pay_amount = models.DecimalField(decimal_places=2, null=True)
    total_paid = models.DecimalField(decimal_places=2, verbose_name="total paid to the organization")
    # The user this Payer is identified with
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ': ' + self.payment_plan.__str__()

    class Meta:
        order_with_respect_to = 'user'


class Transaction(models.Model):
    """
    A transaction made by the Payer. One of these is automatically generated whenever a Payer makes a Venmo transaction.
    """
    date = models.DateTimeField(verbose_name="date of transaction")
    amount = models.DecimalField(decimal_places=2, verbose_name="transaction amount")
    payer = models.ForeignKey(Payer, on_delete=models.CASCADE)

    class Meta:
        order_with_respect_to = 'payer'
