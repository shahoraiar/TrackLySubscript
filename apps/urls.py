from django.urls import path
from apps.exchangerate.views import *

urlpatterns = [
    path('', exchange_rate_list, name="exchange_rate_list"),
    path('subscription/list', all_user_subscription_list, name="all_user_subscription_list"),


    path('api/register', register_view, name="register_view"),
    path('api/login', login_view, name="login_view"),
    path('api/user/info', get_user_data, name="get_user_data"),
    path('api/plan/info', plan_list_view, name="plan_list_view"),


    path('api/subscription', make_subscription, name="make_subscription"),
    path('api/cancel/subscription', cancel_subscription, name="cancel_subscription"),


]

