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
