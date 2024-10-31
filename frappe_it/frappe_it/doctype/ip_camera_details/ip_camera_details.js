// Copyright (c) 2024, buff0k and contributors
// For license information, please see license.txt

frappe.ui.form.on('IP Camera Details', {
    ip_address: function(frm) {
        // Validate only when the field loses focus
        frm.fields_dict.ip_address.$input.on("blur", function() {
            // Regular expression to validate any IPv4 address
            const ipv4Regex = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;

            const ipAddress = frm.doc.ip_address;

            if (ipAddress) {
                // Validate the IP address
                if (ipv4Regex.test(ipAddress)) {
                    // If valid, set the camera_link
                    frm.set_value('camera_link', `http://${ipAddress}`);
                } else {
                    // If invalid, clear the camera_link and show an error message
                    frm.set_value('camera_link', '');
                    frappe.msgprint(__('Please enter a valid IPv4 address.'));
                }
            }
        });
    }
});
