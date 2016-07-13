# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class academy_califiacion(osv.osv):
    _name = 'academy.calificacion'
    _description = 'Calificaciones del Estudiante'
    _columns = {
        'name': fields.many2one('academy.materia', 'Materia'),
        'calificacion': fields.float('Calificacion', digits=(3,2)),
        'student_id': fields.many2one('academy.student',
            'ID Ref'),
    }
    
    def _check_calificacion(self, cr, uid, ids, context=None): 
        for rec in self.browse(cr, uid, ids, context):
            print "############ rec.calificacion ",rec.calificacion
            if rec.calificacion < 5:
                return False
        return True

    _constraints = [(_check_calificacion, 
        'Error: La Calificacion Minima debe ser de 5 puntos', ['calificacion']), ] 

class academy_materia(osv.osv):
    _name = 'academy.materia'
    _description = 'Materias del Estudiante'
    _columns = {
        'name': fields.char('Nombre')
    }
    _sql_constraints = [('name_uniq', 'unique (name)', 
        'El nombre de la Materia debe ser unico!'),]

