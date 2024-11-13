// Copyright (c) 2024, buff0k and contributors
// For license information, please see license.txt

frappe.ui.form.on("NVR Details", {
    refresh: function(frm) {
        if (!frm.is_new()) {
            // Fetch all IP Camera Details directly on the client side
            frappe.db.get_list('IP Camera Details', {
                filters: { 'linked_to_nvr': frm.doc.name },
                fields: ['name as camera', 'ip_address', 'location', 'camera_link', 'username', 'password'],
                limit: null // Set limit to null to fetch all records
            }).then((cameras) => {
                frm.clear_table("linked_cameras");
                cameras.forEach((camera_data) => {
                    let row = frm.add_child("linked_cameras");
                    row.camera = camera_data.camera;
                    row.ip_address = camera_data.ip_address;
                    row.location = camera_data.location;
                    row.camera_link = camera_data.camera_link;
                    row.username = camera_data.username;
                    row.password = camera_data.password;
                });
                frm.refresh_field("linked_cameras");
            });
        }
    },

    ip_address: function(frm) {
        // Validate only when the field loses focus
        frm.fields_dict.ip_address.$input.on("blur", function() {
            // Regular expression to validate any IPv4 address
            const ipv4Regex = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;

            const ipAddress = frm.doc.ip_address;

            if (ipAddress) {
                // Validate the IP address
                if (ipv4Regex.test(ipAddress)) {
                    // If valid, set the device_url
                    frm.set_value('device_url', `http://${ipAddress}`);
                } else {
                    // If invalid, clear the device_url and show an error message
                    frm.set_value('device_url', '');
                    frappe.msgprint(__('Please enter a valid IPv4 address.'));
                }
            }
        });
    }
});
