# core/translation.py
from django.core.cache import cache
from django.utils.translation import get_language
from .models import Language, Translation

class TranslationManager:
    """Gerenciador de traduções customizadas"""
    
    @staticmethod
    def get_translations(language_code=None):
        """Retorna todas as traduções para um idioma"""
        if not language_code:
            language_code = get_language() or 'pt-BR'
        
        # Tentar buscar no cache
        cache_key = f'translations_{language_code}'
        translations = cache.get(cache_key)
        
        if translations is None:
            try:
                language = Language.objects.get(code=language_code, is_active=True)
                translations = {}
                
                for trans in Translation.objects.filter(language=language):
                    # Criar estrutura aninhada baseada na chave
                    keys = trans.key.split('.')
                    current = translations
                    
                    for key in keys[:-1]:
                        if key not in current:
                            current[key] = {}
                        current = current[key]
                    
                    current[keys[-1]] = trans.value
                
                cache.set(cache_key, translations, 3600)
                
            except Language.DoesNotExist:
                translations = {}
        
        return translations
    
    @staticmethod
    def translate(key, language_code=None, context=None, default=None):
        """Traduz uma chave específica"""
        translations = TranslationManager.get_translations(language_code)
        
        # Navegar pela estrutura aninhada
        keys = key.split('.')
        current = translations
        
        try:
            for k in keys:
                current = current[k]
            return current
        except (KeyError, TypeError):
            return default or key

