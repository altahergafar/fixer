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
from werkzeug.utils import redirect

from odoo import http
from odoo.addons.portal.controllers import portal

from odoo.exceptions import AccessError
from odoo.http import request


class requestPortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        """
        Prepare values for the home portal, including request count. Args:
        counters (dict): A dictionary containing counters for various portal
        information. Returns: dict: A dictionary of values for the home portal.
        """
        values = super()._prepare_home_portal_values(counters)
        if 'request_count' in counters:
            request_count = request.env['service.request'].search_count(
                self._get_requests_domain()) if request.env[
                'service.request'].check_access_rights(
                'read', raise_exception=False) else 0
            values['request_count'] = request_count
        return values

    def _get_requests_domain(self):
        """
        Define the domain for searching requests related to the current customer.
        Returns:
            list: A list representing the domain for request search.
        """
        return [('customer_id', '=', request.env.user.partner_id.id)]

    @http.route(['/my/requests'], type='http', auth="user", website=True)
    def portal_my_requests(self):
        """
        Route to display the requests associated with the current customer.
        Returns:
            http.Response: The HTTP response rendering the requests page.
        """
        domain = self._get_requests_domain()
        requests = request.env['service.request'].sudo().search(domain)
        values = {
            'default_url': "/my/requests",
            'requests': requests,
            'page_name': 'request',
        }
        return request.render("odoo_website_service_request.portal_my_requests", values)

    @http.route(['/my/requests/<int:id>'], type='http', auth="public",
                website=True)
    def portal_requests_details(self, **kwargs):
        """
        Route to display the details of a specific request.
        Args:
            request_id (int): The ID of the request to be displayed.
        Returns:
            http.Response: The HTTP response rendering the request details page.
        """
        request_id = kwargs.get("id")
        details = request.env['service.request'].sudo().browse(request_id)
        if not details or details.customer_id != request.env.user.partner_id:
            return redirect('/my/requests')
        data = {
            'page_name': 'request',
            'request': True,
            'details': details,
        }
        return request.render("odoo_website_service_request.portal_request_details",
                              data)

    @http.route('/my/requests/download/<id>', auth='public',
                type='http',
                website=True)
    def request_download_portal(self, **kwargs):
        """
        Route to download a PDF version of a specific request.
        Args:
            request (str): The ID of the request to be downloaded.
        Returns:
            http.Response: The HTTP response with the PDF file for download.
        """
        request_id = int(kwargs.get('id'))
        data = {
            'help': request.env['service.request'].sudo().browse(request_id)}
        report = request.env.ref(
            'odoo_website_service_request.report_request')
        pdf, _ = report.sudo()._render_qweb_pdf(
            report, res_ids=request_id, data=data)
        pdf_http_headers = [('Content-Type', 'application/pdf'),
                            ('Content-Length', len(pdf)),
                            ('Content-Disposition',
                             'attachment; filename="servicerequest request.pdf"')]
        return request.make_response(pdf, headers=pdf_http_headers)
