from __future__ import unicode_literals
import frappe
from frappe import _

def execute():
    # Initialize flags safely
    if not hasattr(frappe.local, 'flags'):
        frappe.local.flags = {}
    
    # Store original flags
    original_flags = frappe.local.flags.copy()
    
    try:
        # Set migration flags
        frappe.local.flags.update({
            'in_migrate': True,
            'ignore_links': True,
            'ignore_validate': True,
            'in_safe_exec': True
        })
        
        # Process all documents
        allocations = frappe.get_all("Simcard Allocations", 
                                  fields=["name", "employee", "branch", "employee_name"])
        
        for alloc in allocations:
            try:
                if alloc.employee:  # Employee case
                    frappe.db.set_value(
                        "Simcard Allocations",
                        alloc.name,
                        {
                            "employee_or_site": "Employee",
                            "branch_or_location": "Branch",
                            "allocated_to": alloc.employee,
                            "site": alloc.branch
                        },
                        update_modified=False
                    )
                else:  # Location case
                    frappe.db.set_value(
                        "Simcard Allocations",
                        alloc.name,
                        {
                            "employee_or_site": "Location",
                            "branch_or_location": "Location",
                            "allocated_to": alloc.branch,
                            "site": alloc.branch,
                            "employee_name": alloc.branch
                        },
                        update_modified=False
                    )
            except Exception as e:
                frappe.log_error(
                    title=_("Migration Error for Simcard Allocation"),
                    message=f"Failed to migrate {alloc.name}: {str(e)}\nData: {alloc}"
                )
                continue
                
    finally:
        # Restore original flags
        frappe.local.flags = original_flags