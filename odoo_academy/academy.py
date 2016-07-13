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
    name = fields.Char('Nombre', size=128, required=True)
    last_name = fields.Char('Apellido', size=128)
    photo = fields.Binary('Fotografia')
    create_date = fields.Datetime('Fecha Creacion', readonly=True)
    notes =  fields.Html('Comentarios')
    active = fields.Boolean('Activo')
    state = fields.Selection([('draft','Documento Borrador'),
                              ('progress','Progeso'),
                              ('done','Egresado'),], 'Estado')
    age  = fields.Integer('Edad', required=True)
    curp = fields.Char('CURP', size=18)

    ### Relacionales ###
    partner_id = fields.Many2one('res.partner', 'Escuela')
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
        print "#### SELF", self
        print "#### SELF ", self.env
        if len(self.curp) < 18:
            raise ValidationError(_('CURP debe contener 18 Caracteres.'))

    _order = 'name'

    _defaults = {  
        'active': True,
        'state': 'draft',

        }

    #### METODO ESCRITURA self, cr, uid, ids, {}, context
    @api.multi
    def write(self, values):
        print "#### VALUES >>>> ", values
        if 'curp' in values:
            values.update({
                'curp':values['curp'].upper(),
                })
        result = super(academy_student, self).write(values)
        return result

    @api.model
    def create(self, values):
        res = super(academy_student, self).create(values)
        print "###### RES >>>> ", res
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
        partner_ids = partner_obj.search([('student_id','=',self.id)])
        print "#### PARTNER IDS >>>> ", partner_ids
        if partner_ids:
            for partner in partner_ids:
                partner.unlink()
        res = super(academy_student, self).unlink()
        return res