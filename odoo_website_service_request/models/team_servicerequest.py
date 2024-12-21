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


class Teamservicerequest(models.Model):
    """servicerequest team"""
    _name = 'team.servicerequest'
    _description = 'servicerequest Team'

    name = fields.Char('Name', help='servicerequest Team Name')
    team_lead_id = fields.Many2one('res.users', string='Team Leader',
                                   help='Team Leader Name',
                                   domain=lambda self: [
                                       ('groups_id', 'in', self.env.ref(
                                           'odoo_website_service_request.servicerequest_team_leader').id)])
    member_ids = fields.Many2many('res.users', string='Members',
                                  help='Team Members',
                                  domain=lambda self: [
                                      ('groups_id', 'in', self.env.ref(
                                          'odoo_website_service_request.servicerequest_user').id)])
    email = fields.Char('Email', help='Email of the team member.')
    project_id = fields.Many2one('project.project',
                                 string='Project',
                                 help='Projects related servicerequest team.')
    create_task = fields.Boolean(string="Create Task",
                                 help="Task created or not")

    @api.onchange('team_lead_id')
    def _onchange_team_lead_id(self):
        """Members selection function"""
        fetch_members = self.env['res.users'].search([])
        filtered_members = fetch_members.filtered(
            lambda x: x.id != self.team_lead_id.id)
        return {'domain': {'member_ids':
                               [('id', '=', filtered_members.ids), (
                                   'groups_id', 'in',
                                   self.env.ref('base.group_user').id),
                                ('groups_id', 'not in', self.env.ref(
                                    'odoo_website_service_request.servicerequest_team_leader').id)]}}
