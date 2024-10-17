import frappe

def execute():
    # Fetch the default company
    default_company = frappe.defaults.get_defaults().get("company")
    if not default_company:
        frappe.throw("Default company is not set in ERPNext.")

    # Query an account with 'Account Type = Fixed Asset' and 'Root Type = Asset' for the default company
    fixed_asset_account = frappe.db.get_value("Account", 
        {
            "account_type": "Fixed Asset", 
            "root_type": "Asset", 
            "company": default_company
        }, 
        "name"
    )

    if not fixed_asset_account:
        frappe.throw(f"No fixed asset account found for company {default_company}. Please ensure that there is an account with Account Type 'Fixed Asset' and Root Type 'Asset'.")

    # Create or update Asset Category DocType record
    if not frappe.db.exists("Asset Category", "Cellphone Simcards"):
        asset_category = frappe.get_doc({
            "doctype": "Asset Category",
            "asset_category_name": "Cellphone Simcards",
            "accounts": [
                {
                    "company_name": default_company,
                    "fixed_asset_account": fixed_asset_account
                }
            ]
        })
        asset_category.insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.msgprint(f"Asset Category 'Cellphone Simcards' created successfully for company {default_company}.")

    # Create or update Item Group DocType record
    if not frappe.db.exists("Item Group", "Cellphone Simcards"):
        item_group = frappe.get_doc({
            "doctype": "Item Group",
            "item_group_name": "Cellphone Simcards"
        })
        item_group.insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.msgprint(f"Item Group 'Cellphone Simcards' created successfully.")
