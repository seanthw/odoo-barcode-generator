from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

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
        # Search on product.product for conflicts
        existing_product = self.env['product.product'].search([
            ('barcode', '=', barcode_base),
            ('id', '!=', record_id)
        ], limit=1)

        suffix = 0
        original_barcode = barcode_base
        while existing_product:
            suffix += 1
            # This leaves room for up to 999 conflict resolutions
            barcode_base = original_barcode[0:9] + str(suffix).zfill(3)
            existing_product = self.env['product.product'].search([
                ('barcode', '=', barcode_base),
                ('id', '!=', record_id)
            ], limit=1)
        return barcode_base

    def generate_barcode(self, force=False):
        for record in self:
            if (not record.barcode or force) and record.product_tmpl_id.default_code:
                # Build a unique reference for the variant
                template_ref = record.product_tmpl_id.default_code
                variant_attributes = record.product_template_attribute_value_ids.mapped('name')
                # Create a stable string from attributes
                variant_ref_parts = sorted(variant_attributes)
                
                # Combine template ref with variant attributes for prefix generation
                full_ref = '-'.join([template_ref] + variant_ref_parts)

                prefix = self._get_barcode_prefix(full_ref)
                sequence = self._get_next_barcode_sequence()
                
                barcode_base = prefix + sequence
                
                barcode = self._resolve_barcode_conflict(barcode_base, record.id)

                # Assign the barcode to the variant
                record.barcode = barcode
