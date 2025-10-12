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
        # For each template being written to, store the set of its current variant IDs.
        # This is done before the write operation creates the new variants.
        variants_before_write = {template.id: set(template.product_variant_ids.ids) for template in self}

        # Perform the standard write operation. This is where Odoo creates the new variants.
        res = super(ProductTemplate, self).write(vals)

        # After the write, check each template for newly created variants.
        for template in self:
            variants_after_write = set(template.product_variant_ids.ids)
            variants_before = variants_before_write.get(template.id, set())
            
            # The difference between the two sets gives us the exact IDs of the new variants.
            new_variant_ids = list(variants_after_write - variants_before)

            if new_variant_ids:
                # Get the actual records for the new variants and generate barcodes for them.
                new_variants = self.env['product.product'].browse(new_variant_ids)
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

