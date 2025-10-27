# -*- coding: utf-8 -*-
from flask import make_response, jsonify, json, request
from backend_model.database import DBManager
from backend import app
from zeep.helpers import serialize_object
import os

from backend import manager
from backend_lib.lib_barobill import *

print("module [backend.api_barobill] loaded")
db = DBManager.db


@app.route('/api/mes/v1/barobill/invoice', methods=['POST'])
def route_post_invoice():
    payload = json.loads(request.data)

    invoice = Invoice()
    invoice.InvoicerParty.MgtNum = payload['InvoicerParty']['MgtNum']
    invoice.InvoicerParty.CorpNum = payload['InvoicerParty']['CorpNum']
    invoice.InvoicerParty.CorpName = payload['InvoicerParty']['CorpName']
    invoice.InvoicerParty.CEOName = payload['InvoicerParty']['CEOName']
    invoice.InvoicerParty.Addr = payload['InvoicerParty']['Addr']
    invoice.InvoicerParty.ContactID = payload['InvoicerParty']['ContactID']
    invoice.InvoicerParty.ContactName = payload['InvoicerParty']['ContactName']
    invoice.InvoicerParty.TEL = payload['InvoicerParty']['TEL']
    invoice.InvoicerParty.HP = payload['InvoicerParty']['HP']
    invoice.InvoicerParty.Email = payload['InvoicerParty']['Email']
    invoice.InvoicerParty.BizClass = payload['InvoicerParty']['BizClass']
    invoice.InvoicerParty.BizType = payload['InvoicerParty']['BizType']

    invoice.InvoiceeParty.CorpNum = payload['InvoiceeParty']['CorpNum']
    invoice.InvoiceeParty.CorpName = payload['InvoiceeParty']['CorpName']
    invoice.InvoiceeParty.CEOName = payload['InvoiceeParty']['CEOName']
    invoice.InvoiceeParty.Addr = payload['InvoiceeParty']['Addr']
    invoice.InvoiceeParty.ContactName = payload['InvoiceeParty']['ContactName']
    invoice.InvoiceeParty.TEL = payload['InvoiceeParty']['TEL']
    invoice.InvoiceeParty.Email = payload['InvoiceeParty']['Email']
    invoice.InvoiceeParty.BizClass = payload['InvoiceeParty']['BizClass']
    invoice.InvoiceeParty.BizType = payload['InvoiceeParty']['BizType']

    invoice.PurposeType = payload['PurposeType']
    invoice.AmountTotal = payload['AmountTotal']
    invoice.TaxTotal = payload['TaxTotal']
    invoice.TotalAmount = payload['TotalAmount']
    
    if 'Remark1' in payload:
        invoice.Remark1 = payload['Remark1']
    else:
        invoice.Remark1 = ''

    if 'WriteDate' in payload:
        invoice.WriteDate = payload['WriteDate']

    if 'IssueDirection' in payload:
        invoice.IssueDirection = payload['IssueDirection']

    if 'TaxCalcType' in payload:
        invoice.TaxCalcType = payload['TaxCalcType']

    if 'TaxType' in payload:
        invoice.TaxType = payload['TaxType']

    for item in payload['TaxInvoiceTradeLineItems']:
        invoice.set_items(item)

    return_value = invoice.register_and_issue()

    result = dict()
    result['data'] = return_value
    if return_value == 1:
        result['success'] = True
        result['error_message'] = None
    else:
        result['success'] = False
        result['error_message'] = get_error_string(return_value)

    return make_response(jsonify(result), 200)


@app.route('/api/mes/v1/barobill/invoice/<mgt_num>', methods=['GET'])
def route_get_invoice(mgt_num):
    invoice = get_invoice(mgt_num)

    result = dict()
    result['success'] = True
    result['error_message'] = None
    result['data'] = serialize_object(invoice, dict)

    if invoice['TaxInvoiceType'] < 0:
        result['success'] = False
        result['error_message'] = get_error_string(invoice['TaxInvoiceType'])

    return make_response(jsonify(result), 200)


@app.route('/api/mes/v1/barobill/state/<mgt_num>/<proc_type>', methods=['PATCH'])
def route_proc_invoice(mgt_num, proc_type):
    payload = json.loads(request.data)
    memo = payload['memo'] if 'memo' in payload else ''
    return_value = proc_invoice(mgt_num, proc_type, memo)

    result = dict()
    result['data'] = return_value
    if return_value > 0:
        result['success'] = True
        result['error_message'] = None
    else:
        result['success'] = False
        result['error_message'] = get_error_string(return_value)

    return make_response(jsonify(result), 200)


@app.route('/api/mes/v1/barobill/state/<mgt_num>', methods=['DELETE'])
def route_delete_invoice(mgt_num):
    return_value = delete_invoice(mgt_num)
    result = dict()
    result['data'] = return_value
    if return_value > 0:
        result['success'] = True
        result['error_message'] = None
    else:
        result['success'] = False
        result['error_message'] = get_error_string(return_value)
    return make_response(jsonify(result), 200)


@app.route('/api/mes/v1/barobill/state/<mgt_num>', methods=['GET'])
def route_get_invoice_state(mgt_num):
    state = get_invoice_state(mgt_num)

    result = dict()
    result['success'] = True
    result['error_message'] = None
    result['data'] = serialize_object(state[0], dict)

    if state[0]['BarobillState'] < 0:
        result['success'] = False
        result['error_message'] = get_error_string(state[0]['BarobillState'])

    return make_response(jsonify(result), 200)


@app.route('/api/mes/v1/barobill/popup/invoice', methods=['POST'])
def route_popup_invoice():
    payload = json.loads(request.data)
    url = get_invoice_popup_url(payload['MgtNum'], payload['ContactID'])

    result = dict()
    result['success'] = True
    result['error_message'] = None
    result['data'] = url

    if url.startswith('-'):
        result['success'] = False
        result['error_message'] = get_error_string(url)

    return make_response(jsonify(result), 200)
