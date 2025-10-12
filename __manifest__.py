{
'name': 'Product Barcode Generator',
'version': '1.0',
'category': 'Inventory',
'summary': 'Generate barcodes for products based on internal references',
'description': """
    This module adds a button to product forms and lists to generate barcodes
    based on a structured formula that uses product category, brand, and internal references.
""",
'author': 'Sean Thawe',
'depends': ['product', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/barcode_sequence.xml',
        'views/products_views.xml',
        'views/barcode_mapping_views.xml',
        'data/barcode.category.mapping.csv',
        'data/barcode.brand.mapping.csv',
        'data/barcode.product.mapping.csv',
    ],

'installable': True,
'application': False,
'auto_install': False,
'license': 'LGPL-3',
}
