# -*- coding: utf-8 -*-
import json

print("module [backend.api_shipment] loaded")


from backend import app, manager
from backend import check_token
from backend_model.database import DBManager
from backend_model.table_shipment import *
from backend_lib.lib_shipment import *
from flask import request, make_response, Response, jsonify
from flask_restful import reqparse
from datetime import datetime, timedelta

db = DBManager.db
# REST API(s) available :
#  - /api/v1/login
#  - /api/v1/logout


manager.create_api(ShipmentQuote,
                   url_prefix='/api/mes/v1/shipment',
                   collection_name='quote',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibShipmentQuote.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   },
                   postprocessors={
                       'POST': [LibShipmentQuote.post_postprocessor]
                   })


manager.create_api(ShipmentQuoteItem,
                   url_prefix='/api/mes/v1/shipment',
                   collection_name='quote_item',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibShipmentQuoteItem.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token, LibShipmentQuoteItem.delete_single_preprocessor]
                   },
                   postprocessors={
                       'GET_MANY': [LibShipmentQuoteItem.get_many_postprocessor]
                   })


manager.create_api(ShipmentQuoteItem2,
                   url_prefix='/api/mes/v1/shipment',
                   collection_name='quote_item2',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(ShipmentQuoteManual,
                   url_prefix='/api/mes/v1/shipment',
                   collection_name='quote_manual',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibShipmentQuoteManual.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   },
                   postprocessors={
                       'POST': [LibShipmentQuoteManual.post_postprocessor]
                   })


manager.create_api(ShipmentQuoteManualItem,
                   url_prefix='/api/mes/v1/shipment',
                   collection_name='quote_manual_item',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(ShipmentOrder,
                   url_prefix='/api/mes/v1/shipment',
                   collection_name='order',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibShipmentOrder.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(ShipmentOrderItem,
                   url_prefix='/api/mes/v1/shipment',
                   collection_name='order_item',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibShipmentOrderItem.post_preprocessor],
                       'PATCH_SINGLE': [check_token, LibShipmentOrderItem.patch_single_preprocessor],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token]
                   },
                   postprocessors={
                       'GET_MANY' : [LibShipmentOrderItem.get_many_postprocessor],
                       'POST': [LibShipmentOrderItem.post_postprocessor],
                       'PATCH_SINGLE': [LibShipmentOrderItem.patch_single_postprocessor]
                   })


manager.create_api(ShipmentRelease,
                   url_prefix='/api/mes/v1/shipment',
                   collection_name='release',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibShipmentRelease.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(ShipmentReleaseItem,
                   url_prefix='/api/mes/v1/shipment',
                   collection_name='release_item',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibShipmentReleaseItem.post_preprocessor],
                       'PATCH_SINGLE': [check_token, LibShipmentReleaseItem.patch_single_preprocessor],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   },
                   postprocessors={
                       'GET_MANY' : [LibShipmentReleaseItem.get_many_postprocessor],
                       'POST': [LibShipmentReleaseItem.post_postprocessor],
                       'PATCH_SINGLE': [LibShipmentReleaseItem.patch_single_postprocessor]
                   })


manager.create_api(ShipmentReleaseItem,
                   url_prefix='/api/mes/v1/shipment',
                   collection_name='release_item_with_client',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   postprocessors={
                       'GET_MANY': [check_token, LisShipmentReleaseItemWithClient.get_many_postprocessor],
                   })


manager.create_api(ShipmentReleaseReturn,
                   url_prefix='/api/mes/v1/shipment',
                   collection_name='release_return',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibShipmentReleaseReturn.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(ShipmentReleaseReturnItem,
                   url_prefix='/api/mes/v1/shipment',
                   collection_name='release_return_item',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   },
                   postprocessors={
                       'GET_MANY' : [LibShipmentReleaseReturnItem.get_many_postprocessor],
                       'POST': [LibShipmentReleaseReturnItem.post_postprocessor],
                       'PATCH_SINGLE': [LibShipmentReleaseReturnItem.patch_single_postprocessor]
                   })


manager.create_api(ShipmentSalesStatement,
                   url_prefix='/api/mes/v1/shipment',
                   collection_name='sales_statement',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibShipmentSalesStatement.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token, LibShipmentSalesStatement.delete_single_preprocessor],  # ✅ 추가
                   },
                   postprocessors={
                       'GET_MANY' : [LibShipmentSalesStatement.get_many_postprocessor]
                   })


manager.create_api(ShipmentSalesStatementItem,
                   url_prefix='/api/mes/v1/shipment',
                   collection_name='sales_statement_item',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   },
                   postprocessors={
                       'GET_MANY' : [LibShipmentSalesStatementItem.get_many_postprocessor],
                       'POST': [LibShipmentSalesStatementItem.post_postprocessor],
                       'PATCH_SINGLE': [LibShipmentSalesStatementItem.patch_single_postprocessor]
                   })


manager.create_api(ShipmentDeposit,
                   url_prefix='/api/mes/v1/shipment',
                   collection_name='deposit',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibShipmentDeposit.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(ShipmentDepositItem,
                   url_prefix='/api/mes/v1/shipment',
                   collection_name='deposit_item',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   },
                   postprocessors={
                       'GET_MANY' : [LibShipmentDepositItem.get_many_postprocessor],
                       'POST': [LibShipmentDepositItem.post_postprocessor],
                       'PATCH_SINGLE': [LibShipmentDepositItem.patch_single_postprocessor]
                   })


manager.create_api(ShipmentLend,
                   url_prefix='/api/mes/v1/shipment',
                   collection_name='lend',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibShipmentLend.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(ShipmentRetrieve,
                   url_prefix='/api/mes/v1/shipment',
                   collection_name='retrieve',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibShipmentRetrieve.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   },
                   postprocessors={
                       'POST': [LibShipmentRetrieve.post_postprocessor],
                       'PATCH_SINGLE': [LibShipmentRetrieve.patch_single_postprocessor]
                   })


