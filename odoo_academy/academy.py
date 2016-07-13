# -*- coding: utf-8 -*-

from openerp import models, fields, api

class res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    is_school = fields.Boolean('Escuela')
    company_type = fields.Selection([('person', 'Individual'),
                       ('company', 'Compañia'),
                       ('is_school','Escuela')],
            string='Company Type',
            help='Technical field, used only to display a boolean using a radio '
                 'button. As for Odoo v9 RadioButton cannot be used on boolean '
                 'fields, this one serves as interface. Due to the old API '
                 'limitations with interface function field, we implement it '
                 'by hand instead of a true function field. When migrating to '
                 'the new API the code should be simplified.')


class academy_student(models.Model):
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

    ### Relacionales ###
    partner_id = fields.Many2one('res.partner', 'Escuela')


    _order = 'name'

    _defaults = {  
        'active': True,
        'state': 'draft',

        }