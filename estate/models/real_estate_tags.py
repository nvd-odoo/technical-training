from odoo import fields,models

class RealEstateTags (models.Model):
    _name = "real.estate.tags"
    _description = "Type of properties"

    name=fields.Char( required=True )
    _sql_constraints = [('name_unique', 'unique(name)', "Tag name must be unique! Please choose another one.")]