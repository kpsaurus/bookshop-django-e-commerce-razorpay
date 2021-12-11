from django import forms


class MakeOrderForm(forms.Form):
    selected_product = forms.IntegerField()


class PaymentGatewayResponse(forms.Form):
    razorpay_payment_id = forms.CharField(max_length=50, required=True)
    razorpay_order_id = forms.CharField(max_length=50, required=True)
    razorpay_signature = forms.CharField(max_length=500, required=True)
