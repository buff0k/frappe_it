# Copyright (c) 2025, BuFf0k and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MonthlyBill(Document):
    def before_save(self):
        # Calculate subtotal
        self.calculated_subtotal = (
            self.subscription +
            self.subscription_discount +
            self.calls_national +
            self.entertainment_services +
            self.direct_provisioning +
            self.calls_international +
            self.calls_roaming +
            self.calls_discount +
            self.calls_data +
            self.calls_data_discount +
            self.calls_messaging +
            self.calls_messaging_discount +
            self.bundles_voice +
            self.bundles_messaging +
            self.bundles_data +
            self.bundles_adhoc +
            self.clip +
            self.blackberry +
            self.itemised_billing +
            self.vodamanage +
            self.look_4_services +
            self.insurance +
            self.equipment +
            self.connection_fee +
            self.connection_fee_discount +
            self.admin_fee +
            self.other
        )

        # Calculate VAT (15% of subtotal)
        self.calculated_vat = self.calculated_subtotal * 0.15

        # Calculate total (subtotal + vat)
        self.calculated_total = self.calculated_subtotal + self.calculated_vat

        # Calculate overspend amount
        self.overspend_amount = self.calculated_subtotal - self.subscription - self.equipment

        # Set overspend flag
        self.overspend = 1 if self.overspend_amount > 0 else 0
