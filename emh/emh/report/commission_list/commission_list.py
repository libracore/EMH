# Copyright (c) 2013, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt

def execute(filters):
    columns = get_columns()
    data =  get_data(filters)
    return columns, data

def get_columns():
    columns = [
        {"label": "Kunde", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 70},
        {"label": "Kundenname", "fieldname": "customer_name", "fieldtype": "Data", "width": 100},
        {"label": "Rechnungsdatum", "fieldname": "invoice_date", "fieldtype": "Date", "width": 90},
        {"label": "Rechnungsnummer", "fieldname": "invoice_no", "fieldtype": "Data", "width": 150},
        {"label": "Verkaufspartner", "fieldname": "sales_partner", "fieldtype": "Data", "width": 110},
        {"label": "Umsatz", "fieldname": "turnover", "fieldtype": "Currency", "width": 80},
        {"label": "Provisionssatz", "fieldname": "commission_rate", "fieldtype": "Percent", "width": 40},
        {"label": "Provision", "fieldname": "total_commission", "fieldtype": "Currency", "width": 75}        
    ]
    return columns


def get_data(filters):
    #original query, with real datas from the invoices
    # ~ sql_query = """
        # ~ SELECT
            # ~ `customer` AS `customer`,
            # ~ `customer_name` AS `customer_name`,
            # ~ `posting_date` AS `invoice_date`,
            # ~ `name` AS `invoice_no`,
            # ~ `sales_partner` AS `sales_partner`,
            # ~ `base_net_total` AS `turnover`,
            # ~ `commission_rate` AS `commission_rate`,
            # ~ `commission` AS `total_commission`
        # ~ FROM `tabSales Invoice`
        # ~ WHERE `posting_date` BETWEEN '{from_date}' AND '{to_date}'
            # ~ AND `commission_rate` > 0
            # ~ AND `docstatus` = 1
        # ~ ORDER BY `customer` DESC
    # ~ """.format(from_date=filters.from_date, to_date=filters.to_date)
    
    #Temporary query which works retroactive, has to be replaced by original query, because it dous only show actual commission rate (from the client)
    sql_query = """
        SELECT
			`invoice`.`name` AS `invoice_no`,
			`invoice`.`base_net_total` AS `turnover`,
			`invoice`.`customer_name`,
			`invoice`.`customer`,
			`invoice`.`posting_date` AS `invoice_date`,
			`tabCustomer`.`default_sales_partner` AS `sales_partner`,
			`tabCustomer`.`default_commission_rate` AS `commission_rate`,
			SUM(`item`.`amount`/100*`tabCustomer`.`default_commission_rate`) AS `total_commission`
        FROM `tabSales Invoice` AS `invoice`
        INNER JOIN `tabCustomer` ON `invoice`.`customer` = `tabCustomer`.`name`
        INNER JOIN `tabSales Invoice Item` AS `item` ON `item`.`parent` = `invoice`.`name`
        WHERE `item`.`item_code` = "1000"
        AND `tabCustomer`.`default_sales_partner` IS NOT NULL
        AND `invoice`.`docstatus` = 1
        AND `invoice`.`posting_date` BETWEEN '{from_date}' AND '{to_date}'
        GROUP BY `invoice_no`
        ORDER BY `invoice_no` DESC
    """.format(from_date=filters.from_date, to_date=filters.to_date)
   
    data = frappe.db.sql(sql_query, as_dict=True)
   
    return data
