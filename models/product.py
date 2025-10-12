from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def generate_barcode(self, force=False):
        """Delegates barcode generation to each of the template's variants."""
        for template in self:
            template.product_variant_ids.generate_barcode(force=force)

    def write(self, vals):
        """
        After any update, check if barcodes need to be generated.
        This robustly handles adding variants, adding an internal reference,
        or doing both in the same transaction.
        """
        res = super(ProductTemplate, self).write(vals)
        for template in self:
            if template.default_code:
                variants_to_process = template.product_variant_ids.filtered(lambda v: not v.barcode)
                if variants_to_process:
                    variants_to_process.generate_barcode()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        """
        After a new product is created, trigger barcode generation.
        This will be called after the variants' own create method.
        """
        records = super(ProductTemplate, self).create(vals_list)
        for record in records:
            if record.default_code:
                record.generate_barcode()
        return records

    def generate_all_barcodes(self, force=False):
        """Server action to generate barcodes for all variants of selected products."""
        domain = [('default_code', '!=', False)]
        if not force:
            domain.append(('product_variant_ids.barcode', '=', False))
        
        products = self.search(domain)
        if products:
            products.generate_barcode(force=force)
        
        return {'type': 'ir.actions.client', 'tag': 'reload'}
    
    def clear_all_barcodes(self):
        """Server action to clear barcodes for all variants of selected products."""
        variants_to_clear = self.search([('default_code', '!=', False)]).product_variant_ids
        variants_to_clear.write({'barcode': False})
        
        return {'type': 'ir.actions.client', 'tag': 'reload'}


