from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _get_code_from_mapping(self, internal_ref, model_name, default_code):
        ref_parts = internal_ref.split('-')
        mappings = self.env[model_name].search([])
        for mapping in mappings:
            if mapping.name in ref_parts:
                return mapping.code
        return default_code

    def _get_barcode_prefix(self, internal_ref):
        category_code = self._get_code_from_mapping(internal_ref, 'barcode.category.mapping', "00")
        brand_code = self._get_code_from_mapping(internal_ref, 'barcode.brand.mapping', "0")
        product_code = self._get_code_from_mapping(internal_ref, 'barcode.product.mapping', "000")
        return category_code + brand_code + product_code

    def _get_next_barcode_sequence(self):
        return self.env['ir.sequence'].next_by_code('barcode.sequence') or ''

    def _resolve_barcode_conflict(self, barcode_base, record_id):
        existing_product = self.env['product.product'].search([
            ('barcode', '=', barcode_base),
            ('id', '!=', record_id)
        ], limit=1)
        original_barcode = barcode_base
        suffix = 0
        while existing_product:
            suffix += 1
            barcode_base = original_barcode[:9] + str(suffix).zfill(3)
            existing_product = self.env['product.product'].search([
                ('barcode', '=', barcode_base),
                ('id', '!=', record_id)
            ], limit=1)
        return barcode_base

    def generate_barcode(self, force=False):
        for record in self:
            if (not record.barcode or force) and record.product_tmpl_id.default_code:
                template_ref = record.product_tmpl_id.default_code
                
                # Prefix is determined ONLY by the template's internal reference.
                prefix = self._get_barcode_prefix(template_ref)
                sequence = self._get_next_barcode_sequence()
                
                if not sequence:
                    continue # Could not get a sequence number

                barcode_base = prefix + sequence
                barcode = self._resolve_barcode_conflict(barcode_base, record.id)
                record.barcode = barcode

    @api.model_create_multi
    def create(self, vals_list):
        # First, create the variants using the original method.
        records = super(ProductProduct, self).create(vals_list)
        # Now, trigger barcode generation for the newly created variants.
        records.generate_barcode()
        return records

