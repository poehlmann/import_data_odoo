#! /usr/bin/env python
# -*- coding: utf-8 -*-

# ********************************************************#
# Importación Productos#
# ********************************************************#

import csv
import xmlrpclib

# HOST='192.168.20.87'
# PORT=80
# DB='roghurv01.redeskbolivia.com'
# USER='bruno.poehlmann@gmail.com'
# PASS='admin'
# url ='http://%s:%d/xmlrpc/' % (HOST,PORT)

HOST = 'localhost'
PORT = 8010
DB = 'femenina'
USER = 'admin'
PASS = 'Redesk2017'
url = 'http://%s:%d/xmlrpc/' % (HOST, PORT)

common_proxy = xmlrpclib.ServerProxy(url + 'common')
object_proxy = xmlrpclib.ServerProxy(url + 'object')
uid = common_proxy.login(DB, USER, PASS)


def _verify(data, table, types, ids):
    # category_model = object_proxy.get_model("product.public.category")
    # ids = category_model.search([("name", "=", category)])
    args = [('name', '=', str(data))]  # query clause
    id = object_proxy.execute(DB, uid, PASS, table, 'search', args)
    if types == 'attribute':
        if id:
            return id
        else:
            vals_attribute = {'name': data, 'type': 'select', 'create_variant': True}
            val = object_proxy.execute(DB, uid, PASS, table, 'create', vals_attribute)
            return [val]
    elif types == 'attribute_val':
        if id:
            return id
        else:
            vals_attribute_val = {'name': data, 'attribute_id': ids}
            val = object_proxy.execute(DB, uid, PASS, table, 'create', vals_attribute_val)
            return [val]
    elif types == 'search_category':
        args = [('id', '=', ids)]
        id = object_proxy.execute(DB, uid, PASS, table, 'search', args)
        vals_product_subcategory = {'parent_id': id[0], 'name': data}
        val = object_proxy.execute(DB, uid, PASS, table, 'create', vals_product_subcategory)
        return [val]
    else:
        if id:
            return id
        else:
            vals_product_category = {'name': data}
            val = object_proxy.execute(DB, uid, PASS, table, 'create', vals_product_category)
            return [val]


def _create(estado):
    global id_product_template, id_product_category
    if estado is True:
        path_file = './GBS.csv'
        archive = csv.DictReader(open(path_file))
        cont = 1

        for field in archive:
            id_category = _verify(field['categoria'], 'product.public.category', '', 0)

            id_subcategory = _verify(field['subcategoria'], 'product.public.category', 'search_category', id_category)

            id_brand = _verify(field['Marca'], 'product.brand', '', 0)

            if (id_subcategory != ''):
                id_category = id_subcategory

            vals_product_template = {'product_brand_id': id_brand[0], 'public_categ_ids': [(6, 0, id_category)],
                                     'name': field['Modelo'], 'standar_price': field['precio'],
                                     'list_price': field['precio'],
                                     'mes_type': 'fixed', 'uom_id': 1, 'iom_po_id': 1, 'type': 'product',
                                     'procure_method': 'make_to_stock', 'cost_method': 'standard',
                                     'supply_method': 'buy',
                                     'sale_ok': True, 'website_published': 1, 'x_idroghur': field['id']}

            product = object_proxy.execute(DB, uid, PASS, 'product.template', 'search',
                                           [('x_idroghur', '=', field['id'])])

            if product:
                product_id = product and product[0]
                do_write = object_proxy.execute(DB, uid, PASS, 'product.template', 'write', product_id,
                                                vals_product_template)
            else:
                id_product_template = object_proxy.execute(DB, uid, PASS, 'product.template', 'create',
                                                           vals_product_template)
                id_attribute = _verify('Potencia (W)', 'product.attribute', 'attribute', 0)
                id_attribute_val = _verify(field['Potencia (W)'], 'product.attribute.value', 'attribute_val',
                                           id_attribute[0])

                product_attribute_line = object_proxy.execute(DB, uid, PASS,
                                                              'product.attribute.line', 'create',
                                                              {'product_tmpl_id': id_product_template,
                                                               'attribute_id': id_attribute[0],
                                                               'value_ids': [[6, 0, id_attribute_val]]
                                                               })
                if id_product_template:
                    cont += 1
                else:
                    print "Error"


# def _update(estado):
#     if estado is True:
#         path_file = './ej.csv'
#         archive = csv.DictReader(open(path_file))
#
#         cont = 1
#         # field['name'] captura valor del campo name solo si estas seguro q vendra un valor en el diccionario
#         # field.get('name', False) captura el valor  y devuelve el segundo parametro en caso de no encontar
#         for field in archive:
#             print field
#             vals = field['price']
#             product = object_proxy.execute(DB,uid,PASS,'product.template','search',[('name','=',field['name1'])])
#             product_id = product and product[0]
#             do_write = object_proxy.execute(DB,uid,PASS,'product.template', 'write', product_id, {'list_price': vals})
#             if do_write:
#                 print "OK:",cont
#             cont = cont + 1
#             print "Contador:",cont
#
#
# def _update_mass(estado):
#     if estado is True:
#         cont = 1
#
#         product = object_proxy.execute(DB,uid,PASS,'product.template','search',[('active','=',True)])
#         code_du = object_proxy.execute(DB,uid,PASS,'account.account','search',[('code','=','630000')])
#
#         for id in product:
#             do_write = object_proxy.execute(DB,uid,PASS,'product.template', 'write',id, {'property_account_expense_id':code_du[0]})
#             if do_write:
#                 print "OK:",cont
#             cont = cont + 1
#             print "Contador:",cont
#
def __main__():
    print 'Ha comenzado el proceso'
    _create(True)
    # _update(True)
    # _update_mass(True)
    print 'Ha finalizado la carga tabla'


__main__()
