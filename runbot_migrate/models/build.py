# -*- coding: utf-8 -*-
import base64
import glob
import os
from odoo import models, fields


class runbot_build(models.Model):
    _iherit = "runbot.build"

    dump_id = fields.Many2one('ir.attachment', string='Build DB dump')

    def _save_dump(self):
        """ If a dump exists in the build dump dir, save it on the branch """
        self.ensure_one()
        dumps = glob.glob(self._path('dump/%s-*.tar.gz' % self.dest))
        if dumps:
            with open(dumps[0], 'rb') as dump_file:
                data = dump_file.read()
                filename = os.path.basename(dumps[0])
                attachment = self.env['ir.attachment'].create({
                    'datas': base64.b64encode(data),
                    'name': filename,
                    'datas_fname': filename
                })
                if self.dump_id:
                    self.dump_id.unlink()
                self.dump_id = attachment
