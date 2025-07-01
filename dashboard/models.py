# -*- coding: utf-8 -*-
# dashboard/models.py
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseAuditModel

class DashboardWidget(BaseAuditModel):
    """Widgets do dashboard"""
    
    WIDGET_TYPE_CHOICES = [
        ('CHART', _('Gráfico')),
        ('COUNTER', _('Contador')),
        ('TABLE', _('Tabela')),
        ('LIST', _('Lista')),
        ('CALENDAR', _('Calendário')),
    ]
    
    WidgetId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='ID_WIDGET'
    )
    
    Nome = models.CharField(
        _('Nome'),
        max_length=100,
        db_column='NOME'
    )
    Tipo = models.CharField(
        _('Tipo'),
        max_length=20,
        choices=WIDGET_TYPE_CHOICES,
        db_column='TIPO'
    )
    Configuracao = models.JSONField(
        _('Configuração'),
        help_text=_('Configurações específicas do widget'),
        db_column='CONFIGURACAO'
    )
    Posicao = models.PositiveIntegerField(
        _('Posição'),
        default=0,
        db_column='POSICAO'
    )
    Tamanho = models.CharField(
        _('Tamanho'),
        max_length=20,
        choices=[
            ('SMALL', _('Pequeno')),
            ('MEDIUM', _('Médio')),
            ('LARGE', _('Grande')),
            ('FULL', _('Completo')),
        ],
        default='MEDIUM',
        db_column='TAMANHO'
    )
    Ativo = models.BooleanField(_('Ativo'), default=True, db_column='ATIVO')
    
    class Meta:
        db_table = 'DSH_WIDGET'
        verbose_name = _('Widget')
        verbose_name_plural = _('Widgets')
        ordering = ['Posicao']
        indexes = [
            models.Index(fields=['Ativo'], name='IDX_DSH_WID_ATIVO'),
            models.Index(fields=['Posicao'], name='IDX_DSH_WID_POS'),
        ]
    
    def __str__(self):
        return self.Nome

class DashboardUserWidget(BaseAuditModel):
    """Widgets personalizados por usuário"""
    
    WidgetUsuarioId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='ID_WIDGET_USUARIO'
    )
    
    Usuario = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name=_('Usuário'),
        db_column='ID_USUARIO'
    )
    
    Widget = models.ForeignKey(
        DashboardWidget,
        on_delete=models.CASCADE,
        verbose_name=_('Widget'),
        db_column='ID_WIDGET'
    )
    PosicaoCustom = models.PositiveIntegerField(
        _('Posição customizada'),
        null=True,
        blank=True,
        db_column='POSICAO_CUSTOM'
    )
    ConfiguracaoCustom = models.JSONField(
        _('Configuração customizada'),
        null=True,
        blank=True,
        db_column='CONFIGURACAO_CUSTOM'
    )
    Visivel = models.BooleanField(
        _('Visível'), 
        default=True,
        db_column='VISIVEL'
    )
    
    class Meta:
        db_table = 'DSH_USUARIO_WIDGET'
        verbose_name = _('Widget do usuário')
        verbose_name_plural = _('Widgets do usuário')
        unique_together = ['Usuario', 'Widget']
        indexes = [
            models.Index(fields=['Usuario'], name='IDX_DSH_USW_USU'),
            models.Index(fields=['Visivel'], name='IDX_DSH_USW_VIS'),
        ]
    
    def __str__(self):
        return f"{self.Usuario.username} - {self.Widget.Nome}"
