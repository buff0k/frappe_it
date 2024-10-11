// Copyright (c) 2024, buff0k and contributors
// For license information, please see license.txt

frappe.ui.form.on('Monthly Bill', {
    validate: function(frm) {
        // Sum up all the fields for the calculated_subtotal
        let subtotal = (
            frm.doc.subscription +
            frm.doc.subscription_discount +
            frm.doc.calls_national +
            frm.doc.entertainment_services +
            frm.doc.direct_provisioning +
            frm.doc.calls_international +
            frm.doc.calls_roaming +
            frm.doc.calls_discount +
            frm.doc.calls_data +
            frm.doc.calls_data_discount +
            frm.doc.calls_messaging +
            frm.doc.calls_messaging_discount +
            frm.doc.bundles_voice +
            frm.doc.bundles_messaging +
            frm.doc.bundles_data +
            frm.doc.bundles_adhoc +
            frm.doc.clip +
            frm.doc.blackberry +
            frm.doc.itemised_billing +
            frm.doc.vodamanage +
            frm.doc.look_4_services +
            frm.doc.insurance +
            frm.doc.equipment +
            frm.doc.connection_fee +
            frm.doc.connection_fee_discount +
            frm.doc.admin_fee +
            frm.doc.other
        );

        // Set calculated_subtotal
        frm.set_value('calculated_subtotal', subtotal);

        // Calculate VAT (15% of subtotal)
        let vat = subtotal * 0.15;
        frm.set_value('calculated_vat', vat);

        // Calculate total (subtotal + vat)
        let total = subtotal + vat;
        frm.set_value('calculated_total', total);

        // Calculate overspend amount
        let overspend = subtotal - frm.doc.subscription - frm.doc.equipment;
        frm.set_value('overspend_amount', overspend);

        // Set overspend flag if overspend_amount is greater than 0
        if (overspend > 0) {
            frm.set_value('overspend', 1);
        } else {
            frm.set_value('overspend', 0);
        }
    }
});