@app.route("/api/mes/v1/shipment/leadtime", methods=["POST"])
def shipment_leadtime():
    """
    출하관리 - 수주출하리드타임
    :return:
    """
    parser = reqparse.RequestParser()
    parser.add_argument("start_date", type=str, location="json")
    parser.add_argument("end_date", type=str, location="json")
    args = parser.parse_args()

    orders = db.session.query(
        ShipmentOrder
    ).filter(
        ShipmentOrder.order_date >= datetime.strptime(args['start_date'], '%Y-%m-%d %H:%M:%S')
    ).filter(
        ShipmentOrder.order_date <= datetime.strptime(args['end_date'], '%Y-%m-%d %H:%M:%S')
    ).all()

    result = []
    total_items = 0
    total_leadtime = 0
    for order in orders:
        release_items = db.session.query(
            ShipmentReleaseItem
        ).filter(
            ShipmentReleaseItem.order_number == order.order_number
        ).all()
        latest_release = None
        latest_date = None
        for release_item in release_items:
            if latest_date is None or latest_date < release_item.release.release_date:
                latest_date = release_item.release.release_date
                latest_release = release_item
        if latest_release and latest_date:
            date_diff = latest_date - order.order_date
            if date_diff.days > 0:
                result.append({
                    'id': total_items,
                    'order_number': order.order_number,
                    'order_date': order.order_date,
                    'client_company': latest_release.release.client_company,
                    'release_number': latest_release.release.release_number,
                    'release_date': latest_release.release.release_date,
                    'item_code': latest_release.item_code,
                    'item_name': latest_release.item.item_name,
                    'item_standard': latest_release.item.item_standard,
                    'leadtime': date_diff.days
                })
                total_items += 1
                total_leadtime += date_diff.days
    try:
        average = int(total_leadtime / total_items)
    except:
        average = 0

    response = {
        'data': result,
        'average': average
    }
    return make_response(jsonify(response), 200)

@app.route("/api/mes/v1/shipment/quote/export/business", methods=["POST"])
def shipment_quote_export_to_business():
    """
    출하관리 - 견적을 영업건으로 보내기
    :return:
    """
    parser = reqparse.RequestParser()
    parser.add_argument("quote_id", type=int, location="json")
    parser.add_argument("department", type=str, location="json")
    parser.add_argument("manager", type=str, location="json")
    args = parser.parse_args()
    quote = db.session.query(
        ShipmentQuote
    ).filter(
        ShipmentQuote.id == args['quote_id']
    ).first()
    if quote:
        import datetime
        from backend_model.table_base import BaseCode
        from backend_model.table_project import ProjectBusiness
        business_status_code = db.session.query(BaseCode).filter(BaseCode.code_name == '현재단계').first()
        business_status = None
        if business_status_code and len(business_status_code.items) > 0:
            business_status = business_status_code.items[0].code_name
        business_progress_code = db.session.query(BaseCode).filter(BaseCode.code_name == '진행현황').first()
        business_progress = None
        if business_progress_code and len(business_progress_code.items) > 0:
            business_progress = business_progress_code.items[0].code_name
        business_important_code = db.session.query(BaseCode).filter(BaseCode.code_name == '중요').first()
        business_important = None
        if business_important_code and len(business_important_code.items) > 0:
            business_important = business_important_code.items[0].code_name
        
        data = {'fk_company_id': quote.fk_company_id}
        LibCommon.get_item_number(data, 'business_number', ProjectBusiness, ProjectBusiness.business_number,
                                      '/project/business')
        new_business = ProjectBusiness()
        new_business.business_number = data['business_number']
        new_business.business_name = quote.business_name
        new_business.business_date = datetime.datetime.now()
        new_business.client_company = quote.client_company
        new_business.client_manager = quote.client_manager
        new_business.business_amount = quote.supply_price
        new_business.business_department = args['department']
        new_business.business_manager = args['manager']
        new_business.contract_company = quote.end_user
        new_business.business_status = business_status
        new_business.business_progress = business_progress
        new_business.business_important = business_important
        new_business.fk_company_id = quote.fk_company_id
        db.session.add(new_business)
        db.session.commit()

        quote.fk_business_id = new_business.id
        db.session.commit()

    return make_response('success', 200)

@app.route("/api/mes/v1/shipment/quote/export/order", methods=["POST"])
def shipment_quote_export_to_order():
    """
    출하관리 - 견적을 수주로 보내기
    :return:
    """
    parser = reqparse.RequestParser()
    parser.add_argument("quote_id", type=int, location="json")
    args = parser.parse_args()

    quote = db.session.query(
        ShipmentQuote
    ).filter(
        ShipmentQuote.id == args['quote_id']
    ).first()
    if quote:
        quote_items = db.session.query(
            ShipmentQuoteItem
        ).filter(
            ShipmentQuoteItem.fk_quote_id == args['quote_id']
        ).filter(
            ShipmentQuoteItem.not_ordered > 0
        ).all()
        if len(quote_items) == 0:
            from backend_lib.lib_exception import MesException
            MesException.raise_not_add_item()
        if len(quote_items) > 0:
            import datetime
            from backend_lib.lib_common import LibCommon

            data = {'fk_company_id': quote.fk_company_id}
            LibCommon.get_item_number(data, 'order_number', ShipmentOrder, ShipmentOrder.order_number,
                                      '/shipment/order')

            from backend_lib.lib_base import LibBaseCode
            order_type = LibBaseCode.get_first_code_name('수주구분')

            order = ShipmentOrder()
            order.order_number = data['order_number']
            order.order_date = datetime.datetime.now()
            order.client_company = quote.client_company
            order.client_manager = quote.client_manager
            order.order_department = quote.quote_department
            order.order_manager = quote.quote_manager
            order.order_type = order_type
            order.vat_type = quote.vat_type
            order.payment_terms = quote.payment_terms
            order.delivery_date = quote.delivery_date
            order.delivery_place = quote.delivery_place
            order.end_user = quote.end_user
            order.note = quote.note
            order.etc = quote.etc
            order.supply_price = quote.supply_price
            order.vat = quote.vat
            order.total_price = quote.total_price
            order.fk_company_id = quote.fk_company_id
            db.session.add(order)

            quote.order_number = order.order_number
            db.session.commit()

            for quote_item in quote_items:
                order_item = ShipmentOrderItem()
                order_item.item_code = quote_item.item_code
                order_item.order_quantity = quote_item.not_ordered
                order_item.unit_price = quote_item.unit_price
                order_item.supply_price = quote_item.not_ordered * quote_item.unit_price
                order_item.request_delivery_date = quote_item.request_delivery_date
                order_item.warehouse_code = quote_item.warehouse_code
                order_item.not_shipped = quote_item.not_ordered
                order_item.quote_number = quote.quote_number
                order_item.client_item_number = quote_item.client_item_number
                order_item.note = quote_item.note
                order_item.fk_order_id = order.id
                order_item.fk_quote_item_id = quote_item.id
                db.session.add(order_item)

                quote_item.not_ordered = 0
                db.session.commit()

                LibShipmentOrderItem.update_assign_quantity(order_item.id, order_item.item_code,
                                                            order_item.warehouse_code)
    return make_response('success', 200)


