# Copyright (c) 2023-2024, libracore and contributors
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
        {"label": "Relevanter Umsatz", "fieldname": "relevant_turnover", "fieldtype": "Currency", "width": 80},
        {"label": "Provisionssatz", "fieldname": "commission_rate", "fieldtype": "Percent", "width": 40},
        {"label": "Provision", "fieldname": "total_commission", "fieldtype": "Currency", "width": 75}        
    ]
    return columns


def get_data(filters):

    sql_query = """
        SELECT
            `invoice`.`customer`,
            `invoice`.`customer_name`,
            `invoice`.`name` AS `invoice_no`,
            `invoice`.`base_net_total` AS `turnover`,
            `invoice`.`posting_date` AS `invoice_date`,
            SUM(`item`.`net_amount`) AS `relevant_turnover`,
            IFNULL(`invoice`.`sales_partner`, `tabCustomer`.`default_sales_partner`) AS `sales_partner`,
            IF(`invoice`.`commission_rate` = 0 OR `invoice`.`commission` = 0,
                `tabCustomer`.`default_commission_rate`,
                `invoice`.`commission_rate`) AS `commission_rate`,
            IF(`invoice`.`commission_rate` = 0 OR `invoice`.`commission` = 0,
                SUM(`item`.`net_amount` / 100 * `tabCustomer`.`default_commission_rate`),
                `invoice`.`commission`) AS `total_commission`
        FROM `tabSales Invoice` AS `invoice`
        LEFT JOIN `tabCustomer` ON `invoice`.`customer` = `tabCustomer`.`name`
        LEFT JOIN `tabSales Invoice Item` AS `item` ON `item`.`parent` = `invoice`.`name`
        WHERE `item`.`item_code` = "1000"
          AND `tabCustomer`.`default_sales_partner` IS NOT NULL
          AND `invoice`.`docstatus` = 1
          AND `invoice`.`posting_date` BETWEEN '{from_date}' AND '{to_date}'
        GROUP BY `invoice_no`
        ORDER BY `invoice_no` DESC;
    """.format(from_date=filters.from_date, to_date=filters.to_date)
   
    data = frappe.db.sql(sql_query, as_dict=True)
   
    return data
