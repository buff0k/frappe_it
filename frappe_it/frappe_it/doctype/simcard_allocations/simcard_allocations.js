// Copyright (c) 2024, buff0k and contributors
// For license information, please see license.txt

frappe.ui.form.on('Simcard Allocations', {
    onload: function (frm) {
        frm.trigger('populate_child_table');
    },
    sim_no: function (frm) {
        frm.trigger('populate_child_table');
    },
    employee: function (frm) {
        if (frm.doc.employee) {
            // Fetch employee details from the Employee DocType
            frappe.db.get_doc('Employee', frm.doc.employee)
                .then(employee_doc => {
                    if (employee_doc) {
                        // Update the fields with the fetched data
                        frm.set_value('employee_name', employee_doc.employee_name);
                        frm.set_value('branch', employee_doc.branch);
                    }
                })
                .catch(error => {
                    console.error('Error fetching employee:', error); // Handle any error fetching the employee
                });
        } else {
            // Clear the fields if employee is not selected
            frm.set_value('employee_name', '');
            frm.set_value('branch', '');
        }
    },
    populate_child_table: function (frm) {
        if (frm.doc.sim_no) {
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Monthly Bill',
                    fields: ['name', 'total', 'overspend_amount'],
                    filters: {
                        sim_card_no: frm.doc.sim_no
                    },
                    limit_page_length: 0 // Fetch all matching records
                },
                callback: function (response) {
                    if (response && response.message) {
                        const bills = response.message;

                        // Clear existing rows in the child table
                        frm.clear_table('simcard_allocations');

                        // Populate the child table with fetched data
                        bills.forEach(bill => {
                            let row = frm.add_child('simcard_allocations');
                            row.monthly_bill = bill.name;
                            row.total = bill.total;
                            row.overspend_amount = bill.overspend_amount;
                        });

                        // Refresh the table to display the new data
                        frm.refresh_field('simcard_allocations');
                    } else {
                        // Clear the child table if no matching records are found
                        frm.clear_table('simcard_allocations');
                        frm.refresh_field('simcard_allocations');
                    }
                }
            });
        } else {
            // Clear the table if sim_no is empty
            frm.clear_table('simcard_allocations');
            frm.refresh_field('simcard_allocations');
        }
    }
});
