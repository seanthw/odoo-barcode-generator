# Odoo Barcode Generator

This Odoo module automatically generates a unique, structured barcode for products based on their Internal Reference (SKU). The barcode is constructed from a prefix derived from the product's category, brand, and type, followed by a unique sequential number.

## Key Features

- **Automated Barcode Creation:** Automatically generates barcodes when a product is created, saving time and reducing manual errors.
- **Configurable Mappings:** Barcode generation rules (for category, brand, and product) are fully configurable through the Odoo UI. No code changes are needed to add new product types or brands.
- **Robust Sequencing:** Uses Odoo's native `ir.sequence` to ensure unique, conflict-free barcode generation, even in a multi-user environment.
- **Bulk Actions:** Provides server actions to generate or clear barcodes for multiple products at once from the product list view.
- **Structured & Readable Code:** The logic is refactored into small, maintainable methods, making it easy to understand and extend.
- **Full Product Variant Support:** Automatically generates a unique barcode for each individual product variant based on its specific attributes.

## How It Works

The barcode is generated from four components:

1.  **Category Code:** A 2-digit code representing the product category (e.g., "70" for Laptop).
2.  **Brand Code:** A 1-digit code for the brand (e.g., "2" for Dell).
3.  **Product Code:** A 3-digit code for the product line (e.g., "002" for Latitude).
4.  **Unique Sequence:** A 5-digit sequential number to ensure the barcode is unique.

**Note on Matching:** The module splits the Internal Reference by the hyphen (`-`) character and looks for an exact match between your defined keywords and the parts of the reference. For example, the reference `LT-DELL-LAT-02` is split into `['LT', 'DELL', 'LAT', '02']`, allowing the module to find the keywords `LT`, `DELL`, and `LAT`.

### Product Variant Support



This module correctly handles products with variants (e.g., different sizes or colors). It generates a unique barcode for **each specific variant**.



The system works by creating a temporary, unique internal reference for each variant before generating the barcode prefix. This is done by combining the main product's Internal Reference with the variant's specific attribute values.



**Example:**

-   **Product Template:**

    -   Internal Reference: `LT-DELL-LAT`

-   **Variant 1:**

    -   Attributes: `16GB`, `512GB`

    -   Temporary Reference for barcode generation: `LT-DELL-LAT-16GB-512GB`

    -   Resulting Barcode: `70200200001`

-   **Variant 2:**

    -   Attributes: `32GB`, `1TB`

    -   Temporary Reference for barcode generation: `LT-DELL-LAT-32GB-1TB`

    -   Resulting Barcode: `70200200002`



This ensures that every unique item in your inventory has its own distinct barcode, which is essential for accurate stock management.



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

## Upgrading the Module

When you update the module's source code (e.g., by pulling changes from git), you need to apply those changes to your Odoo database.

1.  **Update Files & Restart:** First, replace the files in your `addons` directory with the new version, then restart your Odoo container or server using the same method you did for installation.
2.  **Upgrade in Odoo:**
    - Go to the **Apps** menu.
    - Find the "Product Barcode Generator" module.
    - Click the module's menu (three dots) and select **Upgrade**.

This will apply any changes to the database, views, and data files.

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

#### Method 2: Manual & Bulk Actions (for existing products)

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

---

### Optional: Bulk Import Configuration

For initial setup, you can import all your mappings in bulk using CSV files instead of creating them one by one. Example files are provided in the `data/` directory of this module to serve as templates.

1.  **Prepare Your CSV Files:**
    - In the `data/` directory, you will find files ending in `.example.csv` (e.g., `category.mappings.example.csv`).
    - **Copy these files** and rename them without the `.example` extension (e.g., `category.mappings.csv`). These new files are ignored by git, so your private data will not be tracked.
    - Open your new CSV file (e.g., `category.mappings.csv`).
    - The file has two columns: `name` (the keyword from the Internal Reference) and `code` (the corresponding code for the barcode).
    - Add all of your mappings to this file.

2.  **Import into Odoo:**
    - In Odoo, navigate to the mapping screen you want to import (e.g., **Inventory -> Configuration -> Barcode -> Category Mappings**).
    - Click the **Import Records** button (cloud icon) in the top-left.
    - Click the **Upload File** button and select your prepared CSV file (e.g., `category.mappings.csv`).
    - Odoo will automatically map the columns from your file (`name`, `code`) to the correct fields.
    - Click the **Test** button to ensure your data is valid.
    - If the test is successful, click the **Import** button to complete the process.

Repeat this process for the Brand and Product mappings.

---

## Advanced Usage

### Mapping Code Requirements

To ensure barcodes are generated correctly, the codes you define in the mappings must follow these character length rules:

-   **Category Code:** Must be exactly **2** characters (e.g., "70", "AB").
-   **Brand Code:** Must be exactly **1** character (e.g., "2", "D").
-   **Product Code:** Must be exactly **3** characters (e.g., "002", "LAT").

The system will use the default codes ("00", "0", "000") if a mapping is not found, but adhering to these lengths for your custom codes is essential for a consistent barcode structure.

### How to Bulk Update Internal References

If you have many existing products that need their Internal Reference updated to match your new mapping keywords, the most efficient way is to use Odoo's import/export feature.

1.  **Navigate to Products:** Go to the **Products** list view.
2.  **Export Required Fields:**
    - Select the products you want to update.
    - Click the **Action** (gear icon) menu and choose **Export**.
    - In the export dialog, add two fields to the export list: `Name` and `Internal Reference`.
    - Click **Export**.
3.  **Update the File:**
    - Open the downloaded spreadsheet file.
    - Fill in or correct the `Internal Reference` for each product according to your new naming convention (e.g., `LT-DELL-LAT-01`).
    - Save the file.
4.  **Import the Changes:**
    - Go back to the **Products** list view.
    - Click the **Import Records** (cloud icon) button.
    - Upload your updated spreadsheet file.
    - Odoo will automatically match the columns. Click **Test** to verify.
    - If the test is successful, click **Import** to update all your products at once.
