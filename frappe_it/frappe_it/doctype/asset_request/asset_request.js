// Copyright (c) 2025, buff0k and contributors
// For license information, please see license.txt

frappe.ui.form.on("Asset Request", {
    requested_by: function (frm) {
        if (frm.doc.requested_by) {
          frappe.db.get_doc('Employee', frm.doc.requested_by)
            .then(employee => {
              frm.set_value('requested_by_site', employee.branch || '');
              frm.set_value('requested_by_designation', employee.designation || '');
            })
            .catch(err => {
              frappe.msgprint(__('Failed to fetch employee details'));
              console.error(err);
            });
        }
    },
    
    employee_or_asset: function (frm) {
        const selected_doctype = frm.doc.employee_or_asset;

        if (!selected_doctype) {
            frm.set_value('branch_or_location', null);
            frm.set_value('allocate_to_site', null);
            frm.set_value('employee_asset_name', null);
            return;
        }

        // Set branch_or_location based on the selected doctype
        if (selected_doctype === 'Employee') {
            frm.set_value('branch_or_location', 'Branch');
        } else if (selected_doctype === 'Asset') {
            frm.set_value('branch_or_location', 'Location');
        } else if (selected_doctype === 'Location') {
            frm.set_value('branch_or_location', 'Location');
        }

        // Clear dependent fields until new data is fetched
        frm.set_value('allocate_to_site', null);
        frm.set_value('employee_asset_name', null);

        // Trigger updates for site and employee_asset_name
        frm.trigger('update_site_and_name');
    },

    allocate_to: function (frm) {
        frm.trigger('update_site_and_name');
    },

    update_site_and_name: function (frm) {
        const selected_doctype = frm.doc.employee_or_asset;
        const docname = frm.doc.allocate_to;

        if (!selected_doctype || !docname) {
            frm.set_value('allocate_to_site', null);
            frm.set_value('employee_asset_name', null);
            return;
        }

        // Call the server script to fetch both the site and the employee_asset_name
        frappe.call({
            method: 'frappe_it.frappe_it.doctype.asset_request.asset_request.get_employee_or_asset_details',
            args: {
                doctype: selected_doctype,
                docname: docname,
            },
            callback: function (response) {
                if (response.message) {
                    const { allocate_to_site, employee_asset_name } = response.message;
                    frm.set_value('allocate_to_site', allocate_to_site || null);
                    frm.set_value('employee_asset_name', employee_asset_name || null);
                } else {
                    frm.set_value('allocate_to_site', null);
                    frm.set_value('employee_asset_name', null);
                }
            }
        });
    }
});