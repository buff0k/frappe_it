# Copyright (c) 2025, BuFf0k and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class SimcardAllocations(Document):
    def on_update(self):
        self.update_asset_allocations()

    def update_asset_allocations(self):
        if not self.sim_no:
            return  # Cannot assign without a SIM

        # Validate all required dynamic fields
        if not self.employee_or_site or not self.allocated_to:
            frappe.throw("Allocated To and its type must be set.")
        if not self.branch_or_location or not self.site:
            frappe.throw("Site and its type must be set.")

        asset = self.sim_no
        previous_doc = self.get_doc_before_save()
        old_doctype = previous_doc.employee_or_site if previous_doc else None
        old_allocated_to = previous_doc.allocated_to if previous_doc else None

        # Remove asset from old allocation if it changed
        if previous_doc and (old_doctype != self.employee_or_site or old_allocated_to != self.allocated_to):
            self.remove_asset_from_allocation(old_doctype, old_allocated_to, asset)

        # Add to new allocation
        self.add_asset_to_allocation(asset)

    def remove_asset_from_allocation(self, doctype, allocated_to, asset):
        if not doctype or not allocated_to:
            return

        allocations = frappe.get_all("Asset Allocation",
            filters={
                "employee_or_asset": doctype,
                "allocated_to": allocated_to
            },
            fields=["name"]
        )
        for alloc in allocations:
            doc = frappe.get_doc("Asset Allocation", alloc.name)
            original = len(doc.list_of_allocated_assets)
            doc.list_of_allocated_assets = [
                row for row in doc.list_of_allocated_assets if row.asset != asset
            ]
            if len(doc.list_of_allocated_assets) != original:
                doc.save(ignore_permissions=True)

    def add_asset_to_allocation(self, asset):
        try:
            if not self.employee_or_site or not self.allocated_to:
                frappe.throw("Allocated To must be set.")
            if not self.branch_or_location or not self.site:
                frappe.throw("Site must be set.")

            # Ensure dynamic links are valid
            if not frappe.db.exists(self.employee_or_site, self.allocated_to):
                frappe.throw(f"{self.employee_or_site} '{self.allocated_to}' does not exist.")
            if not frappe.db.exists(self.branch_or_location, self.site):
                frappe.throw(f"{self.branch_or_location} '{self.site}' does not exist.")

            # Check if allocation already exists
            existing = frappe.get_all("Asset Allocation", {
                "employee_or_asset": self.employee_or_site,
                "allocated_to": self.allocated_to
            }, ["name"])

            if existing:
                doc = frappe.get_doc("Asset Allocation", existing[0].name)
            else:
                doc = frappe.new_doc("Asset Allocation")
                doc.employee_or_asset = self.employee_or_site
                doc.allocated_to = self.allocated_to
                doc.branch_or_location = self.branch_or_location
                doc.site = self.site

                # Friendly name
                if self.employee_or_site == "Employee":
                    doc.employee_asset_name = frappe.db.get_value("Employee", self.allocated_to, "employee_name")
                else:
                    doc.employee_asset_name = self.allocated_to

                doc.insert(ignore_permissions=True)

            # Add SIM if not already allocated
            if not any(row.asset == asset for row in doc.list_of_allocated_assets):
                asset_name = frappe.db.get_value("Asset", asset, "asset_name")
                doc.append("list_of_allocated_assets", {
                    "asset": asset,
                    "asset_name": asset_name,
                    "check_out_date": nowdate(),
                    "notes": f"Linked via Simcard Allocation {self.name}"
                })
                doc.save(ignore_permissions=True)

        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Simcard Allocations Error")
            raise

@frappe.whitelist()
def get_available_simcards(doctype, txt, searchfield, start, page_len, filters):
    frappe.logger().info("Custom method called with txt: {0}".format(txt))
    simcards = frappe.db.sql("""
        SELECT
            name, asset_name
        FROM
            `tabAsset`
        WHERE
            asset_category = 'Cellphone Simcards'
            AND name NOT IN (
                SELECT sim_no FROM `tabSimcard Allocations` WHERE sim_no IS NOT NULL
            )
            AND ({key} LIKE %(txt)s OR asset_name LIKE %(txt)s)
        LIMIT %(start)s, %(page_len)s
    """.format(key=searchfield), {
        'txt': f"%{txt}%",
        'start': start,
        'page_len': page_len
    })
    frappe.logger().info("SQL Results: {0}".format(simcards))
    return simcards

@frappe.whitelist()
def get_employee_or_site_details(doctype, docname):
    if not doctype or not docname:
        frappe.throw(_("Invalid parameters provided."))

    try:
        if doctype == "Employee":
            # Fetch linked Branch and Employee Name
            doc = frappe.get_doc("Employee", docname)
            return {
                "site": doc.branch if doc.branch else _("Branch not found"),
                "employee_name": doc.employee_name if doc.employee_name else _("Name not found"),
            }
        elif doctype == "Location":
            # Fetch linked Location and Item Name
            doc = frappe.get_doc("Location", docname)
            return {
                "site": doc.name if doc.name else _("Location not found"),
                "employee_name": doc.name if doc.name else _("Location not found"),
            }
        else:
            frappe.throw(_("Invalid Doctype: {0}").format(doctype))
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error in get_employee_or_site_details"))
        frappe.throw(_("An error occurred while fetching the document data: {0}").format(str(e)))