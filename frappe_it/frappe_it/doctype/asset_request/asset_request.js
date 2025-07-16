// Copyright (c) 2025, buff0k and contributors
// For license information, please see license.txt

frappe.ui.form.on('Asset Request', {
    onload: function (frm) {
        // Default requested_by to logged-in user's Employee record on create
        if (frm.is_new()) {
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Employee',
                    filters: { user_id: frappe.session.user },
                    fields: ['name']
                },
                callback: function (r) {
                    if (r.message && r.message.length) {
                        frm.set_value('requested_by', r.message[0].name);
                    }
                }
            });
        }
    },

    company: function(frm) {
        if (frm.doc.company) {
            frappe.db.get_doc('Company', frm.doc.company).then(company => {
                if (company.default_letter_head) {
                    frm.set_value('letter_head', company.default_letter_head);
                } else {
                    frm.set_value('letter_head', '');
                    frappe.msgprint('This company has no default Letter Head set.');
                }
            });
        }
    },

    requested_by: function (frm) {
        if (frm.doc.requested_by) {
            frappe.db.get_doc('Employee', frm.doc.requested_by)
                .then(employee => {
                    frm.set_value('requested_by_site', employee.branch || '');
                    frm.set_value('requested_by_designation', employee.designation || '');
                    frm.set_value('requested_by_names', employee.employee_name || '');
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

        if (selected_doctype === 'Employee') {
            frm.set_value('branch_or_location', 'Branch');
        } else if (['Asset', 'Location'].includes(selected_doctype)) {
            frm.set_value('branch_or_location', 'Location');
        }

        frm.set_value('allocate_to_site', null);
        frm.set_value('employee_asset_name', null);

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
            frm.set_value('employee_asset_designation', null);
            return;
        }

        frappe.call({
            method: 'frappe_it.frappe_it.doctype.asset_request.asset_request.get_employee_or_asset_details',
            args: {
                doctype: selected_doctype,
                docname: docname,
            },
            callback: function (response) {
                if (response.message) {
                    const { allocate_to_site, employee_asset_name, employee_asset_designation } = response.message;
                    frm.set_value('allocate_to_site', allocate_to_site || null);
                    frm.set_value('employee_asset_name', employee_asset_name || null);
                    frm.set_value('employee_asset_designation', employee_asset_designation || null);
                } else {
                    frm.set_value('allocate_to_site', null);
                    frm.set_value('employee_asset_name', null);
                    frm.set_value('employee_asset_designation', null);
                }
            }
        });
    }
});

frappe.ui.form.on('Asset Request List', {
    asset_type: async function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        const designation = frm.doc.employee_asset_designation;

        // Set doctype_link based on asset_type
        if (['Cellular Telephone', 'Cellphone Simcards'].includes(row.asset_type)) {
            row.doctype_link = "Cellphone Plan by Designation";
        } else if (row.asset_type === "Laptop Computer") {
            row.doctype_link = "Laptop Specification";
        } else {
            row.doctype_link = null;
            frm.refresh_field("asset_request_list");
            return;
        }

        frappe.model.set_value(cdt, cdn, "doctype_link", row.doctype_link);

        // If designation not set in parent, exit early
        if (!designation) {
            frm.refresh_field("asset_request_list");
            return;
        }

        // Fetch documents of the target type
        let results = await frappe.db.get_list(row.doctype_link, {
            fields: ['name'],
            limit: 10
        });

        for (let doc of results) {
            const full_doc = await frappe.db.get_doc(row.doctype_link, doc.name);

            // Check if the designation matches
            if (
                full_doc.designations &&
                full_doc.designations.some(d => d.designation === designation)
            ) {
                await frappe.model.set_value(cdt, cdn, "asset_spec", full_doc.name);

                // Manually trigger asset_spec logic to populate asset_spec_details
                frappe.ui.form.on("Asset Request List").asset_spec(frm, cdt, cdn);
                break;
            }
        }

        frm.refresh_field("asset_request_list");
    },

    asset_spec: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        if (!row.doctype_link || !row.asset_spec) return;

        frappe.db.get_doc(row.doctype_link, row.asset_spec).then(spec => {
            if (row.doctype_link === "Laptop Specification") {
                let detail = [
                    spec.cpu || "",
                    spec.ram || "",
                    spec.storage || "",
                    spec.gpu || ""
                ].filter(Boolean).join(', ');
                frappe.model.set_value(cdt, cdn, "asset_spec_details", detail);
            }

            else if (row.doctype_link === "Cellphone Plan by Designation") {
                if (!spec.cellphone_plan) return;

                frappe.db.get_doc("Cellphone Plan", spec.cellphone_plan).then(plan => {
                    let detail = [
                        plan.bundled_minutes || "",
                        plan.bundled_data || ""
                    ].filter(Boolean).join(', ');
                    frappe.model.set_value(cdt, cdn, "asset_spec_details", detail);
                });
            }
        });
    }
});
