from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from .models import User, Plan
from .forms import User_registration, User_login
from django.contrib import messages
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json
import requests

plan_period = 1
selected_plan = 1

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def signup(req):
    if req.method == 'POST':
        fm = User_registration(req.POST)
        try:
            user = User.objects.get(email = req.POST.get('email'))
        except User.DoesNotExist:
            user = None
        
        if fm.is_valid() and user==None:
            fm.save()
            messages.success(req, 'User registration successful')
            fm=User_registration()

        elif user!=None:
            messages.warning(req, 'User Already Registered')
            fm = User_login()
            return render(req, 'login.html', {'form': fm})
        else:
            messages.warning(req, "Please provide valid details!")
    else:
        fm = User_registration()
    return render(req, 'signup.html', {'form':fm})


def login(req):
    if req.method == 'POST':
        try:
            user = User.objects.get(email = req.POST.get('email'))
        except User.DoesNotExist:
            user = None
        
        if user != None: 
            user.is_loggedin = True
            user.save()
            return redirect('choosen_plan', user_id=user.id, plan_id=selected_plan)
        else:
            messages.warning(req, "Please provide valid details!")
            fm = User_login()
            return render(req, 'login.html', {'form':fm})
    else:
        fm = User_login()
        return render(req, 'login.html', {'form':fm})


def monthly_plans(req, user_id):
    if not User.objects.get(pk=user_id).is_authenticated():
        return redirect('signup')
    if req.method == 'POST':
        return redirect('choosen_plan', user_id=user_id, plan_id=selected_plan)

    user = User.objects.get(pk=user_id)
    user.plan_period = 1
    user.save()
    global plan_period
    plan_period = user.plan_period
    return redirect('choosen_plan', user_id=user_id, plan_id=selected_plan)


def annual_plans(req, user_id):
    if not User.objects.get(pk=user_id).is_authenticated():
        return redirect('signup')
    if req.method == 'POST':
        return redirect('choosen_plan', user_id=user_id, plan_id=selected_plan)

    user = User.objects.get(pk=user_id)
    user.plan_period = 12
    user.save()
    global plan_period
    plan_period = user.plan_period
    return redirect('choosen_plan', user_id=user_id, plan_id=selected_plan)


def choosen_plan(req, user_id, plan_id, do_post=True):
    if not User.objects.get(pk=user_id).is_authenticated():
        return redirect('signup')
    if req.method == 'POST' and do_post:
        # MY_DOMAIN = 'http://127.0.0.1:8000/'
        MY_DOMAIN = 'https://prajwalrichpanel.herokuapp.com/'
        data = User.objects.get(pk=user_id).duration()
        if data == 1:
            duration = 'Monthly'
        else:
            duration = 'Annually'
        
        if duration == 'Monthly':
            price = Plan.objects.get(id=plan_id).m_price()
        else:
            price = Plan.objects.get(id=plan_id).a_price()

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': Plan.objects.get(pk=plan_id),
                            'description': duration,
                        },
                        'unit_amount': int(price)*100,
                    },
                    'quantity': 1,
                },
            ],
            mode = 'payment',
            
            success_url = MY_DOMAIN + 'success/' + str(user_id) + '/' + str(plan_id),
            cancel_url =  MY_DOMAIN + 'cancel',
        )
        return redirect(checkout_session.url)

    pl = Plan.objects.all()
    user = User.objects.get(pk=user_id)
    plan = Plan.objects.get(pk=plan_id)
    global selected_plan 
    selected_plan = plan.id
    global plan_period 
    plan_period= user.plan_period
    if plan_period == 1:
        return render(req, 'dashboard.html', {'plans' : pl, 'user' : user, 'plan_period' : plan_period, 'selected_plan' : selected_plan, 'monthly' : 'selected'})
    else:
        return render(req, 'dashboard.html', {'plans' : pl, 'user' : user, 'plan_period' : plan_period, 'selected_plan' : selected_plan, 'yearly' : 'selected'})


def success(req, user_id, plan_id):
    if not User.objects.get(pk=user_id).is_authenticated():
        return redirect('signup')
    
    plan_name = Plan.objects.get(pk=plan_id)
    user = User.objects.get(pk=user_id)
    
    plan_name.user = user
    plan_name.save()
    if(user.plan_period==1):
        period = 'Monthly'
    else:
        period = 'Annually'
    
    if period == 'Monthly':
        price = Plan.objects.get(pk=plan_id).m_price()
    else:
        price = Plan.objects.get(pk=plan_id).a_price()
    
    context = {
        'plan_name': plan_name,
        'price': price,
        'period': period,
        'user': user
    }
    return render(req, 'success.html', context)


def cancel(req):
    return render(req, 'cancel.html')


def logout(req, user_id):
    print(user_id)
    user = User.objects.get(pk=user_id)
    user.is_loggedin = False
    user.save()
    return redirect('signup')