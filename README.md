# Odoo Barcode Generator

This Odoo module automatically generates a unique, structured barcode for products based on their Internal Reference (SKU). The barcode is constructed from a prefix derived from the product's category, brand, and type, followed by a unique sequential number.

## Key Features

- **Automated Barcode Creation:** Automatically generates barcodes when a product is created, saving time and reducing manual errors.
- **Configurable Mappings:** Barcode generation rules (for category, brand, and product) are fully configurable through the Odoo UI. No code changes are needed to add new product types or brands.
- **Robust Sequencing:** Uses Odoo's native `ir.sequence` to ensure unique, conflict-free barcode generation, even in a multi-user environment.
- **Bulk Actions:** Provides server actions to generate or clear barcodes for multiple products at once from the product list view.
- **Structured & Readable Code:** The logic is refactored into small, maintainable methods, making it easy to understand and extend.

## How It Works

The barcode is generated from four components:

1.  **Category Code:** A 2-digit code representing the product category (e.g., "70" for Laptop).
2.  **Brand Code:** A 1-digit code for the brand (e.g., "2" for Dell).
3.  **Product Code:** A 3-digit code for the product line (e.g., "002" for Latitude).
4.  **Unique Sequence:** A 5-digit sequential number to ensure the barcode is unique.

### Example:

- **Internal Reference:** `LT-DELL-LAT`
- **Prefix:** `70` (LT) + `2` (DELL) + `002` (LAT) = `702002`
- **Sequence:** `00001`
- **Final Barcode:** `70200200001`

## Installation

1.  Copy this module folder into your Odoo `addons` directory.
2.  Restart the Odoo server.
3.  Go to **Apps**, search for "Barcode Generator", and click **Install**.

## Configuration

All barcode generation rules are managed within Odoo.

1.  Navigate to **Inventory -> Configuration -> Barcode**.
2.  Here you will find three new menu items:
    - **Category Mappings:** Define keywords (found in the Internal Reference) and their corresponding 2-digit category codes.
    - **Brand Mappings:** Define brand keywords and their 1-digit codes.
    - **Product Mappings:** Define product line keywords and their 3-digit codes.

**Example Configuration:**

- **Category Mapping:**
  - Keyword: `LT`, Code: `70`
- **Brand Mapping:**
  - Keyword: `DELL`, Code: `2`
- **Product Mapping:**
  - Keyword: `LAT`, Code: `002`

Once configured, any new product with an Internal Reference containing these keywords will have a barcode generated automatically.

## Usage

### Automatic Generation

When you create a new product and set its **Internal Reference**, the barcode will be generated automatically upon saving.

### Manual & Bulk Actions

You can manually trigger barcode generation from the product list view.

1.  Go to the **Products** list view.
2.  Select one or more products.
3.  Click the **Action** menu.
4.  Choose one of the following actions:
    - **Generate Barcode(s):** Creates barcodes for selected products that don't already have one.
    - **Force Regenerate Barcode(s):** Overwrites existing barcodes with new ones.
    - **Clear Barcode(s):** Removes the barcodes from the selected products.
