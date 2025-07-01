# -*- coding: utf-8 -*-
import os
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Migra IDs para UUID e renomeia para UPPERCASE'
    
    def handle(self, *args, **options):
        show_debug = True if os.getenv('SHOW_CONSOLE_FULL_DEBUG', False) == 'True' else False
        with connection.cursor() as cursor:
            self.stdout.write('Migrating custom data')
            
            cursor.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
            
            django_tables = [
                'auth_group',
                'auth_group_permissions', 
                'auth_permission',
                'auth_user',
                'auth_user_groups',
                'auth_user_user_permissions',
                'django_admin_log',
                'django_content_type',
                'django_migrations',
                'django_session',
            ]
            
            for table in django_tables:
                try:
                    cursor.execute(f"""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_schema = 'BRAVA' 
                            AND table_name = '{table}'
                        );
                    """)
                    
                    if cursor.fetchone()[0]:
                        uppercase_name = table.upper()
                        cursor.execute(f'ALTER TABLE "{table}" RENAME TO "{uppercase_name}";')
                        if show_debug: self.stdout.write(f'[INFO] Table {table} renamed {uppercase_name}')
                except Exception as e:
                    if show_debug: self.stdout.write(f'[WARN] Error trying to update {table}: {e}')
            
            self.stdout.write(
                self.style.SUCCESS('[SUCCESS] Custom migrations end successfuly!')
            )
