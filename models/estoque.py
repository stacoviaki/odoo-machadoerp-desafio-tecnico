from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Estoque(models.Model):
    _name = 'controle.estoque'
    _description = 'Estoque de Combustível'

    name = fields.Char('Nome', required=True, default='Tanque Principal')
    capacidade = fields.Float('Capacidade (L)', required=True, default=6000)
    quantidade_atual = fields.Float('Estoque Atual (L)', default=0)
    percentual = fields.Float('Ocupação %', compute='_compute_percentual')

    @api.depends('quantidade_atual', 'capacidade')
    def _compute_percentual(self):
        for rec in self:
            rec.percentual = (rec.quantidade_atual / rec.capacidade * 100) if rec.capacidade else 0

    @api.constrains('quantidade_atual', 'capacidade')
    def _check_estoque(self):
        for rec in self:
            if rec.quantidade_atual < 0:
                raise ValidationError('Estoque não pode ser negativo!')
            if rec.quantidade_atual > rec.capacidade:
                raise ValidationError('Estoque não pode exceder a capacidade!')


class EstoqueEntrada(models.Model):
    _name = 'controle.estoque.entrada'
    _description = 'Entrada de Combustível'
    _order = 'data desc'

    name = fields.Char('Número', required=True, copy=False, readonly=True, default='Novo')
    estoque_id = fields.Many2one('controle.estoque', 'Tanque', required=True)
    data = fields.Date('Data', required=True, default=fields.Date.today)
    quantidade = fields.Float('Quantidade (L)', required=True)
    valor_litro = fields.Float('Valor/Litro', required=True)
    valor_total = fields.Float('Total', compute='_compute_total', store=True)
    fornecedor = fields.Char('Fornecedor')
    nota_fiscal = fields.Char('Nota Fiscal')
    usuario_id = fields.Many2one('res.users', 'Responsável', default=lambda self: self.env.user, readonly=True)

    @api.depends('quantidade', 'valor_litro')
    def _compute_total(self):
        for rec in self:
            rec.valor_total = rec.quantidade * rec.valor_litro

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Novo') == 'Novo':
                vals['name'] = self.env['ir.sequence'].next_by_code('controle.estoque.entrada') or 'Novo'
        records = super().create(vals_list)
        for record in records:
            record.estoque_id.quantidade_atual += record.quantidade
        return records    

    @api.constrains('quantidade', 'valor_litro')
    def _check_valores(self):
        for rec in self:
            if rec.quantidade <= 0:
                raise ValidationError('Quantidade deve ser maior que zero!')
            if rec.valor_litro <= 0:
                raise ValidationError('Valor/Litro deve ser maior que zero!')
