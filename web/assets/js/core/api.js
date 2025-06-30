class BRAVAAPIClient {
    constructor() {
        this.baseURL = '/api/v1';
        this.token = null;
        this.defaultHeaders = {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        };
    }
    
    setAuthToken(token) {
        this.token = token;
    }
    
    getHeaders() {
        const headers = { ...this.defaultHeaders };
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        return headers;
    }
    
    async request(method, endpoint, data = null, options = {}) {
        const config = {
            method: method.toUpperCase(),
            headers: this.getHeaders(),
            ...options
        };
        
        if (data && ['POST', 'PUT', 'PATCH'].includes(config.method)) {
            if (data instanceof FormData) {
                delete config.headers['Content-Type']; // Let browser set it for FormData
                config.body = data;
            } else {
                config.body = JSON.stringify(data);
            }
        }
        
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, config);
            return await this.handleResponse(response);
        } catch (error) {
            console.error('API Request Error:', error);
            throw error;
        }
    }
    
    async handleResponse(response) {
        if (response.status === 401) {
            // Token expirado, fazer logout
            Auth.logout();
            throw new Error('Sessão expirada');
        }
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `HTTP ${response.status}`);
        }
        
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return await response.json();
        }
        
        return response;
    }
    
    // Métodos de conveniência
    get(endpoint, options = {}) {
        return this.request('GET', endpoint, null, options);
    }
    
    post(endpoint, data, options = {}) {
        return this.request('POST', endpoint, data, options);
    }
    
    put(endpoint, data, options = {}) {
        return this.request('PUT', endpoint, data, options);
    }
    
    patch(endpoint, data, options = {}) {
        return this.request('PATCH', endpoint, data, options);
    }
    
    delete(endpoint, options = {}) {
        return this.request('DELETE', endpoint, null, options);
    }
    
    // Métodos específicos para recursos
    
    // Auth
    async auth(credentials) {
        return this.post('/auth/login/', credentials);
    }
    
    async refreshToken(refresh) {
        return this.post('/auth/refresh/', { refresh });
    }
    
    // Users
    async getCurrentUser() {
        return this.get('/auth/user/');
    }
    
    // Products
    async getProducts(params = {}) {
        const query = new URLSearchParams(params).toString();
        return this.get(`/products/${query ? '?' + query : ''}`);
    }
    
    async getProduct(id) {
        return this.get(`/products/${id}/`);
    }
    
    async createProduct(data) {
        return this.post('/products/', data);
    }
    
    async updateProduct(id, data) {
        return this.put(`/products/${id}/`, data);
    }
    
    async deleteProduct(id) {
        return this.delete(`/products/${id}/`);
    }
    
    // Orders
    async getOrders(params = {}) {
        const query = new URLSearchParams(params).toString();
        return this.get(`/orders/${query ? '?' + query : ''}`);
    }
    
    async getOrder(id) {
        return this.get(`/orders/${id}/`);
    }
    
    // Customers
    async getCustomers(params = {}) {
        const query = new URLSearchParams(params).toString();
        return this.get(`/customers/${query ? '?' + query : ''}`);
    }
    
    async getCustomer(id) {
        return this.get(`/customers/${id}/`);
    }
    
    // Dashboard
    async getDashboardStats() {
        return this.get('/dashboard/stats/');
    }
}

// Instância global da API
window.API = new BRAVAAPIClient();