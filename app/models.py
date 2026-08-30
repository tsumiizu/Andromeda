from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser

class Plano(models.Model):
    nome = models.CharField(max_length=250)
    descricao = models.TextField(blank=False, null=False)
    preco = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    capa = models.ImageField(upload_to='planos/')
    # Mudar para esse aqui antes de subir pro push:
    # capa = CloudinaryField('image', folder='planos/', null=True, blank=True)

# Usuário custom para incluir CPF e email 
class Usuario(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    cpf_cnpj = models.CharField(max_length=14, unique=True, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=False, null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.email})"