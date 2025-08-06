# Copyright (c) 2025, buff0k and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class AssetReturn(Document):
    def before_submit(self):
        if not self.attach_signed:
            frappe.throw(_("Please attach a signed copy before submitting."))
