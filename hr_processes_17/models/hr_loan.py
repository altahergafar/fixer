# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError



class HrLoan(models.Model):
    _name = 'hr.loan.type'

    name = fields.Char('Description')
    loan_salary_rule_id = fields.Many2one('hr.salary.rule', string='Loan Salary Rule', default=lambda self: self.env.ref('hr_processes_17.hr_processes_rule_loans'))


class HrLoanRequest(models.Model):
    _name = 'hr.loan.request'
    _inherit = ['mail.thread']

    name = fields.Char('Name', default='New')
    state = fields.Selection([
        ('draft','Draft'),('confirme', 'Confirmed'),('computed','Installments Computed'),('full_paid','Fully Paid'),('cancel', 'Cancel')
    ], string='Status', default='draft')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    loan_type_id = fields.Many2one('hr.loan.type', string='Loan Type')
    date_loan = fields.Date('Loan Date')
    date_creation_loan = fields.Date('Request Date', default= fields.Date.today())
    loan_amount = fields.Float('Loan Amount')
    loan_reson = fields.Char('Loan Reson')
    no_months = fields.Integer('Installments Months', default=1)
    payment_st_date = fields.Date('Payment Start date')
    payment_ex_date = fields.Date('Payment Expiry date', compute="_compute_ex_date")
    request_line_id = fields.One2many('hr.loan.request.line','loan_id', string='Loan Installments')
    note = fields.Html('Notes')
    user_id = fields.Many2one('res.users', string='Responsible')
    is_computed = fields.Boolean('Is Computed')
    journal_id = fields.Many2one('account.journal', 'Loan Journal', required=True,
        states={'draft': [('readonly', False)]}, default=lambda self: self.env['account.journal'].search([('type', '=', 'general')], limit=1))
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    move_id = fields.Many2one('account.move', 'Accounting Entry', readonly=True, copy=False)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('loan.request.seq') or '/'
        vals['user_id'] = self.env.user.id
        return super(HrLoanRequest, self).create(vals)

    def reset_to_draft_action(self):
        
        for rec in self:
            loan_installments = self.env['hr.loan.request.line'].search([
                ('loan_id', '=', rec.id),
            ])
            if not loan_installments:
                rec.state = 'draft'
            else:
                # Separate paid and unpaid installments
                paid_installments = loan_installments.filtered(lambda l: l.installment_done)
                pending_installments = loan_installments.filtered(lambda l: not l.installment_done)

                if paid_installments and not pending_installments:
                    # All installments are paid
                    raise UserError('This Loan Request has installments already deducted from %s\'s salary' % rec.employee_id.name)
                elif pending_installments:
                    # If there are pending installments, you can clear lines and reset to draft
                    rec.request_line_id = [(5, 0, 0)]  # Clears the request lines
                    rec.state = 'draft'
                else:
                    # Mixed case: Some installments paid, some pending
                    raise UserError('Some installments are already paid for %s, but there are still pending installments.' % rec.employee_id.name)

            # Check if there is an associated journal entry (move_id)
            if rec.move_id:
                if rec.move_id.state == 'posted':
                    raise UserError('You cannot set this loan request to Draft because the move %s is already posted' % rec.move_id.name)
                elif rec.move_id.state == 'draft':
                    # If the journal entry is still in draft, it can be deleted
                    rec.move_id.unlink()
                    rec.state = 'draft'
            

    def confirme_action(self):
        self.state = 'confirme'

    def full_paid_action(self):
        
        for loan in self:
            line_ids = []
            date = loan.date_loan
            amount = loan.loan_amount
            debit_account_id = loan.employee_id.address_id.property_account_receivable_id.id
            if not debit_account_id:
                raise UserError('No Debit Account found in employee')

            credit_account_id = loan.journal_id.default_account_id.id
            if not credit_account_id:
                raise UserError('No Credit Account found in journal')

            name = _('Loan of %s') % (loan.employee_id.name)
            move_dict = {
                'narration': name,
                'ref': loan.name,
                'journal_id': loan.journal_id.id,
                'company_id': loan.company_id.id,
                'date': date,
            }

            
            debit_line = (0, 0, {
                'name': loan.name,
                'partner_id': loan.employee_id.address_id.id,
                'account_id': debit_account_id,
                'journal_id': loan.journal_id.id,
                'company_id': loan.company_id.id,
                'date': date,
                'debit': amount or 0.0,
                'credit':0.0,
                
            })
            line_ids.append(debit_line)

            credit_line = (0, 0, {
                'name': loan.name,
                'partner_id': loan.employee_id.address_id.id,
                'account_id': credit_account_id,
                'company_id': loan.company_id.id,
                'journal_id': loan.journal_id.id,
                'date': date,
                'debit': 0.0,
                'credit': amount or 0.0,
                
            })
            line_ids.append(credit_line)
            move_dict['line_ids'] = line_ids
            move = self.env['account.move'].create(move_dict)
            loan.write({'move_id': move.id})
            loan.state = 'full_paid'

    def cancel_action(self):
        
        for rec in self:
            loan_installments = self.env['hr.loan.request.line'].search([
                ('loan_id', '=', rec.id),
            ])
            if not loan_installments:
                rec.state = 'cancel'
            else:
                # paid installments
                paid_installments = loan_installments.filtered(lambda l: l.installment_done)
                if paid_installments:
                    raise UserError('You cannot cancel this Loan Request has installments already deducted from %s\'s salary' % rec.employee_id.name)

            if rec.move_id:
                if rec.move_id.state == 'posted':
                    raise UserError('You cannot cancel this Loan Request because the journal entry of %s is already posted.' % rec.move_id.name)

                if rec.move_id.state == 'draft':
                    rec.move_id.unlink()
                    rec.state = 'cancel'
            else:
                rec.state = 'cancel'
           

    @api.depends('no_months','payment_st_date')
    def _compute_ex_date(self):
        for record in self:
            if record.payment_st_date and record.no_months:
                start_date = fields.Date.from_string(record.payment_st_date)
                end_date = start_date + relativedelta(months=record.no_months - 1)
                record.payment_ex_date = fields.Date.to_string(end_date)
            else:
                record.payment_ex_date = False 


    @api.depends('no_months','loan_amount')
    def request_line_installments(self):
        
        for rec in self:
            if rec.loan_amount and rec.payment_st_date:
                installment_amount = rec.loan_amount / rec.no_months
                next_date = fields.Date.from_string(rec.payment_st_date)
                # Clear existing lines before populating
                rec.request_line_id = [(5, 0, 0)]  # Removes existing lines
                lines = []
                for i in range(rec.no_months):
                    # Calculate the installment date for each month
                    installment_date = next_date + relativedelta(months=i)
                    lines.append((0, 0, {
                        'installment_amount': installment_amount,
                        'installment_date': installment_date,
                        'loan_id': rec.id,
                    }))
                rec.request_line_id = lines
                rec.state = 'computed'


class HrLoanRequestLine(models.Model):
    _name = 'hr.loan.request.line'

    installment_amount = fields.Float('Installment amount', readonly=True)
    installment_date = fields.Date('Installment Date', readonly=True)
    installment_done = fields.Boolean('Installment Computed In Payslip')
    loan_id = fields.Many2one('hr.loan.request', string='Loan', readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', related='loan_id.employee_id', readonly=True)
    payslip_id = fields.Many2one('hr.payslip', string='Payslip')