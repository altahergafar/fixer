# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class HrBonus(models.Model):
    _name = 'hr.bonus.type'

    name = fields.Char('Description')
    bonus_salary_rule_id = fields.Many2one('hr.salary.rule', string='Bonus Salary Rule', default=lambda self: self.env.ref('hr_processes_17.hr_processes_rule_bonus'))


class HrBonusRequest(models.Model):
    _name = 'hr.bonus.request'
    _inherit = ['mail.thread']

    name = fields.Char('Name', default='New')
    state = fields.Selection([
        ('draft','Draft'),('confirmed', 'Confirmed'),('approved','Approved'),('payslip','Computed In Payslip'),('refused','Refused')
    ], string='Status', default='draft')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    bonus_type_id = fields.Many2one('hr.bonus.type', string='Bonus Type')
    date_creation_bouns = fields.Date('Request Date', default= fields.Date.today())
    date_bonus = fields.Date('Bonus Date')
    bonus_amount = fields.Float('Bonus Amount')
    bonus_reson = fields.Char('Bonus Reson')
    note = fields.Html('Notes')
    user_id = fields.Many2one('res.users', string='Responsible')
    payslip_id = fields.Many2one('hr.payslip', string='Payslip')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('bonus.request.seq') or '/'
        vals['user_id'] = self.env.user.id
        return super(HrBonusRequest, self).create(vals)



    def confirmed_action(self):
        self.state = 'confirmed'

    def approved_action(self):
        self.state = 'approved'

    def refused_action(self):
        self.state = 'refused'