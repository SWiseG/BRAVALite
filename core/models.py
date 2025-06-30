# core/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache

class Language(models.Model):
    code = models.CharField(
        _('Código'),
        max_length=10,
        unique=True,
        help_text=_('Código do idioma (ex: pt-BR, en-US)')
    )
    name = models.CharField(
        _('Nome'),
        max_length=100,
        help_text=_('Nome do idioma (ex: Português Brasil)')
    )
    native_name = models.CharField(
        _('Nome nativo'),
        max_length=100,
        help_text=_('Nome no idioma nativo (ex: Português Brasil)')
    )
    flag_icon = models.CharField(
        _('Ícone da bandeira'),
        max_length=50,
        blank=True,
        help_text=_('Classe CSS para ícone da bandeira')
    )
    is_active = models.BooleanField(_('Ativo'), default=True)
    is_default = models.BooleanField(_('Padrão do sistema'), default=False)
    created_at = models.DateTimeField(_('Criado em'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Idioma')
        verbose_name_plural = _('Idiomas')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def save(self, *args, **kwargs):
        # Garantir que apenas um idioma seja padrão
        if self.is_default:
            Language.objects.exclude(pk=self.pk).update(is_default=False)
        
        super().save(*args, **kwargs)
        
        # Invalidar cache
        cache.delete('active_languages')
        cache.delete('default_language')
    
    @classmethod
    def get_active_languages(cls):
        """Retorna idiomas ativos (com cache)"""
        languages = cache.get('active_languages')
        if languages is None:
            languages = list(cls.objects.filter(is_active=True).values())
            cache.set('active_languages', languages, 3600)  # 1 hora
        return languages
    
    @classmethod
    def get_default_language(cls):
        """Retorna idioma padrão do sistema"""
        default = cache.get('default_language')
        if default is None:
            try:
                default = cls.objects.get(is_default=True)
            except cls.DoesNotExist:
                # Se não houver padrão, usar o primeiro ativo
                default = cls.objects.filter(is_active=True).first()
            
            if default:
                cache.set('default_language', default, 3600)
        return default

class Translation(models.Model):
    """Modelo para armazenar traduções customizadas"""
    key = models.CharField(
        _('Chave'),
        max_length=255,
        help_text=_('Chave única para a tradução (ex: dashboard.welcome)')
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        verbose_name=_('Idioma')
    )
    value = models.TextField(
        _('Valor'),
        help_text=_('Texto traduzido')
    )
    context = models.CharField(
        _('Contexto'),
        max_length=100,
        blank=True,
        help_text=_('Contexto da tradução (ex: dashboard, products)')
    )
    created_at = models.DateTimeField(_('Criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Atualizado em'), auto_now=True)
    
    class Meta:
        verbose_name = _('Tradução')
        verbose_name_plural = _('Traduções')
        unique_together = ['key', 'language']
        indexes = [
            models.Index(fields=['key', 'language']),
            models.Index(fields=['context']),
        ]
    
    def __str__(self):
        return f"{self.key} ({self.language.code})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Invalidar cache de traduções
        cache.delete(f'translations_{self.language.code}')

