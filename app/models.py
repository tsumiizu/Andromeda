from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from cloudinary.models import CloudinaryField
from cloudinary.utils import cloudinary_url
from django.templatetags.static import static
import random
from django.contrib.auth.models import AbstractUser

DEFAULT_AVATARS = [
    'static/avatars/default01.jpg',
    'static/avatars/default02.png',
    'static/avatars/default03.png',
    'static/avatars/default04.png',
    'static/avatars/default05.png',
    'static/avatars/default06.jpg',
    'static/avatars/default07.jpg',
    'static/avatars/default08.jpg',
]

class Plano(models.Model):
    nome = models.CharField(max_length=250)
    descricao = models.TextField(blank=False, null=False)
    preco = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    # capa = models.ImageField(upload_to='media/planos/')
    capa = CloudinaryField('image', folder='planos/', null=True, blank=True)
    @property
    def capa_url(self):
        # 1. Verifica se existe o campo, se ele não é None e se tem atributo .url
        if self.capa and hasattr(self.capa, 'url') and self.capa.url:
            return self.capa.url
        
        # 2. Se for string do Public ID do Cloudinary (não nula)
        if self.capa:
            capa_str = str(self.capa)
            if capa_str and not capa_str.startswith('static/'):
                url, _ = cloudinary_url(capa_str)
                return url

        # 3. Fallback: Se for NULL/None ou vazio, devolve a imagem padrão estática
        return static('planos/default.jpg')

class Usuario(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    cpf_cnpj = models.CharField(max_length=14, unique=True, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    # foto = models.ImageField(upload_to='media/perfis/', blank=True, null=True)
    foto = CloudinaryField('image', folder='perfis/', default='perfis/default05', null=True, blank=True)

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
            self.foto = random.choice(DEFAULT_AVATARS)
        super().save(*args, **kwargs)
    @property
    def foto_url(self):
        if self.foto and hasattr(self.foto, 'url') and self.foto.url:
            return self.foto.url
        avatar_caminho = str(self.foto) if self.foto else random.choice(DEFAULT_AVATARS)
        if avatar_caminho.startswith('static/'):
            avatar_caminho = avatar_caminho.replace('static/', '', 1)
        return static(avatar_caminho)
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.email})"
