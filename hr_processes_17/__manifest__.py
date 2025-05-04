# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Human Resource Processes',
    'version': '1.1',
    'category': 'Human Resources',
    'website': "http://www.qlinksoftware.com",
    'sequence': 3,
	'author': 'Qlink Software',
    'depends': [
        'hr_payroll',
        'hr',
		'account',
        
    ],
    'data': [
        'security/security_groups.xml',
		'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/salary_rules.xml',
        'views/hr_bonus.xml',
        'views/hr_loan.xml',
        'views/hr_penalty.xml',
        'views/hr_payslip.xml',
        'views/hr_employee.xml',
        'views/hr_payment_percentage.xml',
        'views/account_payment.xml',
        
    ],
    
    'application': True,
    'installable': True,
    'sequence': 1,
}
