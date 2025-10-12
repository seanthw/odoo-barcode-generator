from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_code_from_mapping(self, internal_ref, model_name, default_code):
        # Split the internal reference into parts to allow for more precise matching
        ref_parts = internal_ref.split('-')
        mappings = self.env[model_name].search([])
        for mapping in mappings:
            # Check if a keyword is one of the parts of the internal reference
            if mapping.name in ref_parts:
                return mapping.code
        return default_code

    def _get_barcode_prefix(self, internal_ref):
        category_code = self._get_code_from_mapping(internal_ref, 'barcode.category.mapping', "00")
        brand_code = self._get_code_from_mapping(internal_ref, 'barcode.brand.mapping', "0")
        product_code = self._get_code_from_mapping(internal_ref, 'barcode.product.mapping', "000")
        return category_code + brand_code + product_code

    def _get_next_barcode_sequence(self):
        sequence = self.env['ir.sequence'].next_by_code('barcode.sequence')
        if not sequence:
            # Create sequence if it does not exist
            sequence = self.env['ir.sequence'].create({
                'name': 'Barcode Sequence',
                'code': 'barcode.sequence',
                'prefix': '',
                'padding': 5,
            }).next_by_code('barcode.sequence')
        return sequence

    def _resolve_barcode_conflict(self, barcode_base, record_id):
        existing_product = self.env['product.template'].search([
            ('barcode', '=', barcode_base),
            ('id', '!=', record_id)
        ], limit=1)

        suffix = 0
        original_barcode = barcode_base
        while existing_product:
            suffix += 1
            # Only use the first 9 digits of the original barcode to keep proper length
            # This leaves room for up to 999 conflict resolutions
            barcode_base = original_barcode[0:9] + str(suffix).zfill(3)
            existing_product = self.env['product.template'].search([
                ('barcode', '=', barcode_base),
                ('id', '!=', record_id)
            ], limit=1)
        return barcode_base

    def generate_barcode(self, force=False):
        for record in self:
            if (not record.barcode or force) and record.default_code:
                internal_ref = record.default_code

                prefix = self._get_barcode_prefix(internal_ref)
                sequence = self._get_next_barcode_sequence()
                
                barcode_base = prefix + sequence
                
                barcode = self._resolve_barcode_conflict(barcode_base, record.id)

                # Assign the barcode
                record.barcode = barcode



    def generate_all_barcodes(self, force=False):
        # Get all products with internal references
        domain = [('default_code', '!=', False)]
        if not force:
            domain.append(('barcode', '=', False))
            
        products = self.search(domain)
        
        if products:
            products.generate_barcode(force=force)
        
        # Return a proper action for Odoo 18
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    
    def clear_all_barcodes(self):
        # Clear barcodes for products with an internal reference
        products = self.search([
            ('default_code', '!=', False)
        ])
        products.write({'barcode': False})
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        
    @api.model_create_multi
    def create(self, vals_list):
        # First, create the product(s) using the original method
        records = super(ProductTemplate, self).create(vals_list)
        # Now, iterate through the newly created records to generate barcodes
        for record in records:
            if not record.barcode and record.default_code:
                record.generate_barcode()
        return records
