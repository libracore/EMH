# Copyright (c) 2013, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    columns = [
        {"label": _("Customer"), "fieldname": "customer", "fieldtype": "Data", "width": 200},
        {"label": _("Customer No."), "fieldname": "customer_no", "fieldtype": "Link", "options": "Customer", "width": 120},
        {"label": _("Description"), "fieldname": "description", "fieldtype": "Data", "width": 200},
        {"label": _("IP Address"), "fieldname": "ip_address", "fieldtype": "Data", "width": 200}
    ]
    return columns
    
def get_data(filters):
    
    conditions = ""
    if filters.get("customer"):
        conditions = """ WHERE `cust`.`name` = "{customer}" """.format(customer=filters.get("customer"))
    
    data = frappe.db.sql("""SELECT
        `cust`.`customer_name` AS `customer`,
        `cust`.`name` AS `customer_no`,
        `ip`.`description` AS `description`,
        `ip`.`ip_address` AS `ip_address`
        FROM `tabCustomer IP List` AS `ip`
        LEFT JOIN `tabCustomer` AS `cust` ON `ip`.`parent` = `cust`.`name`
        {conditions}
        ORDER BY `cust`.`name`;""".format(conditions=conditions), as_dict=True)

    return data
