# Copyright (c) 2024, buff0k and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SimcardAllocations(Document):
	pass

@frappe.whitelist()
def get_available_simcards(doctype, txt, searchfield, start, page_len, filters):
    frappe.logger().info("Custom method called with txt: {0}".format(txt))  # Log the call
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
    frappe.logger().info("SQL Results: {0}".format(simcards))  # Log the result
    return simcards
