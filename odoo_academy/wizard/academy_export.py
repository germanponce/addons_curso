# -*- encoding: utf-8 -*-

from openerp import models, fields, api, _

from openerp.tools.translate import _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp import SUPERUSER_ID

from datetime import datetime

import base64
####### TRABAJAR CON LOS EXCEL
import xlsxwriter

import tempfile

##### SOLUCIONA CUALQUIER ERROR DE ENCODING (CARACTERES ESPECIALES)
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

class export_invoices_school_report(models.Model):
    _name = 'export.invoices.school.report'
    _description = 'Exportar Reporte a Excel o CSV'
    
    datas_fname = fields.Char('File Name',size=256)
    file = fields.Binary('Layout')
    download_file = fields.Boolean('Descargar Archivo')
    cadena_decoding = fields.Text('Binario sin encoding')
    type = fields.Selection([('csv','CSV'),('xlsx','Excel')], 'Tipo Exportacion', 
                            required=False, )


    _defaults = {
        'download_file': False,
        'type': 'csv',
        }

    @api.multi
    def export_csv_file(self,):
        document_csv = ""
        date = datetime.now().strftime('%d-%m-%Y')
        datas_fname = "Reporte Facturacion de Escuelas "+str(date)+".csv" # Nombre del Archivo
        sl = "\n"
        document_csv = document_csv+"Reporte General de Facturacion de Escuelas y Estudiantes"

        self.env.cr.execute("""
            select partner_id from academy_student
                group by partner_id;
            """)
        cr_res = self.env.cr.fetchall()
        if not cr_res:
            return {}
        partner_list_ids  =[x[0] for x in cr_res if x]

        partner_obj = self.env['res.partner']

        partner_search = partner_obj.search([('id','in',tuple(partner_list_ids))])

        for partner in partner_search:
            self.env.cr.execute("""
                select sum(amount_invoice) from academy_student
                    where partner_id = %s;
                """, (partner.id,))
            cr_res = self.env.cr.fetchall()
            if not cr_res:
                amount_invoice = 0.0
            else:
                amount_invoice = cr_res[0][0]
            cabeceras_1 = sl+"Escuela"+","+"Monto Facturado"
            document_csv = document_csv+sl+cabeceras_1
            document_csv = document_csv+sl+partner.name+","+str(amount_invoice)+sl

            cabeceras_2 = "Estudiante"+","+"Edad"+","+"Monto Facturado"
            document_csv = document_csv+sl+cabeceras_2
            student_obj = self.env['academy.student']
            student_ids = student_obj.search([('partner_id','=',partner.id)])
            if student_ids:
                for student in student_ids:
                    vals = sl+str(student.name)+" "+str(student.last_name)+","+str(student.age)+","+str(student.amount_invoice)+sl
                    document_csv=document_csv+sl+vals
                    document_csv = document_csv+sl+"Facturas del Estudiante"+sl

                    cabeceras_3 = "Folio"+","+"Fecha"+","+"Monto"
                    document_csv = document_csv+sl+cabeceras_3
                    for factura in student.invoice_ids:
                        vals2 = str(factura.number)+","+str(factura.date_invoice if factura.date_invoice else "")+","+str(factura.amount_total)
                        document_csv = document_csv+sl+vals2

        self.write({'cadena_decoding':document_csv,
            'datas_fname':datas_fname,
            'file':base64.encodestring(document_csv),
            'download_file': True})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'export.invoices.school.report',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
            }

    @api.multi
    def export_xlsx_file(self,):
        fname=tempfile.NamedTemporaryFile(suffix='.xlsx',delete=False)

        workbook = xlsxwriter.Workbook(fname)
        worksheet = workbook.add_worksheet()

        # Widen the first column to make the text clearer.
        worksheet.set_column('A:K', 20)

        # Add a bold format to use to highlight cells.
        #### ESTILOS DE CELDAS #####
        money = workbook.add_format({'num_format': '$#,##0'})
        money.set_align('right')

        bold = workbook.add_format({'bold': True})
        format_red = workbook.add_format({'bold': True})

        format_red.set_bg_color('#830000')
        format_red.set_align('center')
        format_red.set_font_color('white')

        format_red_big = workbook.add_format({'bold': True})
        format_red_big.set_bg_color('#830000')
        format_red_big.set_font_size(12)
        format_red_big.set_font_color('white')

        format_black = workbook.add_format({'bold': True})

        format_black.set_bg_color('#000000')
        format_black.set_align('right')
        format_black.set_font_color('white')

        format_gray = workbook.add_format({'bold': True})
        format_gray.set_font_size(12)
        format_gray.set_bg_color('#7A6E6E')

        format_gray_right = workbook.add_format({'bold': True})

        format_gray_right.set_bg_color('#DADEDA')
        format_gray_right.set_align('right')

        self.env.cr.execute("""
            select partner_id from academy_student;
            """)
        cr_res = self.env.cr.fetchall()
        if not cr_res:
            return {}
        school_ids = [x[0] for x in cr_res if x]
        partner_obj = self.env['res.partner']
        a = 1
        b = 1
        for partner in partner_obj.browse(school_ids):
            worksheet.write('A%s' %a, 'Escuela', format_red)
            worksheet.write('B%s' %b, 'Total Facturacion', format_red)
            a +=1
            b+=1
            self.env.cr.execute("""
                select sum(amount_invoice) from academy_student
                    where partner_id=%s
                """,(partner.id,))
            cr_res = self.env.cr.fetchall()
            if cr_res:
                amount_invoice = cr_res[0][0]
            else:
                amount_invoice = 0.0

            worksheet.write('A%s' % a, partner.name)
            worksheet.write('B%s' % b, float(amount_invoice), money)
            student_ids = []
            self.env.cr.execute("""
                select id from academy_student where partner_id=%s
                """,(partner.id,))
            cr_res = self.env.cr.fetchall()
            student_ids = [x[0] for x in cr_res]
            a+=2
            b+=2
            c=a
            worksheet.write('A%s' % a, 'Estudiante',format_gray)
            worksheet.write('B%s' % b, 'CURP',format_gray)
            worksheet.write('C%s' % c, 'Monto Facturado',format_gray)
            a+=1
            b+=1
            c+=1
            for student in self.env['academy.student'].browse(student_ids):
                worksheet.write('A%s' % a, student.name+" "+student.last_name)
                worksheet.write('B%s' % b, student.curp)
                worksheet.write('C%s' % c, float(student.amount_invoice), money)
                a+=2
                b+=2
                c+=2
                worksheet.write('A%s' % a, "Facturas",format_red)
                a+=1
                b+=1
                c+=1
                worksheet.write('A%s' % a, "Folio", format_gray)
                worksheet.write('B%s' % b, "Fecha", format_gray)
                worksheet.write('C%s' % c, "Monto", format_gray)
                a+=1
                b+=1
                c+=1

                for factura in student.invoice_ids:
                    worksheet.write('A%s' % a, str(factura.number))
                    worksheet.write('B%s' % b, str(factura.date_invoice))
                    worksheet.write('C%s' % c, float(factura.amount_total), money)
                    a+=1
                    b+=1
                    c+=1
        workbook.close()
        f = open(fname.name, "r")
        data = f.read()
        f.close()

        date = datetime.now().strftime('%d-%m-%Y')
        datas_fname = "Reporte Facturacion de Escuelas "+str(date)+".xlsx" # Nombre del Archivo
        
        self.write({'cadena_decoding':"",
            'datas_fname':datas_fname,
            'file':base64.encodestring(data),
            'download_file': True})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'export.invoices.school.report',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
            }

    @api.multi
    def process_export(self,):
        if self.type == 'csv':
            result = self.export_csv_file()
            return result
        else:
            result = self.export_xlsx_file()
            return result
        return True
