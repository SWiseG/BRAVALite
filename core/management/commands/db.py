# -*- coding: utf-8 -*-
import os
from django.core.management.base import BaseCommand
from django.apps import apps
from core.validators import DatabaseNamingValidator

class Command(BaseCommand):
    help = 'Validate the setup of Tables and Columns for DB'
    
    def handle(self, *args, **options):
        show_debug = True if os.getenv('SHOW_CONSOLE_FULL_DEBUG', False) == 'True' else False
        errors = []
        
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                try:
                    table_name = model._meta.db_table
                    if table_name:
                        DatabaseNamingValidator.validate_table_name(table_name)
                        if show_debug: self.stdout.write(f'✓ Table: {table_name}')
                    
                    for field in model._meta.fields:
                        column_name = field.db_column or field.name
                        if column_name not in ['id']:
                            try:
                                if not column_name.startswith('ID_') and column_name != 'id':
                                    DatabaseNamingValidator.validate_column_name(column_name)
                                if show_debug: self.stdout.write(f'  ✓ Column: {column_name}')
                            except Exception as e:
                                errors.append(f'❌ {model.__name__}.{field.name}: {e}')
                
                except Exception as e:
                    errors.append(f'❌ Tabela {model.__name__}: {e}')
        
        if errors and show_debug:
            self.stdout.write('\n' + '='*50)
            self.stdout.write(self.style.ERROR('Errors:'))
            for error in errors:
                self.stdout.write(self.style.ERROR(error))
        elif show_debug:
            self.stdout.write(
                self.style.SUCCESS('\n All tables names are correct!')
            )
            
        self.stdout.write(
            self.style.SUCCESS('BRAVA Lite database verification objects end successfuly!')
        )