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
        # Before the write, find the set of existing variant IDs
        variants_before_write = self.mapped('product_variant_ids')
        
        # Perform the standard write operation, which creates the new variants
        res = super(ProductTemplate, self).write(vals)

        # After the write, get the new set of all variants
        variants_after_write = self.mapped('product_variant_ids')
        
        # The difference between the two sets are the newly created variants
        new_variants = variants_after_write - variants_before_write
        
        # If new variants were created, generate barcodes for them
        if new_variants:
            new_variants.generate_barcode()
            
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

