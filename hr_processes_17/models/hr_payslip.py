# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    loan_installment_count = fields.Integer(compute="_compute_loan_data")
    loan_payslip_amount = fields.Float('Loan Amount')
    bonus_amount_cont = fields.Integer(compute="_compute_bonus_data")
    bonus_payslip_amount = fields.Float('Bonus Amount')
    penalty_amount_cont = fields.Integer(compute="_compute_penalty_data")
    penalty_payslip_amount = fields.Float('Penalty Amount')
    percent_amount_cont = fields.Integer(compute="_compute_percent_data")
    percent_payslip_amount = fields.Float('Percent Amount')


    def percent_amount(self):
        percent_total = 0
        # Batch fetch and update percentage
        percent_domain = [
            ('employee_id', '=', self.employee_id.id),
            ('payment_perc_date', '>=', self.date_from),
            ('payment_perc_date', '<=', self.date_to),
            ('state', '=', 'approved')
        ]
        perecnts = self.env['hr.payment.percentage'].search(percent_domain)
        perecnts.update({'state': 'payslip', 'payslip_id': self.id})
        percent_total = sum(percent.payment_perc_amount for percent in perecnts)
        self.percent_payslip_amount = percent_total
        return percent_total
    
   
    def bonus_amount(self):
        bonus_total = 0
        # Batch fetch and update bonuses
        bonus_domain = [
            ('employee_id', '=', self.employee_id.id),
            ('date_bonus', '>=', self.date_from),
            ('date_bonus', '<=', self.date_to),
            ('state', '=', 'approved')
        ]
        bonuses = self.env['hr.bonus.request'].search(bonus_domain)
        bonuses.update({'state': 'payslip', 'payslip_id': self.id})
        bonus_total = sum(bonus.bonus_amount for bonus in bonuses)
        self.bonus_payslip_amount = bonus_total
        return bonus_total

    def loan_amount(self):
        loan_total = 0
        # Batch fetch and update loan
        loan_domain = [
            ('loan_id.employee_id', 'in', self.mapped('employee_id').ids),
            ('installment_date', '>=', self.date_from),
            ('installment_date', '<=', self.date_to),
            ('installment_done', '=', False)
        ]
        loans = self.env['hr.loan.request.line'].search(loan_domain)
        loans.update({'installment_done': True, 'payslip_id': self.id})
        loan_total = sum(loan.installment_amount for loan in loans)
        self.loan_payslip_amount = loan_total
        return loan_total
    
    def penalty_amount(self):
        penalty_total = 0
        # Batch fetch and update loan
        penalty_domain = [
            ('employee_id', 'in', self.mapped('employee_id').ids),
            ('date_violation', '>=', self.date_from),
            ('date_violation', '<=', self.date_to),
            ('state', '=', 'approved')
        ]
        penalties = self.env['hr.penalty.request'].search(penalty_domain)
        penalties.update({'state': 'payslip', 'payslip_id': self.id})
        penalty_total = sum(penalty.deduction_amount for penalty in penalties)
        self.penalty_payslip_amount = penalty_total
        return penalty_total


    @api.model
    def _get_payslip_lines(self):
        # Call the super method to get the existing lines
        payslip_lines = super(HrPayslip, self)._get_payslip_lines()

        # Your custom logic to compute the bonus,loan,penalty,percent
        bonus_rule_id = self.env.ref('hr_processes_17.hr_processes_rule_bonus').id  # Reference your bonus salary rule
        loan_rule_id = self.env.ref('hr_processes_17.hr_processes_rule_loans').id  # Reference your loan salary rule
        penalty_rule_id = self.env.ref('hr_processes_17.hr_processes_rule_penalty').id  # Reference your penalty salary rule
        percent_rule_id = self.env.ref('hr_processes_17.hr_processes_rule_percentage').id  # Reference your percent salary rule
                
        contract = self.contract_id
        if contract:
            bonus_amount = self.bonus_amount()  # Implement your logic to calculate the bonus
            if bonus_amount:
                bonus_line = {
                    'salary_rule_id': bonus_rule_id,
                    'contract_id': contract.id,
                    'name': 'Bonus',
                    'code': 'BONUS',
                    'category_id': self.env.ref('hr_payroll.ALW').id,  # Reference your salary category
                    'sequence': 9,  # Adjust the sequence as needed
                    'appears_on_payslip': True,
                    # 'condition_select': 'none',
                    'amount': bonus_amount,
                    'employee_id': contract.employee_id.id,
                    'quantity': 1.0,
                    'rate': 100,
                    'slip_id': self.id,
                }
                payslip_lines.append(bonus_line)
            loan_amount = self.loan_amount()  # Implement your logic to calculate the loan
            if loan_amount:
                loan_line = {
                    'salary_rule_id': loan_rule_id,
                    'contract_id': contract.id,
                    'name': 'loans',
                    'code': 'LOANS',
                    'category_id': self.env.ref('hr_processes_17.LOAN').id,  # Reference your salary category
                    'sequence': 180,  # Adjust the sequence as needed
                    'appears_on_payslip': True,
                    # 'condition_select': 'none',
                    'amount': loan_amount,
                    'employee_id': contract.employee_id.id,
                    'quantity': 1.0,
                    'rate': 100,
                    'slip_id': self.id,
                }
                payslip_lines.append(loan_line)
            penalty_amount = self.penalty_amount()  # Implement your logic to calculate the penalty
            if penalty_amount:
                penalty_line = {
                    'salary_rule_id': penalty_rule_id,
                    'contract_id': contract.id,
                    'name': 'Penalties',
                    'code': 'PENALTIES',
                    'category_id': self.env.ref('hr_payroll.DED').id,  # Reference your salary category
                    'sequence': 150,  # Adjust the sequence as needed
                    'appears_on_payslip': True,
                    # 'condition_select': 'none',
                    'amount': -penalty_amount,
                    'employee_id': contract.employee_id.id,
                    'quantity': 1.0,
                    'rate': 100,
                    'slip_id': self.id,
                }
                payslip_lines.append(penalty_line)

            percent_amount = self.percent_amount()  # Implement your logic to calculate the percent
            if percent_amount:
                percent_line = {
                    'salary_rule_id': percent_rule_id,
                    'contract_id': contract.id,
                    'name': 'Percents',
                    'code': 'PERCENTS',
                    'category_id': self.env.ref('hr_payroll.ALW').id,  # Reference your salary category
                    'sequence': 10,  # Adjust the sequence as needed
                    'appears_on_payslip': True,
                    # 'condition_select': 'none',
                    'amount': percent_amount,
                    'employee_id': contract.employee_id.id,
                    'quantity': 1.0,
                    'rate': 100,
                    'slip_id': self.id,
                }
                payslip_lines.append(percent_line)
        return payslip_lines
     

    def compute_sheet(self):
            payslips = self.filtered(lambda slip: slip.state in ['draft', 'verify'])
            
            bonus_rule_id = self.env.ref('hr_processes_17.hr_processes_rule_bonus').id  # Reference your bonus salary rule
            loan_rule_id = self.env.ref('hr_processes_17.hr_processes_rule_loans').id  # Reference your loan salary rule
            penalty_rule_id = self.env.ref('hr_processes_17.hr_processes_rule_penalty').id  # Reference your penalty salary rule
            percent_rule_id = self.env.ref('hr_processes_17.hr_processes_rule_percentage').id  # Reference your percent salary rule
            
            excluded_lines = payslips.mapped('line_ids').filtered(lambda line: line.salary_rule_id.id not in [bonus_rule_id,loan_rule_id,penalty_rule_id,percent_rule_id])
            #delete old payslip lines except lines hold bonus , loan, penalty,percent
            excluded_lines.unlink()
           
            today = fields.Date.today()
            for payslip in payslips:
                number = payslip.number or self.env['ir.sequence'].next_by_code('salary.slip')
                payslip.write({
                    'number': number,
                    'state': 'verify',
                    'compute_date': today
                })

            self.env['hr.payslip.line'].create(payslips._get_payslip_lines())
            return True


    @api.depends('employee_id', 'date_from', 'date_to')
    def _compute_loan_data(self):
        if not self:
            return

        # Calculate the date range for the entire recordset to minimize queries
        date_from_min = min(self.mapped('date_from'))
        date_to_max = max(self.mapped('date_to'))

        # Group loans by payslip_id and compute count and amount
        loans = self.env['hr.loan.request.line'].read_group(
            domain=[
                ('loan_id.employee_id', 'in', self.mapped('employee_id').ids),
                ('installment_date', '>=', date_from_min),
                ('installment_date', '<=', date_to_max),
                # ('loan_id.state', '=', 'full_paid'),
                ('installment_done', '=', True),
                ('payslip_id', '=', self.id)
            ],
            fields=['payslip_id', 'id:count'],
            groupby=['payslip_id']
        )

        # Create a dictionary mapping payslip_id to loan count
        loan_data = {
            record['payslip_id'][0]: record['payslip_id_count']
            for record in loans
            if record.get('payslip_id')
        }

        for payslip in self:
            payslip.loan_installment_count = loan_data.get(payslip.id, 0)
            

    def action_view_loan(self):
        return {
            'name': 'Loans',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hr.loan.request.line',
            'domain': [('payslip_id', '=', self.id), ('loan_id.employee_id', '=', self.employee_id.id),('installment_done', '=', True)],
            'target': 'current',
            'context': {'create': False},
        }
    

    
    @api.depends('employee_id', 'date_from', 'date_to')
    def _compute_percent_data(self):
        if not self:
            return
        
        # Calculate the date range for the entire recordset to avoid multiple queries
        date_from_min = min(self.mapped('date_from'))
        date_to_max = max(self.mapped('date_to'))

        percents = self.env['hr.payment.percentage'].read_group(
            domain=[
                ('employee_id', 'in', self.mapped('employee_id').ids),
                ('state', '=', 'payslip'),
                ('payment_perc_date', '>=', date_from_min),
                ('payment_perc_date', '<=', date_to_max),
                ('payslip_id', '=', self.id),
            ],
            fields=['payslip_id'],
            groupby=['payslip_id']
        )
        percent_data = {
            record['payslip_id'][0]: record['payslip_id_count'] for record in percents if record.get('payslip_id')
        }
        for payslip in self:
            payslip.percent_amount_cont = percent_data.get(payslip.id, 0)


    def action_percent(self):
        return {
            'name': 'Percent',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hr.payment.percentage',
            'domain': [('payslip_id', '=', self.id), ('state', '=', 'payslip'),('employee_id', '=', self.employee_id.id)],
            'target': 'current',
            'context': {'create': False},
        }
            

    @api.depends('employee_id', 'date_from', 'date_to')
    def _compute_bonus_data(self):
        if not self:
            return

        # Calculate the date range for the entire recordset to avoid multiple queries
        date_from_min = min(self.mapped('date_from'))
        date_to_max = max(self.mapped('date_to'))

        # Group bonuses by payslip_id and compute count and amount
        bonuses = self.env['hr.bonus.request'].read_group(
            domain=[
                ('employee_id', 'in', self.mapped('employee_id').ids),
                ('state', '=', 'payslip'),
                ('date_bonus', '>=', date_from_min),
                ('date_bonus', '<=', date_to_max),
                ('payslip_id', '=', self.id),
            ],
            fields=['payslip_id'],
            groupby=['payslip_id']
        )
        # Create mapping of payslip_id to bonus counts safely
        bonus_data = {
            record['payslip_id'][0]: record['payslip_id_count']
            for record in bonuses
            if record.get('payslip_id')
        }
        for payslip in self:
            payslip.bonus_amount_cont = bonus_data.get(payslip.id, 0)
            
    
    def action_bonus(self):
        return {
            'name': 'Bonuses',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hr.bonus.request',
            'domain': [('payslip_id', '=', self.id), ('state', '=', 'payslip'),('employee_id', '=', self.employee_id.id)],
            'target': 'current',
            'context': {'create': False},
        }
            

    @api.depends('employee_id', 'date_from', 'date_to')
    def _compute_penalty_data(self):
        if not self:
            return

        # Calculate the date range for the entire recordset to minimize queries
        date_from_min = min(self.mapped('date_from'))
        date_to_max = max(self.mapped('date_to'))

        # Group penalties by payslip_id and compute count and amount
        penalties = self.env['hr.penalty.request'].read_group(
            domain=[
                ('employee_id', 'in', self.mapped('employee_id').ids),
                ('penalty_type_id.is_salary_deduction', '=', True),
                ('date_violation', '>=', date_from_min),
                ('date_violation', '<=', date_to_max),
                ('state', '=', 'payslip'),
                ('payslip_id', '=', self.id)
            ],
            fields=['payslip_id', 'id:count'],
            groupby=['payslip_id']
        )
        # Create a dictionary mapping payslip_id to penalties count
        penalties_data = {
            record['payslip_id'][0]: record['payslip_id_count']
            for record in penalties
            if record.get('payslip_id')
        }

        for payslip in self:
            payslip.penalty_amount_cont = penalties_data.get(payslip.id, 0)


    def action_penalty(self):
        return {
            'name': 'Penalties',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hr.penalty.request',
            'domain': [('payslip_id', '=', self.id), ('penalty_type_id.is_salary_deduction', '=', True), ('state', '=', 'payslip'),('employee_id', '=', self.employee_id.id)],
            'target': 'current',
            'context': {'create': False},
        }

    