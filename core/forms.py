from django import forms


class MakeOrderForm(forms.Form):
    selected_product = forms.IntegerField()