@app.route("/api/mes/v1/shipment/order/export/release", methods=["POST"])
def shipment_order_export_to_release():
    """
    출하관리 - 수주를 출고로 보내기
    :return:
    """
    parser = reqparse.RequestParser()
    parser.add_argument("order_id", type=int, location="json")
    args = parser.parse_args()

    order = db.session.query(
        ShipmentOrder
    ).filter(
        ShipmentOrder.id == args['order_id']
    ).first()
    if order:
        order_items = db.session.query(
            ShipmentOrderItem
        ).filter(
            ShipmentOrderItem.fk_order_id == args['order_id']
        ).filter(
            ShipmentOrderItem.not_shipped > 0
        ).all()
        if len(order_items) == 0:
            from backend_lib.lib_exception import MesException
            MesException.raise_not_add_item()
        if len(order_items) > 0:
            import datetime
            from backend_lib.lib_common import LibCommon

            data = {'fk_company_id': order.fk_company_id}
            LibCommon.get_item_number(data, 'release_number', ShipmentRelease, ShipmentRelease.release_number,
                                      '/shipment/release')

            from backend_lib.lib_base import LibBaseCode
            # release_type = LibBaseCode.get_first_code_name('출고구분')

            release = ShipmentRelease()
            release.release_number = data['release_number']
            release.release_date = datetime.datetime.now()
            release.client_company = order.client_company
            release.client_manager = order.client_manager
            release.release_department = order.order_department
            release.release_manager = order.order_manager
            release.release_type = order.order_type
            release.vat_type = order.vat_type
            release.payment_terms = order.payment_terms
            release.delivery_date = order.delivery_date
            release.delivery_place = order.delivery_place
            release.end_user = order.end_user
            release.transport = order.transport
            release.note = order.note
            release.etc = order.etc
            release.supply_price = order.supply_price
            release.vat = order.vat
            release.total_price = order.total_price
            release.fk_project_management_id = order.fk_project_management_id
            release.fk_company_id = order.fk_company_id
            db.session.add(release)

            order.release_number = release.release_number
            db.session.commit()

            for order_item in order_items:
                release_item = ShipmentReleaseItem()
                release_item.item_code = order_item.item_code
                release_item.order_quantity = order_item.order_quantity
                release_item.release_quantity = order_item.assign_quantity
                release_item.unit_price = order_item.unit_price
                release_item.supply_price = order_item.assign_quantity * order_item.unit_price
                release_item.request_delivery_date = order_item.request_delivery_date
                release_item.non_invoice = order_item.assign_quantity
                release_item.warehouse_code = order_item.warehouse_code
                release_item.order_number = order.order_number
                release_item.client_item_number = order_item.client_item_number
                release_item.note = order_item.note
                release_item.fk_project_management_id = order_item.fk_project_management_id
                release_item.fk_release_id = release.id
                release_item.fk_order_item_id = order_item.id
                db.session.add(release_item)

                order_item.not_shipped = order_item.not_shipped - order_item.assign_quantity
                order_item.assign_quantity = 0
                db.session.commit()

                from backend_lib.lib_setup import LibSetupBasicStock
                LibSetupBasicStock.update_stock_by_item_code(release_item.item_code, release_item.warehouse_code)

    return make_response('success', 200)


