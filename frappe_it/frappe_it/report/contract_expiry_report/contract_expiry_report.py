# Copyright (c) 2024, buff0k and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate, add_months

def execute(filters=None):
    if not filters:
        filters = {}

    # Prepare the columns for the report
    columns = [
        {"label": "SIM Number", "fieldname": "sim_no", "fieldtype": "Link", "options": "Simcard Allocations", "width": 205},
        {"label": "Telephone Number", "fieldname": "tel_no", "fieldtype": "Phone", "width": 145},
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 120},
        {"label": "Notes", "fieldname": "notes", "fieldtype": "Small Text", "width": 200},
        {"label": "Start Date", "fieldname": "end_date", "fieldtype": "Date", "width": 120},
        {"label": "End Date", "fieldname": "end_date", "fieldtype": "Date", "width": 120}
    ]

    # Calculate today's date and the date three months from now
    today = getdate()
    three_months_later = add_months(today, 3)

    # Query to fetch Simcard Allocations that are expired or about to expire in the next three months
    conditions = "where end_date <= %(three_months_later)s"

    data = frappe.db.sql(f"""
        select 
            s.sim_no, 
            s.tel_no, 
            s.employee, 
            e.employee_name, 
            s.notes,
            s.start_date,
            s.end_date
        from `tabSimcard Allocations` s
        left join `tabEmployee` e on s.employee = e.name 
        {conditions}
    """, {"three_months_later": three_months_later}, as_dict=True)

    return columns, data
