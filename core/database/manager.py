# -*- coding: utf-8 -*-
class BRAVAManager:
    """
    Router para gerenciar múltiplos schemas
    """
    
    from decouple import config
    
    SCHEMA = config('DB_SCHEMA', default='BRAVA')
    
    # Mapeamento de apps para schemas
    
    APP_SCHEMA_MAPPING = {
        'users': SCHEMA,
        'products': SCHEMA, 
        'orders': SCHEMA,
        'customers': SCHEMA,
        'core': SCHEMA,
        'dashboard': SCHEMA,
        # Futuras expansões
        'integrations': SCHEMA,
        'reports': SCHEMA,
    }
    
    def db_for_read(self, model, **hints):
        """Determina qual database usar para leitura"""
        app_label = model._meta.app_label
        if app_label in self.APP_SCHEMA_MAPPING:
            return 'default'
        return None
    
    def db_for_write(self, model, **hints):
        """Determina qual database usar para escrita"""
        app_label = model._meta.app_label
        if app_label in self.APP_SCHEMA_MAPPING:
            return 'default'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        """Permite relações entre objetos do mesmo schema"""
        return True
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Controla em qual database fazer migrações"""
        if app_label in self.APP_SCHEMA_MAPPING:
            return db == 'default'
        return None

# Mixin para aplicar schema nas models
class SchemaModelMixin:
    """Mixin para aplicar schema personalizado nas models"""
    
    class Meta:
        abstract = True
    
    @classmethod
    def get_db_table_name(cls, app_prefix, table_name):
        """Gera nome da tabela com prefixo e validações"""
        # Garantir que não ultrapasse 30 caracteres
        full_name = f"{app_prefix}_{table_name}"
        if len(full_name) > 30:
            # Truncar mantendo prefixo
            available_chars = 30 - len(app_prefix) - 1  # -1 para o underscore
            table_name = table_name[:available_chars]
            full_name = f"{app_prefix}_{table_name}"
        
        return full_name.upper()
