# Copyright 2022 Luis Felipe Mileo <mileo@kmee.com.br>
# License MIT (https://opensource.org/licenses/MIT).

{
    "name": """Hardware Cups Printer""",
    "summary": """Hardware Driver for Cups Printers""",
    "category": "Point of Sale",
    "images": [],
    "version": "13.0.2.0.1",
    "application": False,
    "author": "KMEE",
    "website": "https://github.com/oca/pos",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["hw_escpos"],
    "external_dependencies": {"python": [], "bin": []},
    "data": [],
    "qweb": [],
    "demo": [],
    "post_load": "post_load",
    "pre_init_hook": None,
    "post_init_hook": None,
    "auto_install": False,
    "installable": False,
}
