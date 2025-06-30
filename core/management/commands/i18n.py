# core/management/commands/load_base_translations.py
from django.core.management.base import BaseCommand
from core.models import Language, Translation

class Command(BaseCommand):
    help = 'Reload all system language messages i18n'
    
    def handle(self, *args, **options):
        # Criar idiomas padrão
        pt_br, created = Language.objects.get_or_create(
            code='pt-BR',
            defaults={
                'name': 'Português Brasil',
                'native_name': 'Português Brasil',
                'flag_icon': 'flag-br',
                'is_default': True,
                'is_active': True
            }
        )
        
        en_us, created = Language.objects.get_or_create(
            code='en-US',
            defaults={
                'name': 'English United States',
                'native_name': 'English',
                'flag_icon': 'flag-us',
                'is_default': False,
                'is_active': True
            }
        )
        
        # Traduções base
        base_translations = {
            # Comum
            'common.save': {'pt-BR': 'Salvar', 'en-US': 'Save'},
            'common.cancel': {'pt-BR': 'Cancelar', 'en-US': 'Cancel'},
            'common.delete': {'pt-BR': 'Excluir', 'en-US': 'Delete'},
            'common.edit': {'pt-BR': 'Editar', 'en-US': 'Edit'},
            'common.view': {'pt-BR': 'Visualizar', 'en-US': 'View'},
            'common.add': {'pt-BR': 'Adicionar', 'en-US': 'Add'},
            'common.search': {'pt-BR': 'Pesquisar', 'en-US': 'Search'},
            'common.loading': {'pt-BR': 'Carregando...', 'en-US': 'Loading...'},
            'common.error': {'pt-BR': 'Erro', 'en-US': 'Error'},
            'common.success': {'pt-BR': 'Sucesso', 'en-US': 'Success'},
            'common.warning': {'pt-BR': 'Atenção', 'en-US': 'Warning'},
            'common.info': {'pt-BR': 'Informação', 'en-US': 'Information'},
            'common.language_changed': {'pt-BR': 'Idioma alterado com sucesso', 'en-US': 'Language changed successfully'},
            'common.error_changing_language': {'pt-BR': 'Erro ao alterar idioma', 'en-US': 'Error changing language'},
            
            # Autenticação
            'auth.login': {'pt-BR': 'Entrar', 'en-US': 'Login'},
            'auth.logout': {'pt-BR': 'Sair', 'en-US': 'Logout'},
            'auth.email': {'pt-BR': 'E-mail', 'en-US': 'Email'},
            'auth.password': {'pt-BR': 'Senha', 'en-US': 'Password'},
            'auth.remember_me': {'pt-BR': 'Lembrar-me', 'en-US': 'Remember me'},
            'auth.forgot_password': {'pt-BR': 'Esqueci minha senha', 'en-US': 'Forgot password'},
            'auth.login_success': {'pt-BR': 'Login realizado com sucesso', 'en-US': 'Login successful'},
            'auth.login_error': {'pt-BR': 'Credenciais inválidas', 'en-US': 'Invalid credentials'},
            
            # Dashboard
            'dashboard.title': {'pt-BR': 'Dashboard', 'en-US': 'Dashboard'},
            'dashboard.welcome': {'pt-BR': 'Bem-vindo, {{name}}!', 'en-US': 'Welcome, {{name}}!'},
            'dashboard.total_sales': {'pt-BR': 'Vendas Totais', 'en-US': 'Total Sales'},
            'dashboard.orders': {'pt-BR': 'Pedidos', 'en-US': 'Orders'},
            'dashboard.customers': {'pt-BR': 'Clientes', 'en-US': 'Customers'},
            'dashboard.products': {'pt-BR': 'Produtos', 'en-US': 'Products'},
            
            # Menu
            'menu.dashboard': {'pt-BR': 'Dashboard', 'en-US': 'Dashboard'},
            'menu.products': {'pt-BR': 'Produtos', 'en-US': 'Products'},
            'menu.orders': {'pt-BR': 'Pedidos', 'en-US': 'Orders'},
            'menu.customers': {'pt-BR': 'Clientes', 'en-US': 'Customers'},
            'menu.settings': {'pt-BR': 'Configurações', 'en-US': 'Settings'},
            
            # Produtos
            'products.title': {'pt-BR': 'Produtos', 'en-US': 'Products'},
            'products.add': {'pt-BR': 'Adicionar Produto', 'en-US': 'Add Product'},
            'products.name': {'pt-BR': 'Nome', 'en-US': 'Name'},
            'products.price': {'pt-BR': 'Preço', 'en-US': 'Price'},
            'products.stock': {'pt-BR': 'Estoque', 'en-US': 'Stock'},
            'products.category': {'pt-BR': 'Categoria', 'en-US': 'Category'},
            
            # Pedidos
            'orders.title': {'pt-BR': 'Pedidos', 'en-US': 'Orders'},
            'orders.status': {'pt-BR': 'Status', 'en-US': 'Status'},
            'orders.total': {'pt-BR': 'Total', 'en-US': 'Total'},
            'orders.date': {'pt-BR': 'Data', 'en-US': 'Date'},
        }
        
        # Criar traduções
        for key, translations in base_translations.items():
            for lang_code, value in translations.items():
                language = Language.objects.get(code=lang_code)
                Translation.objects.get_or_create(
                    key=key,
                    language=language,
                    defaults={'value': value}
                )
        
        self.stdout.write(
            self.style.SUCCESS('i18n reload with success!')
        )
