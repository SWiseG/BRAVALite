# -*- coding: utf-8 -*-
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseAuditModel

class Category(BaseAuditModel):
    """Categorias de produtos"""
    CategoriaId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='ID_CATEGORIA'
    )
    Nome = models.CharField(
        _('Nome'),
        max_length=100,
        help_text=_('Nome da categoria'),
        db_column='NOME'
    )
    Descricao = models.TextField(
        _('Descrição'),
        blank=True,
        help_text=_('Descrição da categoria'),
        db_column='DESCRICAO'
    )
    CategoriaPai = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Categoria pai'),
        db_column='ID_CATEGORIA_PAI'
    )
    Icone = models.ImageField(
        _('Ícone'),
        upload_to='categories/',
        blank=True,
        null=True,
        db_column='ICONE'
    )
    Ordem = models.PositiveIntegerField(
        _('Ordem'),
        default=0,
        help_text=_('Ordem de exibição'),
        db_column='ORDEM'
    )
    Ativo = models.BooleanField(_('Ativo'), default=True, db_column='ATIVO')
    
    class Meta:
        db_table = 'PRD_CATEGORIA'
        verbose_name = _('Categoria')
        verbose_name_plural = _('Categorias')
        ordering = ['Ordem', 'Nome']
        indexes = [
            models.Index(fields=['Ativo'], name='IDX_PRD_CAT_ATIVO'),
            models.Index(fields=['CategoriaPai'], name='IDX_PRD_CAT_PAI'),
            models.Index(fields=['Ordem'], name='IDX_PRD_CAT_ORDEM'),
        ]
    
    def __str__(self):
        return self.Nome

class Brand(BaseAuditModel):
    """Marcas de produtos"""
    MarcaId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='ID_MARCA'
    )
    Nome = models.CharField(
        _('Nome'),
        max_length=100,
        unique=True,
        db_column='NOME'
    )
    Descricao = models.TextField(
        _('Descrição'), 
        blank=True,
        db_column='DESCRICAO'
    )
    Logo = models.ImageField(
        _('Logo'),
        upload_to='brands/',
        blank=True,
        null=True,
        db_column='LOGO'
    )
    Website = models.URLField(
        _('Website'), 
        blank=True,
        db_column='WEBSITE'
    )
    Ativo = models.BooleanField(_('Ativo'), default=True, db_column='ATIVO')
    
    class Meta:
        db_table = 'PRD_MARCA'
        verbose_name = _('Marca')
        verbose_name_plural = _('Marcas')
        ordering = ['Nome']
        indexes = [
            models.Index(fields=['Nome'], name='IDX_PRD_MAR_NOME'),
            models.Index(fields=['Ativo'], name='IDX_PRD_MAR_ATIVO'),
        ]
    
    def __str__(self):
        return self.Nome

class Product(BaseAuditModel):
    """Produtos"""
    ProdutoId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='ID_PRODUTO'
    )
    STATUS_CHOICES = [
        ('ACTIVE', _('Ativo')),
        ('INACTIVE', _('Inativo')),
        ('DRAFT', _('Rascunho')),
        ('ARCHIVED', _('Arquivado')),
    ]
    
    Codigo = models.CharField(
        _('Código'),
        max_length=50,
        unique=True,
        help_text=_('Código único do produto'),
        db_column='CODIGO'
    )
    Nome = models.CharField(
        _('Nome'), 
        max_length=255,
        db_column='NOME'
    )
    Descricao = models.TextField(
        _('Descrição'), 
        blank=True,
        db_column='DESCRICAO'
    )
    Resumo = models.CharField(
        _('Resumo'),
        max_length=500,
        blank=True,
        help_text=_('Descrição resumida'),
        db_column='RESUMO'
    )
    Categoria = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name=_('Categoria'),
        db_column='ID_CATEGORIA'
    )
    Marca = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Marca'),
        db_column='ID_MARCA'
    )
    Preco = models.DecimalField(
        _('Preço'),
        max_digits=10,
        decimal_places=2,
        help_text=_('Preço de venda'),
        db_column='PRECO'
    )
    Custo = models.DecimalField(
        _('Custo'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Custo do produto'),
        db_column='CUSTO'
    )
    QuantidadeEstoque = models.IntegerField(
        _('Estoque'),
        default=0,
        help_text=_('Quantidade em estoque'),
        db_column='QUANTIDADE_ESTOQUE'
    )
    EstoqueMinimo = models.IntegerField(
        _('Estoque mínimo'),
        default=0,
        help_text=_('Quantidade mínima em estoque'),
        db_column='ESTOQUE_MINIMO'
    )
    Peso = models.DecimalField(
        _('Peso (kg)'),
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
        db_column='PESO'
    )
    Dimensoes = models.CharField(
        _('Dimensões'),
        max_length=100,
        blank=True,
        help_text=_('Formato: LxAxP em cm'),
        db_column='DIMENSOES'
    )
    Status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='DRAFT',
        db_column='STATUS'
    )
    Destaque = models.BooleanField(
        _('Destaque'), 
        default=False,
        db_column='DESTAQUE'
    )
    SeoTitulo = models.CharField(
        _('SEO Título'),
        max_length=255,
        blank=True,
        db_column='SEO_TITULO'
    )
    SeoDescricao = models.TextField(
        _('SEO Descrição'),
        blank=True,
        db_column='SEO_DESCRICAO'
    )
    
    class Meta:
        db_table = 'PRD_PRODUTO'
        verbose_name = _('Produto')
        verbose_name_plural = _('Produtos')
        ordering = ['-DataInclusao']
        indexes = [
            models.Index(fields=['Codigo'], name='IDX_PRD_PRO_COD'),
            models.Index(fields=['Nome'], name='IDX_PRD_PRO_NOME'),
            models.Index(fields=['Status'], name='IDX_PRD_PRO_STAT'),
            models.Index(fields=['Categoria'], name='IDX_PRD_PRO_CAT'),
            models.Index(fields=['Destaque'], name='IDX_PRD_PRO_DEST'),
            models.Index(fields=['DataInclusao'], name='IDX_PRD_PRO_CRIA'),
        ]
    
    def __str__(self):
        return f"{self.Codigo} - {self.Nome}"
    
    @property
    def is_low_stock(self):
        """Verifica se está com estoque baixo"""
        return self.QuantidadeEstoque <= self.EstoqueMinimo

