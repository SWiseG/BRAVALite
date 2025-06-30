// spa/assets/js/core/i18n.js
class InternationalizationManager {
    constructor() {
        this.currentLanguage = 'pt-BR';
        this.translations = {};
        this.availableLanguages = [];
        this.fallbackLanguage = 'pt-BR';
        
        this.init();
    }
    
    async init() {
        try {
            // Carregar idiomas disponíveis
            await this.loadAvailableLanguages();
            
            // Definir idioma inicial
            await this.setInitialLanguage();
            
            // Carregar traduções
            await this.loadTranslations();
            
            console.log('i18n initialized');
        } catch (error) {
            console.error('Error trying to initialize i18n:', error);
        }
    }
    
    async loadAvailableLanguages() {
        try {
            const response = await API.get('/core/languages/active/');
            this.availableLanguages = response;
        } catch (error) {
            console.error('Erro ao carregar idiomas:', error);
            // Fallback para idiomas padrão
            this.availableLanguages = [
                { code: 'pt-BR', name: 'Português Brasil', native_name: 'Português Brasil' },
                { code: 'en-US', name: 'English United States', native_name: 'English' }
            ];
        }
    }
    
    async setInitialLanguage() {
        // 1. Verificar se usuário tem idioma definido
        if (Auth.getCurrentUser()?.language) {
            this.currentLanguage = Auth.getCurrentUser().language.code;
            return;
        }
        
        // 2. Verificar localStorage
        const savedLang = localStorage.getItem('ecommerce_language');
        if (savedLang && this.isLanguageAvailable(savedLang)) {
            this.currentLanguage = savedLang;
            return;
        }
        
        // 3. Detectar idioma do browser
        const browserLang = navigator.language || navigator.languages?.[0];
        if (browserLang && this.isLanguageAvailable(browserLang)) {
            this.currentLanguage = browserLang;
            return;
        }
        
        // 4. Usar idioma padrão do sistema
        try {
            const response = await API.get('/core/languages/default/');
            this.currentLanguage = response.code;
        } catch (error) {
            this.currentLanguage = this.fallbackLanguage;
        }
    }
    
    async loadTranslations(languageCode = null) {
        const lang = languageCode || this.currentLanguage;
        
        try {
            const response = await API.get(`/core/translations/by_language/?lang=${lang}`);
            this.translations = response;
            
            // Aplicar traduções na interface
            this.applyTranslations();
            
        } catch (error) {
            console.error('Error to load language:', error);
        }
    }
    
    isLanguageAvailable(code) {
        return this.availableLanguages.some(lang => lang.code === code);
    }
    
    // Função principal de tradução
    t(key, params = {}, defaultValue = null) {
        const keys = key.split('.');
        let value = this.translations;
        
        // Navegar pela estrutura aninhada
        for (const k of keys) {
            if (value && typeof value === 'object' && value.hasOwnProperty(k)) {
                value = value[k];
            } else {
                value = defaultValue || key;
                break;
            }
        }
        
        // Substituir parâmetros se fornecidos
        if (typeof value === 'string' && Object.keys(params).length > 0) {
            value = this.interpolate(value, params);
        }
        
        return value;
    }
    
    // Interpolação de parâmetros
    interpolate(text, params) {
        return text.replace(/\{\{(\w+)\}\}/g, (match, key) => {
            return params[key] !== undefined ? params[key] : match;
        });
    }
    
    // Aplicar traduções automáticas na interface
    applyTranslations() {
        // Traduzir elementos com data-i18n
        $('[data-i18n]').each((index, element) => {
            const $el = $(element);
            const key = $el.data('i18n');
            const params = $el.data('i18n-params') || {};
            
            const translation = this.t(key, params);
            
            // Verificar se deve traduzir conteúdo ou atributo
            const attr = $el.data('i18n-attr');
            if (attr) {
                $el.attr(attr, translation);
            } else {
                $el.text(translation);
            }
        });
        
        // Traduzir placeholders
        $('[data-i18n-placeholder]').each((index, element) => {
            const $el = $(element);
            const key = $el.data('i18n-placeholder');
            $el.attr('placeholder', this.t(key));
        });
        
        // Atualizar data-tables se existir
        if ($.fn.DataTable) {
            $('.data-table').each(function() {
                const table = $(this).DataTable();
                if (table) {
                    table.draw();
                }
            });
        }
    }
    
    // Alterar idioma
    async changeLanguage(languageCode) {
        if (!this.isLanguageAvailable(languageCode)) {
            throw new Error('Idioma não disponível');
        }
        
        const oldLanguage = this.currentLanguage;
        this.currentLanguage = languageCode;
        
        try {
            // Salvar no localStorage
            localStorage.setItem('ecommerce_language', languageCode);
            
            // Atualizar no backend se usuário logado
            if (Auth.getCurrentUser()) {
                await API.post('/core/translations/change_user_language/', {
                    language_code: languageCode
                });
            }
            
            // Carregar novas traduções
            await this.loadTranslations();
            
            // Notificar mudança
            $(document).trigger('languageChanged', {
                oldLanguage,
                newLanguage: languageCode
            });
            
            Utils.showToast(this.t('common.language_changed'), 'success');
            
        } catch (error) {
            // Reverter em caso de erro
            this.currentLanguage = oldLanguage;
            localStorage.setItem('ecommerce_language', oldLanguage);
            
            Utils.showToast(this.t('common.error_changing_language'), 'error');
            throw error;
        }
    }
    
    // Obter idioma atual
    getCurrentLanguage() {
        return this.currentLanguage;
    }
    
    // Obter idiomas disponíveis
    getAvailableLanguages() {
        return this.availableLanguages;
    }
    
    // Criar seletor de idiomas
    createLanguageSelector(containerId) {
        const container = $(`#${containerId}`);
        if (!container.length) return;
        
        const currentLang = this.availableLanguages.find(l => l.code === this.currentLanguage);
        
        const selectorHtml = `
            <div class="language-selector dropdown">
                <button class="language-selector-toggle" data-toggle="dropdown">
                    <span class="flag ${currentLang?.flag_icon || ''}"></span>
                    <span class="text">${currentLang?.native_name || 'Language'}</span>
                    <i class="icon-chevron-down"></i>
                </button>
                <div class="language-selector-menu dropdown-menu">
                    ${this.availableLanguages.map(lang => `
                        <a href="#" class="language-option ${lang.code === this.currentLanguage ? 'active' : ''}" 
                           data-lang="${lang.code}">
                            <span class="flag ${lang.flag_icon || ''}"></span>
                            <span class="text">${lang.native_name}</span>
                        </a>
                    `).join('')}
                </div>
            </div>
        `;
        
        container.html(selectorHtml);
        
        // Event handlers
        container.find('.language-option').on('click', async (e) => {
            e.preventDefault();
            const langCode = $(e.currentTarget).data('lang');
            
            if (langCode !== this.currentLanguage) {
                try {
                    await this.changeLanguage(langCode);
                    // Recriar seletor com novo idioma
                    this.createLanguageSelector(containerId);
                } catch (error) {
                    console.error('Erro ao alterar idioma:', error);
                }
            }
        });
    }
}

window.I18n = new InternationalizationManager();

window.t = (key, params, defaultValue) => I18n.t(key, params, defaultValue);
