from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LanguageViewSet, TranslationViewSet

router = DefaultRouter()
router.register(r'languages', LanguageViewSet)
router.register(r'translations', TranslationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
