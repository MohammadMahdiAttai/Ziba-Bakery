from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from catalog.models import Product
from .forms import ContactForm


def home(request):
    featured_products = Product.objects.filter(available=True).order_by('-created')[:4]
    return render(request, 'core/home.html', {'featured_products': featured_products})


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                subject=f"Ziba Bakery enquiry from {form.cleaned_data['name']}",
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=['hello@zibabakery.example.com'],
                fail_silently=True,
            )
            messages.success(request, "Thanks for reaching out — we'll reply within one business day.")
            return redirect('core:contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})
