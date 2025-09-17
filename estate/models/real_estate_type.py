from odoo import fields,models

class RealEstateType (models.Model):
    _name = "real.estate.type"
    _description = "Tags of properties"

    name=fields.Char( required=True )