@app.route("/api/mes/v1/shipment/release_item_by_rank", methods=["GET"])
def shipment_release_item_by_rank():
    from sqlalchemy import func
    from math import ceil

    results_per_page = request.args.get('results_per_page', default=10, type=int)
    page = request.args.get('page', default=1, type=int)
    q = request.args.get('q', default='{}', type=str)

    params = json.loads(q)
    if params['filters'] is None or len(params['filters']) == 0:
        return make_response('invalid parameter', 400)

    item_code = ''
    for item in params['filters']:
        if item['name'] == 'item_code':
            item_code = item['val']

    if item_code == '':
        response = dict(
            num_results=0,
            page=0,
            total_pages=0,
            objects=[]
        )
        return make_response(jsonify(response), 200)

    sq1 = db.session.query(
        ShipmentReleaseItem.id,
        func.row_number().over(
            partition_by=(ShipmentReleaseItem.unit_price, ShipmentRelease.client_company),
            order_by=ShipmentReleaseItem.created.desc()
        ).label('rk')
    ).join(
        ShipmentRelease,
        ShipmentRelease.id == ShipmentReleaseItem.fk_release_id
    ).filter(
        ShipmentReleaseItem.item_code == item_code
    ).order_by(
        ShipmentReleaseItem.created.desc()
    ).subquery()

    base = db.session.query(sq1.c.id).filter(sq1.c.rk == 1)
    sq2 = base.limit(results_per_page).offset((page - 1) * results_per_page).subquery()

    num_results = base.count()
    sq3 = db.session.query(ShipmentReleaseItem).join(sq2, sq2.c.id == ShipmentReleaseItem.id)

    result = [dict(
        id=o.id,
        created=o.created,
        item_code=o.item_code,
        order_quantity=o.order_quantity,
        release_quantity=o.release_quantity,
        unit_price=o.unit_price,
        cost_price=o.cost_price,
        request_delivery_date=o.request_delivery_date,
        non_invoice=o.non_invoice,
        warehouse_code=o.warehouse_code,
        order_number=o.order_number,
        client_item_number=o.client_item_number,
        note=o.note,
        closing_yn=o.closing_yn,
        fk_project_management_id=o.fk_project_management_id,
        fk_release_id=o.fk_release_id,
        fk_order_item_id=o.fk_order_item_id,
        release=dict(
            id=o.release.id,
            created=o.release.created,
            release_number=o.release.release_number,
            release_date=o.release.release_date,
            client_company=o.release.client_company,
            client_manager=o.release.client_manager,
            client_manager_phone=o.release.client_manager_phone,
            release_department=o.release.release_department,
            release_manager=o.release.release_manager,
            release_type=o.release.release_type,
            vat_type=o.release.vat_type,
            payment_terms=o.release.payment_terms,
            delivery_date=o.release.delivery_date,
            delivery_place=o.release.delivery_place,
            client_order_number=o.release.client_order_number,
            end_user=o.release.end_user,
            transport=o.release.transport,
            note=o.release.note,
            etc=o.release.etc,
            supply_price=o.release.supply_price,
            vat=o.release.vat,
            total_price=o.release.total_price,
            confirmed=o.release.confirmed,
            sales_number=o.release.sales_number,
            fk_project_management_id=o.release.fk_project_management_id,
            fk_company_id=o.release.fk_company_id
        ),
        order_item=dict(
            id=o.order_item.id,
            created=o.order_item.created,
            item_code=o.order_item.item_code,
            order_quantity=o.order_item.order_quantity,
            assign_quantity=o.order_item.assign_quantity,
            produce_plan_quantity=o.order_item.produce_plan_quantity,
            unit_price=o.order_item.unit_price,
            supply_price=o.order_item.supply_price,
            request_delivery_date=o.order_item.request_delivery_date,
            warehouse_code=o.order_item.warehouse_code,
            not_shipped=o.order_item.not_shipped,
            quote_number=o.order_item.quote_number,
            client_item_number=o.order_item.client_item_number,
            note=o.order_item.note,
            closing_yn=o.order_item.closing_yn,
            fk_project_management_id=o.order_item.fk_project_management_id,
            fk_order_id=o.order_item.fk_order_id,
            fk_quote_item_id=o.order_item.fk_quote_item_id,
            fk_project_item_id=o.order_item.fk_project_item_id
        ),
        item=dict(
            id=o.item.id,
            created=o.item.created,
            item_code=o.item.item_code,
            item_name=o.item.item_name,
            item_standard=o.item.item_standard,
            asset_type=o.item.asset_type,
            main_category=o.item.main_category,
            middle_category=o.item.middle_category,
            sub_category=o.item.sub_category,
            delivery_date=o.item.delivery_date,
            item_detail=o.item.item_detail,
            etc=o.item.etc,
            safety_stock=o.item.safety_stock,
            unit=o.item.unit,
            sales_price=o.item.sales_price,
            purchase_price=o.item.purchase_price,
            note1=o.item.note1,
            note2=o.item.note2,
            item_img=o.item.item_img,
            moq=o.item.moq,
            packing_quantity=o.item.packing_quantity,
            transfer_quantity=o.item.transfer_quantity,
            import_check=o.item.import_check,
            shipment_check=o.item.shipment_check,
            before_item_code=o.item.before_item_code,
            after_item_code=o.item.after_item_code,
            end_of_use=o.item.end_of_use,
            end_date=o.item.end_date,
            hs_code=o.item.hs_code,
            register_id=o.item.register_id,
            modify_id=o.item.modify_id,
            modify_date=o.item.modify_date,
            bom_yn=o.item.bom_yn,
            fk_company_id=o.item.fk_company_id
        ),
        # warehouse=o.warehouse,
        # basic_stock=o.basic_stock
    ) for o in sq3.all()]

    response = dict(
        num_results=num_results,
        page=page,
        total_pages=ceil(num_results / results_per_page),
        objects=result
    )

    return make_response(jsonify(response), 200)


@app.route("/api/mes/v1/shipment/release/export/sales", methods=["POST"])
def shipment_release_export_to_sales():
    """
    출하관리 - 출고를 계산서로 보내기
    :return:
    """
    parser = reqparse.RequestParser()
    parser.add_argument("release_id", type=int, location="json")
    args = parser.parse_args()

    release = db.session.query(
        ShipmentRelease
    ).filter(
        ShipmentRelease.id == args['release_id']
    ).first()
    if release:
        release_items = db.session.query(
            ShipmentReleaseItem
        ).filter(
            ShipmentReleaseItem.fk_release_id == args['release_id']
        ).filter(
            ShipmentReleaseItem.non_invoice > 0
        ).all()
        if len(release_items) == 0:
            from backend_lib.lib_exception import MesException
            MesException.raise_not_add_item()
        if len(release_items) > 0:
            from backend_lib.lib_base import LibBaseCode
            sales_type = LibBaseCode.get_first_code_name('계산서유형')
            approval_type = LibBaseCode.get_first_code_name('결재유형')
            publish_type = LibBaseCode.get_first_code_name('발행구분')
            office_type = LibBaseCode.get_first_code_name('본지점구분')

            import datetime
            from backend_lib.lib_common import LibCommon

            data = {'fk_company_id': release.fk_company_id}
            LibCommon.get_item_number(data, 'sales_number', ShipmentSalesStatement, ShipmentSalesStatement.sales_number, '/shipment/sales-statement')

            sales = ShipmentSalesStatement()
            sales.sales_number = data['sales_number']
            sales.sales_date = datetime.datetime.now()
            sales.client_company = release.client_company
            sales.client_manager = release.client_manager
            sales.sales_department = release.release_department
            sales.sales_manager = release.release_manager
            sales.sales_type = sales_type
            sales.approval_type = approval_type
            sales.publish_type = publish_type
            sales.office_type = office_type
            sales.etc = release.etc
            sales.vat_type = release.vat_type
            sales.supply_price = release.supply_price
            sales.vat = release.vat
            sales.total_price = release.total_price
            sales.not_deposit = release.total_price
            sales.fk_company_id = release.fk_company_id
            db.session.add(sales)

            release.sales_number = sales.sales_number
            db.session.commit()

            from backend_lib.lib_util import LibUtil

            for release_item in release_items:
                price = LibUtil.calculate_price(sales.vat_type, release_item.non_invoice, release_item.unit_price)

                sales_item = ShipmentSalesStatementItem()
                sales_item.item_code = release_item.item_code
                sales_item.quantity = release_item.non_invoice
                sales_item.unit_price = release_item.unit_price
                sales_item.vat = price['vat']
                sales_item.supply_price = price['supply_price']
                sales_item.total_price = price['total_price']
                sales_item.not_deposit = price['total_price']
                sales_item.note = release_item.note
                sales_item.release_number = release.release_number
                sales_item.fk_project_management_id = release_item.fk_project_management_id
                sales_item.fk_sales_id = sales.id
                sales_item.fk_release_item_id = release_item.id
                db.session.add(sales_item)

                release_item.non_invoice = 0
                db.session.commit()

            LibShipmentSalesStatement.update_not_deposit(sales.id)

    return make_response('success', 200)


