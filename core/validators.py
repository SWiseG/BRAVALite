# -*- coding: utf-8 -*-
import re
from django.core.exceptions import ValidationError

class DatabaseNamingValidator:
    """Validador para convenções de nomenclatura"""
    
    MAX_LENGTH = 30
    
    @classmethod
    def validate_table_name(cls, name):
        """Valida nome de tabela"""
        if len(name) > cls.MAX_LENGTH:
            raise ValidationError(f'Nome da tabela muito longo: {len(name)} caracteres (máximo {cls.MAX_LENGTH})')
        
        if not name.isupper():
            raise ValidationError('Nome da tabela deve estar em maiúsculo')
        
        if not re.match(r'^[A-Z]{3}_[A-Z_]+$', name):
            raise ValidationError('Nome da tabela deve seguir padrão: XXX_NOME')
    
    @classmethod
    def validate_column_name(cls, name):
        """Valida nome de coluna"""
        if len(name) > cls.MAX_LENGTH:
            raise ValidationError(f'Nome da coluna muito longo: {len(name)} caracteres (máximo {cls.MAX_LENGTH})')
        
        if not name.isupper():
            raise ValidationError('Nome da coluna deve estar em maiúsculo')

# Decorator para validar models
def validate_model_naming(model_class):
    """Decorator para validar nomenclatura das models"""
    table_name = model_class._meta.db_table
    
    try:
        DatabaseNamingValidator.validate_table_name(table_name)
    except ValidationError as e:
        raise ValidationError(f'Erro na model {model_class.__name__}: {e}')
    
    # Validar nomes das colunas
    for field in model_class._meta.fields:
        column_name = field.db_column or field.name
        if not column_name.startswith(('id', 'ID')):  # Pular chaves primárias
            try:
                DatabaseNamingValidator.validate_column_name(column_name)
            except ValidationError as e:
                raise ValidationError(f'Erro no campo {field.name} da model {model_class.__name__}: {e}')
    
    return model_class
