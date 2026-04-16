from django import forms


class CustomerRequestForm(forms.Form):
    customer_request = forms.CharField(
        label="Describe what you need",
        widget=forms.Textarea(attrs={
            "class": "textarea",
            "rows": 6,
            "placeholder": "Example: I need to send KES 15,000 to my mother in Kisumu urgently."
        })
    )