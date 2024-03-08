frappe.ui.form.on('Sales Invoice', {
    refresh(frm) {
		if (frm.doc.docstatus == 1) {
			// custom mail dialog (prevent duplicate icons on creation)
            if (document.getElementsByClassName("fa-envelope-o").length === 0) {
                cur_frm.page.add_action_icon(__("fa fa-envelope-o"), function() {
                    custom_mail_dialog(frm);
                });
                var target ="span[data-label='" + __("Email") + "']";
                $(target).parent().parent().remove();   // remove Menu > Email
            }
        }
    }
});

function custom_mail_dialog(frm) {
    frappe.call({
        'method': 'emh.emh.utils.get_email_recipient_and_message',
        'args': {
            'address': frm.doc.customer_address
        },
        'callback': function(response) {
            var recipient = response.message.recipient || cur_frm.doc.contact_email;
            var message = response.message.message
            new frappe.views.CommunicationComposer({
				doc: {
					doctype: cur_frm.doc.doctype,
					name: cur_frm.doc.name
				},
				subject: "Rechnung " + cur_frm.doc.name,
				//~ cc:  cc,
				//~ bcc: bcc,
				recipients: recipient,
				attach_document_print: true,
				message: message
			});
        }
    });
}
