from __future__ import unicode_literals
from frappe import _

def get_data():
    return [
        {
            "label": _("Mobile TS App"),
            "icon": "fa fa-cog",
            "items": [
                {
                    "type": "page",
                    "name": "mobile-ts",
                    "label": _("mobile-ts"),
                    "description": _("mobile-ts"),
                },
            ]
        },
        {
            "label": _("Sales"),
            "icon": "octicon octicon-repo",
            "items": [
                   {
                       "type": "doctype",
                       "name": "Customer",
                       "label": _("Customer"),
                       "description": _("Customer")
                   },
                   {
                       "type": "doctype",
                       "name": "Quotation",
                       "label": _("Quotation"),
                       "description": _("Quotation")
                   },
                   {
                       "type": "doctype",
                       "name": "Sales Order",
                       "label": _("Sales Order"),
                       "description": _("Sales Order")
                   },
                   {
                       "type": "doctype",
                       "name": "Delivery Note",
                       "label": _("Delivery Note"),
                       "description": _("Delivery Note")
                   },
                   {
                       "type": "doctype",
                       "name": "Sales Invoice",
                       "label": _("Sales Invoice"),
                       "description": _("Sales Invoice")
                   }
            ]
        },
        {
            "label": _("Timesheets"),
            "icon": "octicon octicon-repo",
            "items": [
                    {
                        "type": "doctype",
                        "name": "Timesheet",
                        "label": _("Timesheet"),
                        "description": _("Timesheet")
                    }
            ]
        },
        {
            "label": _("Invoicing"),
            "icon": "octicon octicon-repo",
            "items": [
                   {
                       "type": "report",
                       "name": "Offene Positionen",
                       "label": _("Offene Positionen"),
                       "doctype": "Timesheet",
                       "is_query_report": True
                   }
            ]
        },
        {
            "label": _("Settings"),
            "icon": "octicon octicon-repo",
            "items": [
                   {
                       "type": "doctype",
                       "name": "emh settings",
                       "label": _("emh settings"),
                       "description": _("emh settings")
                   },
                   {
                       "type": "doctype",
                       "name": "ERPNextSwiss Settings",
                       "label": _("ERPNextSwiss Settings"),
                       "description": _("ERPNextSwiss Settings")
                   }
            ]
        }
    ]
