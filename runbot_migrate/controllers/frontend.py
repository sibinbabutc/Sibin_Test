# -*- coding: utf-8 -*-
import base64
from odoo.http import Controller, request, route


class RunbotMigrate(Controller):

    @route(['/runbot/branch/<int:branch_id>/lastdump'], website=True, auth='public', type='http')
    def branch_dump(self, branch_id=None, **kwargs):
        """ Download last branch dump if it exists """
        domain = [('id', '=', branch_id), ('dump_id', '!=', False)]
        branch = request.env['runbot.branch'].search(domain, limit=1)
        if branch:
            headers = [
                ('Content-Type', 'application/gzip'),
                ('Content-Disposition',  'attachment; filename="%s"' % branch.dump_id.datas_fname),
            ]
            dump_data = base64.decodebytes(branch.dump_id.datas)
            return request.make_response(dump_data, headers)
        else:
            return request.render('website.404')
