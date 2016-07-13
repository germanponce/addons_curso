# -*- coding: utf-8 -*-

from openerp import models, fields, api

class academy_student(models.Model):
    _name = 'academy.student'
    _description = 'Modelo de Formulario para Estudiantes'
    name = fields.Char('Nombre', size=128)
    last_name = fields.Char('Apellido', size=128)
    photo = fields.Binary('Fotografia')
    create_date = fields.Datetime('Fecha Creacion', readonly=True)

    _order = 'name'