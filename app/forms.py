import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Usuario

class CadastroUsuarioForm(forms.ModelForm):
    nome_completo = forms.CharField(
        max_length=150, 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nome completo do cliente'})
    )
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}),
        required=True
    )
    class Meta:
        model = Usuario
        fields = ['nome_completo', 'cpf_cnpj', 'telefone', 'email', 'senha']

    def clean_cpf_cnpj(self):
        doc_raw = self.cleaned_data.get('cpf_cnpj', '')
        doc_limpo = re.sub(r'\D', '', doc_raw)
        if len(doc_limpo) not in [11, 14]:
            raise ValidationError('Informe um CPF (11 dígitos) ou CNPJ (14 dígitos) válido.')
        if Usuario.objects.filter(cpf_cnpj=doc_limpo).exists():
            raise ValidationError('Este CPF/CNPJ já está cadastrado.')
        return doc_limpo

    def clean_telefone(self):
        tel_raw = self.cleaned_data.get('telefone', '')
        return re.sub(r'\D', '', tel_raw)

    def save(self, commit=True):
        user = super().save(commit=False)
        nome_completo = self.cleaned_data.get('nome_completo', '').strip()
        user.username = user.email
        user.set_password(self.cleaned_data['senha'])
        if commit:
            user.save()
        return user