# -*- coding: utf-8 -*-
import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class RunbotBranch(models.Model):

    _inherit = "runbot.branch"

    dump = fields.Boolean("Dump database after step all", default=False)
    last_dump = fields.Many2one('ir.attachment', string='Last DB dump', compute='_compute_last_dump_id', store=True)

    def _compute_last_dump_id(self):
        for branch in self:
            