from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def generate_barcode(self, force=False):
        """
        This method is called from the product template but delegates
        the barcode generation to each of its variants.
        """
        for template in self:
            template.product_variant_ids.generate_barcode(force=force)

    def generate_all_barcodes(self, force=False):
        """
        Server action to generate barcodes for all variants of selected products.
        """
        domain = [('default_code', '!=', False)]
        if not force:
            # Find templates that have at least one variant without a barcode
            domain.append(('product_variant_ids.barcode', '=', False))
            
        products = self.search(domain)
        
        if products:
            products.generate_barcode(force=force)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    
    def clear_all_barcodes(self):
        """
        Server action to clear barcodes for all variants of selected products.
        """
        variants_to_clear = self.search([('default_code', '!=', False)]).product_variant_ids
        variants_to_clear.write({'barcode': False})
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        
    def write(self, vals):
        # First, perform the standard write operation
        res = super(ProductTemplate, self).write(vals)
        # After the write, check if new variants were created that need barcodes
        for template in self:
            # Find variants of this template that don't have a barcode yet
            variants_to_process = template.product_variant_ids.filtered(lambda v: not v.barcode)
            if variants_to_process:
                variants_to_process.generate_barcode()
        return res
        
    @api.model_create_multi
    def create(self, vals_list):
        """
        On creation of a template, trigger barcode generation for its variants.
        """
        records = super(ProductTemplate, self).create(vals_list)
        for record in records:
            if record.default_code:
                record.generate_barcode()
        return records

