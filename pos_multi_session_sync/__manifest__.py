# Copyright 2017 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2017,2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License MIT (https://opensource.org/licenses/MIT).
{
    "name": """Sync Server in POS""",
    "summary": """Sync orders via main or separate (e.g. local) server""",
    "category": "Point of Sale",
    # "live_test_url": 'http://apps.it-projects.info/shop/product/pos-multi-session?version=12.0',
    "images": ["images/pos_multi_session_sync.jpg"],
    "version": "12.0.1.0.7",
    "application": False,
    "author": "IT-Projects LLC, Kolushov Alexandr",
    "support": "apps@itpp.dev",
    "website": "https://apps.odoo.com/apps/modules/12.0/pos_multi_session_sync/",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["pos_longpolling"],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "security/ir.model.access.csv",

        "views/pos_multi_session_sync_menu.xml",
    ],
    "qweb": [],
    "demo": [],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "auto_install": False,
    "installable": True,
}
