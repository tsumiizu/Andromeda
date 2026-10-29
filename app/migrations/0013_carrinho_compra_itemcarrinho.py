from decimal import Decimal

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_servico_ordem'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # ------------------------------------------------------------------
        # 1) Compra JÁ EXISTE no banco (Neon).
        #    Só registramos no STATE do Django, sem rodar SQL.
        # ------------------------------------------------------------------
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='Compra',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('tipo', models.CharField(choices=[('servico', 'Serviço'), ('plano', 'Plano')], max_length=10)),
                        ('nome_servico', models.CharField(max_length=250)),
                        ('nome_plano', models.CharField(blank=True, max_length=250, null=True)),
                        ('preco', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                        ('ativo', models.BooleanField(default=True)),
                        ('data_compra', models.DateTimeField(auto_now_add=True)),
                        ('data_atualizacao', models.DateTimeField(auto_now=True)),
                        ('plano', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='compras', to='app.plano')),
                        ('servico', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='compras', to='app.servico')),
                        ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compras', to=settings.AUTH_USER_MODEL)),
                    ],
                    options={
                        'verbose_name': 'Compra',
                        'verbose_name_plural': 'Compras',
                        'ordering': ['-data_compra'],
                    },
                ),
            ],
            database_operations=[],   # <-- NÃO executa SQL no banco
        ),

        # ------------------------------------------------------------------
        # 2) Carrinho NÃO existe → cria de verdade
        # ------------------------------------------------------------------
        migrations.CreateModel(
            name='Carrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco_manual', models.DecimalField(blank=True, decimal_places=2, help_text='Se preenchido, sobrescreve o total calculado dos itens.', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='carrinho', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Carrinho',
                'verbose_name_plural': 'Carrinhos',
            },
        ),

        # ------------------------------------------------------------------
        # 3) ItemCarrinho NÃO existe → cria de verdade
        # ------------------------------------------------------------------
        migrations.CreateModel(
            name='ItemCarrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('servico', 'Serviço'), ('plano', 'Plano')], max_length=10)),
                ('nome_servico', models.CharField(max_length=250)),
                ('nome_plano', models.CharField(blank=True, max_length=250, null=True)),
                ('preco', models.DecimalField(decimal_places=2, help_text='Preço do item no momento em que foi adicionado (editável pelo admin).', max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('quantidade', models.PositiveIntegerField(default=1)),
                ('capa_snapshot', models.CharField(blank=True, help_text='Public ID ou URL da capa no momento da adição.', max_length=500, null=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('carrinho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='app.carrinho')),
                ('plano', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='itens_carrinho', to='app.plano')),
                ('servico', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='itens_carrinho', to='app.servico')),
            ],
            options={
                'verbose_name': 'Item do carrinho',
                'verbose_name_plural': 'Itens do carrinho',
                'ordering': ['criado_em'],
            },
        ),

        # ------------------------------------------------------------------
        # 4) Constraint do ItemCarrinho
        # ------------------------------------------------------------------
        migrations.AddConstraint(
            model_name='itemcarrinho',
            constraint=models.CheckConstraint(
                condition=models.Q(('quantidade__gte', 1)),
                name='item_carrinho_quantidade_minima',
            ),
        ),
    ]