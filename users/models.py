# -*- coding: utf-8 -*-
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseAuditModel

class User(BaseAuditModel, AbstractUser):
    """Usuário customizado do sistema"""
    
    # UUID como chave primária (sobrescrever o id padrão)
    UsuarioId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='ID_USUARIO'
    )
    
    ROLE_CHOICES = [
        ('ADMIN', _('Administrador')),
        ('MANAGER', _('Gerente')),
        ('SELLER', _('Vendedor')),
        ('OPERATOR', _('Operador')),
    ]
    
    # Sobrescrever campos do AbstractUser com db_column customizado
    username = models.CharField(
        _('Nome de usuário'),
        max_length=150,
        unique=True,
        db_column='NOME_USUARIO'
    )
    first_name = models.CharField(
        _('Primeiro nome'), 
        max_length=150, 
        blank=True,
        db_column='PRIMEIRO_NOME'
    )
    last_name = models.CharField(
        _('Último nome'), 
        max_length=150, 
        blank=True,
        db_column='ULTIMO_NOME'
    )
    email = models.EmailField(
        _('E-mail'), 
        unique=True,
        db_column='EMAIL'
    )
    is_staff = models.BooleanField(
        _('É da equipe'),
        default=False,
        db_column='IS_STAFF'
    )
    is_active = models.BooleanField(
        _('Ativo'),
        default=True,
        db_column='IS_ACTIVE'
    )
    is_superuser = models.BooleanField(
        _('É superusuário'),
        default=False,
        db_column='IS_SUPERUSER'
    )
    date_joined = models.DateTimeField(
        _('Data de cadastro'),
        auto_now_add=True,
        db_column='DATA_CADASTRO'
    )
    last_login = models.DateTimeField(
        _('Data último login'),
        blank=True,
        null=True,
        db_column='DATA_ULTIMO_LOGIN'
    )
    password = models.CharField(
        _('Senha'), 
        max_length=128,
        db_column='SENHA'
    )
    
    # Campos customizados específicos
    Telefone = models.CharField(
        _('Telefone'),
        max_length=20,
        blank=True,
        db_column='TELEFONE'
    )
    Papel = models.CharField(
        _('Papel'),
        max_length=20,
        choices=ROLE_CHOICES,
        default='OPERATOR',
        db_column='PAPEL'
    )
    Avatar = models.ImageField(
        _('Avatar'),
        upload_to='avatars/',
        blank=True,
        null=True,
        db_column='AVATAR'
    )
    Idioma = models.ForeignKey(
        'core.Language',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Idioma'),
        db_column='ID_IDIOMA'
    )
    Tema = models.CharField(
        _('Tema'),
        max_length=10,
        choices=[('LIGHT', 'Claro'), ('DARK', 'Escuro')],
        default='LIGHT',
        db_column='TEMA'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'USR_USUARIO'
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')
        indexes = [
            models.Index(fields=['email'], name='IDX_USR_USU_EMAIL'),
            models.Index(fields=['Papel'], name='IDX_USR_USU_PAPEL'),
            models.Index(fields=['is_active'], name='IDX_USR_USU_ATIVO'),
            models.Index(fields=['username'], name='IDX_USR_USU_NOME'),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" or self.email
    
    def save(self, *args, **kwargs):
        # Lógica de auditoria customizada
        from core.middleware import get_current_user
        user = get_current_user()
        username = user.username if user and user.is_authenticated else 'BRAVA'
        
        if not self.pk:  # Novo registro
            self.UsuarioInclusao = username
        self.UsuarioAlteracao = username
        
        super().save(*args, **kwargs)
    
    def get_language(self):
        """Retorna idioma do usuário ou padrão"""
        if self.IdIdioma and self.IdIdioma.IsAtivo:
            return self.IdIdioma
        from core.models import Language
        return Language.objects.filter(IsPadrao=True).first()
    
    @property
    def NomeCompleto(self):
        """Retorna nome completo do usuário"""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def Iniciais(self):
        """Retorna iniciais do usuário"""
        primeiro = self.first_name[0] if self.first_name else ''
        ultimo = self.last_name[0] if self.last_name else ''
        return f"{primeiro}{ultimo}".upper()
    
    def has_permission(self, permission):
        """Verifica se o usuário tem uma permissão específica"""
        if self.is_superuser:
            return True
        
        # Verificar permissões por papel
        role_permissions = {
            'ADMIN': ['*'],
            'MANAGER': [
                'view_dashboard', 'manage_products', 'manage_orders', 
                'view_customers', 'view_reports'
            ],
            'SELLER': [
                'view_dashboard', 'view_products', 'manage_orders', 
                'view_customers'
            ],
            'OPERATOR': [
                'view_dashboard', 'view_products', 'view_orders'
            ]
        }
        
        permissions = role_permissions.get(self.Papel, [])
        return '*' in permissions or permission in permissions

class UserPermission(BaseAuditModel):
    """Permissões customizadas por usuário"""
    UsuarioPermissaoId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='ID_USUARIO_PERMISSAO'
    )
    Usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Usuário'),
        db_column='ID_USUARIO'
    )
    CodigoPermissao = models.CharField(
        _('Código permissão'),
        max_length=100,
        help_text=_('Código da permissão'),
        db_column='CODIGO_PERMISSAO'
    )
    DescricaoPermissao = models.CharField(
        _('Descrição'),
        max_length=255,
        help_text=_('Descrição da permissão'),
        db_column='DESCRICAO_PERMISSAO'
    )
    Ativo = models.BooleanField(_('Ativo'), default=True, db_column='ATIVO')
    DataExpiracao = models.DateTimeField(
        _('Expira em'), 
        null=True, 
        blank=True,
        db_column='DATA_EXPIRACAO'
    )
    
    class Meta:
        db_table = 'USR_USUARIO_PERMISSAO'
        verbose_name = _('Permissão')
        verbose_name_plural = _('Permissões')
        unique_together = ['Usuario', 'CodigoPermissao']
        indexes = [
            models.Index(fields=['Usuario', 'CodigoPermissao'], name='IDX_USR_PER_USU_CD'),
            models.Index(fields=['Ativo'], name='IDX_USR_PER_ATIVO'),
        ]

class UserSession(BaseAuditModel):
    """Sessões de usuário para controle"""
    UsuarioSessaoId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='ID_USUARIO_SESSAO'
    )
    Usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Usuário'),
        db_column='ID_USUARIO'
    )
    ChaveSessao = models.CharField(
        _('Chave sessão'),
        max_length=255,
        unique=True,
        db_column='CHAVE_SESSAO'
    )
    EnderecoIp = models.GenericIPAddressField(
        _('Endereço IP'),
        db_column='ENDERECO_IP'
    )
    UserAgent = models.TextField(
        _('User Agent'), 
        blank=True,
        db_column='USER_AGENT'
    )
    DataExpiracao = models.DateTimeField(
        _('Expira em'),
        db_column='DATA_EXPIRACAO'
    )
    Ativo = models.BooleanField(_('Ativo'), default=True, db_column='ATIVO')
    
    class Meta:
        db_table = 'USR_USUARIO_SESSAO'
        verbose_name = _('Sessão')
        verbose_name_plural = _('Sessões')
        indexes = [
            models.Index(fields=['ChaveSessao'], name='IDX_USR_SES_CHAVE'),
            models.Index(fields=['Usuario', 'Ativo'], name='IDX_USR_SES_USU_AT'),
        ]
