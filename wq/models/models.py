# -*- coding: utf-8 -*-
from datetime import timedelta
from openerp import _, models, fields, api, tools
from openerp.exceptions import UserError, ValidationError

class Services(models.Model):
    _name = 'wq.services'
    _description = 'Services'

    name = fields.Char(string="Title", required=True)
    partner_id = fields.Many2one('res.partner', string="Responsible")
    category = fields.Many2many('partner_id.category_id')
    service_start = fields.Datetime('Start On', default=fields.Datetime.now)
    service_end = fields.Datetime('Close On')
    intake_capacity = fields.Integer(string="Intake Capacity", default=1)
    tokens = fields.One2many('wq.services.tokens', 'service_id', string='Tokens Issued')
    end_date = fields.Date(string="End Date", store=True,
        compute='_get_end_date', inverse='_set_end_date')
    rules = fields.Text(string="Rules")
    color = fields.Integer()
    state = fields.Selection([('draft', 'Draft'),('confirm', 'Confirmed'), ('done', 'Done')], default='draft')
    active = fields.Boolean(default=True)
    total_token = fields.Integer(compute="_compute_tokens_issued")
    image = fields.Binary(help="This fields holds the image used as image for the Service")
    image_medium = fields.Binary(compute='_compute_images')
    category_ids = fields.Many2many('service.category', string='Category')
    html_color = fields.Integer('Color Index')
    
    @api.depends('tokens.service_id')
    def _compute_tokens_issued(self):
        Token = self.env['wq.services.tokens']
        for service in self:
            service.total_token = Token.search_count([('service_id','=',service.id)])

    @api.depends('image_medium')
    def _compute_images(self):
        for record in self:
            record.image_medium = tools.image_resize_image_medium(record.image)

    @api.depends('service_start')
    def _get_end_date(self):
        for r in self:
            if not (r.service_start):
                r.end_date = r.service_start
                continue
            start = fields.Datetime.from_string(r.service_start)
    def _set_end_date(self):
        for r in self:
            if not (r.service_start and r.end_date):
                continue
            service_start = fields.Datetime.from_string(r.service_start)

    @api.multi
    def action_confirm(self):
        self.write({'state':'confirm'})

    @api.multi
    def action_done(self):
        self.write({'state':'done'})

    @api.multi
    def action_call_next(self):
        Token = self.env['wq.services.tokens']
        if Token.search([('service_id','=', self.service.id),('status','=','serving')]) :
            Token.action_serve()
        else :
            t = Token.search([('service_id','=', self.service.id),('status','=','granted')])[0]
    

class ServiceCategory(models.Model):
    _name = 'service.category'
    _order = 'sequence, name'

    name = fields.Char(required=True, translate=True)
    parent_id = fields.Many2one('service.category', string='Parent Category')
    child_ids = fields.One2many('service.category', 'parent_id')
    sequence = fields.Integer(help='Gives the sequence order when displaying a list of categories.')
    color = fields.Integer('Color Index')

    @api.multi
    def name_get(self):
        res = []
        for cat in self:
            names = [cat.name]
            pcat = cat.parent_id
            while pcat:
                names.append(pcat.name)
                pcat = pcat.parent_id
            res.append((cat.id, ' / '.join(reversed(names))))
        return res

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValueError(_('Error ! You cannot create recursive categories.'))

 #provider = fields.Char()

# class Organization_type(models.Model):
#     _name = 'wq.org.type'

#     name = fields.Char()


class ServiceToken(models.Model):
    _name = 'wq.services.tokens'
    _description = 'Token'

    _status = [('draft', 'Not-Issued'),
        ('granted', 'Issued'),
        ('serving', "Serving"),
        ('served', 'Served'), 
        ('revoked', 'Cancelled')]

    service_id = fields.Many2one('wq.services', string="Service", required=True)
    unique_token = fields.Char(required=True, default=lambda self: self.env['ir.sequence'].next_by_code('wq.services.tokens') or 'New Token')
    #unique_token = fields.Char(required=True, default=lambda self: self.env['ir.sequence'].next_by_code('wq.services.tokens') or 'New Token')
    service_starttime = fields.Datetime(related='service_id.service_start', string="Issued On")
    expiry_datetime = fields.Datetime(related='service_id.service_end', string="Service End On")
    status = fields.Selection(selection=_status, string="Token Status", default='draft')
    issued_to = fields.Many2one('res.partner')

    @api.multi
    def action_issue(self):
        if self.service_id.state == "confirm":
            if self.service_id.total_token > self.service_id.intake_capacity:
                raise UserError(_('You Reached maximum Capacity.'))
            self.write({'status':'granted', 'service_starttime': fields.Datetime.now()})
        else:
            raise UserError(_('You cannot register token if Service not confirmed'))

    @api.multi
    def action_serve(self):
        self.write({'status':'served', 'expiry_datetime': fields.Datetime.now()})

    @api.multi
    def action_revoked(self):
        self.write({'status':'revoked'})
          

class RegisterToken(models.TransientModel):
    _name = 'wq.tokenregister'

    service_id = fields.Many2one('wq.services')
    partner_id = fields.Many2one('res.partner')

    def generate_token(self):
        pass

    def register_token(self):
        pass

    def notify_user(self):
        pass









# class wq(models.Model):
#     _name = 'wq.wq'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100