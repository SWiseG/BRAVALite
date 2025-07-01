# -*- coding: utf-8 -*-
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseAuditModel

class Customer(BaseAuditModel):
    """Clientes"""
    
    CUSTOMER_TYPE_CHOICES = [
        ('PF', _('Pessoa Física')),
        ('PJ', _('Pessoa Jurídica')),
    ]
    
    GENDER_CHOICES = [
        ('M', _('Masculino')),
        ('F', _('Feminino')),
        ('O', _('Outro')),
        ('N', _('Não informar')),
    ]

    ClienteId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='ID_CLIENTE'
    )
    
    Codigo = models.CharField(
        _('Código'),
        max_length=20,
        unique=True,
        help_text=_('Código único do cliente'),
        db_column='CODIGO'
    )
    TipoPessoa = models.CharField(
        _('Tipo pessoa'),
        max_length=2,
        choices=CUSTOMER_TYPE_CHOICES,
        default='PF',
        db_column='TIPO_PESSOA'
    )
    Nome = models.CharField(
        _('Nome'), 
        max_length=255,
        db_column='NOME'
    )
    NomeFantasia = models.CharField(
        _('Nome fantasia'),
        max_length=255,
        blank=True,
        help_text=_('Para pessoa jurídica'),
        db_column='NOME_FANTASIA'
    )
    Documento = models.CharField(
        _('CPF/CNPJ'),
        max_length=20,
        unique=True,
        help_text=_('CPF ou CNPJ'),
        db_column='DOCUMENTO'
    )
    Email = models.EmailField(
        _('E-mail'), 
        blank=True,
        db_column='EMAIL'
    )
    Telefone = models.CharField(
        _('Telefone'),
        max_length=20,
        blank=True,
        db_column='TELEFONE'
    )
    Celular = models.CharField(
        _('Celular'),
        max_length=20,
        blank=True,
        db_column='CELULAR'
    )
    DataNascimento = models.DateField(
        _('Data nascimento'),
        null=True,
        blank=True,
        db_column='DATA_NASCIMENTO'
    )
    Sexo = models.CharField(
        _('Sexo'),
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        db_column='SEXO'
    )
    Observacoes = models.TextField(
        _('Observações'),
        blank=True,
        db_column='OBSERVACOES'
    )
    Ativo = models.BooleanField(_('Ativo'), default=True, db_column='ATIVO')
    Vip = models.BooleanField(_('VIP'), default=False, db_column='VIP')
    LimiteCredito = models.DecimalField(
        _('Limite crédito'),
        max_digits=10,
        decimal_places=2,
        default=0,
        db_column='LIMITE_CREDITO'
    )
    
    class Meta:
        db_table = 'CSM_CLIENTE'
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')
        ordering = ['Nome']
        indexes = [
            models.Index(fields=['Codigo'], name='IDX_CSM_CLI_COD'),
            models.Index(fields=['Documento'], name='IDX_CSM_CLI_DOC'),
            models.Index(fields=['Email'], name='IDX_CSM_CLI_EMAIL'),
            models.Index(fields=['Ativo'], name='IDX_CSM_CLI_ATIVO'),
            models.Index(fields=['TipoPessoa'], name='IDX_CSM_CLI_TIPO'),
        ]
    
    def __str__(self):
        return f"{self.Codigo} - {self.Nome}"
    
    def save(self, *args, **kwargs):
        if not self.Codigo:
            self.Codigo = self.generate_customer_code()
        super().save(*args, **kwargs)
    
    def generate_customer_code(self):
        """Gera código único do cliente"""
        import uuid
        prefix = 'CLI'
        uuid_short = str(uuid.uuid4())[:6].upper()
        return f"{prefix}{uuid_short}"