@app.route("/api/mes/v1/kpi/produce/leadtime", methods=["POST"])
def kpi_produce_leadtime():
    """
    KPI - 제조리드타임
    :return:
    """
    parser = reqparse.RequestParser()
    parser.add_argument("start_date", type=str, location="json")
    parser.add_argument("end_date", type=str, location="json")
    args = parser.parse_args()

    from backend_model.table_production import WorkOrder, PerformanceRegistrationItem1

    orders = db.session.query(
        WorkOrder
    ).filter(
        WorkOrder.target_date >= datetime.strptime(args['start_date'], '%Y-%m-%d %H:%M:%S')
    ).filter(
        WorkOrder.target_date <= datetime.strptime(args['end_date'], '%Y-%m-%d %H:%M:%S')
    ).all()

    result = []
    total_items = 0
    total_leadtime = 0
    for order in orders:
        reg_items = db.session.query(
            PerformanceRegistrationItem1
        ).filter(
            PerformanceRegistrationItem1.work_order_number == order.number
        ).all()
        latest_item = None
        latest_date = None
        for reg_item in reg_items:
            if latest_date is None or latest_date < reg_item.performance_registration.target_date:
                latest_date = reg_item.performance_registration.target_date
                latest_item = reg_item
        if latest_item and latest_date:
            date_diff = latest_date - order.target_date
            if date_diff.days > 0:
                result.append({
                    'id': total_items,
                    'order_number': order.number,
                    'order_date': order.target_date,
                    'client_company': latest_item.client_company,
                    'produce_number': latest_item.performance_registration.number,
                    'produce_date': latest_item.performance_registration.target_date,
                    'item_code': latest_item.item_code,
                    'item_name': latest_item.item.item_name,
                    'item_standard': latest_item.item.item_standard,
                    'leadtime': date_diff.days
                })
                total_items += 1
                total_leadtime += date_diff.days
    try:
        average = int(total_leadtime / total_items)
    except:
        average = 0

    response = {
        'data': result,
        'average': average
    }
    return make_response(jsonify(response), 200)


