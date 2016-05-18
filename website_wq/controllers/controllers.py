# -*- coding: utf-8 -*-
import babel.dates
import time
import re
import werkzeug.urls
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp import http
from openerp import tools, SUPERUSER_ID
from openerp.addons.website.models.website import slug
from openerp.http import request
from openerp.tools.translate import _


class website_wq(http.Controller):

    @http.route(['/services'], type='http', auth='public', website=True)
    def index(self, **kw):
    	Services = http.request.env['wq.services'].sudo().search([])
        values = {'services': Services}
        return http.request.render('website_wq.index', values)

    @http.route('/services/<model("wq.services"):service>', auth='public', website=True)
    def service_details(self, service, **kw):
        values = {
            'service': service,
            'main_object': service,
            'range': range,
        }
        return http.request.render('website_wq.service_details', values)


    @http.route(['/services/token/<int:service_id>'], type='http', auth="public", website=True)
    def page(self, service_id=None, **kw):
        Services = http.request.env['wq.services'].sudo().search([])
        values = {'services': Services}
        return http.request.website.render('website_wq.token_details', values)

    @http.route(['/services/<model("wq.services"):service>/registration/new'], type='json', auth="public", methods=['POST'], website=True)
    def registration_new(self, service, **post):
        #return request.redirect("/services/%s" % slug(service))
        return request.website._render("website_wq.token_details", {'service':service, 'name': service.name})

    # def send_mail(self,service,partner,token):
    #    # Partner = http.request.env['res.partner'].sudo().search(['id','=', partner])
    #     Partner_obj = http.request.env['res.partner'].browse(partner)
    #     Mail = http.request.env['mail.mail']
    #     mail_values = {
    #         'body_html' : '''
    #         Thanks for registering for our service %s.
    #         The Registration details for Service are as below.
    #         Schedule:
    #         Datetime from: %s
    #         Datetime To: %s
    #         Address: 
    #         Token: %s
    #         Pleas bring this document while reach us.
    #         Thanks and Regards. ''' % (service.name, service.service_start, service.service_end, token.unique_token),
    #         'email_to' : Partner_obj.email,
    #         #'attachment_ids': [(4, attachment.id) for attachment in token.attachment_ids],
    #     }
    #     mail = Mail.create(mail_values)
    #     mail.send()


    @http.route(['/services/<model("wq.services"):service>/registration/confirm'], type='http', auth="public", methods=['POST'], website=True)
    def registration_confirm(self, service, **post):
        cr, uid, context = request.cr, request.uid, request.context
        Tokens = request.registry['wq.services.tokens']
        Partner = request.registry['res.partner']

        vals = {'service_id': service.id}
        #partner Detail
        Partner_id = Partner.create(cr, SUPERUSER_ID, post, context=context)

        vals.update({'issued_to':Partner_id})
        Token_id = Tokens.create(cr, SUPERUSER_ID, vals ,context=context)
        token_name = Tokens.browse(cr, uid, Token_id, context=context)

        #send mail
        # self.send_mail(service,Partner_id,token_name)

        request.session['token_last_id'] = Token_id
        return request.website.render("website_wq.registration_complete", {'unique_token': token_name, 'service': service})
        
    @http.route(['/services/print'], type='http', auth="public", website=True)
    def print_token(self):
        cr, uid, context = request.cr, SUPERUSER_ID, request.context
        token_id = request.session.get('token_last_id')
        if token_id:
            pdf = request.registry['report'].get_pdf(cr, uid, [token_id], 'wq.report_token', data=None, context=context)
            pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
            return request.make_response(pdf, headers=pdfhttpheaders)
        else:
            return request.redirect('/services')


    @http.route(['/services/operator'], type='http', auth="public", website=True)
    def operator_view(self):
        return request.website.render("website_wq.operator", {'service': service})