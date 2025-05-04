# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class HrPaymentPercentage(models.Model):
    _name = 'hr.payment.percentage'
    _inherit = ['mail.thread']

    name = fields.Char('Name', default='New')
    state = fields.Selection([
        ('draft','Draft'),('confirmed', 'Confirmed'),('approved','Approved'),('payslip','Computed In Payslip'),('refused','Refused')
    ], string='Status', default='draft')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    date_creation_payment = fields.Date('Request Date', default= fields.Date.today())
    payment_perc_date = fields.Date('Percentage Date')
    payment_perc_amount = fields.Float('Percentage Amount', compute="_compute_payment_perc_amount")
    payment_perc_reson = fields.Char('Reson')
    note = fields.Html('Notes')
    user_id = fields.Many2one('res.users', string='Responsible')
    payslip_id = fields.Many2one('hr.payslip', string='Payslip')
    invoice_id = fields.Many2one('account.move', string='Invoice', domain="[('move_type','=','out_invoice')]")
    payment_id = fields.Many2one('account.payment', string='Payment', domain="[('state','=','posted')]")
    percentage = fields.Float('Percentage', default=0.20)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.payment.percentage.seq') or '/'
        vals['user_id'] = self.env.user.id
        return super(HrPaymentPercentage, self).create(vals)
    
    
    @api.depends('payment_id.amount', 'percentage')
    def _compute_payment_perc_amount(self):
        for rec in self:
            perecnatge_amount = 0
            if rec.payment_id:
                perecnatge_amount = (rec.payment_id.amount * rec.percentage * 100)/100
            rec.payment_perc_amount = perecnatge_amount
                
    def confirmed_action(self):
        self.state = 'confirmed'

    def approved_action(self):
        self.state = 'approved'

    def refused_action(self):
        self.state = 'refused'