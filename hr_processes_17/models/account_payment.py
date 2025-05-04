# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    percentage = fields.Float('Percentage', default=0.20)
    percentage_done = fields.Boolean('Percentage Done')

    
    def action_create_perecntage(self):
        if not self.env.user.has_group('hr_processes_17.group_hr_processes'):
            raise UserError(_('Only the Hr Processes Officer can Create Payment Percentage.'))
        if self.state == 'posted' and self.employee_id:
            perecnatge_amount = (self.amount * self.percentage * 100)/100
            payment_percentage = self.env['hr.payment.percentage'].create({
            'payment_perc_amount': perecnatge_amount,
            'employee_id': self.employee_id.id,
            'percentage': self.percentage,
            'payment_id': self.id,
            'payment_perc_date': self.date,
            
        })
            if payment_percentage:
                self.percentage_done = True
                return payment_percentage