class ProductImage(BaseAuditModel):
    """Imagens dos produtos"""
    ProdutoImagemId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='ID_PRODUTO_IMAGEM'
    )
    Produto = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='imagens',
        verbose_name=_('Produto'),
        db_column='ID_PRODUTO'
    )
    Arquivo = models.ImageField(
        _('Imagem'),
        upload_to='products/',
        db_column='ARQUIVO'
    )
    TextoAlternativo = models.CharField(
        _('Texto alternativo'),
        max_length=255,
        blank=True,
        db_column='TEXTO_ALTERNATIVO'
    )
    Ordem = models.PositiveIntegerField(
        _('Ordem'), 
        default=0,
        db_column='ORDEM'
    )
    Principal = models.BooleanField(
        _('Principal'), 
        default=False,
        db_column='PRINCIPAL'
    )
    
    class Meta:
        db_table = 'PRD_PRODUTO_IMAGEM'
        verbose_name = _('Imagem')
        verbose_name_plural = _('Imagens')
        ordering = ['Ordem']
        indexes = [
            models.Index(fields=['Produto', 'Ordem'], name='IDX_PRD_IMG_PRO_ORD'),
            models.Index(fields=['Principal'], name='IDX_PRD_IMG_PRINC'),
        ]
    
    def save(self, *args, **kwargs):
        if self.Principal:
            # Remover flag principal de outras imagens do mesmo produto
            ProductImage.objects.filter(
                Produto=self.Produto
            ).exclude(pk=self.pk).update(Principal=False)
        super().save(*args, **kwargs)

class ProductVariation(BaseAuditModel):
    """Variações de produtos (cor, tamanho, etc.)"""
    ProdutoVarianteId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='ID_PRODUTO_VARIANTE'
    )
    Produto = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variacoes',
        verbose_name=_('Produto'),
        db_column='ID_PRODUTO'
    )
    TipoVariacao = models.CharField(
        _('Tipo variação'),
        max_length=50,
        help_text=_('Ex: Cor, Tamanho, Modelo'),
        db_column='TIPO_VARIACAO'
    )
    ValorVariacao = models.CharField(
        _('Valor variação'),
        max_length=100,
        help_text=_('Ex: Azul, P, Standard'),
        db_column='VALOR_VARIACAO'
    )
    CodigoSku = models.CharField(
        _('SKU'),
        max_length=100,
        unique=True,
        help_text=_('Código SKU da variação'),
        db_column='CODIGO_SKU'
    )
    PrecoAdicional = models.DecimalField(
        _('Preço adicional'),
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text=_('Valor adicional ao preço base'),
        db_column='PRECO_ADICIONAL'
    )
    EstoqueVariacao = models.IntegerField(
        _('Estoque variação'),
        default=0,
        db_column='ESTOQUE_VARIACAO'
    )
    Ativo = models.BooleanField(_('Ativo'), default=True, db_column='ATIVO')
    
    class Meta:
        db_table = 'PRD_PRODUTO_VARIACAO'
        verbose_name = _('Variação')
        verbose_name_plural = _('Variações')
        unique_together = ['Produto', 'TipoVariacao', 'ValorVariacao']
        indexes = [
            models.Index(fields=['Produto'], name='IDX_PRD_VAR_PRO'),
            models.Index(fields=['CodigoSku'], name='IDX_PRD_VAR_SKU'),
            models.Index(fields=['TipoVariacao'], name='IDX_PRD_VAR_TIPO'),
        ]
    
    def __str__(self):
        return f"{self.Produto.Nome} - {self.TipoVariacao}: {self.ValorVariacao}"
