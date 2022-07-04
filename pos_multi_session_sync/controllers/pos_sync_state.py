
import logging
import os
from datetime import timedelta

from odoo import http, fields

_logger = logging.getLogger(__name__)


try:
    from odoo.addons.bus.controllers.main import BusController
except ImportError:
    _logger.error("pos_multi_session_sync inconsisten with odoo version")
    BusController = object


class PosSyncStateController(http.Controller):

    @http.route(['/pos_sync_monit/poll'], type='json', auth="public")
    def get_poll_status(self, **kw):
        """ Return datetime of the last poll request from all POS"""
        minutes_poll_limit = os.environ.get('POLL_LIMIT_HEALTH', 2)
        poll_limit_health = timedelta(minutes=minutes_poll_limit)
        pos_ids = http.request.env["pos_multi_session_sync.pos"].sudo().search([])
        res = {}
        for pos in pos_ids:
            pos_id = http.request.env["pos.config"].sudo().browse(pos.pos_ID)
            health = 'NOK'
            if pos.date_last_poll:
                delta_last_poll = fields.Datetime.now() - pos.date_last_poll
                if delta_last_poll < poll_limit_health:
                    health = 'OK'

            res[pos_id.name] = health + " - " + str(pos.date_last_poll)

        return res

    @http.route(['/pos_sync_monit/update'], type='json', auth="public")
    def get_update_status(self, **kw):
        """ Return datetime of the last update request from all POS"""
        pos_ids = http.request.env["pos_multi_session_sync.pos"].sudo().search([])
        res = {}
        for pos in pos_ids:
            pos_id = http.request.env["pos.config"].sudo().browse(pos.pos_ID)
            res[pos_id.name] = str(pos.date_last_update)

        return res

    @http.route(['/pos_sync_monit/status'], type='http', auth="public")
    def get_status(self, **kw):
        """ Return datetime of the last update request from all POS"""
        pos_ids = http.request.env["pos_multi_session_sync.pos"].sudo().search([])

        res ="""<table border="1" >
            <tbody>
            <tr>
            <td>&nbsp;Esta&ccedil;&atilde;o</td>
            <td>Poll&nbsp;</td>
            <td>Update&nbsp;</td>
            </tr>
            <tr>"""

        for pos in pos_ids:
            pos_id = http.request.env["pos.config"].sudo().browse(pos.pos_ID)
            terminal_name = pos_id.name
            date_last_poll = str(pos.date_last_poll)
            date_last_update = str(pos.date_last_update)

            res += f"""
                <tr>
                <td>&nbsp;{terminal_name}</td>
                <td>&nbsp;{date_last_poll}</td>
                <td>&nbsp;{date_last_update}</td>
                </tr>
            """

        res += """
            </tbody>
            </table>"""

        return res

