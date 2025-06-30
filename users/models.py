from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import Language

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', _('Administrador')),
        ('manager', _('Gerente')),
        ('seller', _('Vendedor')),
        ('operator', _('Operador')),
    ]
    
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        _('função'),
        max_length=20,
        choices=ROLE_CHOICES,
        default='operator'
    )
    phone = models.CharField(_('telefone'), max_length=20, blank=True)
    avatar = models.ImageField(
        _('avatar'),
        upload_to='avatars/',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(_('ativo'), default=True)
    created_at = models.DateTimeField(_('criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('atualizado em'), auto_now=True)
    
    # Configurações pessoais
    theme = models.CharField(
        _('tema'),
        max_length=10,
        choices=[('light', 'Claro'), ('dark', 'Escuro')],
        default='light'
    )
    
    language = models.ForeignKey(
        'core.Language',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Idioma preferido'),
        help_text=_('Se não definido, será usado o idioma padrão do sistema')
    )
    
    def get_language(self):
        """Retorna idioma do usuário ou padrão do sistema"""
        if self.language and self.language.is_active:
            return self.language
        return Language.get_default_language()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}" or self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def has_permission(self, permission):
        """Verifica se o usuário tem uma permissão específica"""
        return self.is_superuser or self.user_permissions.filter(
            codename=permission
        ).exists()