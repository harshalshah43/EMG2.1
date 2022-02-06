from .models import Quotation
from django import forms

class QuotationCreateForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ['price_quotated']