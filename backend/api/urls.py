from django.conf.urls import url
from rest_framework.authtoken import views as drf_views

from . import views


urlpatterns = [
    # Post the username & password here to obtain the auth token
    url(r'^auth/$', drf_views.obtain_auth_token, name='auth'),
    url(r'^user/$', views.UserProfileDetail.as_view(), name='user'),
    url(r'^payer/create/$', views.CreatePayer.as_view(), name='create_payer'),
    url(r'^payer/(?P<pk>[0-9]+)/$', views.PayerDetail.as_view(), name='payer_detail'),
    url(r'^transaction/create/$', views.CreateTransaction.as_view(), name='create_transaction'),
    url(r'^transaction/(?P<pk>[0-9]+)/$', views.TransactionDetail.as_view(), name='transaction_detail'),
    url(r'^paymentplan/create/$', views.CreatePaymentPlanOption.as_view(), name='create_payment_plan'),
    url(r'^paymentplan/(?P<pk>[0-9]+)/$', views.PaymentPlanOptionDetail.as_view(), name='payment_plan_detail'),
    url(r'^payment/create/$', views.CreatePayment.as_view(), name='create_payment'),
    url(r'^payment/(?P<pk>[0-9]+)/$', views.PaymentDetail.as_view(), name='payment_detail')
]
