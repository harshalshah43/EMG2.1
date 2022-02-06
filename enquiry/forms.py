from .models import Enquiry
from django import forms

class DateInput(forms.DateInput):
    input_type='date'

class EnquiryCreateForm(forms.ModelForm):
    class Meta:
        model=Enquiry
        widgets={'date_posted':DateInput()}
        fields='__all__'






