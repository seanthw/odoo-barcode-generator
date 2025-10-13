# Odoo Barcode Generator

This Odoo module automatically generates unique, structured barcodes for products and their variants based on the product's Internal Reference (SKU).

## Core Functionality

- **Automatic Barcode Generation:** Barcodes are created automatically when a product is saved.
- **Structured Barcodes:** Barcodes are built from a prefix (Category, Brand, Product) and a unique sequential number.
- **Configurable Mappings:** Define barcode prefixes through the Odoo UI without any code changes.
- **Product Variant Support:** Generates a unique barcode for each product variant.
- **Bulk Actions:** Server actions to generate, force-generate, or clear barcodes for multiple products at once.

## How It Works

The module generates a barcode by combining codes from three mappings:

1.  **Category Code:** 3-digit code (e.g., "060" for a specific category).
2.  **Brand Code:** 3-digit code (e.g., "010" for a brand).
3.  **Product Code:** 4-digit code (e.g., "0000" for a product type).
4.  **Unique Sequence:** A date-prefixed, 5-digit sequential number (e.g., `25101300001`).

The module finds the correct codes by splitting the product's **Internal Reference** by the hyphen (`-`) character and matching the parts to your defined keywords. For example, `LT-DELL-LAT` would match the keywords `LT`, `DELL`, and `LAT`.

**Note:** The codes for Category, Brand, and Product can now be of any length. The system is fully flexible.

For product variants, the module uses the following priority for finding keywords:
1.  Variant's own Internal Reference.
2.  Variant's attribute values.
3.  The parent product's Internal Reference.

## Installation

1.  Place the `odoo-barcode-generator` folder into your Odoo `addons` directory.
2.  Restart your Odoo server.
3.  Activate developer mode in Odoo.
4.  Go to `Apps`, click `Update Apps List`.
5.  Search for `Product Barcode Generator` and click `Install`.

## Configuration

1.  Navigate to **Inventory -> Configuration -> Barcode**.
2.  Create mappings for your categories, brands, and products.
    -   **Keyword:** The text to look for in the Internal Reference (e.g., `DELL`).
    -   **Code:** The corresponding code for the barcode (e.g., `2`).

## Usage

### Automatic Generation
- Create a new product.
- Set the **Internal Reference** to match your mapping keywords (e.g., `LT-DELL-LAT`).
- Save the product. The barcode will be generated automatically.

### Bulk Actions
- From the **Products** or **Product Variants** list view, select the items you want to update.
- Click the **Action** menu to generate or clear barcodes.

## Advanced Topics

### Bulk Import
You can import mappings from CSV files. Use the `.example.csv` files in the `data/` directory as templates.

1.  Navigate to **Inventory -> Configuration -> Barcode** and select the mapping type (e.g., **Category Mappings**).
2.  Click **Import Records** and upload your CSV file.