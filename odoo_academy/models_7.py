# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

# class stock_warehouse(osv.osv):
#     _name = 'stock.warehouse'
#     # _inherit = ['mail.thread', 'ir.needaction_mixin','stock.warehouse']

#     def create(self, cr, uid, vals, context=None):
#         print "############ VALS >>>> ", vals
#         res = super(stock_warehouse, self).create(cr, uid, vals, context)
#         return res

class academy_rev(osv.osv):
    _name = 'academy.rev'
    _description = 'Descripcion del Modelo'
    _columns = {
        'name':fields.boolean('Label', required=False), 
    }

    def _check_invoices(self, cr, uid, automatic=False, use_new_cursor=False, context=None):
        print "#### SE ESTA EJECUTANDO >>>> "
        print "#### SE ESTA EJECUTANDO >>>> "
        cr.execute("""
            select id from academy_student 
                where id in 
                (select student_id from student_invoice_rel);
            """)
        cr_res = cr.fetchall()
        student_ids = [x[0] for x in cr_res if x]
        student_ids = self.pool.get('academy.student').search(
            cr, uid, [('invoiced','=',False),('id','in',tuple(student_ids))])
        print "#### SUTDENT IDS >>> ", student_ids
        self.pool.get('academy.student').write(cr, uid, student_ids,
                            {'invoiced':True})
        

        return True

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
            if rec.calificacion < 5 or rec.calificacion > 10:
                return False
        return True

    _constraints = [(_check_calificacion, 
        'Error: La Calificacion Minima debe ser de 5 puntos y Menor o igual a 10.', ['calificacion']), ] 

class academy_materia(osv.osv):
    _name = 'academy.materia'
    _description = 'Materias del Estudiante'
    _columns = {
        'name': fields.char('Nombre'),
    }
    _sql_constraints = [('name_uniq', 'unique (name)', 
        'El nombre de la Materia debe ser unico!'),]

