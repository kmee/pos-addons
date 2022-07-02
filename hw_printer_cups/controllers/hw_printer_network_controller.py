# Copyright 2017-2018 Dinar Gabbasov <https://it-projects.info/team/GabbasovDinar>
# Copyright 2018 Tom Blauwendraat <tom@sunflowerweb.nl>
# License MIT (https://opensource.org/licenses/MIT).

import logging
import socket
import subprocess
import threading
import time
import traceback

from odoo import http

_logger = logging.getLogger(__name__)

try:
    from odoo.addons.hw_escpos.escpos import escpos
    from odoo.addons.hw_escpos.controllers.main import EscposProxy
    from odoo.addons.hw_escpos.controllers.main import EscposDriver
    from odoo.addons.hw_escpos.escpos.printer import Network
    from odoo.addons.hw_printer_network.escpos.printer import Cups
    #    import odoo.addons.hw_proxy.controllers.main as hw_proxy
    from odoo.addons.hw_drivers.controllers import proxy
except ImportError:
    EscposProxy = object
    EscposDriver = object


class EscposCupsDriver(EscposDriver):
    def __init__(self):
        self.cups_printers = []
        self.ping_processes = {}
        self.printer_objects = {}
        super(EscposCupsDriver, self).__init__()

    def update_driver_status(self):
        self.set_status("connected: for printer status se cups")

    def run(self):
        while True:
            try:
                error = True
                timestamp, task, data = self.queue.get(True)
                if task == "xml_receipt":
                    error = False
                    receipt, printer_name = data
                    _logger.info("Printing XML receipt on printer %s...")
                    printer = Cups(printer_name)
                    printer.open()
                    printer.receipt(receipt)

                elif task == "printstatus":
                    pass
                elif task == "status":
                    self.update_driver_status()
                error = False
            except Exception as e:
                self.set_status("error", str(e))
                errmsg = (
                    str(e)
                    + "\n"
                    + "-" * 60
                    + "\n"
                    + traceback.format_exc()
                    + "-" * 60
                    + "\n"
                )
                _logger.error(errmsg)
            finally:
                if error:
                    self.queue.put((timestamp, task, data))


# Separate instance, mainloop and queue for network printers
# original driver runs in parallel and deals with USB printers
cups_driver = EscposCupsDriver()

proxy.proxy_drivers["escpos_cups"] = cups_driver

# this will also start the message handling loop
cups_driver.push_task("printstatus")


class UpdatedEscposProxy(EscposProxy):
    @http.route("/hw_proxy/print_xml_receipt", type="json", auth="none", cors="*")
    def print_xml_receipt(self, receipt, proxy=None):
        if proxy:
            _logger.info('print_xml_receipt proxy %s', proxy)
            cups_driver.push_task("xml_receipt", (receipt, proxy))
        else:
            super(UpdatedEscposProxy, self).print_xml_receipt(receipt)

    @http.route("/hw_proxy/network_printers", type="json", auth="none", cors="*")
    def network_printers(self, network_printers=None):
        for printer in network_printers:
            cups_driver.get_network_printer(printer["ip"], name=printer["name"])

    @http.route("/hw_proxy/status_network_printers", type="json", auth="none", cors="*")
    def network_printers_status(self):
        return [dict(ip='epson-mileo', status="online", name="epson-mileo")]

    @http.route('/hw_proxy/open_cashbox', type='json', auth='none', cors='*')
    def open_cashbox(self, proxy=None):
        _logger.info('Open cashbox via network printer')
        cups_driver.push_task('cashbox', '10.0.2.73')

    @http.route('/hw_proxy/without_usb', type='http', auth='none', cors='*')
    def without_usb(self):
        """ Old pos_printer_network module expects this to work """
        return "ping"
