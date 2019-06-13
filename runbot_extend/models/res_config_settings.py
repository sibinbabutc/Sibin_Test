# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    nginx_client_max_body_size = fields.Char('Max uploadable size (nginx)')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(nginx_client_max_body_size=get_param('runbot.nginx_client_max_body_size', default='100M'))
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param("runbot.nginx_client_max_body_size", self.nginx_client_max_body_size)
