# -*- coding: utf-8 -*-
print("module [backend.api_export] loaded")


from backend import app, manager, check_token, check_permission
from backend.api_common import validate_token
from flask import make_response, jsonify, request, json, Response
from backend_model.table_export import *
from flask_restful import reqparse
from urllib.parse import quote
from backend_lib.lib_export import LibExportSalesOrder, LibExportSalesOrderItem, LibExportCommInvoice, LibExportCommInvoiceItem
from backend_lib.lib_excel import sample_excel, import_excel, parse_excel, ImportExcelException

db = DBManager.db
# REST API(s) available :
#  - /api/v1/login
#  - /api/v1/logout

manager.create_api(ExportSalesOrder,
                   url_prefix='/api/mes/v1/export',
                   collection_name='sales_order',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibExportSalesOrder.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(ExportSalesOrderItem,
                   url_prefix='/api/mes/v1/export',
                   collection_name='sales_order_item',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibExportSalesOrderItem.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   },
                   postprocessors={
                       'POST': [LibExportSalesOrderItem.post_postprocessor],
                   })

manager.create_api(ExportCommInvoice,
                   url_prefix='/api/mes/v1/export',
                   collection_name='comm_invoice',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibExportCommInvoice.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })

manager.create_api(ExportCommInvoiceItem,
                   url_prefix='/api/mes/v1/export',
                   collection_name='comm_invoice_item',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibExportCommInvoiceItem.post_preprocessor],
                       'PATCH_SINGLE': [check_token, LibExportCommInvoiceItem.patch_single_preprocessor],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   },
                   postprocessors={
                       'POST': [LibExportCommInvoiceItem.post_postprocessor],
                       'PATCH_SINGLE': [LibExportCommInvoiceItem.patch_single_postprocessor]
                   })


@app.route("/api/mes/v1/export-update-assign-quantity", methods=["POST"])
def export_update_stock():
    parser = reqparse.RequestParser()
    parser.add_argument("order_item_id", type=int, location="json")
    parser.add_argument("item_code", type=str, location="json")
    parser.add_argument("warehouse", type=str, location="json")
    args = parser.parse_args()

    LibExportSalesOrderItem.sales_order_update_assign_quantity(args['order_item_id'], args['item_code'], args['warehouse'])

    return make_response('success', 200)


# @app.route("/api/mes/v1/export/sales-order/export/comm-invoice", methods=["POST"])
# def shipment_order_export_to_release():
#     """
#     수출관리 - 수주를 출고로 보내기
#     :return:
#     """
#     parser = reqparse.RequestParser()
#     parser.add_argument("order_id", type=int, location="json")
#     args = parser.parse_args()

#     order = db.session.query(
#         ExportSalesOrder
#     ).filter(
#         ExportSalesOrder.id == args['order_id']
#     ).first()
#     if order:
#         order_items = db.session.query(
#             ExportSalesOrderItem
#         ).filter(
#             ExportSalesOrderItem.fk_export_sales_order_id == args['order_id']
#         ).filter(
#             ExportSalesOrderItem.not_shipped > 0
#         ).all()
#         if len(order_items) == 0:
#             from backend_lib.lib_exception import MesException
#             MesException.raise_not_add_item()
#         if len(order_items) > 0:
#             import datetime
#             from backend_lib.lib_common import LibCommon

#             data = {'fk_company_id': order.fk_company_id}
#             LibCommon.get_item_number(data, 'release_number', ShipmentRelease, ShipmentRelease.release_number,
#                                       '/shipment/release', 'RELEASE')

#             from backend_lib.lib_base import LibBaseCode
#             release_type = LibBaseCode.get_first_code_name('출고구분')

#             release = ShipmentRelease()
#             release.release_number = data['release_number']
#             release.release_date = datetime.datetime.now()
#             release.client_company = order.client_company
#             release.client_manager = order.client_manager
#             release.release_department = order.order_department
#             release.release_manager = order.order_manager
#             release.release_type = release_type
#             release.vat_type = order.vat_type
#             release.payment_terms = order.payment_terms
#             release.delivery_date = order.delivery_date
#             release.delivery_place = order.delivery_place
#             release.fk_project_management_id = order.fk_project_management_id
#             release.end_user = order.end_user
#             release.note = order.note
#             release.etc = order.etc
#             release.supply_price = order.supply_price
#             release.vat = order.vat
#             release.total_price = order.total_price
#             release.fk_company_id = order.fk_company_id
#             db.session.add(release)

#             order.release_number = release.release_number
#             db.session.commit()

#             for order_item in order_items:
#                 release_item = ShipmentReleaseItem()
#                 release_item.item_code = order_item.item_code
#                 release_item.order_quantity = order_item.order_quantity
#                 release_item.release_quantity = order_item.assign_quantity
#                 release_item.unit_price = order_item.unit_price
#                 release_item.supply_price = order_item.assign_quantity * order_item.unit_price
#                 release_item.request_delivery_date = order_item.request_delivery_date
#                 release_item.non_invoice = order_item.assign_quantity
#                 release_item.warehouse_code = order_item.warehouse_code
#                 release_item.order_number = order.order_number
#                 release_item.client_item_number = order_item.client_item_number
#                 release_item.note = order_item.note
#                 release_item.fk_project_management_id = order_item.fk_project_management_id
#                 release_item.fk_release_id = release.id
#                 release_item.fk_order_item_id = order_item.id
#                 db.session.add(release_item)

#                 order_item.not_shipped = order_item.not_shipped - order_item.assign_quantity
#                 order_item.assign_quantity = 0
#                 db.session.commit()

#                 from backend_lib.lib_setup import LibSetupBasicStock
#                 LibSetupBasicStock.update_stock_by_item_code(release_item.item_code, release_item.warehouse_code)

#     return make_response('success', 200)


@app.route('/api/mes/v1/excel/export/sales_order', methods=['GET'])
def sales_order_excel_sample():
    io = sample_excel(ExportSalesOrderItem)
    content = io.getvalue()
    encoded = quote('SalesOrderSample')

    return Response(
        content,
        mimetype='application/octet-stream',
        headers={'Content-Disposition': 'attachment;filename={}.xlsx'.format(encoded)})


@app.route('/api/mes/v1/excel/export/sales_order', methods=['POST'])
def sales_order_excel_import():
    token = request.headers.get('token')

    if token is None:
        return make_response('Not Authorized', 410)

    user = validate_token(token)
    exc = check_permission(user, method='EXCEL')
    if exc is not None:
        return make_response(exc.description, exc.code)

    f = request.files['file']
    if f is None:
        return make_response('require parameter is missing', 400)

    filepath, ext = f.filename.rsplit('.', 1)
    if ext not in ['xlsx']:
        return make_response('invalid file extension', 400)

    f.seek(0)
    # 모든 행 공통 데이터
    common_values = dict(
        fk_company_id=user.fk_company_id,
        register_id=user.user_id,
        warehouse_code='본사창고'
    )

    try:
        result = dict()
        result['objects'] = parse_excel(table=ExportSalesOrderItem, common_values=common_values, file=f)
        return make_response(jsonify(result), 200)
    except ImportExcelException as e:
        print(e)
        result = '데이터를 불러오는 중 에러가 발생하였습니다'
        if e.message is not None:
            result = e.message

        return make_response(result, 400)


