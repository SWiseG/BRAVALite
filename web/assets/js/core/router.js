class BRAVARouter {
    constructor() {
        this.routes = {};
        this.currentRoute = null;
        this.params = {};
    }
    
    init(routes) {
        this.routes = routes;
        
        // Escutar mudanças no hash
        $(window).on('hashchange', () => this.handleRouteChange());
        
        // Interceptar cliques em links
        $(document).on('click', 'a[href^="#"]', (e) => {
            e.preventDefault();
            const href = $(e.currentTarget).attr('href');
            this.navigate(href.slice(1));
        });
    }
    
    navigate(path) {
        window.location.hash = '#' + path;
    }
    
    handleRouteChange() {
        const path = window.location.hash.slice(1) || '/';
        this.matchRoute(path);
    }
    
    matchRoute(path) {
        this.params = {};
        
        // Tentar match exato primeiro
        if (this.routes[path]) {
            this.currentRoute = path;
            this.routes[path]();
            return;
        }
        
        // Tentar match com parâmetros
        for (const route in this.routes) {
            if (route.includes(':')) {
                const regex = this.createRouteRegex(route);
                const match = path.match(regex);
                
                if (match) {
                    this.currentRoute = route;
                    this.extractParams(route, match);
                    this.routes[route](...Object.values(this.params));
                    return;
                }
            }
        }
        
        // Rota não encontrada
        if (this.routes['*']) {
            this.routes['*']();
        }
    }
    
    createRouteRegex(route) {
        const regexPattern = route
            .replace(/:[^/]+/g, '([^/]+)')
            .replace(/\//g, '\\/');
        return new RegExp(`^${regexPattern}$`);
    }
    
    extractParams(route, match) {
        const paramNames = route.match(/:([^/]+)/g) || [];
        paramNames.forEach((param, index) => {
            const paramName = param.slice(1);
            this.params[paramName] = match[index + 1];
        });
    }
    
    getCurrentRoute() {
        return this.currentRoute;
    }
    
    getParams() {
        return this.params;
    }
}

window.Router = new BRAVARouter();