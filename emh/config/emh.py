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
    ]
