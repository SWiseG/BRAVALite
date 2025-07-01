# -*- coding: utf-8 -*-
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseAuditModel

class Order(BaseAuditModel):
    """Pedidos"""
    PedidoId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='ID_PEDIDO'
    )
    STATUS_CHOICES = [
        ('PENDING', _('Pendente')),
        ('CONFIRMED', _('Confirmado')),
        ('PROCESSING', _('Processando')),
        ('SHIPPED', _('Enviado')),
        ('DELIVERED', _('Entregue')),
        ('CANCELLED', _('Cancelado')),
        ('RETURNED', _('Devolvido')),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', _('Pendente')),
        ('PAID', _('Pago')),
        ('FAILED', _('Falhou')),
        ('REFUNDED', _('Reembolsado')),
        ('PARTIAL', _('Parcial')),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('MONEY', _('Dinheiro')),
        ('CARD', _('Cartão')),
        ('PIX', _('PIX')),
        ('TRANSFER', _('Transferência')),
        ('INSTALLMENT', _('Parcelado')),
    ]
    
    Numero = models.CharField(
        _('Número'),
        max_length=20,
        unique=True,
        help_text=_('Número único do pedido'),
        db_column='NUMERO'
    )
    Cliente = models.ForeignKey(
        'customers.Customer',
        on_delete=models.PROTECT,
        verbose_name=_('Cliente'),
        db_column='ID_CLIENTE'
    )
    Vendedor = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Vendedor'),
        db_column='ID_VENDEDOR'
    )
    Status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        db_column='STATUS'
    )
    StatusPagamento = models.CharField(
        _('Status pagamento'),
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='PENDING',
        db_column='STATUS_PAGAMENTO'
    )
    FormaPagamento = models.CharField(
        _('Forma pagamento'),
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        null=True,
        blank=True,
        db_column='FORMA_PAGAMENTO'
    )
    Subtotal = models.DecimalField(
        _('Subtotal'),
        max_digits=10,
        decimal_places=2,
        default=0,
        db_column='SUBTOTAL'
    )
    Desconto = models.DecimalField(
        _('Desconto'),
        max_digits=10,
        decimal_places=2,
        default=0,
        db_column='DESCONTO'
    )
    Frete = models.DecimalField(
        _('Frete'),
        max_digits=10,
        decimal_places=2,
        default=0,
        db_column='FRETE'
    )
    Total = models.DecimalField(
        _('Total'),
        max_digits=10,
        decimal_places=2,
        default=0,
        db_column='TOTAL'
    )
    Observacoes = models.TextField(
        _('Observações'),
        blank=True,
        db_column='OBSERVACOES'
    )
    DataPedido = models.DateTimeField(
        _('Data pedido'),
        auto_now_add=True,
        db_column='DATA_PEDIDO'
    )
    DataEntregaPrevista = models.DateTimeField(
        _('Previsão entrega'),
        null=True,
        blank=True,
        db_column='DATA_ENTREGA_PREVISTA'
    )
    DataEntrega = models.DateTimeField(
        _('Data entrega'),
        null=True,
        blank=True,
        db_column='DATA_ENTREGA'
    )
    
    class Meta:
        db_table = 'PED_PEDIDO'
        verbose_name = _('Pedido')
        verbose_name_plural = _('Pedidos')
        ordering = ['-DataPedido']
        indexes = [
            models.Index(fields=['Numero'], name='IDX_PED_PED_NUM'),
            models.Index(fields=['Cliente'], name='IDX_PED_PED_CLI'),
            models.Index(fields=['Status'], name='IDX_PED_PED_STAT'),
            models.Index(fields=['DataPedido'], name='IDX_PED_PED_DATA'),
            models.Index(fields=['StatusPagamento'], name='IDX_PED_PED_PAG'),
        ]
    
    def __str__(self):
        return f"Pedido {self.Numero}"
    
    def save(self, *args, **kwargs):
        if not self.Numero:
            self.Numero = self.generate_order_number()
        self.calculate_total()
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        """Gera número único do pedido"""
        import uuid
        from datetime import datetime
        
        year = datetime.now().year
        uuid_short = str(uuid.uuid4())[:8].upper()
        return f"{year}{uuid_short}"
    
    def calculate_total(self):
        """Calcula o total do pedido"""
        self.Total = self.Subtotal - self.Desconto + self.Frete

