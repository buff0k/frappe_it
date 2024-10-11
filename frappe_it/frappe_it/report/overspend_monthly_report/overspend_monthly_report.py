# Copyright (c) 2024, buff0k and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    if not filters.get("month"):
        frappe.throw("Please select a month to run the report.")

    columns = [
        {"label": "Monthly Bill", "fieldname": "name", "fieldtype": "Link", "options": "Monthly Bill", "width": 120},
        {"label": "SIM Card No", "fieldname": "sim_card_no", "fieldtype": "Link", "options": "Simcard Allocations", "width": 120},
        {"label": "Telephone Number", "fieldname": "tel_no", "fieldtype": "Data", "width": 120},
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Data", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 120},
        {"label": "Overspend Amount", "fieldname": "overspend_amount", "fieldtype": "Currency", "width": 120}
    ]

    conditions = "where b.overspend = 1"

    if filters.get("month"):
        conditions += " and MONTH(b.creation) = MONTH(%(month)s) and YEAR(b.creation) = YEAR(%(month)s)"

    data = frappe.db.sql(f"""
        select 
            b.name, 
            b.sim_card_no, 
            s.tel_no,  -- Fetching tel_no from Simcard Allocations
            b.employee, 
            e.employee_name, 
            b.overspend_amount
        from `tabMonthly Bill` b
        left join `tabEmployee` e on b.employee = e.name
        left join `tabSimcard Allocations` s on b.sim_card_no = s.name  -- Join with Simcard Allocations
        {conditions}
    """, filters, as_dict=True)

    return columns, data
