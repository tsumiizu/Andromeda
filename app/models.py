from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal
from cloudinary.models import CloudinaryField

class Plano(models.Model):
    nome = models.CharField(max_length=250)
    descricao = models.TextField(blank=False, null=False)
    preco = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    capa = models.ImageField(upload_to='planos/')
    # Mudar para esse aqui antes de subir pro push:
    # capa = CloudinaryField('image', folder='planos/', null=True, blank=True)