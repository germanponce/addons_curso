# -*- coding: utf-8 -*-

{
    'name' : 'Modulo Aprendizaje',
    'version' : '1',
    'summary': 'Modulo para el Aprendizaje de la Programacion con Odoo',
    'sequence': 30,
    'description': """

    Puede Exir un Registro de Clientes/Proovedores con el nombre Escuela Comodin y este sera el que tome por defecto en la creación de Estudiantes.

    Para poder Facturar es necesario tener productos con la categoria Facturacion Colegiatura.

    """,
    'category' : 'Customizaciones',
    'website': 'http://ww.argil.mx',
    'images' : [],
    'depends' : ['sale','account','stock','mail'],
    'data': [
        'academy.xml',
    ],
    'demo': [

    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
