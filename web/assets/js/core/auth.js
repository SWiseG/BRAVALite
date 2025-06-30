// spa/assets/js/core/auth.js
class AuthManager {
    constructor() {
        this.tokenKey = 'brava_access_token';
        this.refreshKey = 'brava_refresh_token';
        this.userKey = 'brava_user';
        this.currentUser = null;
        
        this.loadStoredAuth();
    }
    
    loadStoredAuth() {
        const user = localStorage.getItem(this.userKey);
        if (user) {
            this.currentUser = JSON.parse(user);
        }
    }
    
    async login(credentials) {
        try {
            const response = await API.post('/auth/login/', credentials);
            
            // Armazenar tokens e usuário
            localStorage.setItem(this.tokenKey, response.access);
            localStorage.setItem(this.refreshKey, response.refresh);
            localStorage.setItem(this.userKey, JSON.stringify(response.user));
            
            this.currentUser = response.user;
            API.setAuthToken(response.access);
            
            return { success: true, user: response.user };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
    
    async refreshToken() {
        try {
            const refresh = localStorage.getItem(this.refreshKey);
            if (!refresh) throw new Error('No refresh token');
            
            const response = await API.post('/auth/refresh/', { refresh });
            
            localStorage.setItem(this.tokenKey, response.access);
            API.setAuthToken(response.access);
            
            return true;
        } catch (error) {
            this.logout();
            return false;
        }
    }
    
    async logout() {
        try {
            const refresh = localStorage.getItem(this.refreshKey);
            if (refresh) {
                await API.post('/auth/logout/', { refresh });
            }
        } catch (error) {
            console.warn('Erro no logout:', error);
        } finally {
            // Limpar storage sempre
            localStorage.removeItem(this.tokenKey);
            localStorage.removeItem(this.refreshKey);
            localStorage.removeItem(this.userKey);
            
            this.currentUser = null;
            API.setAuthToken(null);
            
            // Notificar app sobre logout
            if (window.App) {
                window.App.onLogout();
            }
        }
    }
    
    getToken() {
        return localStorage.getItem(this.tokenKey);
    }
    
    isTokenExpired(token) {
        if (!token) return true;
        
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            return payload.exp < Date.now() / 1000;
        } catch (error) {
            return true;
        }
    }
    
    getCurrentUser() {
        return this.currentUser;
    }
    
    hasPermission(permission) {
        if (!this.currentUser) return false;
        
        // Implementar lógica de permissões baseada em role
        const rolePermissions = {
            'admin': ['*'],
            'manager': ['view_dashboard', 'manage_products', 'manage_orders', 'view_customers'],
            'seller': ['view_dashboard', 'view_products', 'manage_orders'],
            'operator': ['view_dashboard', 'view_products', 'view_orders']
        };
        
        const userRole = this.currentUser.role;
        const permissions = rolePermissions[userRole] || [];
        
        return permissions.includes('*') || permissions.includes(permission);
    }
    
    // Inicializar formulários de auth
    initForm(type) {
        if (type === 'login') {
            this.initLoginForm();
        } else if (type === 'register') {
            this.initRegisterForm();
        }
    }
    
    initLoginForm() {
        $('#login-form').validate({
            rules: {
                email: {
                    required: true,
                    email: true
                },
                password: {
                    required: true,
                    minlength: 6
                }
            },
            messages: {
                email: {
                    required: "Email é obrigatório",
                    email: "Digite um email válido"
                },
                password: {
                    required: "Senha é obrigatória",
                    minlength: "Senha deve ter no mínimo 6 caracteres"
                }
            },
            submitHandler: async (form) => {
                const $form = $(form);
                const $btn = $form.find('button[type="submit"]');
                
                // Loading state
                $btn.prop('disabled', true).html('Entrando...');
                
                const formData = {
                    email: $form.find('input[name="email"]').val(),
                    password: $form.find('input[name="password"]').val()
                };
                
                const result = await this.login(formData);
                
                if (result.success) {
                    Utils.showToast('Login realizado com sucesso!', 'success');
                    // App será notificado automaticamente
                } else {
                    Utils.showToast(result.error, 'error');
                    $btn.prop('disabled', false).html('Entrar');
                }
            }
        });
    }
    
    initRegisterForm() {
        // Implementar registro se necessário
    }
}

window.Auth = new AuthManager();
