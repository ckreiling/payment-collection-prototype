import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from . import models


class TestCreateEndpoints(TestCase):
    """
    Test the endpoints to ensure that any client can successfully
    interact with the URLs defined in urls.py.
    """

    def setUp(self):
        User.objects.create_user(username='test_user',
                                 email='test@test.com',
                                 password='secret')
        self.user_profile = models.UserProfile.objects.get(user__username='test_user')
        self.token = Token.objects.get(user__username='test_user')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_payment_plan(self):
        payment_plan = {
            'option_name': 'Test Payment Plan!',
            'description': 'This is a test payment plan option creation.',
        }
        request = self.client.post(reverse('api:create_payment_plan'), data=payment_plan)
        assert request.status_code == 201

    def test_create_payment(self):
        payment_plan = models.PaymentPlanOption.objects.create(option_name='test option',
                                                               user_profile=self.user_profile)
        payment = {
            'date_due': datetime.datetime(year=2017, month=3, day=10),
            'amount_due': 100.00,
            'payment_plan': payment_plan.pk
        }
        request = self.client.post(reverse('api:create_payment'), data=payment)
        assert request.status_code == 201

    def test_create_payer_as_registered_user(self):
        payment_plan = models.PaymentPlanOption.objects.create(option_name='test option',
                                                               user_profile=self.user_profile)
        payer = {
            'first_name': 'John',
            'last_name': 'Doe',
            'venmo_username': 'john_doe',
            'email': 'john@doe.com',
            'phone_number': '5129874563',
            'payment_plan': payment_plan.pk,
            'survey_code': self.user_profile.survey_code
        }
        request = self.client.post(reverse('api:create_payer'), data=payer)
        assert request.status_code == 201

    def test_create_payer_as_anonymous_user(self):
        payment_plan = models.PaymentPlanOption.objects.create(option_name='test option',
                                                               user_profile=self.user_profile)
        payer = {
            'first_name': 'John',
            'last_name': 'Doe',
            'venmo_username': 'john_doe',
            'email': 'john@doe.com',
            'phone_number': '5129874563',
            'payment_plan': payment_plan.pk,
            'survey_code': self.user_profile.survey_code
        }
        # Disable the client header
        self.client.credentials()
        request = self.client.post(reverse('api:create_payer'), data=payer)
        # re-enable the client header
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        assert request.status_code == 201

    def test_create_transaction(self):
        payment_plan = models.PaymentPlanOption.objects.create(option_name='test option',
                                                               user_profile=self.user_profile)
        payer = models.Payer.objects.create(first_name='John',
                                            last_name='Doe',
                                            venmo_username='john_doe',
                                            email='john@doe.com',
                                            phone_number='5128763562',
                                            payment_plan=payment_plan,
                                            user_profile=self.user_profile)
        transaction = {
            'date': datetime.datetime(year=2015, month=5, day=10),
            'amount': 100.00,
            'payer': payer.pk
        }
        request = self.client.post(reverse('api:create_transaction'), data=transaction)
        assert request.status_code == 201


class TestRetrieveEndpoints(TestCase):
    def setUp(self):
        User.objects.create_user(username='test_user',
                                 email='test@test.com',
                                 password='secret')
        self.user_profile = models.UserProfile.objects.get(user__username='test_user')
        self.token = Token.objects.get(user__username='test_user')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_auth_token(self):
        data = {
            'username': self.user_profile.user.username,
            'password': 'secret'
        }
        request = self.client.post(reverse('api:auth'), data=data)
        assert request.status_code == 200

    def test_retrieve_user(self):
        request = self.client.get(reverse('api:user'))
        assert request.status_code == 200

    def test_retrieve_payer(self):
        payment_plan = models.PaymentPlanOption.objects.create(option_name='test option',
                                                               user_profile=self.user_profile)
        payer = models.Payer.objects.create(first_name='John',
                                            last_name='Doe',
                                            venmo_username='john_doe',
                                            email='john@doe.com',
                                            phone_number='5128763562',
                                            payment_plan=payment_plan,
                                            user_profile=self.user_profile)
        request = self.client.get(reverse('api:payer_detail', kwargs={'pk': payer.pk}))
        assert request.status_code == 200

    def test_retrieve_payment_plan_option(self):
        payment_plan = models.PaymentPlanOption.objects.create(option_name='test option',
                                                               user_profile=self.user_profile)
        request = self.client.get(reverse('api:payment_plan_detail', kwargs={'pk': payment_plan.pk}))
        assert request.status_code == 200 and request.data['option_name'] == 'test option'

    def test_retrieve_payment(self):
        payment_plan = models.PaymentPlanOption.objects.create(option_name='test option',
                                                               user_profile=self.user_profile)
        payment = models.Payment.objects.create(date_due=datetime.datetime(year=2017, month=5, day=10),
                                                amount_due=100.00,
                                                payment_plan=payment_plan)
        request = self.client.get(reverse('api:payment_detail', kwargs={'pk': payment.pk}))
        assert request.status_code == 200

    def test_retrieve_transaction(self):
        payment_plan = models.PaymentPlanOption.objects.create(option_name='test option',
                                                               user_profile=self.user_profile)
        payer = models.Payer.objects.create(first_name='John',
                                            last_name='Doe',
                                            venmo_username='john_doe',
                                            email='john@doe.com',
                                            phone_number='5128763562',
                                            payment_plan=payment_plan,
                                            user_profile=self.user_profile)
        transaction = models.Transaction.objects.create(date=datetime.datetime(year=2017, month=8, day=10),
                                                        amount=50.00,
                                                        payer=payer)
        request = self.client.get(reverse('api:transaction_detail', kwargs={'pk': transaction.pk}))
        assert request.status_code == 200
