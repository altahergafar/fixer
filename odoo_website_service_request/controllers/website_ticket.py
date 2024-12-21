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


class WebsiteDesk(http.Controller):
    @http.route(['/servicerequest_ticket'], type='http', auth="public", website=True,
                sitemap=True)
    def servicerequest_ticket(self, **kwargs):
        """
        Route to display the servicerequest ticket creation form.
        Returns:
            http.Response: The HTTP response rendering the servicerequest ticket form.
        """
        types = request.env['servicerequest.type'].sudo().search([])
        categories = request.env['servicerequest.category'].sudo().search([])
        product = request.env['product.template'].sudo().search([])
        values = {}
        values.update({
            'types': types,
            'categories': categories,
            'product_website': product
        })
        return request.render('odoo_website_service_request.ticket_form', values)

    @http.route(['/rating/<int:ticket_id>'], type='http', auth="public",
                website=True,
                sitemap=True)
    def rating(self, ticket_id):
        """
        Route to display the rating form for a specific ticket. Args:
        ticket_id (int): The ID of the ticket for which the rating form is
        displayed. Returns: http.Response: The HTTP response rendering the
        rating form.
        """
        ticket = request.env['service.request'].browse(ticket_id)
        data = {
            'ticket': ticket.id,
        }
        return request.render('odoo_website_service_request.rating_form', data)

    @http.route(['/rating/<int:ticket_id>/submit'], type='http', auth="user",
                website=True, csrf=False,
                sitemap=True)
    def rating_backend(self, ticket_id, **post):
        ticket = request.env['service.request'].browse(ticket_id)
        ticket.write({
            'customer_rating': post['rating'],
            'review': post['message'],
        })
        return request.render('odoo_website_service_request.rating_thanks')
