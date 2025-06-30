class Utilities {
    constructor() {
        this.templates = new Map(); // Cache de templates
    }
    
    // Carregar templates HTML
    async loadTemplate(path) {
        if (this.templates.has(path)) {
            return this.templates.get(path);
        }
        
        try {
            const response = await fetch(`/static/${path}`);
            const html = await response.text();
            this.templates.set(path, html);
            return html;
        } catch (error) {
            console.error(`Erro ao carregar template ${path}:`, error);
            return '<div class="error">Erro ao carregar conteúdo</div>';
        }
    }
    
    // Sistema de toast/notifications
    showToast(message, type = 'info', duration = 5000) {
        const toastId = 'toast-' + Date.now();
        const toastHtml = `
            <div id="${toastId}" class="toast toast-${type}">
                <div class="toast-content">
                    <span class="toast-message">${message}</span>
                    <button class="toast-close">&times;</button>
                </div>
            </div>
        `;
        
        $('#toast-container').append(toastHtml);
        
        const $toast = $(`#${toastId}`);
        
        // Animar entrada
        $toast.addClass('show');
        
        // Auto-remover
        setTimeout(() => {
            $toast.removeClass('show');
            setTimeout(() => $toast.remove(), 300);
        }, duration);
        
        // Remover ao clicar
        $toast.find('.toast-close').on('click', () => {
            $toast.removeClass('show');
            setTimeout(() => $toast.remove(), 300);
        });
    }
    
    // Modal system
    async showModal(title, content, options = {}) {
        const modalId = 'modal-' + Date.now();
        const defaultOptions = {
            size: 'md', // sm, md, lg, xl
            backdrop: true,
            keyboard: true,
            buttons: []
        };
        
        const opts = { ...defaultOptions, ...options };
        
        const modalHtml = `
            <div id="${modalId}" class="modal modal-${opts.size}">
                <div class="modal-backdrop"></div>
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${title}</h5>
                            <button class="modal-close">&times;</button>
                        </div>
                        <div class="modal-body">
                            ${content}
                        </div>
                        ${opts.buttons.length ? `
                            <div class="modal-footer">
                                ${opts.buttons.map(btn => `
                                    <button class="btn btn-${btn.type || 'secondary'}" data-action="${btn.action}">
                                        ${btn.text}
                                    </button>
                                `).join('')}
                            </div>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;
        
        $('body').append(modalHtml);
        const $modal = $(`#${modalId}`);
        
        // Mostrar modal
        $modal.addClass('show');
        $('body').addClass('modal-open');
        
        // Event handlers
        const closeModal = () => {
            $modal.removeClass('show');
            $('body').removeClass('modal-open');
            setTimeout(() => $modal.remove(), 300);
        };
        
        // Fechar com X ou backdrop
        $modal.find('.modal-close').on('click', closeModal);
        if (opts.backdrop) {
            $modal.find('.modal-backdrop').on('click', closeModal);
        }
        if (opts.keyboard) {
            $(document).on('keyup.modal', (e) => {
                if (e.keyCode === 27) closeModal();
            });
        }
        
        // Botões customizados
        $modal.find('[data-action]').on('click', function() {
            const action = $(this).data('action');
            if (opts.buttons.find(b => b.action === action)?.callback) {
                opts.buttons.find(b => b.action === action).callback($modal, closeModal);
            }
        });
        
        return $modal;
    }
    
    // Confirm dialog
    confirm(message, title = 'Confirmação') {
        return new Promise((resolve) => {
            this.showModal(title, message, {
                buttons: [
                    {
                        text: 'Cancelar',
                        type: 'secondary',
                        action: 'cancel',
                        callback: (modal, close) => {
                            close();
                            resolve(false);
                        }
                    },
                    {
                        text: 'Confirmar',
                        type: 'primary',
                        action: 'confirm',
                        callback: (modal, close) => {
                            close();
                            resolve(true);
                        }
                    }
                ]
            });
        });
    }
    
    // Formatação de dados
    formatCurrency(value) {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value);
    }
    
    formatDate(date, format = 'dd/MM/yyyy') {
        if (!date) return '';
        return moment(date).format(format.replace(/dd/, 'DD').replace(/MM/, 'MM').replace(/yyyy/, 'YYYY'));
    }
    
    // Debounce para pesquisas
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Loading states
    showLoading(element) {
        const $el = $(element);
        $el.addClass('loading').prop('disabled', true);
        
        if (!$el.find('.spinner').length) {
            $el.append('<span class="spinner"></span>');
        }
    }
    
    hideLoading(element) {
        const $el = $(element);
        $el.removeClass('loading').prop('disabled', false);
        $el.find('.spinner').remove();
    }
    
    // Validação de formulários personalizada
    setupFormValidation($form, rules, options = {}) {
        const defaultOptions = {
            errorClass: 'error',
            validClass: 'valid',
            errorPlacement: (error, element) => {
                error.addClass('field-error');
                error.insertAfter(element);
            }
        };
        
        return $form.validate({
            ...defaultOptions,
            ...options,
            rules
        });
    }
}

window.Utils = new Utilities();
