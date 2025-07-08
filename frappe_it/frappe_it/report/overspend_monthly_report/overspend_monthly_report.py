# Copyright (c) 2024, buff0k and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    if not filters.get("month"):
        frappe.throw("Please select a month to run the report.")

    columns = [
        {"label": "Monthly Bill", "fieldname": "name", "fieldtype": "Link", "options": "Monthly Bill", "width": 100},
        {"label": "SIM Card No", "fieldname": "sim_card_no", "fieldtype": "Link", "options": "Simcard Allocations", "width": 205},
        {"label": "Telephone Number", "fieldname": "tel_no", "fieldtype": "Data", "width": 145},
        {"label": "Allocated To", "fieldname": "allocated_to", "fieldtype": "Link", "options": "Employee", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 150},
        {"label": "Notes", "fieldname": "notes", "fieldtype": "Small Text", "width": 250},
        {"label": "Overspend Amount", "fieldname": "overspend_amount", "fieldtype": "Data", "width": 100}
    ]

    conditions = "where b.overspend = 1"

    if filters.get("month"):
        conditions += " and MONTH(b.creation) = MONTH(%(month)s) and YEAR(b.creation) = YEAR(%(month)s)"

    data = frappe.db.sql(f"""
        select 
            b.name, 
            b.sim_card_no, 
            s.tel_no,  -- Fetching tel_no from Simcard Allocations
            s.allocated_to,  -- Fetching allocated_to from Simcard Allocations
            s.notes, -- Fetching notes from Simcard Allocations
            e.employee_name, 
            b.overspend_amount
        from `tabMonthly Bill` b
        left join `tabSimcard Allocations` s on b.sim_card_no = s.name  -- Join with Simcard Allocations
        left join `tabEmployee` e on s.allocated_to = e.name  -- Use employee from Simcard Allocations to fetch employee_name
        {conditions}
    """, filters, as_dict=True)

    return columns, data
