#!/usr/bin/python

from __future__ import print_function

import subprocess

from tempfile import NamedTemporaryFile


from odoo.addons.hw_escpos.escpos.escpos import Escpos


class Cups(Escpos):
    """ Define Network printer """

    def __init__(self, printer_name):
        """
        @param printer_name : Printer's on localhost cups
        """
        self.device = None
        self.cups_server = 'localhost'
        self.temp_file = NamedTemporaryFile()
        self.printer_name = printer_name
        self.auto_flush = True

    def open(self):
        """Open system file."""
        self.device = open(self.temp_file.name, "wb+")
        if self.device is None:
            print("Could not open the specified file {0}".format(self.temp_file.name))

    def _raw(self, msg):
        """Print any command sent in raw format.
        :param bytes data: arbitrary code to be printed by cups.
        """
        if type(msg) is str:
            msg = msg.encode("utf-8")
        self.device.write(msg)
        if self.auto_flush:
            """ Write on file every time _raw is called"""
            self.device.flush()

    def close(self):
        """Close system file."""
        print_process = subprocess.Popen(
            ['lp', '-h', self.cups_server, '-d', self.printer_name, self.temp_file.name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print_process.wait(timeout=3000)
        self.temp_file.close()
