# Copyright (c) 2025, buff0k and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class AssetRequest(Document):
    def before_submit(self):
        if not self.attach_signed:
            frappe.throw(_("Please attach a signed copy before submitting."))

@frappe.whitelist()
def get_employee_or_asset_details(doctype, docname):
    if not doctype or not docname:
        frappe.throw(_("Invalid parameters provided."))

    try:
        if doctype == "Employee":
            # Fetch linked Branch and Employee Name
            doc = frappe.get_doc("Employee", docname)
            return {
                "allocate_to_site": doc.branch if doc.branch else _("Branch not found"),
                "employee_asset_name": doc.employee_name if doc.employee_name else _("Name not found"),
                "employee_asset_designation": doc.designation if doc.designation else _("Designation not found"),
            }
        elif doctype == "Asset":
            # Fetch linked Location and Item Name
            doc = frappe.get_doc("Asset", docname)
            return {
                "allocate_to_site": doc.location if doc.location else _("Location not found"),
                "employee_asset_name": doc.item_name if doc.item_name else _("Name not found"),
            }
        elif doctype == "Location":
            # Fetch linked Location and Item Name
            doc = frappe.get_doc("Location", docname)
            return {
                "allocate_to_site": doc.name if doc.name else _("Location not found"),
                "employee_asset_name": doc.name if doc.name else _("Location not found"),
            }
        else:
            frappe.throw(_("Invalid Doctype: {0}").format(doctype))
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error in get_employee_or_asset_details"))
        frappe.throw(_("An error occurred while fetching the document data: {0}").format(str(e)))