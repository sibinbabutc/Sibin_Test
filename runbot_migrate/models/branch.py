# -*- coding: utf-8 -*-
import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class RunbotBranch(models.Model):

    _inherit = "runbot.branch"

    dump = fields.Boolean("Dump database after step all", default=False)
    last_dump_id = fields.Many2one('ir.attachment', string='Last DB dump', compute='_compute_last_dump_id', store=True)

    def _compute_last_dump_id(self):
        Build = self.env['runbot.build']
        for branch in self:
            last_build = Build.search([('branch_id', '=', branch.id), ('dump_id', '!=', False)], order_by="sequence DESC", limit=1)
            if last_build:
                branch.last_dump_id = last_build.dump_id