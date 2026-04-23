from django import forms
from .models import Gasto, Gasto_Fixo, Compromissos


class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ["nome", "data_gasto", "classificacao", "valor"]

        widgets = {
            "data_gasto": forms.DateInput(attrs={"type": "date"}),
            "valor": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
        }

class LoginForms(forms.Form):
    nome_login=forms.CharField(
        label="Usuário",
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class":"form-control",
            }
        )
    )
    senha=forms.CharField(
        label="Senha",
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control"
            }
        )
    )

class GastoFixoForm(forms.ModelForm):
    class Meta:
        model = Gasto_Fixo
        fields = ["nome", "data_compensacao", "classificacao", "valor_provisonado"]

        widgets = {
            "data_compensacao": forms.NumberInput(attrs={"type": "number"}),
            "valor_provisonado": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
        }

class CompromissoForm(forms.ModelForm):
    class Meta:
        model = Compromissos
        fields = ["nome", "data_compromisso", "classificacao", "valor_provisonado","valor_pago"]

        widgets = {
            "data_compromisso": forms.NumberInput(attrs={"type": "number"}),
            "valor_provisonado": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
        }
