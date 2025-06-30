class BRAVA {
    constructor() {
        this.isAuthenticated = false;
        this.currentUser = null;
        this.currentRoute = null;
        
        this.init();
    }
    
    async init() {
        console.log('System getting started...');
        
        try {
            // Verificar autenticação
            await this.checkAuth();
            
            // Inicializar roteador
            this.initRouter();
            
            // Carregar componentes base
            await this.loadBaseComponents();
            
            // Ocultar loading screen
            this.hideLoadingScreen();
            
            // Navegar para rota inicial
            this.navigateToInitialRoute();
            
        } catch (error) {
            console.error('Error. Trying to initialize base app:', error);
            this.showError('Error trying to load the app');
        }
    }
    
    async checkAuth() {
        const token = Auth.getToken();
        if (token && !Auth.isTokenExpired(token)) {
            this.isAuthenticated = true;
            this.currentUser = await Auth.getCurrentUser();
            API.setAuthToken(token);
        } else {
            this.isAuthenticated = false;
            Auth.logout();
        }
    }
    
    initRouter() {
        // Configurar rotas
        Router.init({
            // Rotas públicas
            '/': () => this.isAuthenticated ? this.redirectTo('/dashboard') : this.redirectTo('/login'),
            '/login': () => this.loadAuthPage('login'),
            '/register': () => this.loadAuthPage('register'),
            
            // Rotas protegidas
            '/dashboard': this.requireAuth(() => Dashboard.load()),
            '/products': this.requireAuth(() => Products.loadList()),
            '/products/new': this.requireAuth(() => Products.loadForm()),
            '/products/:id': this.requireAuth((id) => Products.loadDetail(id)),
            '/products/:id/edit': this.requireAuth((id) => Products.loadForm(id)),
            
            '/orders': this.requireAuth(() => Orders.loadList()),
            '/orders/:id': this.requireAuth((id) => Orders.loadDetail(id)),
            
            '/customers': this.requireAuth(() => Customers.loadList()),
            '/customers/new': this.requireAuth(() => Customers.loadForm()),
            '/customers/:id': this.requireAuth((id) => Customers.loadDetail(id)),
            
            '/settings': this.requireAuth(() => Settings.load()),
            
            // 404
            '*': () => this.show404()
        });
    }
    
    requireAuth(callback) {
        return (...args) => {
            if (!this.isAuthenticated) {
                this.redirectTo('/login');
                return;
            }
            return callback(...args);
        };
    }
    
    async loadBaseComponents() {
        if (this.isAuthenticated) {
            // Carregar layout principal
            $('#main-layout').show();
            $('#auth-layout').hide();
            
            // Carregar sidebar e header
            await Promise.all([
                Sidebar.load(),
                Header.load()
            ]);
        } else {
            // Carregar layout de autenticação
            $('#auth-layout').show();
            $('#main-layout').hide();
        }
    }
    
    async loadAuthPage(page) {
        const html = await Utils.loadTemplate(`views/auth/${page}.html`);
        $('#auth-content').html(html);
        
        // Inicializar formulário de auth
        Auth.initForm(page);
    }
    
    hideLoadingScreen() {
        $('#loading-screen').fadeOut(500, function() {
            $('#app').fadeIn(300);
        });
    }
    
    navigateToInitialRoute() {
        const hash = window.location.hash.slice(1) || '/';
        Router.navigate(hash);
    }
    
    redirectTo(path) {
        Router.navigate(path);
    }
    
    show404() {
        $('#main-content').html(`
            <div class="error-page">
                <h1>404</h1>
                <p>Página não encontrada</p>
                <a href="#/dashboard" class="btn btn-primary">Voltar ao Dashboard</a>
            </div>
        `);
    }
    
    showError(message) {
        // Implementar toast de erro
        console.error(message);
    }
    
    // Event handlers
    onAuthSuccess(user) {
        this.isAuthenticated = true;
        this.currentUser = user;
        this.loadBaseComponents();
        this.redirectTo('/dashboard');
    }
    
    onLogout() {
        this.isAuthenticated = false;
        this.currentUser = null;
        this.redirectTo('/login');
    }
}

$(document).ready(() => {
    window.App = new BRAVA();
});