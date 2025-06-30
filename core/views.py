from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import get_language
from .models import Language, Translation
from api.serializers import LanguageSerializer, TranslationSerializer
from .translation import TranslationManager

class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.filter(is_active=True)
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Retorna idiomas ativos"""
        languages = Language.get_active_languages()
        return Response(languages)
    
    @action(detail=False, methods=['get'])
    def default(self, request):
        """Retorna idioma padrão do sistema"""
        default = Language.get_default_language()
        if default:
            return Response(LanguageSerializer(default).data)
        return Response({'error': 'Nenhum idioma padrão configurado'}, 
                       status=status.HTTP_404_NOT_FOUND)

class TranslationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def by_language(self, request):
        """Retorna todas as traduções para um idioma"""
        language_code = request.query_params.get('lang', get_language())
        translations = TranslationManager.get_translations(language_code)
        return Response(translations)
    
    @action(detail=False, methods=['post'])
    def change_user_language(self, request):
        """Altera idioma do usuário logado"""
        language_code = request.data.get('language_code')
        
        try:
            language = Language.objects.get(code=language_code, is_active=True)
            request.user.language = language
            request.user.save()
            
            return Response({
                'message': 'Idioma alterado com sucesso',
                'language': LanguageSerializer(language).data
            })
        except Language.DoesNotExist:
            return Response({'error': 'Idioma não encontrado'}, 
                           status=status.HTTP_404_NOT_FOUND)