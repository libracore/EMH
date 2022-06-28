frappe.pages['mobile-ts'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Mobile TS',
        single_column: true
    });
    
    // get Employee and current Timesheet by User
    frappe.call({
        "method": "emh.emh.page.mobile_ts.mobile_ts.get_employee_and_timesheet",
        "args": {
            "user": frappe.session.user_email
        },
        "callback": function(r) {
            page.employee = r.message.employee;
            page.timesheet = r.message.timesheet;
            
            // build page
            frappe.mobile_ts.build_essential(page);
        }
    });
}

frappe.mobile_ts = {
    build_essential: function(page) {
        // Employee Link
        page.add_field({
            label: 'Employee',
            fieldtype: 'Link',
            fieldname: 'employee',
            options: 'Employee',
            default: page.employee,
            reqd: 1
        });
        // set width of employee-link
        page.fields_dict.employee.$wrapper.removeClass("col-md-2");
        page.fields_dict.employee.$wrapper.addClass("col-md-4");
        
        // Date
        page.add_field({
            label: 'Date',
            fieldtype: 'Date',
            fieldname: 'date',
            reqd: 1,
            default: frappe.datetime.nowdate()
        });
        // set width of date
        page.fields_dict.date.$wrapper.removeClass("col-md-2");
        page.fields_dict.date.$wrapper.addClass("col-md-4");
        
        // TS Link
        page.add_field({
            label: 'Timesheet',
            fieldtype: 'Link',
            fieldname: 'timesheet',
            options: 'Timesheet',
            default: page.timesheet
        });
        // set width of timesheet-link
        page.fields_dict.timesheet.$wrapper.removeClass("col-md-2");
        page.fields_dict.timesheet.$wrapper.addClass("col-md-4");
        
        // Section Break
        page.add_break();
        
        // Activity Type
        page.add_field({
            label: 'Aktivitätsart',
            fieldtype: 'Link',
            fieldname: 'activity_type',
            options: 'Activity Type',
            reqd: 1
        });
        // set width of from_time
        page.fields_dict.activity_type.$wrapper.removeClass("col-md-2");
        page.fields_dict.activity_type.$wrapper.addClass("col-md-4");
        
        // From time
        page.add_field({
            label: 'Von',
            fieldtype: 'Time',
            fieldname: 'from_time',
            default: frappe.datetime.now_time(),
            reqd: 1
        });
        // set width of from_time
        page.fields_dict.from_time.$wrapper.removeClass("col-md-2");
        page.fields_dict.from_time.$wrapper.addClass("col-md-4");
        
        // To time
        page.add_field({
            label: 'Bis',
            fieldtype: 'Time',
            fieldname: 'to_time',
            reqd: 1
        });
        // set width of to_time
        page.fields_dict.to_time.$wrapper.removeClass("col-md-2");
        page.fields_dict.to_time.$wrapper.addClass("col-md-4");
        
        // Section Break
        page.add_break();
        
        // Project
        page.add_field({
            label: 'Project',
            fieldtype: 'Link',
            fieldname: 'project',
            options: 'Project'
        });
        // set width of to_time
        page.fields_dict.project.$wrapper.removeClass("col-md-2");
        page.fields_dict.project.$wrapper.addClass("col-md-4");
        
        // Bill Checkbox
        page.add_field({
            label: __('Bill'),
            fieldtype: 'Check',
            fieldname: 'bill'
        });
        
        // Section Break
        page.add_break();
        
        // Remarks
        page.add_field({
            label: 'Bemerkungen',
            fieldtype: 'Text',
            fieldname: 'remarks'
        });
        
        // set width of remarks
        page.fields_dict.remarks.$wrapper.removeClass("col-md-2");
        page.fields_dict.remarks.$wrapper.addClass("col-md-12");
        
        // "Add" Button
        page.add_field({
            label: 'Add',
            fieldtype: 'Button',
            fieldname: 'add',
            click() {
                frappe.mobile_ts.check_ts(page);
            }
        });
        
        // collabse section breaks
        page.page_form.collapse();
        
        // set filter to linkfields
        frappe.mobile_ts.set_filter(page);
    },
    set_filter: function(page) {
        // Emplyoee based on User
        page.fields_dict.employee.get_query = function(user) {
             return {
                 filters: {
                     "user_id": frappe.session.user_email
                 }
             }
        }
        
        // Timesheet based on employee
        page.fields_dict.timesheet.get_query = function(employee, date) {
             return {
                 filters: {
                     "employee": page.fields_dict.employee.get_value(),
                     "start_date": page.fields_dict.date.get_value()
                 }
             }
        }
    },
    check_ts: function(page) {
        if (
            !page.fields_dict.employee.get_value()||
            !page.fields_dict.activity_type.get_value()||
            !page.fields_dict.from_time.get_value()||
            !page.fields_dict.to_time.get_value()||
            !page.fields_dict.date.get_value()
        ) {
            frappe.msgprint({
                "title": "Fehlende Angaben",
                "message": "Bitte alle Pflichtfelder ausfüllen",
                "indicator": "red"
            });
        } else {
            if (!page.fields_dict.timesheet.get_value()) {
                frappe.confirm(
                    'Es wurde <b>kein</b> Timesheet ausgewählt, möchten Sie ein neues anlegen?',
                    function(){
                        // on yes
                        frappe.mobile_ts.create_ts(page);
                    },
                    function(){
                        // on no
                        show_alert('Timsheet-Anlage abgebrochen')
                    }
                )
            } else {
                frappe.mobile_ts.create_ts_entry(page);
            }
        }
    },
    create_ts: function(page) {
        var data = frappe.mobile_ts.get_page_values(page);
        
        frappe.call({
            "method": "emh.emh.page.mobile_ts.mobile_ts.create_ts",
            "args": {
                "data": data
            },
            "callback": function(r) {
                show_alert('Ausgeführt')
                page.timesheet = r.message;
                // reset page
                frappe.mobile_ts.reset_page(page);
            }
        });
    },
    create_ts_entry: function(page) {
        var data = frappe.mobile_ts.get_page_values(page);
        
        frappe.call({
            "method": "emh.emh.page.mobile_ts.mobile_ts.create_ts_entry",
            "args": {
                "data": data
            },
            "callback": function(r) {
                show_alert('Ausgeführt')
                // reset page
                frappe.mobile_ts.reset_page(page);
            }
        });
    },
    get_page_values: function(page) {
        var data = {}
        data.employee = page.fields_dict.employee.get_value();
        data.date = page.fields_dict.date.get_value();
        data.timesheet = page.fields_dict.timesheet.get_value();
        data.activity_type = page.fields_dict.activity_type.get_value();
        data.from_time = page.fields_dict.from_time.get_value();
        data.to_time = page.fields_dict.to_time.get_value();
        data.remarks = page.fields_dict.remarks.get_value();
        data.bill = page.fields_dict.bill.get_value();
        data.project = page.fields_dict.project.get_value();
        return data
    },
    reset_page: function(page) {
        // clear fields
        page.clear_fields();
        
        // build page
        frappe.mobile_ts.build_essential(page);
    }
}