class OrderItem(BaseAuditModel):
    """Itens do pedido"""
    PedidoItemId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='ID_PEDIDO_ITEM'
    )
    Pedido = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name=_('Pedido'),
        db_column='ID_PEDIDO'
    )
    Produto = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        verbose_name=_('Produto'),
        db_column='ID_PRODUTO'
    )
    ProdutoVariante = models.ForeignKey(
        'products.ProductVariation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Variação'),
        db_column='ID_VARIACAO'
    )
    Quantidade = models.PositiveIntegerField(
        _('Quantidade'),
        default=1,
        db_column='QUANTIDADE'
    )
    ValorUnitario = models.DecimalField(
        _('Valor unitário'),
        max_digits=10,
        decimal_places=2,
        db_column='VALOR_UNITARIO'
    )
    ValorTotal = models.DecimalField(
        _('Valor total'),
        max_digits=10,
        decimal_places=2,
        db_column='VALOR_TOTAL'
    )
    Desconto = models.DecimalField(
        _('Desconto'),
        max_digits=10,
        decimal_places=2,
        default=0,
        db_column='DESCONTO'
    )
    Observacoes = models.TextField(
        _('Observações'),
        blank=True,
        db_column='OBSERVACOES'
    )
    
    class Meta:
        db_table = 'PED_PEDIDO_ITEM'
        verbose_name = _('Item do pedido')
        verbose_name_plural = _('Itens do pedido')
        indexes = [
            models.Index(fields=['Pedido'], name='IDX_PED_ITE_PED'),
            models.Index(fields=['Produto'], name='IDX_PED_ITE_PRO'),
        ]
    
    def save(self, *args, **kwargs):
        self.ValorTotal = (self.Quantidade * self.ValorUnitario) - self.Desconto
        super().save(*args, **kwargs)
        
        # Atualizar total do pedido
        self.Pedido.calculate_total()
        self.Pedido.save()
    
    def __str__(self):
        return f"{self.Produto.Nome} x{self.Quantidade}"

class OrderPayment(BaseAuditModel):
    """Pagamentos do pedido"""
    PedidoPagamentoId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='ID_PEDIDO_PAGAMENTO'
    )
    PAYMENT_TYPE_CHOICES = [
        ('FULL', _('À vista')),
        ('INSTALLMENT', _('Parcelado')),
        ('PARTIAL', _('Parcial')),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', _('Pendente')),
        ('APPROVED', _('Aprovado')),
        ('REJECTED', _('Rejeitado')),
        ('CANCELLED', _('Cancelado')),
    ]
    
    Pedido = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='pagamentos',
        verbose_name=_('Pedido'),
        db_column='ID_PEDIDO'
    )
    TipoPagamento = models.CharField(
        _('Tipo'),
        max_length=20,
        choices=PAYMENT_TYPE_CHOICES,
        db_column='TIPO_PAGAMENTO'
    )
    FormaPagamento = models.CharField(
        _('Forma'),
        max_length=20,
        choices=Order.PAYMENT_METHOD_CHOICES,
        db_column='FORMA_PAGAMENTO'
    )
    Valor = models.DecimalField(
        _('Valor'),
        max_digits=10,
        decimal_places=2,
        db_column='VALOR'
    )
    Status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        db_column='STATUS'
    )
    TransacaoId = models.CharField(
        _('ID Transação'),
        max_length=255,
        blank=True,
        help_text=_('ID da transação no gateway'),
        db_column='TRANSACAO_ID'
    )
    DataPagamento = models.DateTimeField(
        _('Data pagamento'),
        null=True,
        blank=True,
        db_column='DATA_PAGAMENTO'
    )
    DataVencimento = models.DateTimeField(
        _('Data vencimento'),
        null=True,
        blank=True,
        db_column='DATA_VENCIMENTO'
    )
    Observacoes = models.TextField(
        _('Observações'),
        blank=True,
        db_column='OBSERVACOES'
    )
    
    class Meta:
        db_table = 'PED_PEDIDO_PAGAMENTO'
        verbose_name = _('Pagamento')
        verbose_name_plural = _('Pagamentos')
        indexes = [
            models.Index(fields=['Pedido'], name='IDX_PED_PAG_PED'),
            models.Index(fields=['Status'], name='IDX_PED_PAG_STAT'),
            models.Index(fields=['TransacaoId'], name='IDX_PED_PAG_TRANS'),
        ]
    
    def __str__(self):
        return f"Pagamento {self.Pedido.Numero} - {self.Valor}"

class OrderHistory(BaseAuditModel):
    """Histórico de alterações do pedido"""
    PedidoHistoricoId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='ID_PEDIDO_HISTORICO'
    )
    Pedido = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='historico',
        verbose_name=_('Pedido'),
        db_column='ID_PEDIDO'
    )
    StatusAnterior = models.CharField(
        _('Status anterior'),
        max_length=20,
        blank=True,
        db_column='STATUS_ANTERIOR'
    )
    StatusNovo = models.CharField(
        _('Status novo'),
        max_length=20,
        db_column='STATUS_NOVO'
    )
    Descricao = models.TextField(
        _('Descrição'),
        help_text=_('Descrição da alteração'),
        db_column='DESCRICAO'
    )
    IdUsuario = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Usuário'),
        db_column='ID_USUARIO'
    )
    
    class Meta:
        db_table = 'PED_PEDIDO_HISTORICO'
        verbose_name = _('Histórico')
        verbose_name_plural = _('Históricos')
        ordering = ['-DataInclusao']
        indexes = [
            models.Index(fields=['Pedido'], name='IDX_PED_HIS_PED'),
            models.Index(fields=['DataInclusao'], name='IDX_PED_HIS_DATA'),
        ]
    
    def __str__(self):
        return f"Histórico {self.Pedido.Numero} - {self.StatusNovo}"
