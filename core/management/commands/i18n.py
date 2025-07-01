# -*- coding: utf-8 -*-
# core/management/commands/load_base_translations.py
from django.core.management.base import BaseCommand
from core.models import Language, Translation

class Command(BaseCommand):
    help = 'Reload all system language messages i18n'
    
    def handle(self, *args, **options):
        # Criar idiomas padrão
        pt_br, created = Language.objects.get_or_create(
            Codigo='pt-br',
            defaults={
                'Nome': 'Português Brasil',
                'NomeNativo': 'Português Brasil',
                'Bandeira': 'flag-br',
                'Padrao': True,
                'Ativo': True
            }
        )
        
        en_us, created = Language.objects.get_or_create(
            Codigo='en-us',
            defaults={
                'Nome': 'English United States',
                'NomeNativo': 'English',
                'Bandeira': 'flag-us',
                'Padrao': False,
                'Ativo': True
            }
        )
        
        # Traduções base
        base_translations = {
            # Comum
            'common.save': {'pt-br': 'Salvar', 'en-us': 'Save'},
            'common.cancel': {'pt-br': 'Cancelar', 'en-us': 'Cancel'},
            'common.delete': {'pt-br': 'Excluir', 'en-us': 'Delete'},
            'common.edit': {'pt-br': 'Editar', 'en-us': 'Edit'},
            'common.view': {'pt-br': 'Visualizar', 'en-us': 'View'},
            'common.add': {'pt-br': 'Adicionar', 'en-us': 'Add'},
            'common.search': {'pt-br': 'Pesquisar', 'en-us': 'Search'},
            'common.loading': {'pt-br': 'Carregando...', 'en-us': 'Loading...'},
            'common.error': {'pt-br': 'Erro', 'en-us': 'Error'},
            'common.success': {'pt-br': 'Sucesso', 'en-us': 'Success'},
            'common.warning': {'pt-br': 'Atenção', 'en-us': 'Warning'},
            'common.info': {'pt-br': 'Informação', 'en-us': 'Information'},
            'common.language_changed': {'pt-br': 'Idioma alterado com sucesso', 'en-us': 'Language changed successfully'},
            'common.error_changing_language': {'pt-br': 'Erro ao alterar idioma', 'en-us': 'Error changing language'},
            
            # Autenticação
            'auth.login': {'pt-br': 'Entrar', 'en-us': 'Login'},
            'auth.logout': {'pt-br': 'Sair', 'en-us': 'Logout'},
            'auth.email': {'pt-br': 'E-mail', 'en-us': 'Email'},
            'auth.password': {'pt-br': 'Senha', 'en-us': 'Password'},
            'auth.remember_me': {'pt-br': 'Lembrar-me', 'en-us': 'Remember me'},
            'auth.forgot_password': {'pt-br': 'Esqueci minha senha', 'en-us': 'Forgot password'},
            'auth.login_success': {'pt-br': 'Login realizado com sucesso', 'en-us': 'Login successful'},
            'auth.login_error': {'pt-br': 'Credenciais inválidas', 'en-us': 'Invalid credentials'},
            
            # Dashboard
            'dashboard.title': {'pt-br': 'Dashboard', 'en-us': 'Dashboard'},
            'dashboard.welcome': {'pt-br': 'Bem-vindo, {{name}}!', 'en-us': 'Welcome, {{name}}!'},
            'dashboard.total_sales': {'pt-br': 'Vendas Totais', 'en-us': 'Total Sales'},
            'dashboard.orders': {'pt-br': 'Pedidos', 'en-us': 'Orders'},
            'dashboard.customers': {'pt-br': 'Clientes', 'en-us': 'Customers'},
            'dashboard.products': {'pt-br': 'Produtos', 'en-us': 'Products'},
            
            # Menu
            'menu.dashboard': {'pt-br': 'Dashboard', 'en-us': 'Dashboard'},
            'menu.products': {'pt-br': 'Produtos', 'en-us': 'Products'},
            'menu.orders': {'pt-br': 'Pedidos', 'en-us': 'Orders'},
            'menu.customers': {'pt-br': 'Clientes', 'en-us': 'Customers'},
            'menu.settings': {'pt-br': 'Configurações', 'en-us': 'Settings'},
            
            # Produtos
            'products.title': {'pt-br': 'Produtos', 'en-us': 'Products'},
            'products.add': {'pt-br': 'Adicionar Produto', 'en-us': 'Add Product'},
            'products.name': {'pt-br': 'Nome', 'en-us': 'Name'},
            'products.price': {'pt-br': 'Preço', 'en-us': 'Price'},
            'products.stock': {'pt-br': 'Estoque', 'en-us': 'Stock'},
            'products.category': {'pt-br': 'Categoria', 'en-us': 'Category'},
            
            # Pedidos
            'orders.title': {'pt-br': 'Pedidos', 'en-us': 'Orders'},
            'orders.status': {'pt-br': 'Status', 'en-us': 'Status'},
            'orders.total': {'pt-br': 'Total', 'en-us': 'Total'},
            'orders.date': {'pt-br': 'Data', 'en-us': 'Date'},
        }
        
        # Criar traduções
        for key, translations in base_translations.items():
            for lang_code, value in translations.items():
                language = Language.objects.get(Codigo=lang_code)
                Translation.objects.get_or_create(
                    Chave=key,
                    Idioma=language,
                    defaults={'Valor': value}
                )
        
        self.stdout.write(
            self.style.SUCCESS('i18n reload with success!')
        )
