from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Abastecimento(models.Model):
    _name = 'controle.abastecimento'
    _description = 'Abastecimento'
    _order = 'data_hora desc'

    name = fields.Char('Número', required=True, copy=False, readonly=True, default='Novo')
    equipamento_id = fields.Many2one('maintenance.equipment', 'Equipamento', required=True)
    placa = fields.Char('Placa')
    data_hora = fields.Datetime('Data/Hora', required=True, default=fields.Datetime.now)
    odometro = fields.Float('Odômetro/Horímetro', required=True)
    litros = fields.Float('Litros', required=True)
    valor_litro = fields.Float('Valor/Litro', required=True)
    valor_total = fields.Float('Total', compute='_compute_total', store=True)
    motorista_id = fields.Many2one('res.users', 'Motorista', required=True, default=lambda self: self.env.user)
    usuario_id = fields.Many2one('res.users', 'Responsável', default=lambda self: self.env.user, readonly=True)
    state = fields.Selection([('rascunho', 'Rascunho'), ('confirmado', 'Confirmado')], 'Status', default='rascunho')

    @api.depends('litros', 'valor_litro')
    def _compute_total(self):
        for rec in self:
            rec.valor_total = rec.litros * rec.valor_litro
	
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Novo') == 'Novo':
                vals['name'] = self.env['ir.sequence'].next_by_code('controle.abastecimento') or 'Novo'
        records = super().create(vals_list)
        for record in records:
            if record.state == 'confirmado':
                record._atualizar_estoque()
        return records

    def action_confirmar(self):
        self.ensure_one()
        self._atualizar_estoque()
        self.state = 'confirmado'

    def _atualizar_estoque(self):
        estoque = self.env['controle.estoque'].search([], limit=1)
        if not estoque:
            raise ValidationError('Nenhum tanque cadastrado!')
        if estoque.quantidade_atual < self.litros:
            raise ValidationError(f'Estoque insuficiente! Disponível: {estoque.quantidade_atual}L')
        estoque.quantidade_atual -= self.litros

    @api.constrains('litros', 'valor_litro', 'odometro')
    def _check_valores(self):
        for rec in self:
            if rec.litros <= 0:
                raise ValidationError('Litros deve ser maior que zero!')
            if rec.valor_litro <= 0:
                raise ValidationError('Valor/Litro deve ser maior que zero!')
            if rec.odometro <= 0:
                raise ValidationError('Odômetro deve ser maior que zero!')
