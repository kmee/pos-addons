# Copyright 2022 Luis Felipe Mileo <mileo@kmee.com.br>
# License MIT (https://opensource.org/licenses/MIT).

import logging
import traceback

from odoo import http

_logger = logging.getLogger(__name__)

try:
    from odoo.addons.hw_escpos.escpos import escpos
    from odoo.addons.hw_escpos.controllers.main import EscposProxy
    from odoo.addons.hw_escpos.controllers.main import EscposDriver
    from odoo.addons.hw_printer_cups.escpos.printer import Cups
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

    def get_cups_printers(self, cups_name, name=None):
        found_printer = False
        for printer in self.cups_printers:
            if printer["cups_name"] == cups_name:
                found_printer = True
                if name:
                    printer["name"] = name
                if printer["status"] == "online":
                    printer_object = self.printer_objects.get(cups_name, None)
                    if not printer_object:
                        try:
                            printer_object = Cups(cups_name)
                            self.printer_objects[cups_name] = printer_object
                        except Exception:
                            pass
                    return printer
        if not found_printer:
            self.add_cups_printer(cups_name, name)
        return None

    def add_cups_printer(self, cups_name, name=None):
        printer = dict(cups_name=cups_name, status="online", name=name or "Unnamed printer")
        self.cups_printers.append(printer)  # dont return because offline
        # self.start_pinging(ip)

    def update_driver_status(self):
        self.set_status("connected: for printer status se cups")

    def run(self):
        while True:
            try:
                error = True
                timestamp, task, data = self.queue.get(True)
                if task == "xml_receipt":
                    receipt, printer_name = data
                    printer = self.printer_objects.get(printer_name,  Cups(printer_name))
                    _logger.info("Printing XML receipt on printer {}".format(printer_name))
                    printer.open()
                    printer.receipt(receipt)
                    printer.close()
                    error = False
                elif task == "printstatus":
                    error = False
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
            cups_driver.get_cups_printers(cups_name=printer["ip"], name=printer["name"])

    @http.route("/hw_proxy/status_network_printers", type="json", auth="none", cors="*")
    def network_printers_status(self):
        return cups_driver.cups_printers
