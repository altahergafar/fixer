# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class HrViolation(models.Model):
    _name= 'hr.violation.type'

    name = fields.Char('Description')
    penalty_type_id = fields.Many2one('hr.penalty.type', string='Penalty Type')

class HrPenalty(models.Model):
    _name = 'hr.penalty.type'

    name = fields.Char('Description')
    is_salary_deduction = fields.Boolean('Is Salary Deduction')
    penalty_salary_rule_id = fields.Many2one('hr.salary.rule', string='Penalty Salary Rule', default=lambda self: self.env.ref('hr_processes_17.hr_processes_rule_penalty'))



class HrPenaltyRequest(models.Model):
    _name = 'hr.penalty.request'
    _inherit = ['mail.thread']

    name = fields.Char('Name', default='New')
    state = fields.Selection([
        ('draft','Draft'),('confirmed', 'Confirmed'),('approved','Approved'),('payslip','Computed In Payslip'),('refused','Refused')
    ], string='Status', default='draft')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    violation_id = fields.Many2one('hr.violation.type', string='Violation Type')
    violation_details = fields.Char('Violation Details')
    penalty_type_id = fields.Many2one('hr.penalty.type', string='Penalty Type', related='violation_id.penalty_type_id')
    is_salary_deduction = fields.Boolean('Is Salary Deduction', related='penalty_type_id.is_salary_deduction')
    deduction_amount = fields.Float('Deduction Amount')
    date_from_penalty = fields.Date('Penalty Period')
    date_to_penalty = fields.Date('To')
    date_violation = fields.Date('Violation Date')
    penalty_creation_date = fields.Date('Request Date', default= fields.Date.today())
    note = fields.Html('Notes')
    user_id = fields.Many2one('res.users', string='Responsible')
    payslip_id = fields.Many2one('hr.payslip', string='Payslip')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('penalty.request.seq') or '/'
        vals['user_id'] = self.env.user.id
        return super(HrPenaltyRequest, self).create(vals)


    def confirmed_action(self):
        self.state = 'confirmed'

    def approved_action(self):
        self.state = 'approved'

    def refused_action(self):
        self.state = 'refused'