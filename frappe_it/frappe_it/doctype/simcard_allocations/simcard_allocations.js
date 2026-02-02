// Copyright (c) 2026, BuFf0k
// For license information, please see license.txt

frappe.ui.form.on('Simcard Allocations', {
    onload: function (frm) {
        frm.trigger('set_sim_no_query');
        render_linked_bills_html(frm);
    },

    refresh: function(frm) {
        render_linked_bills_html(frm);
    },

    after_save: function(frm) {
        render_linked_bills_html(frm);
    },

    msisdn: function (frm) {
        render_linked_bills_html(frm);
    },

    employee: function (frm) {
        if (frm.doc.employee) {
            frappe.db.get_doc('Employee', frm.doc.employee)
                .then(employee_doc => {
                    if (employee_doc) {
                        frm.set_value('employee_name', employee_doc.employee_name);
                        frm.set_value('branch', employee_doc.branch);
                    }
                })
                .catch(error => {
                    console.error('Error fetching employee:', error);
                });
        } else {
            frm.set_value('employee_name', '');
            frm.set_value('branch', '');
        }
    },

    set_sim_no_query: function (frm) {
        frm.set_query('sim_no', function () {
            return {
                query: 'frappe_it.frappe_it.doctype.simcard_allocations.simcard_allocations.get_available_simcards',
                filters: {}
            };
        });
    },

    employee_or_site: function (frm) {
        const selected_doctype = frm.doc.employee_or_site;

        if (!selected_doctype) {
            frm.set_value('branch_or_location', null);
            frm.set_value('site', null);
            frm.set_value('employee_name', null);
            frm.set_value('allocated_to', null);
            return;
        }

        if (selected_doctype === 'Employee') {
            frm.set_value('branch_or_location', 'Branch');
        } else if (selected_doctype === 'Location') {
            frm.set_value('branch_or_location', 'Location');
        }

        frm.set_value('site', null);
        frm.set_value('employee_name', null);
        frm.set_value('allocated_to', null);

        frm.trigger('update_site_and_name');
    },

    allocated_to: function (frm) {
        frm.trigger('update_site_and_name');
    },

    update_site_and_name: function (frm) {
        const selected_doctype = frm.doc.employee_or_site;
        const docname = frm.doc.allocated_to;

        if (!selected_doctype || !docname) {
            frm.set_value('site', null);
            frm.set_value('employee_name', null);
            return;
        }

        frappe.call({
            method: 'frappe_it.frappe_it.doctype.simcard_allocations.simcard_allocations.get_employee_or_site_details',
            args: {
                doctype: selected_doctype,
                docname: docname,
            },
            callback: function (response) {
                if (response.message) {
                    const { site, employee_name } = response.message;
                    frm.set_value('site', site || null);
                    frm.set_value('employee_name', employee_name || null);
                } else {
                    frm.set_value('site', null);
                    frm.set_value('employee_name', null);
                }
            }
        });
    }
});


function render_linked_bills_html(frm) {
    if (!frm.fields_dict.linked_bills_html) return;

    frappe.require('/assets/frappe_it/css/it_ui.css');

    if (frm.is_new() || frm.doc.__islocal) {
        frm.fields_dict.linked_bills_html.$wrapper.html(`
            <div class="it-linked-panel">
              <div class="it-linked-panel__empty">
                Linked bills will appear here once the record is saved.
              </div>
            </div>
        `);
        return;
    }

    frappe.call({
        method: 'frappe_it.frappe_it.doctype.simcard_allocations.simcard_allocations.get_linked_bills_html',
        args: { simcard_alloc_name: frm.doc.name },
        callback: function(r) {
            frm.fields_dict.linked_bills_html.$wrapper.html(r.message || '');
        }
    });
}
