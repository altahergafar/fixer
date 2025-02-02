# -*- coding: utf-8 -*-
############################################################################
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
############################################################################
{
    'name': "Website Service Request Management",
    'version': '17.0.1.0.1',
    'category': 'Website',
    'summary': """The website allows for the creation of requests, which can 
    then be controlled from the backend. Furthermore, a bill that includes 
    the service charge can be generated for the request for odoo community 
    Edition version 17.""",
    'description': """A request can be created from the website and subsequently
     managed from the backend. Additionally, a bill can be generated for the
     request, which includes the service cost.""",
    'author': "Cybrosys Techno Solutions",
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'depends': ['website', 'project', 'sale_project', 'hr_timesheet',
                'mail', 'contacts'],
    'data': [
        'security/odoo_website_service_request_groups.xml',
        'security/odoo_website_service_request_security.xml',
        'security/ir.model.access.csv',
        'data/servicerequest_category_data.xml',
        'data/servicerequest_replay_template_data.xml',
        'data/servicerequest_type_data.xml',
        'data/ir_cron_data.xml',
        'data/ir_sequence_data.xml',
        'data/mail_template_data.xml',
        'data/request_stage_data.xml',
        'views/servicerequest_category_views.xml',
        'views/servicerequest_tag_views.xml',
        'views/servicerequest_type_views.xml',
        'views/merge_request_views.xml',
        'views/odoo_website_service_request_portal_templates.xml',
        'views/portal_templates.xml',
        'views/rating_form.xml',
        'report/servicerequest_request_report_template.xml',
        'views/res_config_settings_views.xml',
        'views/team_servicerequest_views.xml',
        'views/request_servicerequest_views.xml',
        'views/request_stage_views.xml',
        'views/website_form.xml',
        'views/servicerequest_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'odoo_website_service_request/static/src/js/request_details.js',
            '/odoo_website_service_request/static/src/js/portal_search.js',
            '/odoo_website_service_request/static/src/js/multiple_product_choose.js',
        ]
    },
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
