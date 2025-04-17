from django import forms
from .models import EducationPlace

class EducationPForm(forms.ModelForm):
    class Meta:
        model = EducationPlace
        fields = '__all__'
        widgets = {
            'data': forms.Textarea(attrs={'rows': 10, 'cols': 80}),
        }
