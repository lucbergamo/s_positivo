from django import forms
from .models import Gasto


class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ["nome", "data_gasto", "classificacao", "valor"]

        widgets = {
            "data_gasto": forms.DateInput(attrs={"type": "date"}),
            "valor": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
        }
