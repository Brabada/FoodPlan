from datetime import datetime, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import CustomUserCreationForm, OrderForm
from .models import Dish, Subscription, MealType
from foodplan.settings import BASE_PRICE, BULK_DISCOUNT


def index(request):
    return render(request, 'index.html')

@login_required(login_url='auth')
def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            menu_category = form.cleaned_data['menu_category']
            allergies = form.cleaned_data['allergies']
            month_count = form.cleaned_data['month_count']
            portion_quantity = form.cleaned_data['portion_quantity']
            meal_type_ids = list(map(int, form.cleaned_data['meal_types']))

            subscription = Subscription.objects.create(
                user = request.user,
                expires_at=datetime.now() + timedelta(days=month_count*30),
                portion_quantity=portion_quantity,
                menu_category=menu_category,
            )
            subscription.allergies.set(allergies)
            subscription.meal_types.set(MealType.objects.filter(id__in=meal_type_ids))

            price = BASE_PRICE * month_count * subscription.meal_types.count()
            if month_count > 1:
                price = int(price * (100 - BULK_DISCOUNT) / 100)

            context = {
                'subscription': subscription,
                'price': price,
                'month_count': month_count,
            }
            return render(request, 'order_confirm.html', context=context)
    else:
        form = OrderForm()

    context = {
        'form': form,
    }
    return render(request, 'order.html', context=context)


@login_required(login_url='auth')
def lk(request):
    return render(request, 'lk.html')


def dish(request, dish_id=None):
    if dish_id is None:
        dish = Dish.objects.filter(is_free=True).order_by('?').first()
    else:
        dish = get_object_or_404(Dish, pk=dish_id)
    context = {
        'dish': dish,
    }
    return render(request, 'dish.html', context=context)


def register(request, redirect_to_order='False'):

    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'GET':
        request.session['redirect_to_order'] = redirect_to_order
        print(f"0 {request.session['redirect_to_order']}")

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, new_user)
            if request.session['redirect_to_order'] == 'True':
                print(f"1 {request.session['redirect_to_order']}")
                del request.session['redirect_to_order']
                return redirect('order')
            else:
                print(f"2 {request.session['redirect_to_order']}")
                del request.session['redirect_to_order']
                return redirect('index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }

    return render(request, 'auth/register.html', context=context)


def contacts(request):
    return render(request, 'contacts.html')


def auth(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'auth/auth.html')


@login_required(login_url='auth')
def logged_out(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'auth/logged_out.html')
