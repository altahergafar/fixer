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


class requestSearch(http.Controller):
    @http.route(['/requestsearch'], type='json', auth="public", website=True)
    def request_search(self, **kwargs):
        """
        Search for requests based on the provided search value.
        :param search_value: The value to search for in the request name or subject.
        :type search_value: str
        :return: A JSON response containing the matching requests.
        :rtype: http.Response
        """
        search_value = kwargs.get("search_value")
        requests = request.env["service.request"].search(
            ['|', ('name', 'ilike', search_value),
             ('subject', 'ilike', search_value)])
        values = {
            'requests': requests,
        }
        response = http.Response(template='odoo_website_service_request.request_table',
                                 qcontext=values)
        return response.render()
