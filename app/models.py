from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from cloudinary.models import CloudinaryField
from cloudinary.utils import cloudinary_url
from django.templatetags.static import static
import random
from django.contrib.auth.models import AbstractUser

DEFAULT_AVATARS = [
    'avatar_default01',
    'avatar_default02',
    'avatar_default03',
    'avatar_default04',
    'avatar_default05',
    'avatar_default06',
    'avatar_default07',
]
def get_random_avatar():
    return random.choice(DEFAULT_AVATARS)

class Plano(models.Model):
    nome = models.CharField(max_length=250)
    descricao = models.TextField(blank=False, null=False)
    preco = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    # capa = models.ImageField(upload_to='media/planos/')
    capa = CloudinaryField('image', folder='planos/', default='default', null=True, blank=True)
    @property
    def capa_url(self):
        if self.capa and hasattr(self.capa, 'url') and self.capa.url: 
            return self.capa.url
        if self.capa:
            capa_str = str(self.capa)
            if capa_str and not capa_str.startswith('static/'):
                url, _ = cloudinary_url(capa_str)
                return url
        url, _ = cloudinary_url('planos/default') 
        return url

class Usuario(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    cpf_cnpj = models.CharField(max_length=14, unique=True, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    # foto = models.ImageField(upload_to='media/perfis/', blank=True, null=True)
    foto = CloudinaryField('image', folder='perfis/', null=True, blank=True)

    cep = models.CharField(max_length=9, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def save(self, *args, **kwargs):
        if not self.pk and not self.foto:
            self.foto = get_random_avatar()
        elif self.foto == 'perfis/default05':
            self.foto = get_random_avatar()   
        super().save(*args, **kwargs)
    @property
    def foto_url(self):
        if not self.foto:
            url, _ = cloudinary_url(get_random_avatar(), secure=True)
            return url
        if hasattr(self.foto, 'url') and self.foto.url:
            return self.foto.url
        foto_str = str(self.foto)
        if foto_str == 'perfis/default05':
            url, _ = cloudinary_url(get_random_avatar(), secure=True)
            return url
        url, _ = cloudinary_url(foto_str, secure=True)
        return url
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.email})"
