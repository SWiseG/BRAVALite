# -*- coding: utf-8 -*-
from django.utils import translation
from django.db import connection
from django.utils.deprecation import MiddlewareMixin
from .models import Language
from threading import local

_user = local()

class UserLanguageMiddleware(MiddlewareMixin):
    """Middleware para definir idioma baseado no usuário"""
    
    def process_request(self, request):
        if request.user.is_authenticated:
            user_language = request.user.get_language()
            if user_language:
                translation.activate(user_language.Codigo)
                request.LANGUAGE_CODE = user_language.Codigo
            else:
                # Usar idioma padrão do sistema
                default_lang = Language.get_default_language()
                if default_lang:
                    translation.activate(default_lang.Codigo)
                    request.LANGUAGE_CODE = default_lang.Codigo

class DatabaseSchemaMiddleware(MiddlewareMixin):
    """Middleware para garantir que o schema correto seja usado"""
    
    def process_request(self, request):
        """Configura schema no início da requisição"""
        with connection.cursor() as cursor:
            cursor.execute('SET search_path TO BRAVA, public;')
    
    def process_response(self, request, response):
        """Limpa configurações após a resposta"""
        return response
 
class AuditMiddleware(MiddlewareMixin):
    """Middleware para capturar usuário atual para auditoria"""
    
    def process_request(self, request):
        _user.value = getattr(request, 'user', None)

def get_current_user():
    """Retorna o usuário atual para uso nos models"""
    return getattr(_user, 'value', None)

