from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def generate_barcode(self, force=False):
        """
        Delegates barcode generation to each of the template's variants.
        """
        for template in self:
            template.product_variant_ids.generate_barcode(force=force)

    def write(self, vals):
        """
        Handles two scenarios on update:
        1. If variants are added to a product that already has an internal reference.
        2. If an internal reference is added to a product that already has variants.
        """
        variants_before_write = {template.id: set(template.product_variant_ids.ids) for template in self}
        
        res = super(ProductTemplate, self).write(vals)

        for template in self:
            variants_after_write = set(template.product_variant_ids.ids)
            variants_before = variants_before_write.get(template.id, set())
            new_variant_ids = list(variants_after_write - variants_before)

            # If new variants were added, generate barcodes for them.
            if new_variant_ids:
                new_variants = self.env['product.product'].browse(new_variant_ids)
                new_variants.generate_barcode()
            
            # If the internal reference was just added, generate barcodes for all existing variants.
            if 'default_code' in vals and vals['default_code']:
                template.product_variant_ids.generate_barcode()
            
        return res

    @api.model_create_multi
    def create(self, vals_list):
        """
        After a new product template and its initial variants are created,
        trigger the barcode generation for all of them.
        """
        records = super(ProductTemplate, self).create(vals_list)
        for record in records:
            if record.default_code:
                record.generate_barcode()
        return records

    def generate_all_barcodes(self, force=False):
        """
        Server action to generate barcodes for all variants of selected products.
        """
        domain = [('default_code', '!=', False)]
        if not force:
            domain.append(('product_variant_ids.barcode', '=', False))
            
        products = self.search(domain)
        if products:
            products.generate_barcode(force=force)
        
        return {'type': 'ir.actions.client', 'tag': 'reload'}
    
    def clear_all_barcodes(self):
        """
        Server action to clear barcodes for all variants of selected products.
        """
        variants_to_clear = self.search([('default_code', '!=', False)]).product_variant_ids
        variants_to_clear.write({'barcode': False})
        
        return {'type': 'ir.actions.client', 'tag': 'reload'}