@app.route("/api/mes/v1/shipment/sales/balance", methods=["GET"])
def get_shipment_sales_balance():
    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        return make_response(jsonify('No Parameters'), 400)

    start_date = parameter_dict['start']
    end_date = parameter_dict['end']

    response = dict()
    response['objects'] = []

    res_id = 0

    from backend_model.table_common import Companies
    from backend_model.table_setup import SetupBasicBalance

    tmp = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    balance_date = tmp.strftime('%Y-%m-01 00:00:00')
    is_past_balance = True
    company = db.session.query(
        Companies
    ).filter(
        Companies.basic_balance_date < balance_date
    ).first()
    if not company:
        is_past_balance = False

    from backend_model.table_base import BaseClient
    from backend_lib.lib_barobill import get_invoice_state
    clients = db.session.query(BaseClient).all()
    for client in clients:
        past_basic_balance = 0
        if is_past_balance:
            setup_basic_balance = db.session.query(
                SetupBasicBalance
            ).filter(
                SetupBasicBalance.fk_base_client_id == client.id
            ).first()
            if setup_basic_balance:
                past_basic_balance = setup_basic_balance.sales_balance

        past_sum_total_supply_price = db.session.query(
            db.func.sum(ShipmentRelease.supply_price)
        ).filter(
            ShipmentRelease.client_company == client.name
        ).filter(
            ShipmentRelease.release_date < start_date
        ).first()[0]
        if not past_sum_total_supply_price:
            past_sum_total_supply_price = 0

        past_sum_total_return_supply_price = db.session.query(
            db.func.sum(ShipmentReleaseReturn.supply_price)
        ).filter(
            ShipmentReleaseReturn.client_company == client.name
        ).filter(
            ShipmentReleaseReturn.return_date < start_date
        ).first()[0]
        if not past_sum_total_return_supply_price:
            past_sum_total_return_supply_price = 0

        past_deposits = db.session.query(
            ShipmentDeposit
        ).filter(
            ShipmentDeposit.client_company == client.name
        ).filter(
            ShipmentDeposit.deposit_date < start_date
        ).all()
        past_sum_deposit_price = 0
        for past_deposit in past_deposits:
            deposit_price = db.session.query(
                db.func.sum(ShipmentDepositItem.price)
            ).filter(
                ShipmentDepositItem.fk_deposit_id == past_deposit.id
            ).first()[0]
            if deposit_price:
                past_sum_deposit_price += deposit_price
        
        past_sales_statement_vat = db.session.query(
            db.func.sum(ShipmentSalesStatement.vat)
        ).filter(
            ShipmentSalesStatement.client_company == client.name
        ).filter(
            ShipmentSalesStatement.sales_date < start_date
        ).first()[0]
        if not past_sales_statement_vat:
            past_sales_statement_vat = 0

        search_sales_statement= db.session.query(
            ShipmentSalesStatement
        ).filter(
            ShipmentSalesStatement.client_company == client.name
        ).filter(
            ShipmentSalesStatement.sales_date >= start_date
        ).filter(
            ShipmentSalesStatement.sales_date <= end_date
        ).all()

        sum_total_vat = sum(sales.vat for sales in search_sales_statement)
        sum_total_vat_adjustment = sum(sales.vat_adjustment for sales in search_sales_statement)

        search_release = db.session.query(
            db.func.sum(ShipmentRelease.supply_price),
            db.func.sum(ShipmentRelease.vat),
            db.func.sum(ShipmentRelease.total_price)
        ).filter(
            ShipmentRelease.client_company == client.name
        ).filter(
            ShipmentRelease.release_date >= start_date
        ).filter(
            ShipmentRelease.release_date <= end_date
        ).first()
        if not search_release:
            sum_sales_price = 0
            sum_vat = 0
            sum_total_sales_price = 0
        else:
            sum_sales_price = search_release[0] if search_release[0] else 0
            sum_vat = search_release[1] if search_release[1] else 0
            sum_total_sales_price = search_release[2] if search_release[2] else 0

        search_return = db.session.query(
            db.func.sum(ShipmentReleaseReturn.supply_price),
            db.func.sum(ShipmentReleaseReturn.vat),
            db.func.sum(ShipmentReleaseReturn.total_price)
        ).filter(
            ShipmentReleaseReturn.client_company == client.name
        ).filter(
            ShipmentReleaseReturn.return_date >= start_date
        ).filter(
            ShipmentReleaseReturn.return_date <= end_date
        ).first()
        if not search_return:
            sum_return_sales_price = 0
            sum_return_vat = 0
            sum_return_total_sales_price = 0
        else:
            sum_return_sales_price =  search_return[0] if search_return[0] else 0
            sum_return_vat = search_return[1] if search_return[1] else 0
            sum_return_total_sales_price = search_return[2] if search_return[2] else 0

        search_deposits = db.session.query(
            ShipmentDeposit
        ).filter(
            ShipmentDeposit.client_company == client.name
        ).filter(
            ShipmentDeposit.deposit_date >= start_date
        ).filter(
            ShipmentDeposit.deposit_date <= end_date
        ).all()
        sum_deposit_price = 0
        for search_deposit in search_deposits:
            deposit_price = db.session.query(
                db.func.sum(ShipmentDepositItem.price)
            ).filter(
                ShipmentDepositItem.fk_deposit_id == search_deposit.id
            ).first()[0]
            if deposit_price:
                sum_deposit_price += deposit_price

        past_account_receivable = past_basic_balance + past_sum_total_supply_price - past_sum_total_return_supply_price - past_sum_deposit_price + past_sales_statement_vat
        if past_account_receivable == 0 and \
                sum_sales_price == 0 and sum_total_vat == 0 and sum_total_sales_price == 0 and \
                sum_return_sales_price == 0 and sum_return_vat == 0 and sum_return_total_sales_price == 0 and \
                sum_deposit_price == 0:
            continue

        client_manager = client.manager
        if not client_manager:
            client_manager = ''

        res = {
            'id': res_id,
            'client_id': client.id,
            'client_alias': client.alias,
            'client_name': client.name,
            'client_manager': client_manager,
            'past_account_receivable': past_account_receivable,
            'sales_price': sum_sales_price - sum_return_sales_price,
            'vat': sum_total_vat,
            'vat_adjustment': sum_total_vat_adjustment,
            'total_price': sum_sales_price - sum_return_sales_price + sum_total_vat,
            'deposit_price': sum_deposit_price,
            'account_receivable': past_account_receivable + sum_sales_price - sum_return_sales_price - sum_deposit_price + sum_total_vat,
        }
        response['objects'].append(res)
        res_id += 1

    return make_response(response, 200)


