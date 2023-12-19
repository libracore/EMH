# Copyright (c) 2021-2023, libracore and Contributors
# License: GNU General Public License v3. See license.txt

import frappe

@frappe.whitelist()
def calculate_comission(sales_invoice):
	#check for sales partner
	sales_partner = frappe.db.get_value("Sales Invoice", sales_invoice, "sales_partner")
	#if sales partner -> get all items with item code 1000
	if sales_partner:
		sql_query = """
			SELECT SUM(`amount`)
			FROM `tabSales Invoice Item`
			WHERE `parent` = "{si}"
			AND `item_code` = "1000"
		""".format(si=sales_invoice)
		
		data = frappe.db.sql(sql_query, as_dict=True)
		
		#get commission rate
		commission_rate = frappe.db.get_value("Sales Invoice", sales_invoice, "commission_rate")
		
		#if an item with item code 1000 was found -> calculate commission
		if data[0]['SUM(`amount`)'] is not None:
			commission = data[0]['SUM(`amount`)'] / 100 * commission_rate
		else:
			commission = 0
		
		return commission
	#if not sales partner -> return nothing
	else:
		return
