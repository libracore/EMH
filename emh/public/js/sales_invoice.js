// Copyright (c) 2021-2023, libracore AG and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Invoice', {
    before_save: function(frm) {
        calculate_comission(frm);
        }
});

function calculate_comission(frm) {
    frappe.call({
        "method": "emh.emh.utils.calculate_comission",
        "args": {
            "sales_invoice": frm.doc.name
        },
        "callback": function(response) {
            cur_frm.set_value("commission", response.message);
        }
    });
}
