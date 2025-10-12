from odoo import models, fields

class BarcodeCategoryMapping(models.Model):
    _name = 'barcode.category.mapping'
    _description = 'Barcode Category Mapping'

    name = fields.Char('Keyword', required=True)
    code = fields.Char('Code', required=True)

class BarcodeBrandMapping(models.Model):
    _name = 'barcode.brand.mapping'
    _description = 'Barcode Brand Mapping'

    name = fields.Char('Keyword', required=True)
    code = fields.Char('Code', required=True)

class BarcodeProductMapping(models.Model):
    _name = 'barcode.product.mapping'
    _description = 'Barcode Product Mapping'

    name = fields.Char('Keyword', required=True)
    code = fields.Char('Code', required=True)
