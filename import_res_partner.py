#! /usr/bin/env python
# -*- coding: utf-8 -*-

#********************************************************#
# Importación Clientes y Proveedores                     #
#********************************************************#

import os
import csv
import xmlrpclib
import re


HOST='localhost'
PORT=8010
DB='femenina'
USER='admin'
PASS='Redesk2017'
url ='http://%s:%d/xmlrpc/' % (HOST,PORT)

common_proxy = xmlrpclib.ServerProxy(url+'common')
object_proxy = xmlrpclib.ServerProxy(url+'object')
uid = common_proxy.login(DB,USER,PASS)

def _create(estado):
    if estado is True:
        path_file = './ej.csv'
        archive = csv.DictReader(open(path_file))
        cont = 1

        for field in archive:
            print field
            vals = {'name': field['nombre'],'type': field['tipo_producto']}
            do_write = object_proxy.execute(DB,uid,PASS,'product.template','create',vals)
            if do_write:
                cont = cont + 1
                print "Contador:",cont
            else:
                print "Error"

def _update(estado):
    if estado is True:
        path_file = './ej.csv'
        archive = csv.DictReader(open(path_file))

        cont = 1
        # field['name'] captura valor del campo name solo si estas seguro q vendra un valor en el diccionario
        # field.get('name', False) captura el valor  y devuelve el segundo parametro en caso de no encontar
        for field in archive:
            print field
            vals = field['price1']
            product = object_proxy.execute(DB,uid,PASS,'product.template','search',[('name','=',field['name1'])])
            product_id = product and product[0]
            do_write = object_proxy.execute(DB,uid,PASS,'product.template', 'write', product_id, {'list_price': vals})
            if do_write:
                print "OK:",cont
            cont = cont + 1
            print "Contador:",cont


def _update_mass(estado):
    if estado is True:
        cont = 1

        product = object_proxy.execute(DB,uid,PASS,'product.template','search',[('active','=',True)])
        code_du = object_proxy.execute(DB,uid,PASS,'account.account','search',[('code','=','630000')])

        for id in product:
            do_write = object_proxy.execute(DB,uid,PASS,'product.template', 'write',id, {'property_account_expense_id':code_du[0]})
            if do_write:
                print "OK:",cont
            cont = cont + 1
            print "Contador:",cont

def __main__():
    print 'Ha comenzado el proceso'
    _create(False)
    _update(True)
    _update_mass(True)
    print 'Ha finalizado la carga tabla'
__main__()





# for row in reader:
#         print row[1]
#         statement = "INSER INTO product_template(name,standar_price,list_price,mes_type,uom_id,iom_po_id," \
#                     "type,procure_method,cost_method,categ_id,supply_method,sale_ok)" \
#                     "VALUES('"+row[1]+"',"+str(row[2])+","+ str(row[2])+",'fixed',1,1,'product','make_to_stock','standard',1,'buy',True) RETURNING id"
#
#         cursor.execute(statement)
#         conn.commit()
#         templateid=cursor.fetchone()[0]
#
#         statement="INSERT INTO product_product(product_tmpl_id,default_code,active,valuation) VALUES" \
#                   "("+ str(templateid) + ",'" + row[0] + "',True,'manual_periodic')"
#
#         cursor.execute(statement)
#         conn.commit()