@app.route("/api/mes/v1/shipment/sales/balance/<client_id>", methods=["GET"])
def get_shipment_sales_balance_detail(client_id):
    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        return make_response(jsonify('No Parameters'), 400)

    start_date = parameter_dict['start']
    end_date = parameter_dict['end']

    response = dict()
    response['objects'] = []

    res_id = 0

    from backend_model.table_common import Companies
    from backend_model.table_setup import SetupBasicBalance

    tmp = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    balance_date = tmp.strftime('%Y-%m-01 00:00:00')

    is_past_balance = True
    company = db.session.query(
        Companies
    ).filter(
        Companies.basic_balance_date < balance_date
    ).first()
    if not company:
        is_past_balance = False

    from backend_model.table_base import BaseClient

    client = db.session.query(
        BaseClient
    ).filter(
        BaseClient.id == client_id
    ).first()

    if client:
        client_manager = client.manager
        if not client_manager:
            client_manager = ''

        # 이월 미수금
        tmp = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').date() - timedelta(days=1)
        start_date_one_day_ago = datetime(tmp.year, tmp.month, tmp.day)  # date to datetime

        past_basic_balance = 0
        if is_past_balance:
            setup_basic_balance = db.session.query(
                SetupBasicBalance
            ).filter(
                SetupBasicBalance.fk_base_client_id == client.id
            ).first()
            if setup_basic_balance:
                past_basic_balance = setup_basic_balance.sales_balance

        past_sum_total_sales_supply_price = db.session.query(
            db.func.sum(ShipmentRelease.supply_price)
        ).filter(
            ShipmentRelease.client_company == client.name
        ).filter(
            ShipmentRelease.release_date < start_date
        ).first()[0]
        if not past_sum_total_sales_supply_price:
            past_sum_total_sales_supply_price = 0

        past_sum_total_return_supply_price = db.session.query(
            db.func.sum(ShipmentReleaseReturn.supply_price)
        ).filter(
            ShipmentReleaseReturn.client_company == client.name
        ).filter(
            ShipmentReleaseReturn.return_date < start_date
        ).first()[0]
        if not past_sum_total_return_supply_price:
            past_sum_total_return_supply_price = 0

        past_deposits = db.session.query(
            ShipmentDeposit
        ).filter(
            ShipmentDeposit.client_company == client.name
        ).filter(
            ShipmentDeposit.deposit_date < start_date
        ).all()
        past_sum_deposit_price = 0
        for past_deposit in past_deposits:
            sum_deposit_price = db.session.query(
                db.func.sum(ShipmentDepositItem.price)
            ).filter(
                ShipmentDepositItem.fk_deposit_id == past_deposit.id
            ).first()[0]
            if sum_deposit_price:
                past_sum_deposit_price += sum_deposit_price

        past_sales_statement_vat = db.session.query(
            db.func.sum(ShipmentSalesStatement.vat)
        ).filter(
            ShipmentSalesStatement.client_company == client.name
        ).filter(
            ShipmentSalesStatement.sales_date < start_date
        ).first()[0]
        if not past_sales_statement_vat:
            past_sales_statement_vat = 0
            
        past_account_receivable = past_basic_balance + past_sum_total_sales_supply_price - past_sum_total_return_supply_price - past_sum_deposit_price + past_sales_statement_vat

        res = make_shipment_sales_balance_detail_response(
            response_id=res_id,
            action_type='이월미수금',
            action_date=start_date_one_day_ago,
            client_company=client.name,
            client_manager=client_manager,
            past_account_receivable=past_account_receivable)
        response['objects'].append(res)

        #매출계산서 부가세 리스트
        sales_statement= db.session.query(
            ShipmentSalesStatement
            ).filter(
            ShipmentSalesStatement.client_company == client.name
            ).filter(
            ShipmentSalesStatement.sales_date >= start_date
            ).filter(
            ShipmentSalesStatement.sales_date <= end_date
            ).all()

        for sales in sales_statement:
            res_id += 1
            res = make_shipment_sales_balance_detail_response(
                response_id=res_id,
                action_type='계산서 부가세',
                action_date=sales.sales_date,
                client_company=client.name,
                client_manager=client_manager,
                vat=sales.vat,
                vat_adjustment= -sales.vat_adjustment,
                number=sales.sales_number)
            response['objects'].append(res)

        # 출고 리스트
        release_list = db.session.query(
            ShipmentRelease
        ).filter(
            ShipmentRelease.client_company == client.name
        ).filter(
            ShipmentRelease.release_date >= start_date
        ).filter(
            ShipmentRelease.release_date <= end_date
        ).all()
        for release in release_list:
            res_id += 1
            res = make_shipment_sales_balance_detail_response(
                response_id=res_id,
                action_type='출고',
                action_date=release.release_date,
                client_company=client.name,
                client_manager=client_manager,
                sales_price=release.supply_price,
                # vat=release.vat,
                total_sales_price=release.supply_price,
                # total_sales_price=release.total_price,
                number=release.release_number)
            response['objects'].append(res)

        # 출고반품 리스트
        return_list = db.session.query(
            ShipmentReleaseReturn
        ).filter(
            ShipmentReleaseReturn.client_company == client.name
        ).filter(
            ShipmentReleaseReturn.return_date >= start_date
        ).filter(
            ShipmentReleaseReturn.return_date <= end_date
        ).all()
        for _item in return_list:
            res_id += 1
            res = make_shipment_sales_balance_detail_response(
                response_id=res_id,
                action_type='반품',
                action_date=_item.return_date,
                client_company=client.name,
                client_manager=client_manager,
                sales_price=-_item.supply_price,
                # vat=-_item.vat,
                total_sales_price=-_item.supply_price,
                # total_sales_price=-_item.total_price,
                number=_item.return_number)
            response['objects'].append(res)

        # 입금 리스트
        deposit_list = db.session.query(
            ShipmentDeposit
        ).filter(
            ShipmentDeposit.client_company == client.name
        ).filter(
            ShipmentDeposit.deposit_date >= start_date
        ).filter(
            ShipmentDeposit.deposit_date <= end_date
        ).all()
        for deposit in deposit_list:
            deposit_price = db.session.query(
                db.func.sum(ShipmentDepositItem.price)
            ).filter(
                ShipmentDepositItem.fk_deposit_id == deposit.id
            ).first()[0]
            if not deposit_price:
                deposit_price = 0

            res_id += 1
            res = make_shipment_sales_balance_detail_response(
                response_id=res_id,
                action_type='입금',
                action_date=deposit.deposit_date,
                client_company=client.name,
                client_manager=client_manager,
                deposit_price=deposit_price,
                number=deposit.deposit_number)
            response['objects'].append(res)

        # 날짜순 정렬
        response['objects'] = sorted(response['objects'], key=(lambda x: x['action_date']))
    else:
        return make_response(response, 404)

    return make_response(response, 200)


