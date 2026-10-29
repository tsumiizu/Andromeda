from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from cloudinary.models import CloudinaryField
from cloudinary.utils import cloudinary_url
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

class Servico(models.Model):
    nome = models.CharField(max_length=250)
    descricao = models.TextField(blank=False, null=False)
    preco = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    capa = CloudinaryField('image', folder='serviços/', default='default', null=True, blank=True)
    ordem = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
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
    def save(self, *args, **kwargs):
        try:
            num = int(self.ordem) if self.ordem is not None else 0
        except (TypeError, ValueError):
            num = 0
        if num < 0 or num > 9:
            num = 0
        if num != 0:
            conflito = Servico.objects.exclude(pk=self.pk).filter(ordem=num).exists()
            if conflito:
                num = 0
        self.ordem = num
        super().save(*args, **kwargs)

class Plano(models.Model):
    servico = models.ForeignKey(
        Servico, 
        on_delete=models.CASCADE, 
        related_name='planos', 
        null=False, 
        blank=False
    )
    nome = models.CharField(max_length=250)
    descricao = models.TextField(blank=False, null=False)
    preco = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
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
        # Garante carrinho para o usuário
        if not hasattr(self, 'carrinho'):
            Carrinho.objects.get_or_create(usuario=self)
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

class Compra(models.Model):
    TIPO_CHOICES = [
        ('servico', 'Serviço'),
        ('plano', 'Plano'),
    ]
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='compras',
        null=False,
        blank=False
    )
    servico = models.ForeignKey(
        Servico,
        on_delete=models.PROTECT, 
        related_name='compras',
        null=False,
        blank=False
    )
    plano = models.ForeignKey(
        Plano,
        on_delete=models.PROTECT,
        related_name='compras',
        null=True,
        blank=True
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    nome_servico = models.CharField(max_length=250)
    nome_plano = models.CharField(max_length=250, blank=True, null=True)
    preco = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    ativo = models.BooleanField(default=True)
    data_compra = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-data_compra']
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
    def save(self, *args, **kwargs):
        # Preenche automaticamente nome_servico e nome_plano
        if self.servico and not self.nome_servico:
            self.nome_servico = self.servico.nome
        if self.tipo == 'plano':
            if not self.plano:
                raise ValueError('Compra do tipo "plano" precisa ter um Plano associado.')
            if not self.nome_plano:
                self.nome_plano = self.plano.nome
            # Garante que o plano pertence ao serviço informado
            if self.plano.servico_id != self.servico_id:
                raise ValueError('O plano informado não pertence ao serviço selecionado.')
        else:
            # Para serviço de pagamento único, não deve ter plano
            self.plano = None
            self.nome_plano = None
            # Serviço único não tem status ativo/inativo
            self.ativo = True
        super().save(*args, **kwargs)
    def _str_(self):
        if self.tipo == 'plano':
            return f"{self.usuario} - {self.nome_servico} / {self.nome_plano} ({self.preco})"
        return f"{self.usuario} - {self.nome_servico} ({self.preco})"


class Carrinho(models.Model):
    """
    Um carrinho por usuário (OneToOne). O total é recalculado a partir
    dos itens, mas pode ser sobrescrito manualmente por um admin
    (ex.: desconto, ajuste de preço).
    """
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='carrinho',
        null=False,
        blank=False,
    )
    # Preço total manual (opcional). Se None, usa o cálculo automático
    # da soma dos itens.
    preco_manual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text='Se preenchido, sobrescreve o total calculado dos itens.',
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Carrinho'
        verbose_name_plural = 'Carrinhos'

    # ---------- Propriedades de total ----------
    @property
    def subtotal(self):
        """Soma dos preços (snapshot) de todos os itens."""
        return sum(
            (item.preco * item.quantidade for item in self.itens.all()),
            Decimal('0.00'),
        )

    @property
    def total(self):
        """Total final: usa preco_manual se definido, senão o subtotal."""
        if self.preco_manual is not None:
            return self.preco_manual
        return self.subtotal

    @property
    def quantidade_itens(self):
        return sum(item.quantidade for item in self.itens.all())

    @property
    def vazio(self):
        return not self.itens.exists()

    def __str__(self):
        return f"Carrinho de {self.usuario} ({self.quantidade_itens} itens)"


class ItemCarrinho(models.Model):
    TIPO_CHOICES = [
        ('servico', 'Serviço'),
        ('plano', 'Plano'),
    ]

    carrinho = models.ForeignKey(
        Carrinho,
        on_delete=models.CASCADE,
        related_name='itens',
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

    servico = models.ForeignKey(
        Servico,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='itens_carrinho',
    )
    plano = models.ForeignKey(
        Plano,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='itens_carrinho',
    )

    # ---------- SNAPSHOT ----------
    nome_servico = models.CharField(max_length=250)
    nome_plano = models.CharField(max_length=250, blank=True, null=True)
    preco = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text='Preço do item no momento em que foi adicionado (editável pelo admin).',
    )
    quantidade = models.PositiveIntegerField(default=1)

    capa_snapshot = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text='Public ID ou URL da capa no momento da adição.',
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['criado_em']
        verbose_name = 'Item do carrinho'
        verbose_name_plural = 'Itens do carrinho'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantidade__gte=1),
                name='item_carrinho_quantidade_minima',
            ),
        ]

    @property
    def preco_total(self):
        # Como não há quantidade no fluxo, é sempre o preço do item
        return self.preco * self.quantidade

    @property
    def capa_url(self):
        if self.capa_snapshot:
            if self.capa_snapshot.startswith('http'):
                return self.capa_snapshot
            url, _ = cloudinary_url(self.capa_snapshot, secure=True)
            return url
        if self.servico and self.servico.capa_url:
            return self.servico.capa_url
        if self.plano and self.plano.capa_url:
            return self.plano.capa_url
        url, _ = cloudinary_url('planos/default', secure=True)
        return url

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.tipo == 'plano':
            if not self.plano and not (self.nome_plano and self.nome_servico):
                raise ValidationError(
                    'Item do tipo "plano" precisa ter um Plano associado '
                    'ou nome_plano/nome_servico preenchidos (snapshot órfão).'
                )
            if self.plano and self.servico and self.plano.servico_id != self.servico_id:
                raise ValidationError(
                    'O plano informado não pertence ao serviço selecionado.'
                )
        else:
            if self.plano or self.nome_plano:
                raise ValidationError(
                    'Item do tipo "servico" não deve ter plano associado.'
                )

    def save(self, *args, **kwargs):
        # Garante que quantidade seja sempre 1 — fluxo de serviço único
        self.quantidade = 1

        if not self.pk:
            if self.tipo == 'servico' and self.servico and not self.nome_servico:
                self.nome_servico = self.servico.nome
                self.preco = self.servico.preco
                self.capa_snapshot = str(self.servico.capa) if self.servico.capa else None
            elif self.tipo == 'plano' and self.plano:
                if not self.nome_servico:
                    self.nome_servico = self.plano.servico.nome
                if not self.nome_plano:
                    self.nome_plano = self.plano.nome
                if not self.servico:
                    self.servico = self.plano.servico
                if not self.preco:
                    self.preco = self.plano.preco
                self.capa_snapshot = str(self.plano.capa) if self.plano.capa else None

        if not self.nome_servico:
            raise ValueError('ItemCarrinho precisa de nome_servico preenchido.')

        super().save(*args, **kwargs)

    def __str__(self):
        if self.tipo == 'plano':
            return f"{self.nome_servico} / {self.nome_plano}"
        return self.nome_servico