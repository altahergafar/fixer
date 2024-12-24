# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
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
#############################################################################
from odoo import http
from odoo.http import request


class HelpDeskrequests(http.Controller):
    @http.route(['/help/requests'], type="json", auth="user")
    def elearning_snippet(self):
        requests = []
        help_requests = request.env['service.request'].sudo().search(
            [('stage_id.name', '=', 'Inbox')])
        for i in help_requests:
            requests.append(
                {'name': i.name, 'subject': i.subject, 'id': i.id})
        values = {
            'h_requests': requests
        }
        response = http.Response(
            template='odoo_website_service_request_dashboard.dashboard_requests',
            qcontext=values)
        return response.render()
