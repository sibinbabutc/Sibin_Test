# -*- coding: utf-8 -*-
import glob
import os
from odoo import models


class RunbotBuild(models.Model):
    _iherit = "runbot.build"

    def _save_dump(self):
        """ If a dump exists in the build dump dir, save it on the branch """
        self.ensure_one()
        dumps = glob.glob(self._path('dump/%s-*.tar.gz' % self.dest))
        if dumps:
            with open(dumps[0], 'rb') as dump_file:
                data = dump_file.read()
                self.branch_id._save_lastdb(data, os.path.basename(dumps[0]))
