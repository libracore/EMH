// Copyright (c) 2022, libracore and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Offene Positionen"] = {
    "filters": [
        {
            "fieldname":"from_date",
            "label": __("From Date"),
            "fieldtype": "Date"
        },
        {
            "fieldname":"to_date",
            "label": __("To Date"),
            "fieldtype": "Date"
        },
        {
            "fieldname":"customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer"
        },
        {
            "fieldname":"project",
            "label": __("Project"),
            "fieldtype": "Link",
            "options": "Project"
        }
    ],
    "initial_depth": 0
};

/* add event listener for double clicks to move up */
cur_page.container.addEventListener("dblclick", function(event) {
    // restrict to this report to prevent this event on other reports once loaded
    if (window.location.toString().includes("/Offene%20Positionen") ) {
        var row = event.delegatedTarget.getAttribute("data-row-index");
        var column = event.delegatedTarget.getAttribute("data-col-index");
        if (column.toString() === "10") {                 // 10 is the column index of "Create invoice"
            console.log("Create invoice for " + frappe.query_report.data[row]['customer']);
            frappe.call({
                'method': "emh.emh.report.offene_positionen.offene_positionen.create_invoice",
                'args': {
                    'from_date': frappe.query_report.filters[0].value,
                    'to_date': frappe.query_report.filters[1].value,
                    'customer': frappe.query_report.data[row]['customer'],
                    'project': (frappe.query_report.filters[3].value || "%")
                },
                'callback': function(response) {
                    frappe.show_alert( __("Created") + ": <a href='/desk#Form/Sales Invoice/" + response.message
                        + "'>" + response.message + "</a>");
                    frappe.query_report.refresh();
                }
            });
        }
    }
});
