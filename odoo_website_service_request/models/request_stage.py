# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Dhanya B (odoo@cybrosys.com)
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
from odoo import fields, models, _
from odoo.exceptions import UserError


class RequestStage(models.Model):
    """Stage request model """
    _name = 'service.request.stage'
    _description = 'request Stage'
    _order = 'sequence, id'
    _fold_name = 'fold'

    name = fields.Char('Name', help='Name of the request stage')
    active = fields.Boolean(string='Active', default=True, help='Active option'
                                                                'for request '
                                                                'stage.')
    sequence = fields.Integer(string='Sequence', default=50,
                              help='Sequence number of the request stage.')
    closing_stage = fields.Boolean('Closing Stage', default=False,
                                   help='Closing stage of the request.')
    cancel_stage = fields.Boolean('Cancel Stage', default=False,
                                  help='Cancel stage of the request.')
    starting_stage = fields.Boolean('Start Stage', default=False,
                                    help='Starting Stage of the request.')
    folded = fields.Boolean('Folded in Kanban', default=False,
                            help='Folded Stage of the request.')
    template_id = fields.Many2one('mail.template',
                                  help='Templates', string='Template',
                                  domain="[('model', '=', 'service.request')]")
    group_ids = fields.Many2many('res.groups', help='Group', string='Groups')
    fold = fields.Boolean(string='Fold', help='Folded option in request.')

    def unlink(self):
        """Unlinking Function to unlink the stage"""
        for rec in self:
            requests = rec.search([])
            sequence = requests.mapped('sequence')
            lowest_sequence = requests.filtered(
                lambda x: x.sequence == min(sequence))
            if self.name == "Draft":
                raise UserError(_("Cannot Delete This Stage"))
            if rec == lowest_sequence:
                raise UserError(_("Cannot Delete '%s'" % (rec.name)))
            else:
                res = super().unlink()
                return res
