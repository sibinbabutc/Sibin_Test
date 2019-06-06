# -*- encoding: utf-8 -*-

import base64
import glob
import logging
import os

from odoo import models, fields
from odoo.addons.runbot.container import docker_run

_logger = logging.getLogger(__name__)


class DumpStep(models.Model):
    _inherit = "runbot.build.config.step"

    job_type = fields.Selection(selection_add=[('dump_db', 'Dump database')])

    def _run_step(self, build, log_path):
        if self.job_type == 'dump_db':
            return self._dump_db(build, log_path)
        return super(DumpStep, self)._run_step(build, log_path)

    def _dump_db(self, build, log_path):
        previous_step_index = build.config_id.step_ids().index(build.active_step) - 1
        previous_step_name = build.config_id.step_ids()[previous_step_index].name
        db_name = "%s-%s" % (build.dest, previous_step_name)
        cmd = '&&'.join([
            'cd /data/build',
            'mkdir -p dump',
            'pg_dump -d %(db_name)s > %(db_name)s.sql',
            r'tar -c --transform "s/datadir\/filestore\/%(db_name)s/filestore/" -f dump/%(db_name)s.tar.gz %(db_name)s.sql datadir/filestore/%(db_name)s' % {'db_name': db_name}
        ])
        docker_run(cmd, log_path, build._path(), build._get_docker_name())


class SaveStep(models.Model):
    _inherit = "runbot.build.config.step"

    job_type = fields.Selection(selection_add=[('save_dump', 'Save database dump')])

    def _run_step(self, build, log_path):
        if self.job_type == 'save_dump':
            return self._save_dump(build, log_path)
        return super(SaveStep, self)._run_step(build, log_path)

    def _save_dump(self, build, log_path):
        """ If a dump exists in the build dump dir, save it as an ir.attachement """
        dumps = glob.glob(build._path('dump/%s-*.tar.gz' % build.dest))
        if dumps:
            with open(dumps[0], 'rb') as dump_file:
                data = dump_file.read()
                filename = os.path.basename(dumps[0])
                self.env['ir.attachment'].create({
                    'res_model': 'runbot.build',
                    'res_id': build.id,
                    'res_name': build.dest,
                    'datas': base64.b64encode(data),
                    'name': filename,
                    'datas_fname': filename
                })
