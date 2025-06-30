from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from .models import Language

class UserLanguageMiddleware(MiddlewareMixin):
    """Middleware para definir idioma baseado no usuário"""
    
    def process_request(self, request):
        if request.user.is_authenticated:
            user_language = request.user.get_language()
            if user_language:
                translation.activate(user_language.code)
                request.LANGUAGE_CODE = user_language.code
            else:
                # Usar idioma padrão do sistema
                default_lang = Language.get_default_language()
                if default_lang:
                    translation.activate(default_lang.code)
                    request.LANGUAGE_CODE = default_lang.code