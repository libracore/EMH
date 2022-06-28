# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022, libracore and contributors
# For license information, please see license.txt
#

# imports
import frappe
import json
from frappe.utils.data import get_datetime, today

@frappe.whitelist()
def get_employee_and_timesheet(user):
    data = {
        'employee': None,
        'timesheet': None
    }
    data = frappe._dict(data)
    if not user:
        user = frappe.session.user
    employee = frappe.db.sql("""SELECT `name` FROM `tabEmployee` WHERE `user_id` = '{user}' LIMIT 1""".format(user=user), as_dict=True)
    if len(employee) > 0:
        data.employee = employee[0].name
        timesheet = frappe.db.sql("""SELECT `name` FROM `tabTimesheet` WHERE `docstatus` = 0 AND `employee` = '{employee}' AND `start_date` = '{today}'""".format(employee=data.employee, today=today()), as_dict=True)
        if len(timesheet) > 0:
            data.timesheet = timesheet[0].name
    
    return data

@frappe.whitelist()
def create_ts(data):
    try:
        basestring
    except NameError:
        basestring = str
    
    if isinstance(data, basestring):
      data = json.loads(data)
    
    data = frappe._dict(data)
    
    timesheet = frappe.get_doc({
        "doctype": "Timesheet",
        "employee": data.employee,
        "time_logs": [
            {
                "activity_type": data.activity_type,
                "from_time": get_datetime(str(data.date) + " " + str(data.from_time)),
                "to_time": get_datetime(str(data.date) + " " + str(data.to_time)),
                "remarks": data.remarks,
                "project": data.project,
                "billable": data.bill
            }
        ]
    })
    timesheet.insert()
    return timesheet.name

@frappe.whitelist()
def create_ts_entry(data):
    try:
        basestring
    except NameError:
        basestring = str
    
    if isinstance(data, basestring):
      data = json.loads(data)
    
    data = frappe._dict(data)
    
    timesheet = frappe.get_doc("Timesheet", data.timesheet)
    
    row = timesheet.append('time_logs', {})
    row.activity_type = data.activity_type
    row.from_time = get_datetime(str(data.date) + " " + str(data.from_time))
    row.to_time = get_datetime(str(data.date) + " " + str(data.to_time))
    row.remarks = data.remarks
    row.project = data.project
    row.billable = data.bill
    
    timesheet.save()
    
    return timesheet.name