class CustomerAddress(BaseAuditModel):
    """Endereços dos clientes"""

    ADDRESS_TYPE_CHOICES = [
        ('BILLING', _('Cobrança')),
        ('SHIPPING', _('Entrega')),
        ('BOTH', _('Ambos')),
    ]
    
    EnderecoId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='ID_ENDERECO'
    )
    
    Cliente = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='enderecos',
        verbose_name=_('Cliente'),
        db_column='ID_CLIENTE'
    )
    TipoEndereco = models.CharField(
        _('Tipo'),
        max_length=20,
        choices=ADDRESS_TYPE_CHOICES,
        default='BOTH',
        db_column='TIPO_ENDERECO'
    )
    NomeEndereco = models.CharField(
        _('Nome endereço'),
        max_length=100,
        help_text=_('Ex: Casa, Trabalho, etc.'),
        db_column='NOME_ENDERECO'
    )
    Logradouro = models.CharField(
        _('Logradouro'),
        max_length=255,
        db_column='LOGRADOURO'
    )
    Numero = models.CharField(
        _('Número'),
        max_length=20,
        db_column='NUMERO'
    )
    Complemento = models.CharField(
        _('Complemento'),
        max_length=100,
        blank=True,
        db_column='COMPLEMENTO'
    )
    Bairro = models.CharField(
        _('Bairro'), 
        max_length=100,
        db_column='BAIRRO'
    )
    Cidade = models.CharField(
        _('Cidade'), 
        max_length=100,
        db_column='CIDADE'
    )
    Estado = models.CharField(
        _('Estado'), 
        max_length=2,
        db_column='ESTADO'
    )
    Cep = models.CharField(
        _('CEP'), 
        max_length=10,
        db_column='CEP'
    )
    Pais = models.CharField(
        _('País'),
        max_length=100,
        default='Brasil',
        db_column='PAIS'
    )
    Referencia = models.TextField(
        _('Referência'),
        blank=True,
        help_text=_('Ponto de referência'),
        db_column='REFERENCIA'
    )
    Principal = models.BooleanField(
        _('Principal'),
        default=False,
        db_column='PRINCIPAL'
    )
    Ativo = models.BooleanField(_('Ativo'), default=True, db_column='ATIVO')
    
    class Meta:
        db_table = 'CSM_ENDERECO'
        verbose_name = _('Endereço')
        verbose_name_plural = _('Endereços')
        indexes = [
            models.Index(fields=['Cliente'], name='IDX_CSM_END_CLI'),
            models.Index(fields=['Cep'], name='IDX_CSM_END_CEP'),
            models.Index(fields=['Principal'], name='IDX_CSM_END_PRINC'),
        ]
    
    def save(self, *args, **kwargs):
        if self.Principal:
            # Remover flag principal de outros endereços do cliente
            CustomerAddress.objects.filter(
                Cliente=self.Cliente
            ).exclude(pk=self.pk).update(Principal=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.NomeEndereco} - {self.Cliente.Nome}"

class CustomerContact(BaseAuditModel):
    """Contatos adicionais dos clientes"""
    
    CONTACT_TYPE_CHOICES = [
        ('PHONE', _('Telefone')),
        ('EMAIL', _('E-mail')),
        ('WHATSAPP', _('WhatsApp')),
        ('TELEGRAM', _('Telegram')),
        ('OTHER', _('Outro')),
    ]
    
    ContatoId = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='ID_CONTATO'
    )
    
    Cliente = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='contatos',
        verbose_name=_('Cliente'),
        db_column='ID_CLIENTE'
    )
    TipoContato = models.CharField(
        _('Tipo'),
        max_length=20,
        choices=CONTACT_TYPE_CHOICES,
        db_column='TIPO_CONTATO'
    )
    NomeContato = models.CharField(
        _('Nome'),
        max_length=100,
        help_text=_('Ex: Telefone comercial, E-mail pessoal'),
        db_column='NOME_CONTATO'
    )
    ValorContato = models.CharField(
        _('Valor'),
        max_length=255,
        help_text=_('Telefone, e-mail, etc.'),
        db_column='VALOR_CONTATO'
    )
    Principal = models.BooleanField(
        _('Principal'),
        default=False,
        db_column='PRINCIPAL'
    )
    Ativo = models.BooleanField(_('Ativo'), default=True, db_column='ATIVO')
    
    class Meta:
        db_table = 'CSM_CONTATO'
        verbose_name = _('Contato')
        verbose_name_plural = _('Contatos')
        indexes = [
            models.Index(fields=['Cliente'], name='IDX_CSM_CON_CLI'),
            models.Index(fields=['TipoContato'], name='IDX_CSM_CON_TIPO'),
        ]
    
    def __str__(self):
        return f"{self.NomeContato}: {self.ValorContato}"
