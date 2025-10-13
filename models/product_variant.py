from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _get_code_from_mapping(self, model_name, default_code, record):
        # Prioritize variant's internal reference
        if record.default_code:
            ref_parts = record.default_code.split('-')
            mappings = self.env[model_name].search([])
            for mapping in mappings:
                if mapping.name in ref_parts:
                    return mapping.code

        # Then, check variant's attributes
        for attribute_value in record.product_template_attribute_value_ids:
            mappings = self.env[model_name].search([('name', '=', attribute_value.name)])
            if mappings:
                return mappings[0].code

        # Fallback to template's internal reference
        if record.product_tmpl_id.default_code:
            ref_parts = record.product_tmpl_id.default_code.split('-')
            mappings = self.env[model_name].search([])
            for mapping in mappings:
                if mapping.name in ref_parts:
                    return mapping.code
        
        return default_code

    def _get_barcode_prefix(self, record):
        category_code = self._get_code_from_mapping('barcode.category.mapping', "00", record)
        brand_code = self._get_code_from_mapping('barcode.brand.mapping', "0", record)
        product_code = self._get_code_from_mapping('barcode.product.mapping', "000", record)
        return category_code + brand_code + product_code

    def _get_next_barcode_sequence(self):
        return self.env['ir.sequence'].next_by_code('barcode.sequence') or ''

    def _resolve_barcode_conflict(self, barcode_base, record_id):
        """
        Resolves barcode conflicts by appending a suffix.
        If a barcode already exists, it appends '-1', '-2', etc., until a unique
        barcode is found.
        """
        # Check if the initial barcode exists
        existing_product = self.env['product.product'].search([
            ('barcode', '=', barcode_base),
            ('id', '!=', record_id)
        ], limit=1)

        if not existing_product:
            return barcode_base

        # If it exists, start appending a suffix
        original_barcode = barcode_base
        suffix = 1
        while True:
            new_barcode = f"{original_barcode}-{suffix}"
            existing_product = self.env['product.product'].search([
                ('barcode', '=', new_barcode),
                ('id', '!=', record_id)
            ], limit=1)
            if not existing_product:
                return new_barcode
            suffix += 1

    def generate_barcode(self, force=False):
        for record in self:
            if (not record.barcode or force) and (record.default_code or record.product_tmpl_id.default_code):
                
                # Prefix is determined by the variant's attributes or the template's internal reference.
                prefix = self._get_barcode_prefix(record)
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

