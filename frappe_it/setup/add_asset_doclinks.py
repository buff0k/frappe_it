# Copyright (c) 2025, buff0k and contributors
# For license information, please see license.txt

import frappe

def ensure_asset_links():
    """Ensure required Document Links exist in the Asset DocType and expand to Asset Allocation List."""
    
    required_links = [
        {"link_doctype": "Simcard Allocations", "link_fieldname": "sim_no"},
        {"link_doctype": "Asset Allocation Table", "link_fieldname": "asset", "parent_doctype": "Asset Allocation", "table_fieldname": "list_of_allocated_assets", "is_child_table": 1}
    ]

    # Fetch existing links
    existing_links = frappe.get_all(
        "DocType Link",
        filters={"parent": "Asset"},
        fields=["link_doctype", "link_fieldname"]
    )

    existing_links_set = {(link["link_doctype"], link["link_fieldname"]) for link in existing_links}

    for link in required_links:
        # Check if the link already exists
        if (link["link_doctype"], link["link_fieldname"]) not in existing_links_set:
            # If it's a child table, we need to handle it differently
            if link.get("is_child_table"):
                doc = frappe.get_doc({
                    "doctype": "DocType Link",
                    "parent": "Asset",  # The parent of the child table
                    "parentfield": "links",  # The parentfield for the parent doctype
                    "parenttype": "DocType",  # The parent type
                    "link_doctype": link["link_doctype"],
                    "link_fieldname": link["link_fieldname"],
                    "parent_doctype": link["parent_doctype"],
                    "table_fieldname": link["table_fieldname"],
                    "is_child_table": link["is_child_table"],
                    "group": "IT Resources"
                })
            else:
                # If it's not a child table, the original logic applies
                doc = frappe.get_doc({
                    "doctype": "DocType Link",
                    "parent": "Asset",  # Linking to Asset DocType
                    "parentfield": "links",  # Parentfield for links in the Asset DocType
                    "parenttype": "DocType",  # The parent type
                    "link_doctype": link["link_doctype"],
                    "link_fieldname": link["link_fieldname"],
                    "group": "IT Resources"
                })
                
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            frappe.msgprint(f"Added missing Document Link: {link['link_doctype']} to {link.get('parent_doctype', 'Asset')}")

