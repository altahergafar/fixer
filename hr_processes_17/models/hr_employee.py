# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    penalty_count = fields.Integer('Penalty Count', compute="_compute_employee_penalty")
    bonus_count = fields.Integer('Bonus Count', compute="_compute_employee_bonus")
    loan_count = fields.Integer('Loan Count', compute="_compute_employee_loan")


    def _preare_penalty_search_domain(self, employee_id):
        domain = [
            ('employee_id', '=', employee_id),
            ('penalty_type_id.is_salary_deduction', '=', True),
            ('state', '=', 'payslip')]

        return domain
    
    def _preare_bonus_search_domain(self, employee_id):
        domain = [
            ('employee_id', '=', employee_id),
            ('state', '=', 'payslip')]

        return domain

    def _preare_loan_search_domain(self, employee_id):
        domain = [
            ('employee_id', '=', employee_id),
            ('state', '=', 'full_paid')]
        return domain


    def _compute_employee_penalty(self):
        for payslip in self:
            penalty_ids = payslip.env['hr.penalty.request'].search(payslip._preare_penalty_search_domain(self.id))
            if penalty_ids:
                payslip.penalty_count = len(penalty_ids)
                print('penalty_count', payslip.penalty_count)
            else:
                payslip.penalty_count = 0


    def _compute_employee_bonus(self):
        for payslip in self:
            bonus_ids = payslip.env['hr.bonus.request'].search(payslip._preare_bonus_search_domain(self.id))
            if bonus_ids:
                payslip.bonus_count = len(bonus_ids)
                print('bonus_count', payslip.bonus_count)
            else:
                payslip.bonus_count = 0


    def _compute_employee_loan(self):
        for payslip in self:
            loan_ids = payslip.env['hr.loan.request'].search(payslip._preare_loan_search_domain(self.id))
            if loan_ids:
                payslip.loan_count = len(loan_ids)
                print('penalty_count', payslip.loan_count)
            else:
                payslip.loan_count = 0


    def action_employee_penalty(self):
        penalty_ids = self.env['hr.penalty.request'].search(self._preare_penalty_search_domain(self.id))
        return {
            'name': 'Penalties',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hr.penalty.request',
            'domain': [('id', 'in', penalty_ids.ids)],
            'target': 'current',
            'context': {'create': False},
        }

    def action_employee_bonus(self):
        bonus_ids = self.env['hr.bonus.request'].search(self._preare_bonus_search_domain(self.id))
        return {
            'name': 'Bonuses',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hr.bonus.request',
            'domain': [('id', 'in', bonus_ids.ids)],
            'target': 'current',
            'context': {'create': False},
        }

    def action_employee_loan(self):
        loan_ids = self.env['hr.loan.request'].search(self._preare_loan_search_domain(self.id))
        return {
            'name': 'Loans',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hr.loan.request',
            'domain': [('id', 'in', loan_ids.ids)],
            'target': 'current',
            'context': {'create': False},
        }