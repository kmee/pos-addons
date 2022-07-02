#!/usr/bin/python

from __future__ import print_function

import logging
import tempfile
import subprocess

from odoo.addons.hw_escpos.escpos.escpos import Escpos


class Cups(Escpos):
    """ Define Network printer """

    def __init__(self, printer_name):
        """
        @param printer_name : Printer's on localhost cups
        """
        self.temp_file = NamedTemporaryFile()
        self.printer_name = printer_name
        self.auto_flush = True
        self.open()

    def open(self):
        """Open system file."""
        self.device = open(self.temp_file.name, "wb+")
        if self.device is None:
            print("Could not open the specified file {0}".format(self.temp_file.name))

    def _raw(self, msg):
        self.device.send(msg)

    def __del__(self):
        """ Close TCP connection """
        self.device.close()

    def _raw(self, msg):
        """Print any command sent in raw format.
        :param bytes data: arbitrary code to be printed by cups.
        """
        self.device.write(msg)
        if self.auto_flush:
            self.flush()

    def close(self):
        """Close system file."""
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('sends to printer %s with cups \n%s', self.printer_name)
        print_process = subprocess.Popen(
            ['lp', '-d', self.printer_name, self.temp_file.name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print_process.wait(timeout=3000)
        self.temp_file.close()
