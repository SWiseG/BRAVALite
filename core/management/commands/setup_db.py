# -*- coding: utf-8 -*-
# core/management/commands/setup_database.py
import os
from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings

class Command(BaseCommand):
    help = 'Setup the basic configuration for brava_lite DB'
    
    def handle(self, *args, **options):
        show_debug = True if os.getenv('SHOW_CONSOLE_FULL_DEBUG', False) == 'True' else False
        with connection.cursor() as cursor:
            if show_debug: self.stdout.write('Criando schema BRAVA...')
            
            # Criar schema
            cursor.execute('CREATE SCHEMA IF NOT EXISTS BRAVA;')
            
            # Configurar search_path
            cursor.execute('SET search_path TO BRAVA, public;')
            
            # Criar extensões
            cursor.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
            cursor.execute('CREATE EXTENSION IF NOT EXISTS "unaccent";')
            
            if show_debug: self.stdout.write(
                self.style.SUCCESS('BRAVA schema created!')
            )
            
            # Executar migrações
            if show_debug: self.stdout.write('Making migrations...')
            from django.core.management import call_command
            call_command('migrate')
            
            self.stdout.write(
                self.style.SUCCESS('BRAVA Lite database configurated successfuly!')
            )
