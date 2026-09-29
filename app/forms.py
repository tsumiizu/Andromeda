import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Usuario, Servico, Plano

class CadastroUsuarioForm(forms.ModelForm):
    nome_completo = forms.CharField(
        max_length=150, 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nome completo do cliente'})
    )
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}),
        required=False
    )
    class Meta:
        model = Usuario
        fields = ['nome_completo', 'cpf_cnpj', 'telefone', 'email', 'senha']

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if not (self.instance and self.instance.pk):
                self.fields['senha'].required = True
            else:
                self.fields['nome_completo'].initial = self.instance.get_full_name()
                
            # Garante que os campos extras de endereço/foto sejam explicitamente opcionais
            campos_opcionais = ['cpf_cnpj', 'telefone', 'foto', 'cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado']
            for campo in campos_opcionais:
                if campo in self.fields:
                    self.fields[campo].required = False

    def clean_cpf_cnpj(self):
        doc_raw = self.cleaned_data.get('cpf_cnpj', '')
        if not doc_raw: return None
        doc_limpo = re.sub(r'\D', '', doc_raw)
        if len(doc_limpo) not in [11, 14]:
            raise ValidationError('Informe um CPF (11 dígitos) ou CNPJ (14 dígitos) válido.')
        if Usuario.objects.filter(cpf_cnpj=doc_limpo).exists():
            raise ValidationError('Este CPF/CNPJ já está cadastrado.')
        return doc_limpo

    def clean_telefone(self):
        tel_raw = self.cleaned_data.get('telefone', '')
        if not tel_raw: return None
        return re.sub(r'\D', '', tel_raw)

    def save(self, commit=True):
        user = super().save(commit=False)
        nome_completo = self.cleaned_data.get('nome_completo', '').strip()
        nomes = nome_completo.split(' ', 1)
        user.first_name = nomes[0]
        user.last_name = nomes[1] if len(nomes) > 1 else ''
        user.username = user.email
        senha = self.cleaned_data.get('senha')
        if senha:
            user.set_password(senha)
        if commit:
            user.save()
        return user

class FotoPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['foto']

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado']

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'descricao', 'preco', 'capa']

class PlanoForm(forms.ModelForm):
    class Meta:
        model = Plano
        fields = ['servico', 'nome', 'descricao', 'preco', 'capa']