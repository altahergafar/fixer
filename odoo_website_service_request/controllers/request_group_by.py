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
from odoo import http
from odoo.http import request


class requestGroupBy(http.Controller):
    """Controller for handling request grouping based on different criteria."""

    @http.route(['/requestgroupby'], type='json', auth="public", website=True)
    def request_group_by(self, **kwargs):
        """grouping requests based on user-defined criteria.
        Args:
        - kwargs (dict): Keyword arguments received from the HTTP request.
        Returns:
        - http.Response: Rendered HTTP response containing grouped request information.
        """
        context = []
        group_value = kwargs.get("search_value")
        if group_value == '0':
            context = []
            requests = request.env["service.request"].search(
                [('user_id', '=', request.env.user.id)])
            if requests:
                context.append({
                    'name': '',
                    'data': requests
                })
        if group_value == '1':
            context = []
            stage_ids = request.env['service.request.stage'].search([])
            for stage in stage_ids:
                request_ids = request.env['service.request'].search([
                    ('stage_id', '=', stage.id),
                    ('user_id', '=', request.env.user.id)
                ])
                if request_ids:
                    context.append({
                        'name': stage.name,
                        'data': request_ids
                    })
        if group_value == '2':
            context = []
            type_ids = request.env['servicerequest.type'].search([])
            for types in type_ids:
                request_ids_1 = request.env['service.request'].search([
                    ('request_type_id', '=', types.id),
                    ('user_id', '=', request.env.user.id)
                ])
                if request_ids_1:
                    context.append({
                        'name': types.name,
                        'data': request_ids_1
                    })
        values = {
            'requests': context,
        }
        response = http.Response(
            template='odoo_website_service_request.request_group_by_table',
            qcontext=values)
        return response.render()
