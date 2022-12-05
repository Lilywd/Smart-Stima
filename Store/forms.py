from django import forms


class BillingForm(forms.Form):
    first_name = forms.CharField (widget=forms.TextInput(attrs={'class': 'form__input'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input'}))
    apartment = forms.CharField (widget=forms.TextInput(attrs={'class': 'form__input'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input'}))
    country = forms.ChoiceField()
    zip = forms.CharField (widget=forms.TextInput(attrs={'class': 'form__input'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form__input'}))


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input'}))
