# Copyright (c) 2021-2023, libracore and Contributors
# License: GNU General Public License v3. See license.txt

import frappe

@frappe.whitelist()
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
	frappe.log_error(commissioned_amount, "commissioned_amount")	
	#if there is a commissioned amount, calculate commission
	if commissioned_amount > 0:
		commission = commissioned_amount / 100 * commission_rate
	else:
		commission = 0
	
	self.commission = commission
	self.save()
		
	return
