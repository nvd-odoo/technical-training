from odoo import fields, models,api, Command

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    property_id = fields.Many2one('real.estate')