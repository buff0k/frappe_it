// Copyright (c) 2026, BuFf0k
// For license information, please see license.txt

frappe.ui.form.on("NVR Details", {
    refresh: function(frm) {
        render_linked_cameras_html(frm);
    },

    after_save: function(frm) {
        render_linked_cameras_html(frm);
    },

    ip_address: function(frm) {
        // Validate only when the field loses focus
        frm.fields_dict.ip_address.$input.on("blur", function() {
            const ipv4Regex =
                /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;

            const ipAddress = frm.doc.ip_address;

            if (ipAddress) {
                if (ipv4Regex.test(ipAddress)) {
                    frm.set_value('device_url', `http://${ipAddress}`);
                } else {
                    frm.set_value('device_url', '');
                    frappe.msgprint(__('Please enter a valid IPv4 address.'));
                }
            }
        });
    }
});


function render_linked_cameras_html(frm) {
    if (!frm.fields_dict.linked_cameras_html) return;

    frappe.require('/assets/frappe_it/css/it_ui.css');

    if (frm.is_new() || frm.doc.__islocal) {
        frm.fields_dict.linked_cameras_html.$wrapper.html(`
            <div class="it-linked-panel">
              <div class="it-linked-panel__empty">
                Linked cameras will appear here once the record is saved.
              </div>
            </div>
        `);
        return;
    }

    frappe.call({
        method: 'frappe_it.frappe_it.doctype.nvr_details.nvr_details.get_linked_cameras_html',
        args: { nvr_details_name: frm.doc.name },
        callback: function(r) {
            frm.fields_dict.linked_cameras_html.$wrapper.html(r.message || '');
        }
    });
}
