# -*- coding: utf-8 -*-
import base64
import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class RunbotBranch(models.Model):

    _inherit = "runbot.branch"

    dump = fields.Boolean("Dump database after step all", default=False)
    dump_id = fields.Many2one('ir.attachment', string='Last DB dump')

    def _save_lastdb(self, data, filename):
        """ Save last database dump as an ir_attachment"""
        self.ensure_one()
        attachment = self.env['ir.attachment'].create({
            'datas': base64.b64encode(data),
            'name': filename,
            'datas_fname': filename
        })
        if self.dump_id:
            self.dump_id.unlink()
        self.dump_id = attachment
