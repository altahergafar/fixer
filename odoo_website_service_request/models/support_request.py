# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Dhanya Babu (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import fields, models


class Supportservicerequest(models.Model):
    """Creating onetoMany model"""
    _name = 'support.servicerequest'
    _description = 'Support Service Request'

    subject = fields.Char(string='Subject', help='Subject of the merged '
                                                 'requests.')
    display_name = fields.Char(string='Display Name',
                               help='Display name of the merged requests.')
    description = fields.Char(string='Description',
                              help='Description of the requests.')
    support_request_id = fields.Many2one('merge.request.request',
                                        string='Support requests',
                                        help='Support requests')
    merged_request = fields.Integer(string='Merged request ID',
                                   help='Storing merged request id')
