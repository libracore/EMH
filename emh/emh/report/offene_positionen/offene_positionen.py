# Copyright (c) 2022, libracore and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import calendar
import datetime
from frappe.utils import cint

def execute(filters=None):
    columns, data = [], []
            
    columns = get_columns()
    
    data = get_data(filters)
    
    return columns, data

def get_columns():
    return [
        {'fieldname': 'customer', 'label': _('Customer'), 'fieldtype': 'Link', 'options': 'Customer', 'width': 75},
        {'fieldname': 'customer_name', 'label': _('Customer name'), 'fieldtype': 'Data', 'width': 150},
        {'fieldname': 'date', 'label': _('Date'), 'fieldtype': 'Date', 'width': 80},
        {'fieldname': 'project', 'label': _('Project'), 'fieldtype': 'Link', 'options': 'Project', 'width': 150},
        {'fieldname': 'item', 'label': _('Item'), 'fieldtype': 'Link', 'options': 'Item', 'width': 200},
        {'fieldname': 'hours', 'label': _('Billing Hours'), 'fieldtype': 'Float', 'width': 100},
        {'fieldname': 'qty', 'label': _('Qty'), 'fieldtype': 'Float', 'width': 50},
        {'fieldname': 'rate', 'label': _('Rate'), 'fieldtype': 'Currency', 'width': 100},
        {'fieldname': 'reference', 'label': _('Reference'), 'fieldtype': 'Dynamic Link', 'options': 'dt', 'width': 120},
        {'fieldname': 'action', 'label': _('Action'), 'fieldtype': 'Data', 'width': 100}
    ]
    
def get_data(filters):
    entries = get_invoiceable_entries(from_date=filters.from_date, to_date=filters.to_date, customer=filters.customer)
    
    # find customers
    customers = []
    for e in entries:
        if e.customer not in customers:
            customers.append(e.customer)
    
    # create grouped entries
    output = []
    for c in customers:
        details = []
        total_h = 0
        total_amount = 0
        customer_name = None
        for e in entries:
            if e.customer == c:
                total_h += e.hours or 0
                total_amount += ((e.qty or 1) * (e.rate or 0))
                customer_name = e.customer_name
                details.append(e)
                
        # insert customer row
        output.append({
            'customer': c,
            'customer_name': customer_name,
            'hours': total_h,
            'qty': 1,
            'rate': total_amount,
            'action': 'Create invoice',
            'indent': 0
        })
        for d in details:
            output.append(d)
            
    return output

