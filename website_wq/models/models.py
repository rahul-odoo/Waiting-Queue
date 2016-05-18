# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import api, models
from openerp.addons.website.models.website import slug


class Services(models.Model):
    _name = 'wq.services'
    _inherit = ['wq.services', 'website.published.mixin']

    @api.multi
    def _website_url(self, name, arg):
        res = super(Services, self)._website_url(name, arg)
        res.update({(service.id, '/services/%s' % slug(service)) for service in self})
        return res