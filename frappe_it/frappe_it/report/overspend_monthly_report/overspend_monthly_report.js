// Copyright (c) 2025, BuFf0k and contributors
// For license information, please see license.txt

frappe.query_reports["Overspend Monthly Report"] = {
	"filters": [
        {
            "fieldname": "month",
            "label": "Month",
            "fieldtype": "Date",
            "reqd": 1,
        }
    ],
    onload: function(report) {
        // This function can be used to handle other onload actions for the report
    },
    // If you need any custom logic on filter changes, you can use this method
    filter: function() {
        // Custom logic for when the filter changes can go here
    }
};
