# -*- coding: utf-8 -*-
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from .database.manager import SchemaModelMixin

class BaseAuditModel(SchemaModelMixin, models.Model):
    """Model base com campos de auditoria"""
    
    UsuarioInclusao = models.CharField(
        _('Criado por'), 
        max_length=50, 
        blank=True, 
        null=True, 
        db_column="USUARIO_INCLUSAO"
    )
    UsuarioAlteracao = models.CharField(
        _('Alterado por'), 
        max_length=50, 
        blank=True, 
        null=True, 
        db_column="USUARIO_ALTERACAO"
    )
    DataInclusao = models.DateTimeField(
        _('Criado em'), 
        auto_now_add=True, 
        db_column="DATA_INCLUSAO"
    )
    DataAlteracao = models.DateTimeField(
        _('Alterado em'), 
        auto_now=True, 
        db_column="DATA_ALTERACAO"
    )
    
    class Meta:
        abstract = True

class Language(BaseAuditModel):
    """Modelo para idiomas do sistema"""
    IdiomaId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='ID_IDIOMA'
    )
    
    Codigo = models.CharField(
        _('Código'),
        max_length=10,
        unique=True,
        help_text=_('Código do idioma (ex: pt-br)'),
        db_column="CODIGO"
    )
    Nome = models.CharField(
        _('Nome'),
        max_length=100,
        help_text=_('Nome do idioma'),
        db_column="NOME"
    )
    NomeNativo = models.CharField(
        _('Nome nativo'),
        max_length=100,
        help_text=_('Nome no idioma nativo'),
        db_column="NOME_NATIVO"
    )
    Bandeira = models.CharField(
        _('Ícone bandeira'),
        max_length=50,
        blank=True,
        help_text=_('Classe CSS para bandeira'),
        db_column="BANDEIRA"
    )
    Ativo = models.BooleanField(_('Ativo'), default=True, db_column="ATIVO")
    Padrao = models.BooleanField(_('Padrão'), default=False, db_column="PADRAO")
    
    class Meta:
        db_table = 'SYS_IDIOMA'
        verbose_name = _('Idioma')
        verbose_name_plural = _('Idiomas')
        ordering = ['NomeNativo']
        indexes = [
            models.Index(fields=['Codigo'], name='IDX_SYS_IDI_CD'),
            models.Index(fields=['Ativo'], name='IDX_SYS_IDI_AT'),
        ]
    
    def __str__(self):
        return f"{self.NomeNativo} ({self.Codigo})"
    
    def save(self, *args, **kwargs):
        if self.Padrao:
            Language.objects.exclude(pk=self.pk).update(Padrao=False)
        super().save(*args, **kwargs)
        cache.delete('active_languages')

class Translation(BaseAuditModel):
    """Modelo para traduções customizadas"""
    TraducaoId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='ID_TRADUCAO'
    )
    
    Chave = models.CharField(
        _('Chave'),
        max_length=255,
        help_text=_('Chave única para tradução'),
        db_column="CHAVE"
    )
    Idioma = models.ForeignKey(
        'core.Language',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Idioma'),
        db_column='ID_IDIOMA'
    )
    Valor = models.TextField(
        _('Valor'),
        help_text=_('Texto traduzido'),
        db_column="VALOR"
    )
    Contexto = models.CharField(
        _('Contexto'),
        max_length=100,
        blank=True,
        help_text=_('Contexto da tradução'),
        db_column="CONTEXTO"
    )
    
    class Meta:
        db_table = 'SYS_TRADUCAO'
        verbose_name = _('Tradução')
        verbose_name_plural = _('Traduções')
        unique_together = ['Chave', 'Idioma']
        indexes = [
            models.Index(fields=['Chave', 'Idioma'], name='IDX_SYS_TRA_CH_ID'),
            models.Index(fields=['Contexto'], name='IDX_SYS_TRA_CTX'),
        ]
    
    def __str__(self):
        return f"{self.Chave} ({self.Idioma.Codigo})"

class SystemConfig(BaseAuditModel):
    """Configurações do sistema"""
    ConfigId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='ID_CONFIG'
    )
    
    Chave = models.CharField(
        _('Chave'),
        max_length=100,
        unique=True,
        help_text=_('Chave da configuração'),
        db_column="CHAVE"
    )
    Valor = models.TextField(
        _('Valor'),
        help_text=_('Valor da configuração'),
        db_column="VALOR"
    )
    Descricao = models.CharField(
        _('Descrição'),
        max_length=255,
        help_text=_('Descrição da configuração'),
        db_column="DESCRICAO"
    )
    Tipo = models.CharField(
        _('Tipo'),
        max_length=20,
        choices=[
            ('STRING', _('Texto')),
            ('INTEGER', _('Número')),
            ('BOOLEAN', _('Verdadeiro/Falso')),
            ('JSON', _('JSON')),
        ],
        default='STRING',
        db_column="TIPO"
    )
    Publico = models.BooleanField(
        _('Público'),
        default=False,
        help_text=_('Se pode ser acessado sem autenticação'),
        db_column="PUBLICO"
    )
    
    class Meta:
        db_table = 'SYS_CONFIG'
        verbose_name = _('Configuração')
        verbose_name_plural = _('Configurações')
        indexes = [
            models.Index(fields=['Chave'], name='IDX_SYS_CFG_CH'),
            models.Index(fields=['Publico'], name='IDX_SYS_CFG_PUB'),
        ]
    
    def __str__(self):
        return f"{self.Chave}: {self.Valor[:50]}"
