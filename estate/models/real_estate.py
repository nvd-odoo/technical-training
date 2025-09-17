from odoo import fields,models,api,_
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import math
from odoo.exceptions import ValidationError,UserError
from odoo.tools.float_utils import float_compare

class RealEstate (models.Model):
    _name = "real.estate"
    _description = "List of properties" 

    name = fields.Char(
         required=True,
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default= fields.date.today() + relativedelta(months=3)
    )
    expected_price = fields.Float(
         required=True,
    )
    selling_price = fields.Float(
        readonly=True,
        copy=False,
    )
    bedrooms = fields.Integer(
        default="2",
    )
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
         selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
         ]
    )
    active=fields.Boolean(
        default=True
    )
    state = fields.Selection(
         selection=[
            ('new', 'New'),
            ('received', 'Offer Received'),
            ('accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
         ],
        default="new",
        copy=False,
        required=True,
    
    )
    estate_type_id=fields.Many2one("real.estate.type", string="Property Type")
    buyer_id=fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id=fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    estate_tags_ids=fields.Many2many("real.estate.tags", string="Property Tags")
    offer_ids=fields.One2many("real.estate.offer",'property_id', string="Property Offers")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    _sql_constraints = [('check_selling_price','CHECK(selling_price >= 0)',"the selling price must be positive"),
                       ('check_expecting_price','CHECK(expected_price > 0)',"the expecting price must be positive")
                       ]


    @api.depends("garden_area","living_area")
    def _compute_total_area(self):
        for estate in self:
            estate.total_area = estate.garden_area + estate.living_area

    @api.depends("offer_ids.price","offer_ids")
    def _compute_best_price(self):
        for estate in self:
            if estate.offer_ids:
                estate.best_price = max(estate.offer_ids.mapped("price"))
            else:
                estate.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def property_sold(self):
        if self.state == 'cancelled' or self.state == 'sold':
            raise UserError(_("You CANNOT sell a property which is cancelled or already sold."))
        else:            
            self.state = 'sold'
        

    def property_cancel(self):
        if self.state == 'cancelled' or self.state == 'sold':
            raise UserError(_("You CANNOT cancel a property which is already cancelled or sold."))
        else:
            self.state = 'cancelled'

    @api.constrains('selling_price','expected_price')
    def _compare_selling_expecting(self):
        for order in self:
            if order.selling_price != 0 and float_compare(order.selling_price/order.expected_price, 0.9, 2) == -1:
                raise ValidationError("Non non non")

    def unlink(self):
        for offer in self:
            if offer.state == 'received' or offer.state =='accepted' or offer.state =='sold':
                raise ValidationError("pas possible de delete frero")
        return super().unlink()
      


        
                 
        


    
