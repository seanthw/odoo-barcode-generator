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

**Note on Matching:** The module splits the Internal Reference by the hyphen (`-`) character and looks for an exact match between your defined keywords and the parts of the reference. For example, the reference `LT-DELL-LAT-02` is split into `['LT', 'DELL', 'LAT', '02']`, allowing the module to find the keywords `LT`, `DELL`, and `LAT`.

### Example:

- **Internal Reference:** `LT-DELL-LAT`
- **Prefix:** `70` (LT) + `2` (DELL) + `002` (LAT) = `702002`
- **Sequence:** `00001`
- **Final Barcode:** `70200200001`

## Installation

Follow the instructions for your specific Odoo setup.

### For Docker (Recommended)

1.  **Copy Module:** Place the `odoo-barcode-generator` folder into the Odoo addons directory that is mounted into your container (e.g., `test-addons`).
2.  **Restart Container:** Restart the Odoo container to ensure the new module is detected and file permissions are correctly set.
    ```bash
    docker compose restart <your_odoo_service_name>
    ```
3.  **Activate Developer Mode:** Log into your Odoo database, go to `Settings`, and click `Activate the developer mode`.
4.  **Update Apps List:** Go to the `Apps` menu. In the top menu, click `Update Apps List` and confirm the update in the dialog box.
5.  **Install:** Search for `Product Barcode Generator` (you may need to remove the default `Apps` filter in the search bar) and click `Install`.

### For Traditional Setups

1.  **Copy Module:** Place the `odoo-barcode-generator` folder into your Odoo's primary `addons` directory.
2.  **Set Permissions:** Ensure the module's files are owned by the user that runs the Odoo service.
    ```bash
    sudo chown -R odoo:odoo /path/to/odoo/addons/odoo-barcode-generator
    ```
3.  **Restart Server:** Restart the Odoo service.
    ```bash
    sudo systemctl restart odoo
    ```
4.  **Activate Developer Mode:** Log into your Odoo database, go to `Settings`, and click `Activate the developer mode`.
5.  **Update Apps List:** Go to the `Apps` menu. In the top menu, click `Update Apps List` and confirm the update in the dialog box.
6.  **Install:** Search for `Product Barcode Generator` (you may need to remove the default `Apps` filter in the search bar) and click `Install`.

## Getting Started: A Step-by-Step Guide

The entire system is based on matching keywords in a product's **Internal Reference** to codes that you define.

### Step 1: Configure the Barcode Mappings

This is the most important step. You need to teach the module how to build the barcode prefix.

1.  Navigate to the **Inventory** app.
2.  In the top menu, go to **Configuration -> Barcode**.
3.  You will see three new menu items:
    - **Category Mappings**
    - **Brand Mappings**
    - **Product Mappings**

Let's use the example from this README: a Dell Latitude laptop with the Internal Reference `LT-DELL-LAT`.

4.  **Create a Category Mapping:**
    - Click on **Category Mappings**.
    - Click "New".
    - In the **Keyword** field, type `LT`.
    - In the **Code** field, type `70`.
    - Save.

5.  **Create a Brand Mapping:**
    - Go back to **Configuration -> Barcode** and click on **Brand Mappings**.
    - Click "New".
    - In the **Keyword** field, type `DELL`.
    - In the **Code** field, type `2`.
    - Save.

6.  **Create a Product Mapping:**
    - Go back to **Configuration -> Barcode** and click on **Product Mappings**.
    - Click "New".
    - In the **Keyword** field, type `LAT`.
    - In the **Code** field, type `002`.
    - Save.

The configuration is now complete for this type of product.

### Step 2: Generate Barcodes

You can now generate barcodes automatically or manually.

#### Method 1: Automatic Generation (for new products)

1.  Go to **Inventory -> Products -> Products**.
2.  Click the **New** button to create a new product.
3.  Give it a name, like "Dell Latitude Laptop".
4.  Crucially, set the **Internal Reference** to `LT-DELL-LAT`.
5.  Click **Save**.

The module will automatically run, find your mappings, and generate the barcode.

#### Method 2: Manual Generation (for existing products)

If you have products that already exist, you can generate barcodes in bulk.

1.  Go to the **Products** list view (the view with all the checkboxes).
2.  Select one or more products that have an Internal Reference but no barcode.
3.  Click the **Action** button (the gear icon).
4.  You will see three new options:
    - **Generate Barcode(s):** Creates barcodes for the selected products.
    - **Force Regenerate Barcode(s):** Deletes old barcodes and creates new ones.
    - **Clear Barcode(s):** Removes the barcodes from the selected products.
5.  Choose the action you want to perform.

### Step 3: Verify the Result

Open the product form for the "Dell Latitude Laptop". In the **General Information** tab, you will see the **Barcode** field is now filled with a value like `70200200001`.

-   `702002` is the prefix we configured (`70` + `2` + `002`).
-   `00001` is the unique 5-digit sequence number. The next product you create will get `00002`, and so on.
