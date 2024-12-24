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
from odoo import api, fields, models


class Mergerequest(models.Model):
    """requests merging class"""
    _name = 'merge.request.request'
    _description = 'Merging the selected requests'
    _rec_name = 'support_request_id'

    user_id = fields.Many2one('res.partner',
                              string='Responsible User',
                              help='User name of responsible person.',
                              default=lambda self: self.env.user.partner_id.id)
    support_team_id = fields.Many2one('team.servicerequest',
                                      string='Support Team',
                                      help='Name of the support team.')
    customer_id = fields.Many2one('res.partner', string='Customer',
                                  help='Name of the Customer ')
    support_request_id = fields.Many2one('service.request',
                                        string='Support request',
                                        help="Name of the support request")
    new_request = fields.Boolean(string='Create New request ?',
                                help='Creating new requests or not.',
                                default=False)
    subject = fields.Char(string='Subject', help='Enter the New request Subject')
    merge_reason = fields.Char(string='Merge Reason',
                               help='Reason for Merging the requests. ')
    support_request_ids = fields.One2many('support.servicerequest',
                                         'support_request_id',
                                         string='Support Service Request',
                                         help='Merged requests')
    active = fields.Boolean(string='Disable Record', help='Disable Record',
                            default=True)

    def default_get(self, fields_list):
        """Override the default_get method to provide default values for fields
        when creating a new record."""
        defaults = super(Mergerequest, self).default_get(fields_list)
        active_ids = self._context.get('active_ids', [])
        selected_requests = self.env['service.request'].browse(active_ids)
        customer_ids = selected_requests.mapped('customer_id')
        subjects = selected_requests.mapped('subject')
        display_names = selected_requests.mapped('display_name')
        servicerequest_team = selected_requests.mapped('team_id')
        descriptions = selected_requests.mapped('description')
        if len(customer_ids):
            defaults.update({
                'customer_id': customer_ids[0].id,
                'support_team_id': servicerequest_team,
                'support_request_ids': [(0, 0, {
                    'subject': subject,
                    'display_name': display_name,
                    'description': description,
                }) for subject, display_name, description in
                                       zip(subjects, display_names,
                                           descriptions)]
            })
        return defaults

    def action_merge_request(self):
        """Merging the requests or creating new requests"""
        if self.new_request:
            description = "\n\n".join(
                f"{request.subject}\n{'-' * len(request.subject)}\n{request.description}"
                for request in self.support_request_ids
            )
            self.env['service.request'].create({
                'subject': self.subject,
                'description': description,
                'customer_id': self.customer_id.id,
                'team_id': self.support_team_id.id,
            })
        else:
            if len(self.support_request_ids):
                description = "\n\n".join(
                    f"{request.subject}\n{'-' * len(request.subject)}\n{request.description}"
                    for request in self.support_request_ids
                )
                self.support_request_id.write({
                    'description': description,
                    'merge_request_invisible': True,
                    'merge_count': len(self.support_request_ids),
                })

    @api.onchange('support_request_id')
    def _onchange_support_request_id(self):
        """Onchange function to add the support request id."""
        self.support_request_ids.write({
            'merged_request': self.support_request_id
        })
