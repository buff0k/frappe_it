import frappe

def execute():
    # Get the default company configured in ERPNext
    default_company = frappe.db.get_single_value('Global Defaults', 'default_company')
    if not default_company:
        frappe.throw("Default company not found. Please ensure the default company is set in Global Defaults.")

    # Check if the Asset Category with the name 'IP Cameras' already exists
    if not frappe.db.exists('Asset Category', 'IP Cameras'):
        # Get the default Fixed Asset Account for the default company
        fixed_asset_account = frappe.db.get_value('Account', 
            {'company': default_company, 'account_type': 'Fixed Asset', 'root_type': 'Asset'}, 'name')
        
        if not fixed_asset_account:
            frappe.throw(f"Default Fixed Asset Account not found for company {default_company}. Please ensure the account exists.")

        # Create the new Asset Category
        asset_category = frappe.get_doc({
            'doctype': 'Asset Category',
            'asset_category_name': 'IP Cameras',
            'accounts': [{
                'company_name': default_company,
                'fixed_asset_account': fixed_asset_account
            }]
        })
        
        # Insert the document into the database
        asset_category.insert(ignore_permissions=True)
        frappe.msgprint(f"Asset Category 'IP Cameras' created successfully.")
    else:
        frappe.msgprint("Asset Category 'IP Cameras' already exists.")

    # Check if the Asset Category with the name 'NVRs' already exists
    if not frappe.db.exists('Asset Category', 'NVRs'):
        # Get the default Fixed Asset Account for the default company
        fixed_asset_account = frappe.db.get_value('Account', 
            {'company': default_company, 'account_type': 'Fixed Asset', 'root_type': 'Asset'}, 'name')
        
        if not fixed_asset_account:
            frappe.throw(f"Default Fixed Asset Account not found for company {default_company}. Please ensure the account exists.")

        # Create the new Asset Category
        asset_category = frappe.get_doc({
            'doctype': 'Asset Category',
            'asset_category_name': 'NVRs',
            'accounts': [{
                'company_name': default_company,
                'fixed_asset_account': fixed_asset_account
            }]
        })
        
        # Insert the document into the database
        asset_category.insert(ignore_permissions=True)
        frappe.msgprint(f"Asset Category 'NVRs' created successfully.")
    else:
        frappe.msgprint("Asset Category 'NVRs' already exists.")

    # Create or update Item Group DocType record
    if not frappe.db.exists("Item Group", "NVRs"):
        item_group = frappe.get_doc({
            "doctype": "Item Group",
            "item_group_name": "NVRs"
        })
        item_group.insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.msgprint(f"Item Group 'NVRs' created successfully.")

    if not frappe.db.exists("Item Group", "IP Cameras"):
        item_group = frappe.get_doc({
            "doctype": "Item Group",
            "item_group_name": "IP Cameras"
        })
        item_group.insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.msgprint(f"Item Group 'IP Cameras' created successfully.")