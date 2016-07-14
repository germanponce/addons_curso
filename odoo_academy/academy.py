# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import UserError, RedirectWarning, ValidationError


class res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    # is_school = fields.Boolean('Escuela')
    company_type = fields.Selection([('person', 'Individual'),
                       ('company', 'Compañia'),
                       ('is_school','Escuela'),
                       ('student','Estudiante')],
            string='Company Type',
            help='Technical field, used only to display a boolean using a radio '
                 'button. As for Odoo v9 RadioButton cannot be used on boolean '
                 'fields, this one serves as interface. Due to the old API '
                 'limitations with interface function field, we implement it '
                 'by hand instead of a true function field. When migrating to '
                 'the new API the code should be simplified.')
    student_id = fields.Many2one('academy.student', 'Estudiante')

class academy_student(models.Model):
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _name = 'academy.student'
    _description = 'Modelo de Formulario para Estudiantes'

    @api.model
    def _get_school_default(self):
        print "#### SCHOOL METODO"
        print "#### SCHOOL METODO"
        print "#### SCHOOL METODO"
        partner_obj = self.env['res.partner']
        school_id = partner_obj.search([('name','=','Escuela Comodin')])
        print "##### SCHOOL IDS >>> ", school_id
        return school_id

    name = fields.Char('Nombre', size=128, required=True, )
    last_name = fields.Char('Apellido', size=128)
    photo = fields.Binary('Fotografia')
    create_date = fields.Datetime('Fecha Creacion', readonly=True)
    notes =  fields.Html('Comentarios')
    active = fields.Boolean('Activo')
    state = fields.Selection([('draft','Documento Borrador'),
                              ('progress','Progeso'),
                              ('done','Egresado'),], 'Estado', default="draft")
    age  = fields.Integer('Edad', required=True)
    curp = fields.Char('CURP', size=18)

    ### Relacionales ###
    partner_id = fields.Many2one('res.partner', 'Escuela', default=_get_school_default, copy=False)
    calificaciones_ids = fields.One2many('academy.calificacion','student_id',
        'Calificaciones')
    country = fields.Many2one('res.country', 'Pais',
                                related='partner_id.country_id', readonly=True)

    invoice_ids = fields.Many2many('account.invoice',
                                    'student_invoice_rel',
                                    'student_id','invoice_id',
                                    'Facturas')

    @api.constrains('curp')
    @api.one
    def _check_curp(self):
        if len(self.curp) < 18:
            raise ValidationError(_('CURP debe contener 18 Caracteres.'))

    _order = 'name'

    _defaults = {  
        'active': True,
        }

    #### METODO ESCRITURA self, cr, uid, ids, {}, context
    @api.multi
    def write(self, values):
        if 'curp' in values:
            values.update({
                'curp':values['curp'].upper(),
                })
        result = super(academy_student, self).write(values)
        return result

    @api.model
    def create(self, values):
        exist_ids = []
        if values['name']:
            nombre = values['name']
            exist_ids = self.env['academy.student'].search([('name','=',nombre)])
            new_name = values['name']+" (Copia)" if exist_ids else values['name']            
            values['name'] = new_name

        res = super(academy_student, self).create(values)
        res.name = new_name
        partner_obj = self.env['res.partner']

        vals_to_partner = {
                'name': res.name+" "+res.last_name,
                'company_type': 'student',
                'student_id': res.id,
                'customer': True,
                }
        partner_obj.create(vals_to_partner)
        return res

    @api.multi
    def unlink(self):
        partner_obj = self.env['res.partner']
        print "### SELF ID >>> ", self.ids
        partner_ids = partner_obj.search([('student_id','in',self.ids)])
        print "#### PARTNER IDS >>>> ", partner_ids
        if partner_ids:
            for partner in partner_ids:
                print "### PARTNER >>>> ", partner
                partner.unlink()
        ##### Utilizando SQL directo en Odoo ####
        # self.env.cr("""
        #     select id from res_partner where student_id=%s
        #     """ % self.id)
        # cr_res = cr.fetchall()
        # if cr_res:
        #     partner_ids = [x[0] for x in cr_res if x]
        #########################################
        res = super(academy_student, self).unlink()
        return res