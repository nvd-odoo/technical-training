from odoo import fields,models,api
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.exceptions import ValidationError,UserError

class RealEstateOffer (models.Model):
    _name = "real.estate.offer"
    _description = "Offer for properties"

    name=fields.Char( required=True )
    price=fields.Float()
    status = fields.Selection(
         selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
         ],
    )
    partner_id=fields.Many2one('res.partner')
    property_id=fields.Many2one('real.estate')
    validity=fields.Integer()
    date_deadline=fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_dealine")

    _sql_constraints = [
        ("check_offer_price","CHECK(price > 0)","the price must be positive")
    ]


    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            base_date = offer.create_date.date() if offer.create_date else date.today()
            offer.date_deadline = base_date + relativedelta(days=offer.validity or 0)

    def _inverse_date_dealine(self):
        for offer in self:    
            if offer.date_deadline:
                dif = offer.date_deadline - offer.create_date.date()
                offer.validity = dif.days
            else:
                offer.validity = False      

    def accept_offer(self):
        for offer in self:
            if offer.status != 'accepted':
                offer.status = 'accepted'
                offer.property_id.selling_price = offer.price
                offer.property_id.buyer_id = offer.partner_id

    def refuse_offer(self):
        for offer in self:
            if offer.status != 'refused':
                offer.status = 'refused'
    
    @api.model_create_multi
    def create(self,vals_list):
        offers = super().create(vals_list)
        for offer in offers:
            if offer.property_id.best_price > offer.price:
                raise ValidationError("Non non non on veut plus cher mon grand")
            elif len(offer.property_id.offer_ids) == 1:
                offer.property_id.state = 'received'
        return offers


                    
