# -*- coding: utf-8 -*-

{
    'name' : 'Modulo Aprendizaje',
    'version' : '1',
    'summary': 'Modulo para el Aprendizaje de la Programacion con Odoo',
    'sequence': 30,
    'description': """

    Puede Exir un Registro de Clientes/Proovedores con el nombre Escuela Comodin y este sera el que tome por defecto en la creación de Estudiantes.

    Para poder Facturar es necesario tener productos con la categoria Facturacion Colegiatura, de no hacerlo solo agregara Facturas Vacias.

    Para trabajar los reportes el modulo en Excel es necesario Instalar la libreri de python xlxswriter
        - sudo pip install xlxswriter
        - Documentacion: http://xlsxwriter.readthedocs.io/


    """,
    'author': 'German Ponce Dominguez',
    'category' : 'Customizaciones',
    'website': 'http://ww.argil.mx',
    'images' : [],
    'depends' : ['sale','account','stock','mail'],
    'data': [
        'academy.xml',
        'report/academy_report.xml',
        'wizard/academy_export.xml',
    ],
    'demo': [

    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
