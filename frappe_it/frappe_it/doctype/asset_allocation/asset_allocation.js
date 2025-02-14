// Copyright (c) 2025, buff0k and contributors
// For license information, please see license.txt

frappe.ui.form.on('Asset Allocation', {
    employee_or_asset: function (frm) {
        const selected_doctype = frm.doc.employee_or_asset;

        if (!selected_doctype) {
            frm.set_value('branch_or_location', null);
            frm.set_value('site', null);
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
        frm.set_value('site', null);
        frm.set_value('employee_asset_name', null);

        // Trigger updates for site and employee_asset_name
        frm.trigger('update_site_and_name');
    },

    allocated_to: function (frm) {
        frm.trigger('update_site_and_name');
    },

    update_site_and_name: function (frm) {
        const selected_doctype = frm.doc.employee_or_asset;
        const docname = frm.doc.allocated_to;

        if (!selected_doctype || !docname) {
            frm.set_value('site', null);
            frm.set_value('employee_asset_name', null);
            return;
        }

        // Call the server script to fetch both the site and the employee_asset_name
        frappe.call({
            method: 'frappe_it.frappe_it.doctype.asset_allocation.asset_allocation.get_employee_or_asset_details',
            args: {
                doctype: selected_doctype,
                docname: docname,
            },
            callback: function (response) {
                if (response.message) {
                    const { site, employee_asset_name } = response.message;
                    frm.set_value('site', site || null);
                    frm.set_value('employee_asset_name', employee_asset_name || null);
                } else {
                    frm.set_value('site', null);
                    frm.set_value('employee_asset_name', null);
                }
            }
        });
    }
});

frappe.ui.form.on('Asset Allocation Table', {
    asset: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.asset) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Asset',
                    name: row.asset
                },
                callback: function (r) {
                    if (r.message) {
                        let item_name = r.message.item_name || '';
                        let asset_name = r.message.asset_name || '';
                        frappe.model.set_value(cdt, cdn, 'asset_name', `${item_name} - ${asset_name}`);
                    }
                }
            });
        } else {
            frappe.model.set_value(cdt, cdn, 'asset_name', '');
        }
    }
});
