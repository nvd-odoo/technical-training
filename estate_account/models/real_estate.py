from odoo import fields, models,api, Command

class RealEstate(models.Model):
    _inherit = "real.estate"

    count_invoices = fields.Integer(compute="_count_invoices")

    def property_sold(self):
        for property in self:
            journal = self.env['account.journal'].search(
                [('type', '=', 'sale')],
                order="sequence asc",
                limit=1
            )
            move_vals = {
                'move_type': 'out_invoice',
                'partner_id': property.buyer_id.id,
                'journal_id': journal.id if journal else False,
                'line_ids' : [
                    Command.create({
                        'name': '6% du selling price',
                        'quantity': 1,
                        'price_unit': property.selling_price*0.06,
                        'property_id': property.id
                    }),
                    Command.create({
                        'name': 'Additionnal fees',
                        'quantity': 1,
                        'price_unit': 100000,
                        'property_id': property.id
                    })
                ]
            }
            move = self.env['account.move'].create(move_vals)
        return super().property_sold()

    def _count_invoices(self):
        for property in self:
            move_lines = self.env['account.move.line'].search([('property_id','=',property.id)])
            property.count_invoices = len(move_lines.move_id)
     
    def action_view_invoices(self):
        self.ensure_one()
        source_invoices = self.env['account.move'].search([('invoice_line_ids.property_id','=',self.id)])
        result = self.env['ir.actions.act_window']._for_xml_id('account.action_move_out_invoice_type')
        if len(source_invoices) > 1:
            result['domain'] = [('id', 'in', source_invoices.ids)]
        elif len(source_invoices) == 1:
            result['views'] = [(self.env.ref('account.view_move_form', False).id, 'form')]
            result['res_id'] = source_invoices.id
        else:
            result = {'type': 'ir.actions.act_window_close'}
        return result
            


