# -*- coding: utf-8 -*-

# import base64
# from odoo import models, fields, api
# from odoo.exceptions import UserError



from odoo import models, fields, api
import base64
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    contract_generated = fields.Boolean(string='Contract Generated', default=False)

    def create_contract_pdf(self):
        if not self.contract_generated:
            # Render the PDF using the report template
            report_action = self.env.ref('contract_after_sale_order.action_report_contract_sale_id')
            pdf_content, content_type = report_action.render_qweb_pdf(self.ids)
            pdf_attachment = self.env['ir.attachment'].create({
                'name': f'Contract_{self.name}.pdf',
                'type': 'binary',
                'datas': base64.b64encode(pdf_content),
                'res_model': 'sale.order',
                'res_id': self.id,
                'mimetype': 'application/pdf',
            })
            self.contract_generated = True
            return pdf_attachment
        else:
            raise UserError("Contract has already been generated.")

    def send_contract_email(self):
        # Ensure the contract PDF is generated
        if not self.contract_generated:
            attachment = self.create_contract_pdf()
        else:
            attachment = self.env['ir.attachment'].search([
                ('res_model', '=', 'sale.order'),
                ('res_id', '=', self.id),
                ('name', 'like', f'Contract_{self.name}.pdf')
            ], limit=1)

        # Prepare and send the email
        template = self.env.ref('contract_after_sale_order.email_template_contract')
        template.attachment_ids = [(4, attachment.id)]
        template.send_mail(self.id, force_send=True)



# class SaleOrder(models.Model):
#     _inherit = 'sale.order'

#     contract_generated = fields.Boolean(string='Contract Generated', default=False)

#     @api.model
#     def create_contract(self):
#         if not self.contract_generated:
#             # Generate the contract (you can customize the content here)
#             contract_content = f"""
#             Contract Agreement
#             -------------------
#             Customer: {self.partner_id.name}
#             Sale Order: {self.name}
#             Total: {self.amount_total} {self.currency_id.name}
#             """
#             # Save the contract as an attachment
#             attachment = self.env['ir.attachment'].create({
#                 'name': f'Contract_{self.name}.pdf',
#                 'type': 'binary',
#                 'datas': base64.b64encode(contract_content.encode('utf-8')),
#                 'res_model': 'sale.order',
#                 'res_id': self.id,
#                 'mimetype': 'text/plain',
#             })
#             self.contract_generated = True
#             return attachment
#         else:
#             raise UserError("Contract has already been generated.")

#     def send_contract_email(self):
#         # Ensure the contract is generated
#         if not self.contract_generated:
#             attachment = self.create_contract()
#         # else:
#         #     attachment = self.env['ir.attachment'].search([
#         #         ('res_model', '=', 'sale.order'),
#         #         ('res_id', '=', self.id),
#         #         ('name', 'like', f'Contract_{self.name}.pdf')
#         #     ], limit=1)

#         # # Prepare and send the email
#         template = self.env.ref('contract_after_sale_order.email_template_contract')
#         template.attachment_ids = [(4, attachment.id)]
#         template.send_mail(self.id, force_send=True)