@app.route("/api/mes/v1/shipment/summary-sales-balance/<path:client_name>", methods=["GET"])
def get_shipment_sales_balance_summary(client_name):
    from backend_model.table_setup import SetupBasicBalance
    from backend_model.table_base import BaseClient
    from backend_model.table_common import Companies
    import calendar

    current_time = datetime.now()
    company = Companies.query.first()
    if not company:
        return make_response('업체 정보를 찾지 못했습니다', 400)

    client = BaseClient.query.filter_by(name=client_name).first()
    if not client:
        return make_response('고객 업체가 없습니다', 400)

    base_balance = SetupBasicBalance.query.filter_by(fk_base_client_id=client.id).first()
    # if not base_balance:
    #     return make_response('기초 잔고가 없습니다', 400)

    # 전월말 미수 금액
    receivable_balance = base_balance.sales_balance if base_balance else 0
    if current_time.month > (company.basic_balance_date.month + 1):
        before_month = current_time.month - 1
        _, last_day = calendar.monthrange(current_time.year, before_month)
        before_time = current_time.replace(month=before_month, day=last_day, hour=23, minute=59, second=59)

        release_items = ShipmentReleaseItem.query\
            .join(ShipmentRelease, ShipmentRelease.id == ShipmentReleaseItem.fk_release_id)\
            .filter(ShipmentRelease.release_date > company.basic_balance_date)\
            .filter(ShipmentRelease.release_date <= before_time)\
            .filter(ShipmentRelease.client_company == client_name)\
            .all()

        for item in release_items:
            receivable_balance += item.unit_price * item.release_quantity

        deposit_items = ShipmentDepositItem.query\
            .join(ShipmentDeposit, ShipmentDeposit.id == ShipmentDepositItem.fk_deposit_id)\
            .filter(ShipmentDeposit.deposit_date > company.basic_balance_date)\
            .filter(ShipmentDeposit.deposit_date <= before_time)\
            .filter(ShipmentDeposit.client_company == client_name)\
            .all()

        for item in deposit_items:
            receivable_balance -= item.price

    start_time = current_time.replace(day=1, hour=0, minute=0, second=0)
    release_balance = 0
    release_items = ShipmentReleaseItem.query\
        .join(ShipmentRelease, ShipmentRelease.id == ShipmentReleaseItem.fk_release_id)\
        .filter(ShipmentRelease.release_date > start_time)\
        .filter(ShipmentRelease.release_date <= current_time)\
        .filter(ShipmentRelease.client_company == client_name)\
        .all()

    for item in release_items:
        release_balance += item.release_quantity * item.unit_price

    deposit_balance = 0
    deposit_items = ShipmentDepositItem.query \
        .join(ShipmentDeposit, ShipmentDeposit.id == ShipmentDepositItem.fk_deposit_id)\
        .filter(ShipmentDeposit.deposit_date > start_time) \
        .filter(ShipmentDeposit.deposit_date <= current_time) \
        .filter(ShipmentDeposit.client_company == client_name) \
        .all()

    for item in deposit_items:
        deposit_balance += item.price

    return make_response(jsonify(dict(
        receivable_balance=receivable_balance,
        release_balance=release_balance,
        deposit_balance=deposit_balance,
        client=dict(
            id=client.id,
            created=client.created,
            alias=client.alias,
            name=client.name,
            address=client.address,
            address_detail=client.address_detail,
            zip_code=client.zip_code,
            phone=client.phone,
            fax=client.fax,
            email=client.email,
            homepage=client.homepage,
            bill_manager=client.bill_manager,
            bill_email=client.bill_email,
            client_type=client.client_type,
            district_type=client.district_type,
            manager=client.manager,
            trade_yn=client.trade_yn,
            before_alias=client.before_alias,
            after_alias=client.after_alias,
            corp_number=client.corp_number,
            business_number=client.business_number,
            ceo_name=client.ceo_name,
            business_status=client.business_status,
            business_sector=client.business_sector,
            name_en=client.name_en,
            ceo_name_en=client.ceo_name_en,
            phone_en=client.phone_en,
            fax_en=client.fax_en,
            address_en=client.address_en,
            etc=client.etc,
            register_id=client.register_id,
            modify_id=client.modify_id
        )
    )), 200)


@app.route("/api/mes/v1/shipment/release-item-by-lot/<lot_number>", methods=["GET"])
def shipment_release_item_by_lot(lot_number):
    from sqlalchemy import and_
    from backend_model.table_production \
        import ProcessMaterialConsumption, ProcessPerformanceRegistration, PerformanceRegistrationItem1

    result = db.session.query(ShipmentReleaseItem)\
        .join(PerformanceRegistrationItem1,
              PerformanceRegistrationItem1.order_number == ShipmentReleaseItem.order_number)\
        .join(ProcessPerformanceRegistration,
              and_(
                  ProcessPerformanceRegistration.fk_work_order_item == PerformanceRegistrationItem1.fk_work_order_item,
                  ProcessPerformanceRegistration.item_code == PerformanceRegistrationItem1.item_code
              ))\
        .join(ProcessMaterialConsumption,
              ProcessMaterialConsumption.process_number == ProcessPerformanceRegistration.number)\
        .filter(ProcessMaterialConsumption.lot_number == lot_number)\
        .order_by(ShipmentReleaseItem.created.desc())\
        .all()

    objects = [
        dict(
            id=item.id,
            created=item.created,
            item_code=item.item_code,
            order_quantity=item.order_quantity,
            release_quantity=item.release_quantity,
            unit_price=item.unit_price,
            cost_price=item.cost_price,
            request_delivery_date=item.request_delivery_date,
            non_invoice=item.non_invoice,
            warehouse_code=item.warehouse_code,
            order_number=item.order_number,
            lot_number=item.lot_number,
            client_item_number=item.client_item_number,
            note=item.note,
            closing_yn=item.closing_yn,
            fk_project_management_id=item.fk_project_management_id,
            fk_release_id=item.fk_release_id,
            fk_order_item_id=item.fk_order_item_id,
            release = dict(
                release_number=item.release.release_number,
                release_date=item.release.release_date,
                release_manager=item.release.release_manager,
                release_type=item.release.release_type
            ),
            item = dict(
                item_code=item.item.item_code,
                item_name=item.item.item_name,
                item_standard=item.item.item_standard
            ),
            warehouse = dict(
                wh_name=item.warehouse.wh_name
            )
        ) for item in result
    ]

    return make_response(jsonify(objects), 200)


def make_shipment_sales_balance_detail_response(response_id, action_date, action_type, number='', client_company='', client_manager = '', past_account_receivable=0, sales_price=0, vat=0, vat_adjustment=0, total_sales_price=0, deposit_price=0):
    res = {
        'id': response_id,
        'number': number,
        'action_date': action_date,
        'action_type': action_type,
        'company': client_company,
        'manager': client_manager,
        'past_account_receivable': past_account_receivable,
        'sales_price': sales_price,
        'vat': vat,
        'vat_adjustment': vat_adjustment,
        'total_sales_price': total_sales_price,
        'deposit_price': deposit_price,
        'group_id': action_date.strftime('%Y-%m')
    }
    return res
