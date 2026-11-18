from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart
from .forms import OrderCreateForm, PaymentForm
from .models import Order, OrderItem

DELIVERY_SESSION_KEY = 'checkout_delivery'


def order_create(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.info(request, "Your cart is empty — add something delicious first.")
        return redirect('catalog:product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            request.session[DELIVERY_SESSION_KEY] = form.cleaned_data
            return redirect('orders:order_payment')
    else:
        initial = request.session.get(DELIVERY_SESSION_KEY)
        if not initial:
            initial = {}
            if request.user.is_authenticated:
                initial = {
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'email': request.user.email,
                }
                if hasattr(request.user, 'profile'):
                    initial['address'] = request.user.profile.address
                    initial['suburb'] = request.user.profile.suburb
                    initial['postcode'] = request.user.profile.postcode
        form = OrderCreateForm(initial=initial)

    return render(request, 'orders/create.html', {'cart': cart, 'form': form})


def order_payment(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.info(request, "Your cart is empty — add something delicious first.")
        return redirect('catalog:product_list')

    delivery = request.session.get(DELIVERY_SESSION_KEY)
    if not delivery:
        messages.info(request, "Please enter your delivery details first.")
        return redirect('orders:order_create')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            for item in cart:
                if item['quantity'] > item['product'].stock:
                    messages.error(
                        request,
                        f"Sorry, only {item['product'].stock} of "
                        f"\"{item['product'].name}\" left in stock."
                    )
                    return redirect('cart:cart_detail')

            with transaction.atomic():
                order = Order.objects.create(
                    paid=True,
                    user=request.user if request.user.is_authenticated else None,
                    **delivery,
                )

                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity'],
                    )
                    item['product'].stock -= item['quantity']
                    item['product'].save()

            cart.clear()
            del request.session[DELIVERY_SESSION_KEY]
            return render(request, 'orders/created.html', {'order': order})
    else:
        form = PaymentForm()

    return render(request, 'orders/payment.html', {'cart': cart, 'form': form})


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/created.html', {'order': order})