def get_invoiceable_entries(from_date=None, to_date=None, customer=None):
    if not from_date:
        from_date = "2000-01-01"
    if not to_date:
        to_date = "2099-12-31"
    if not customer:
        customer = "%"
        
    invoicing_item = frappe.get_value("simpliq settings", "simpliq settings", "service_item")
    
    sql_query = """
        SELECT 
            `tabProject`.`customer` AS `customer`,
            `tabCustomer`.`customer_name` AS `customer_name`,
            DATE(`tabTimesheet Detail`.`from_time`) AS `date`,
            "Timesheet"  AS `dt`,
            `tabTimesheet`.`name` AS `reference`,
            `tabTimesheet`.`employee_name` AS `employee_name`,
            `tabTimesheet Detail`.`name` AS `detail`,
            `tabProject`.`name` AS `project`,
            "{invoicing_item}" AS `item`,
            `tabTimesheet Detail`.`billing_hours` AS `hours`,
            1 AS `qty`,
            NULL AS `rate`,
            `tabTimesheet Detail`.`remarks` AS `remarks`,
            1 AS `indent`
        FROM `tabTimesheet Detail`
        LEFT JOIN `tabTimesheet` ON `tabTimesheet`.`name` = `tabTimesheet Detail`.`parent`
        LEFT JOIN `tabSales Invoice Item` ON (
            `tabTimesheet Detail`.`name` = `tabSales Invoice Item`.`ts_detail`
            AND `tabSales Invoice Item`.`docstatus` < 2
        )
        LEFT JOIN `tabProject` ON `tabProject`.name = `tabTimesheet Detail`.`project`
        LEFT JOIN `tabCustomer` ON `tabCustomer`.`name` = `tabProject`.`customer`
        WHERE 
           `tabTimesheet`.`docstatus` = 1
           AND `tabCustomer`.`name` LIKE "{customer}"
           AND ((`tabTimesheet Detail`.`from_time` >= "{from_date}" AND `tabTimesheet Detail`.`from_time` <= "{to_date}")
            OR (`tabTimesheet Detail`.`to_time` >= "{from_date}" AND `tabTimesheet Detail`.`to_time` <= "{to_date}"))
           AND `tabSales Invoice Item`.`name` IS NULL
        
        UNION SELECT
            `tabDelivery Note`.`customer` AS `customer`,
            `tabDelivery Note`.`customer_name` AS `customer_name`,
            `tabDelivery Note`.`posting_date` AS `date`,
            "Delivery Note" AS `dt`,
            `tabDelivery Note`.`name` AS `reference`,
            NULL AS `employee_name`,
            `tabDelivery Note Item`.`name` AS `detail`,
            `tabDelivery Note`.`project` AS `project`,
            `tabDelivery Note Item`.`item_code` AS `item`,
            NULL AS `hours`,
            `tabDelivery Note Item`.`qty` AS `qty`,
            `tabDelivery Note Item`.`net_rate` AS `rate`,
            `tabDelivery Note`.`name` AS `remarks`,
            1 AS `indent`
        FROM `tabDelivery Note Item`
        LEFT JOIN `tabDelivery Note` ON `tabDelivery Note`.`name` = `tabDelivery Note Item`.`parent`
        LEFT JOIN `tabSales Invoice Item` ON (
            `tabDelivery Note Item`.`name` = `tabSales Invoice Item`.`dn_detail`
            AND `tabSales Invoice Item`.`docstatus` < 2
        )
        WHERE 
            `tabDelivery Note`.`docstatus` = 1
            AND `tabDelivery Note`.`customer` LIKE "{customer}"
            AND (`tabDelivery Note`.`posting_date` >= "{from_date}" AND `tabDelivery Note`.`posting_date` <= "{to_date}")
            AND `tabSales Invoice Item`.`name` IS NULL
            
        UNION SELECT
            `tabAbo`.`customer` AS `customer`,
            `tabAbo`.`customer_name` AS `customer_name`,
            `tabAbo`.`start_date` AS `date`,
            "Abo" AS `dt`,
            `tabAbo`.`name` AS `reference`,
            NULL AS `employee_name`,
            `tabAbo Item`.`name` AS `detail`,
            NULL AS `project`,
            `tabAbo Item`.`item` AS `item`,
            NULL AS `hours`,
            `tabAbo Item`.`qty` AS `qty`,
            `tabAbo Item`.`rate` AS `rate`,
            `tabAbo`.`name` AS `remarks`,
            1 AS `indent`
        FROM `tabAbo Item`
        LEFT JOIN `tabAbo` ON `tabAbo`.`name` = `tabAbo Item`.`parent`
        WHERE
            `tabAbo`.`enabled` = 1
            AND `tabAbo`.`customer` LIKE "{customer}"
            AND `tabAbo`.`start_date` <= "{to_date}" 
            AND (`tabAbo`.`end_date` IS NULL OR `tabAbo`.`end_date` >= "{to_date}")
            AND ((`tabAbo`.`interval` = "Monhtly" AND (SELECT IFNULL(MAX(`tAI1`.`date`), "2000-01-01") 
                                                      FROM `tabAbo Invoice` AS `tAI1`
                                                      WHERE `tAI1`.`parent` = `tabAbo`.`name`) <= DATE_FORMAT(NOW() ,'%Y-%m-01'))
                 OR (`tabAbo`.`interval` = "Yearly" AND (SELECT IFNULL(MAX(`tAI2`.`date`), "2000-01-01")
                                                      FROM `tabAbo Invoice` AS `tAI2`
                                                      WHERE `tAI2`.`parent` = `tabAbo`.`name`) <= DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 12 MONTH) ,'%Y-%m-01'))
                )
        
        ORDER BY `date` ASC;
    """.format(from_date=from_date, to_date=to_date, invoicing_item=invoicing_item, customer=customer)
    entries = frappe.db.sql(sql_query, as_dict=True)
    return entries

@frappe.whitelist()
def create_invoice(from_date, to_date, customer):
    # fetch entries
    entries = get_invoiceable_entries(from_date=from_date, to_date=to_date, customer=customer)
    
    # create sales invoice
    sinv = frappe.get_doc({
        'doctype': "Sales Invoice",
        'customer': customer,
        'customer_group': frappe.get_value("Customer", customer, "customer_group")
    })
    
    for e in entries:
        #Format Remarks 
        if e.remarks:
            remarkstring = "{0} : {1} <br>{2}".format(e.date.strftime("%d.%m.%Y"), e.employee_name,  e.remarks.replace("\n", "<br>"))
        else:
            remarkstring = "{0} : {1}".format(e.date.strftime("%d.%m.%Y"), e.employee_name)

        item = {
            'item_code': e.item,
            'qty': e.qty,
            'rate': e.rate,
            'description': e.remarks,            # will be overwritten by frappe
            'remarks': remarkstring

        }
        if e.dt == "Delivery Note":
            item['delivery_note'] = e.reference
            item['dn_detail'] = e.detail
        elif e.dt == "Timesheet":
            item['timesheet'] = e.reference
            item['ts_detail'] = e.detail
            item['qty'] = e.hours
     
        sinv.append('items', item)
        
    sinv.insert()
    
    # insert abo references
    abos = []
    for e in entries:
        if e.dt == "Abo" and e.reference not in abos:
            abos.append(e.reference)
    for a in abos:
        abo = frappe.get_doc("Abo", a)
        abo.append("invoices", {
            'date': datetime.datetime.now(),
            'sales_invoice': sinv.name
        })
        abo.save()
    
    frappe.db.commit()
    
    return sinv.name
