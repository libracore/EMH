# Copyright (c) 2021-2023, libracore and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe.utils import add_months, add_years, today, getdate

def calculate_comission(self, event):
	#get service item
	service_item = frappe.get_cached_value("emh settings", "emh settings", "service_item")
	
	#get commissioned amount
	commissioned_amount = 0
	
	for item in self.items:
		if item.item_code == service_item:
			commissioned_amount += item.net_amount
	
	#get commission rate
	commission_rate = self.commission_rate	
	#if there is a commissioned amount, calculate commission
	if commissioned_amount > 0:
		commission = commissioned_amount / 100 * commission_rate
	else:
		commission = 0
	
	self.commission = commission
		
	return

def autocreate_abo_invoice():
	#get all abos and current date
	abos = frappe.db.get_list("Abo", filters={"enabled": 1, "manually_invoice": 0})
	current_date = getdate(today())
	
	for abo in abos:
		#get abo doc
		abo_doc = frappe.get_doc("Abo", abo.name)
		
		#check next invoice date
		last_invoice = None
		if len(abo_doc.invoices) > 0:
			for invoice in abo_doc.invoices:
				if last_invoice:
					if invoice.date > last_invoice:
						last_invoice = invoice.date
				else:
					last_invoice = invoice.date
		
		if abo_doc.interval == "Monthly":
			if last_invoice:
				next_invoice = add_months(last_invoice, 1)
			else:
				next_invoice = abo_doc.start_date
		elif abo_doc.interval == "Yearly":
			if last_invoice:
				next_invoice = add_years(last_invoice, 1)
			else:
				next_invoice = abo_doc.start_date
		
		print(next_invoice)
			
		#check if next invoice date is overdue and create invoice if needed
		if next_invoice <= current_date:
			abo_doc.create_invoice()
			
	return

@frappe.whitelist()	
def get_email_recipient_and_message(address):
	recipient = frappe.db.get_value("Address", address, "email_id")
	
	template = frappe.db.get_value("emh settings", "emh settings", "invoice_email_template")

	html = frappe.db.get_value("Email Template", template, "response")
	
	return {
		'recipient': recipient,
		'message': html
		}
	
