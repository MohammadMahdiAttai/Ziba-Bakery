import re

from django import forms
from django.utils import timezone

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'suburb', 'postcode']
        widgets = {
            'address': forms.TextInput(attrs={'placeholder': 'Street address'}),
            'suburb': forms.TextInput(attrs={'placeholder': 'e.g. Carlton'}),
            'postcode': forms.TextInput(attrs={'placeholder': 'e.g. 3053'}),
        }


def _luhn_is_valid(digits):
    total = 0
    for i, d in enumerate(reversed([int(c) for c in digits])):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


class PaymentForm(forms.Form):
    card_number = forms.CharField(
        label='Card number', max_length=23,
        widget=forms.TextInput(attrs={
            'placeholder': '4242 4242 4242 4242', 'inputmode': 'numeric', 'autocomplete': 'cc-number',
        }),
        help_text='Demo only - try 4242 4242 4242 4242.',
    )
    expiry = forms.CharField(
        label='Expiry', max_length=5,
        widget=forms.TextInput(attrs={'placeholder': 'MM/YY', 'inputmode': 'numeric', 'autocomplete': 'cc-exp'}),
    )
    cvc = forms.CharField(
        label='CVC', max_length=4,
        widget=forms.TextInput(attrs={'placeholder': '123', 'inputmode': 'numeric', 'autocomplete': 'cc-csc'}),
    )

    def clean_card_number(self):
        raw = re.sub(r'[\s-]', '', self.cleaned_data['card_number'])
        if not raw.isdigit():
            raise forms.ValidationError('Card number must contain digits only.')
        if not (13 <= len(raw) <= 19):
            raise forms.ValidationError('That card number is the wrong length.')
        if not _luhn_is_valid(raw):
            raise forms.ValidationError('That card number doesn\'t look valid. Try 4242 4242 4242 4242 for this demo.')
        return raw

    def clean_expiry(self):
        value = self.cleaned_data['expiry'].strip()
        if not re.match(r'^(0[1-9]|1[0-2])/\d{2}$', value):
            raise forms.ValidationError('Use MM/YY format, e.g. 09/28.')
        month, year = value.split('/')
        expiry_year = 2000 + int(year)
        today = timezone.localdate()
        if (expiry_year, int(month)) < (today.year, today.month):
            raise forms.ValidationError('This card has expired.')
        return value

    def clean_cvc(self):
        value = self.cleaned_data['cvc'].strip()
        if not (value.isdigit() and 3 <= len(value) <= 4):
            raise forms.ValidationError('CVC must be 3 or 4 digits.')
        return value
