from django.shortcuts import render, HttpResponse
from apps.exchangerate.models import ExchangeRateLog
from system.utils import paginate_data
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Plan, Subscription, Wallet, ExchangeRateLog
from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from decimal import Decimal

# Create your views here.
def exchange_rate_list(request):
    if request.method == 'POST':
        data = ExchangeRateLog.objects.all().order_by('-id')
        # print('data : ', data)
        response_data, page_data = paginate_data(ExchangeRateLog, data, request)  
        count = 0
        for data in page_data:  
            count += 1
            response_data['data'].append({
                'count' : count,
                'base_currency' : data.base_currency,
                'target_currency' : data.target_currency,
                'rate' : data.rate,
                'fetched_at' : data.fetched_at.strftime('%Y-%m-%d %I:%M:%S %p')

            })
        return JsonResponse(response_data)
    
    return render(request, 'backend/main/exchange_rate/exchange_rate_list.html') 

@csrf_exempt
@api_view(['POST'])
def register_view(request):
    if request.method != 'POST':
        return Response({'error': 'Method must be POST'})
    username = request.data.get('username')
    password = request.data.get('password')
    if username and password:
        user = User.objects.create_user(username=username, password=password)
        Wallet.objects.create(user=user, balance=1000.00)
        return Response({'msg': 'User created'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({'error': 'Invalid Method'})

@api_view(['GET'])
def get_user_data(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Unauthorized'}, status=401)
    wallet = Wallet.objects.get(user=request.user)
    try:
        subscription = Subscription.objects.filter(user=request.user).latest('start_date')
        subscription_status = subscription.status
    except Subscription.DoesNotExist:
        subscription_status = 'none'
    return Response({
        'username': request.user.username,
        'wallet_balance': float(wallet.balance),
        'subscription_status': subscription_status
    })
@api_view(['GET'])
def plan_list_view(request):
    plans = Plan.objects.all()
    data = []
    for plan in plans:
        data.append({
            'id': plan.id,
            'name': plan.name,
            'price_usd': float(plan.price),
            'duration_days': plan.duration_days
        })
    return Response(data)

@api_view(['POST'])
def make_subscription(request):
    if request.method != 'POST':
        return Response({'error': 'Method must be POST'})
    user = request.user
    plan_id = request.data.get('plan_id')
    if not plan_id:
        return Response({'error': 'Missing plan_id'})
    try:
        plan = Plan.objects.get(id=plan_id)
        rate = ExchangeRateLog.objects.latest('fetched_at').rate
        cost_bdt = Decimal(str(plan.price)) * Decimal(str(rate))
        print('cost bdt : ', cost_bdt, type(cost_bdt))
        wallet = Wallet.objects.get(user=user)
        if wallet.balance < cost_bdt:
            return Response({'error': 'Insufficient balance'})
        print('wallet balance: ', wallet.balance, type(wallet.balance))
        with transaction.atomic():
            wallet.balance -= cost_bdt
            wallet.save()

            Subscription.objects.create(
                user=user,
                plan=plan,
                start_date=timezone.now(),
                end_date=timezone.now() + timedelta(days=plan.duration_days),
                status='active'
            )
        return Response({'msg': 'Subscribed successfully'})
    except Plan.DoesNotExist:
        return Response({'error': 'Plan not found'})
    except Exception as e:
        return Response({'error': str(e)})

@api_view(['POST'])
def cancel_subscription(request):
    if request.method != 'POST':
        return Response({'error': 'Method must be POST'})
    user = request.user
    try:
        subscription = Subscription.objects.filter(user=user, status='active').latest('start_date')
        now = timezone.now()
        days_passed = (now - subscription.start_date).days
        plan_price_usd = Decimal(subscription.plan.price)
        rate = Decimal(ExchangeRateLog.objects.latest('fetched_at').rate)
        total_cost = plan_price_usd * rate
        refund = Decimal('0.00')
        if days_passed <= 7:
            refund = total_cost
        else:
            per_day_cost = total_cost / Decimal('30')
            refund = total_cost - (Decimal(days_passed) * per_day_cost)

        with transaction.atomic():
            wallet = Wallet.objects.get(user=user)
            wallet.balance += refund
            wallet.save()

            subscription.status = 'cancelled'
            subscription.save()

        return Response({'msg': 'Subscription cancelled', 'refund': round(float(refund), 2)})
    except Subscription.DoesNotExist:
        return Response({'error': 'No active subscription'})
    except Exception as e:
        return Response({'error': str(e)})

def all_user_subscription_list(request):
    if request.method == 'POST':
        data = Subscription.objects.all().order_by('-id')
        # print('data : ', data)
        response_data, page_data = paginate_data(Subscription, data, request)  
        count = 0
        for data in page_data:  
            count += 1
            response_data['data'].append({
                'count' : count,
                'user' : data.user.username,
                'plan' : data.plan.name,
                'start_date' : data.start_date.strftime('%Y-%m-%d %I:%M:%S %p'),
                'end_date' : data.end_date.strftime('%Y-%m-%d %I:%M:%S %p'),
                'status' : data.status

            })
        return JsonResponse(response_data)
    
    return render(request, 'backend/main/exchange_rate/all_subscription_user_list.html') 


