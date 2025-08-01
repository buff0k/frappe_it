// Copyright (c) 2025, buff0k and contributors
// For license information, please see license.txt

frappe.ui.form.on("Asset Return", {
    receiver: function (frm) {
        if (frm.doc.receiver) {
            frappe.db.get_doc('Employee', frm.doc.receiver)
                .then(employee => {
                    frm.set_value('receiver_branch', employee.branch || '');
                    frm.set_value('receiver_designation', employee.designation || '');
                    frm.set_value('receiver_name', employee.employee_name || '');
                })
                .catch(err => {
                    frappe.msgprint(__('Failed to fetch employee details'));
                    console.error(err);
                });
        }
    },

    employee: async function (frm) {
        if (!frm.doc.employee) return;

        try {
            // Set Employee Details
            const employee = await frappe.db.get_doc('Employee', frm.doc.employee);
            frm.set_value('branch', employee.branch || '');
            frm.set_value('designation', employee.designation || '');
            frm.set_value('employee_name', employee.employee_name || '');

            // Fetch all Asset Allocation documents with allocated_to matching this employee
            const allocations = await frappe.db.get_list('Asset Allocation', {
                fields: ['name', 'allocated_to'],
                filters: {
                    allocated_to: frm.doc.employee
                }
            });

            frm.clear_table('list_of_allocated_assets');

            for (let alloc of allocations) {
                const alloc_doc = await frappe.db.get_doc('Asset Allocation', alloc.name);
                for (let asset_row of alloc_doc.list_of_allocated_assets || []) {
                    let new_row = frm.add_child('list_of_allocated_assets');
                    new_row.asset = asset_row.asset;
                    new_row.asset_name = asset_row.asset_name;
                    new_row.check_in_date = frappe.datetime.get_today(); // or leave blank
                    new_row.condition_photo_out = asset_row.condition_photo;
                    new_row.notes = asset_row.notes;
                }
            }

            frm.refresh_field('list_of_allocated_assets');
        } catch (err) {
            frappe.msgprint(__('Failed to fetch employee or allocation details'));
            console.error(err);
        }
}
});

frappe.ui.form.on('Asset Return Table', {
    asset: function (frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        if (!row.asset) return;

        frappe.db.get_value('Asset', row.asset, 'asset_name')
            .then(r => {
                if (r.message && r.message.asset_name) {
                    frappe.model.set_value(cdt, cdn, 'asset_name', r.message.asset_name);
                }
            });
    }
});
