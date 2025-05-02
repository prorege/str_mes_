# -*- coding: utf-8 -*-
print("module [backend.api_purchase] loaded")


from backend import manager
from backend import check_token
from backend_model.table_purchase import *
from backend_model.table_shipment import *
from backend_lib.lib_purchase import *
from datetime import datetime, timedelta
db = DBManager.db
# REST API(s) available :
#  - /api/v1/login
#  - /api/v1/logout


manager.create_api(PurchaseOrderPlan,
                   url_prefix='/api/mes/v1/purchase',
                   collection_name='order_plan',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibPurchaseOrderPlan.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(PurchaseOrderPlanItem,
                   url_prefix='/api/mes/v1/purchase',
                   collection_name='order_plan_item',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibPurchaseOrderPlanItem.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token, LibPurchaseOrderPlanItem.delete_single_preprocessor]
                   }, postprocessors={
                       'GET_MANY' : [LibPurchaseOrderPlanItem.get_many_postprocessor],
                       'POST': [LibPurchaseOrderPlanItem.post_postprocessor],
                       'PATCH_SINGLE': [LibPurchaseOrderPlanItem.patch_single_postprocessor]
                   })


manager.create_api(PurchaseOrder,
                   url_prefix='/api/mes/v1/purchase',
                   collection_name='order',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibPurchaseOrder.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(PurchaseOrderItem,
                   url_prefix='/api/mes/v1/purchase',
                   collection_name='order_item',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibPurchaseOrderItem.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token, LibPurchaseOrderItem.delete_single_preprocessor]
                   },
                   postprocessors={
                       'POST': [LibPurchaseOrderItem.post_postprocessor],
                       'PATCH_SINGLE': [LibPurchaseOrderItem.patch_single_postprocessor],
                       'GET_MANY': [LibPurchaseOrderItem.get_many_postprocessor]
                   })


manager.create_api(PurchaseOrderItem,
                   url_prefix='/api/mes/v1/purchase',
                   collection_name='order_receiving_status',
                   methods=['GET'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'GET_MANY': [check_token],
                   },
                   postprocessors={
                       'GET_MANY': [LibPurchaseOrderReceivingStatus.get_many_postprocessor]
                   })


manager.create_api(PurchasePreReceiving,
                   url_prefix='/api/mes/v1/purchase',
                   collection_name='prereceiving',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibPurchasePreReceiving.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(PurchasePreReceivingItem,
                   url_prefix='/api/mes/v1/purchase',
                   collection_name='prereceiving_item',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token, LibPurchasePreReceivingItem.delete_single_preprocessor]
                   },
                   postprocessors={
                       'GET_MANY': [LibPurchasePreReceivingItem.get_many_postprocessor] 
                   })


manager.create_api(PurchaseReceiving,
                   url_prefix='/api/mes/v1/purchase',
                   collection_name='receiving',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibPurchaseReceiving.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(PurchaseReceivingItem,
                   url_prefix='/api/mes/v1/purchase',
                   collection_name='receiving_item',
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
                       'GET_MANY': [LibPurchaseReceivingItem.get_many_postprocessor],
                       'POST': [LibPurchaseReceivingItem.post_postprocessor],
                       'PATCH_SINGLE': [LibPurchaseReceivingItem.patch_single_postprocessor]
                   })


manager.create_api(PurchaseReceivingReturn,
                   url_prefix='/api/mes/v1/purchase',
                   collection_name='receiving_return',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibPurchaseReceivingReturn.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(PurchaseReceivingReturnItem,
                   url_prefix='/api/mes/v1/purchase',
                   collection_name='receiving_return_item',
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
                   },postprocessors={
                       'GET_MANY': [LibPurchaseReceivingReturnItem.get_many_postprocessor],
                       'POST': [LibPurchaseReceivingReturnItem.post_postprocessor],
                       'PATCH_SINGLE': [LibPurchaseReceivingReturnItem.patch_single_postprocessor]
                   })

manager.create_api(PurchaseStatement,
                   url_prefix='/api/mes/v1/purchase',
                   collection_name='statement',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibPurchaseStatement.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   },postprocessors={
                       'GET_MANY': [],
                       'POST': [],
                       'PATCH_SINGLE': []
                   })
manager.create_api(PurchaseStatementItem,
                   url_prefix='/api/mes/v1/purchase',
                   collection_name='statement_item',
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
                   },postprocessors={
                       'GET_MANY': [],
                       'POST': [],
                       'PATCH_SINGLE': []
                   })

manager.create_api(PurchasePayment,
                   url_prefix='/api/mes/v1/purchase',
                   collection_name='payment',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibPurchasePayment.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   },postprocessors={
                       'GET_MANY': [],
                       'POST': [],
                       'PATCH_SINGLE': []
                   })
manager.create_api(PurchasePaymentItem,
                   url_prefix='/api/mes/v1/purchase',
                   collection_name='payment_item',
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
                   },postprocessors={
                       'GET_MANY': [],
                       'POST': [],
                       'PATCH_SINGLE': []
                   })

import datetime
from backend import app
from flask import make_response, jsonify, request, json, send_from_directory
from flask_restless import ProcessingException
from flask_restful import reqparse
from urllib.parse import urlparse


@app.route("/api/mes/v1/export-plan-to-order", methods=["POST"])
def export_plan_to_order():
    parser = reqparse.RequestParser()
    parser.add_argument("id", type=int, location="json")
    parser.add_argument("department", type=str, location="json")
    parser.add_argument("manager", type=str, location="json")
    parser.add_argument("company_id", type=int, location="json")
    parser.add_argument('order_plan_item_ids', type=int, action='append')
    args = parser.parse_args()

    from backend_model.table_base import BaseCode
    vat_code = db.session.query(BaseCode).filter(BaseCode.code_name == '부가세구분').first()
    vat_type = None
    if vat_code and len(vat_code.items) > 0:
        vat_type = vat_code.items[0].code_name
    order_code = db.session.query(BaseCode).filter(BaseCode.code_name == '발주구분').first()
    order_type = None
    if order_code and len(order_code.items) > 0:
        order_type = order_code.items[0].code_name
    payment_code = db.session.query(BaseCode).filter(BaseCode.code_name == '결재조건').first()
    payment_type = None
    if payment_code and len(payment_code.items) > 0:
        payment_type = payment_code.items[0].code_name
    delivery_code = db.session.query(BaseCode).filter(BaseCode.code_name == '납품장소').first()
    delivery_type = None
    if delivery_code and len(delivery_code.items) > 0:
        delivery_type = delivery_code.items[0].code_name

    from backend_lib.lib_util import LibUtil
    from backend_lib.lib_common import LibCommon

    add_count = 0
    valid_items = {}

    plan_items = db.session.query(
        PurchaseOrderPlanItem
    ).filter(
        PurchaseOrderPlanItem.id.in_(args['order_plan_item_ids'])
    ).all()
    for plan_item in plan_items:
        if plan_item.unordered_quantity <= 0:
            continue
        if not plan_item.main_supplier:
            continue

        if plan_item.main_supplier in valid_items:
            new_order = valid_items[plan_item.main_supplier]

            new_order_item = PurchaseOrderItem()
            new_order_item.item_code = plan_item.item_code
            new_order_item.order_quantity = plan_item.unordered_quantity
            new_order_item.unit_price = plan_item.unit_price
            new_order_item.supply_price = plan_item.supply_price
            new_order_item.request_delivery_date = plan_item.request_delivery_date
            new_order_item.not_shipped = plan_item.unordered_quantity
            new_order_item.order_plan_number = plan_item.order_plan.order_plan_number
            new_order_item.client_item_number = plan_item.client_item_number
            new_order_item.fk_project_management_id = plan_item.fk_project_management_id
            new_order_item.warehouse_code = plan_item.warehouse_code
            new_order_item.closing_yn = 0
            new_order_item.fk_order_plan_item_id = plan_item.id
            new_order_item.fk_purchase_order_id = new_order.id
            if plan_item.item.import_check:
                new_order_item.check_yn = 0
            else:
                new_order_item.check_yn = 1
            db.session.add(new_order_item)

            price = LibUtil.calculate_price(vat_type, plan_item.unordered_quantity, plan_item.unit_price)
            new_order.supply_price += price['supply_price']
            new_order.vat += price['vat']
            new_order.total_price += price['total_price']
            db.session.commit()
        else:
            data = {
                'fk_company_id': args['company_id']
            }
            LibCommon.get_item_number(data, 'order_number', PurchaseOrder, PurchaseOrder.order_number,
                                      '/purchase/order-plan')

            price = LibUtil.calculate_price(vat_type, plan_item.unordered_quantity, plan_item.unit_price)

            new_order = PurchaseOrder()
            new_order.order_number = data['order_number']
            new_order.order_date = datetime.datetime.now()
            new_order.order_department = args['department']
            new_order.order_manager = args['manager']
            new_order.client_company = plan_item.main_supplier
            new_order.fk_company_id = args['company_id']
            new_order.vat_type = vat_type
            new_order.order_type = plan_item.order_plan.order_type if plan_item.order_plan.order_type else order_type
            new_order.payment_terms = payment_type
            new_order.delivery_place = delivery_type
            new_order.supply_price = price['supply_price']
            new_order.vat = price['vat']
            new_order.total_price = price['total_price']
            db.session.add(new_order)
            db.session.commit()

            new_order_item = PurchaseOrderItem()
            new_order_item.item_code = plan_item.item_code
            new_order_item.order_quantity = plan_item.unordered_quantity
            new_order_item.unit_price = plan_item.unit_price
            new_order_item.supply_price = plan_item.supply_price
            new_order_item.request_delivery_date = plan_item.request_delivery_date
            new_order_item.not_shipped = plan_item.unordered_quantity
            new_order_item.order_plan_number = plan_item.order_plan.order_plan_number
            new_order_item.client_item_number = plan_item.client_item_number
            new_order_item.fk_project_management_id = plan_item.fk_project_management_id
            new_order_item.warehouse_code = plan_item.warehouse_code
            new_order_item.closing_yn = 0
            new_order_item.fk_order_plan_item_id = plan_item.id
            new_order_item.fk_purchase_order_id = new_order.id
            if plan_item.item.import_check:
                new_order_item.check_yn = 0
            else:
                new_order_item.check_yn = 1
            db.session.add(new_order_item)

            valid_items[plan_item.main_supplier] = new_order
        db.session.commit()
        LibPurchaseOrderPlanItem.update_unordered_quantity(plan_item.id)
        add_count += 1
    if add_count <= 0:
        from backend_lib.lib_exception import MesException
        MesException.raise_not_add_item()
    return make_response('success', 200)

@app.route("/api/mes/v1/purchase/balance/<client_id>", methods=["GET"])
def get_purchase_balance_detail(client_id):
    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        return make_response(jsonify('No Parameters'), 400)
    
    start_date = parameter_dict['start']
    end_date = parameter_dict['end']
    
    response = dict()
    response['objects'] = []

    res_id = 0
    from datetime import datetime, timedelta
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

        #이월 미수금
        tmp = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').date() - timedelta(days=1)
        start_date_one_day_ago = datetime(tmp.year, tmp.month, tmp.day)  # date to datetime

        # 입고
        past_sum_total_receiving_supply_price = db.session.query(
            db.func.sum(PurchaseReceiving.supply_price)
        ).filter(
            PurchaseReceiving.client_company == client.name
        ).filter(
            PurchaseReceiving.receiving_date < start_date
        ).first()[0]

        if not past_sum_total_receiving_supply_price:
            past_sum_total_receiving_supply_price = 0

        # 입고 반품
        past_sum_total_receiving_return_supply_price = db.session.query(
            db.func.sum(PurchaseReceivingReturn.supply_price)
        ).filter(
            PurchaseReceivingReturn.client_company == client.name
        ).filter(
            PurchaseReceivingReturn.return_date < start_date
        ).first()[0]

        if not past_sum_total_receiving_return_supply_price:
            past_sum_total_receiving_return_supply_price = 0

        # 결재
        past_sum_total_payment_price = db.session.query(
            db.func.sum(PurchasePayment.total_price)
        ).filter(
            PurchasePayment.client_company == client.name
        ).filter(
            PurchasePayment.payment_date < start_date
        ).first()[0]

        if not past_sum_total_payment_price:
            past_sum_total_payment_price = 0

        # 매입
        past_sum_total_statement_vat = db.session.query(
            db.func.sum(PurchaseStatement.vat)
        ).filter(
            PurchaseStatement.client_company == client.name
        ).filter(
            PurchaseStatement.statement_date < start_date
        ).first()[0]

        if not past_sum_total_statement_vat:
            past_sum_total_statement_vat = 0
        
        past_account_receivable = past_sum_total_receiving_supply_price - past_sum_total_receiving_return_supply_price - past_sum_total_payment_price + past_sum_total_statement_vat

        res = make_purchase_balance_detail_response(
            response_id=res_id,
            action_type='이월미지급금',
            action_date=start_date_one_day_ago,
            client_company=client.name,
            client_manager=client_manager,
            past_account_receivable=past_account_receivable
        )

        response['objects'].append(res)

        # 입고 리스트
        receiving_list = db.session.query(
            PurchaseReceiving
        ).filter(
            PurchaseReceiving.client_company == client.name
        ).filter(
            PurchaseReceiving.receiving_date >= start_date
        ).filter(
            PurchaseReceiving.receiving_date <= end_date
        ).all()

        for receiving in receiving_list:
            res_id += 1
            res = make_purchase_balance_detail_response(
                response_id=res_id,
                action_type='입고',
                action_date=receiving.receiving_date,
                client_company=client.name,
                client_manager=client_manager,
                purchase_price=receiving.supply_price,
                # vat=release.vat,
                total_purchase_price=receiving.supply_price,
                # total_sales_price=release.total_price,
                number=receiving.receiving_number
            )
            response['objects'].append(res)
        
        # 입고 반품 리스트
        receiving_return_list = db.session.query(
            PurchaseReceivingReturn
        ).filter(
            PurchaseReceivingReturn.client_company == client.name
        ).filter(
            PurchaseReceivingReturn.return_date >= start_date
        ).filter(
            PurchaseReceivingReturn.return_date <= end_date
        ).all()

        for receiving_return in receiving_return_list:
            res_id += 1
            res = make_purchase_balance_detail_response(
                response_id=res_id,
                action_type='반품',
                action_date=receiving_return.return_date,
                client_company=client.name,
                client_manager=client_manager,
                purchase_price= -receiving_return.supply_price,
                total_purchase_price=-receiving_return.supply_price,
                number=receiving_return.return_number
            )
            response['objects'].append(res)

        #결재
        payment_list = db.session.query(
            PurchasePayment
        ).filter(
            PurchasePayment.client_company == client.name
        ).filter(
            PurchasePayment.payment_date >= start_date
        ).filter(
            PurchasePayment.payment_date <= end_date
        ).all()

        for payment in payment_list:
            res_id += 1
            res = make_purchase_balance_detail_response(
                response_id=res_id,
                action_type='결재',
                action_date=payment.payment_date,
                client_company=client.name,
                client_manager=client_manager,
                payment_price=payment.total_price,
                number=payment.payment_number,
            )
            response['objects'].append(res)

        #매입계산서 부가세 리스트
        statement_list = db.session.query(
            PurchaseStatement
        ).filter(
            PurchaseStatement.client_company == client.name
        ).filter(
            PurchaseStatement.statement_date >= start_date
        ).filter(
            PurchaseStatement.statement_date <= end_date
        ).all()

        for statement in statement_list:
            res_id += 1
            res = make_purchase_balance_detail_response(
                response_id=res_id,
                action_type='계산서 부가세',
                action_date=statement.statement_date,
                client_company=client.name,
                client_manager=client_manager,
                vat=statement.vat,
                vat_adjustment= -statement.vat_adjustment,
                number=statement.statement_number
            )
            response['objects'].append(res)


        response['objects'] = sorted(response['objects'], key=(lambda x: x['action_date']))
    else:
        return make_response(response, 404)

    return make_response(response, 200)

@app.route("/api/mes/v1/purchase/balance", methods=["GET"])
def get_purchase_purchase_balance():
    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        return make_response(jsonify('No Parameters'), 400)

    start_date = parameter_dict['start']
    end_date = parameter_dict['end']

    response = dict()
    response['objects'] = []

    res_id = 0
    from datetime import datetime, timedelta
    from backend_model.table_base import BaseClient
    tmp = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    balance_date = tmp.strftime('%Y-%m-01 00:00:00')
   

    clients = db.session.query(BaseClient).all()
    for client in clients:

        past_receiving_supply_price = db.session.query(
            db.func.sum(PurchaseReceiving.supply_price)
        ).filter(
            PurchaseReceiving.client_company == client.name
        ).filter(
            PurchaseReceiving.receiving_date < start_date
        ).first()[0]
        if not past_receiving_supply_price:
            past_receiving_supply_price = 0

        past_receiving_return_supply_price = db.session.query(
            db.func.sum(PurchaseReceivingReturn.supply_price)
        ).filter(
            ShipmentReleaseReturn.client_company == client.name
        ).filter(
            ShipmentReleaseReturn.return_date < start_date
        ).first()[0]
        if not past_receiving_return_supply_price:
            past_receiving_return_supply_price = 0

        past_payment_price = db.session.query(
            db.func.sum(PurchasePayment.total_price)
        ).filter(
            PurchasePayment.client_company == client.name
        ).filter(
            PurchasePayment.payment_date < start_date
        ).first()[0]

        if not past_payment_price:
            past_payment_price = 0

        past_statement_vat = db.session.query(
            db.func.sum(PurchaseStatement.vat)
        ).filter(
            PurchaseStatement.client_company == client.name
        ).filter(
            PurchaseStatement.statement_date < start_date
        ).first()[0]

        if not past_statement_vat:
            past_statement_vat = 0

        search_receiving = db.session.query(
            db.func.sum(PurchaseReceiving.supply_price),
            db.func.sum(PurchaseReceiving.vat),
            db.func.sum(PurchaseReceiving.total_price)
        ).filter(
            PurchaseReceiving.client_company == client.name
        ).filter(
            PurchaseReceiving.receiving_date >= start_date
        ).filter(
            PurchaseReceiving.receiving_date <= end_date
        ).first()

        if not search_receiving:
            sum_receiving_price = 0
            sum_receiving_vat = 0
            sum_receiving_total_price = 0
        else:
            sum_receiving_price = search_receiving[0] if search_receiving[0] else 0
            sum_receiving_vat = search_receiving[1] if search_receiving[1] else 0
            sum_receiving_total_price = search_receiving[2] if search_receiving[2] else 0

        search_return = db.session.query(
            db.func.sum(PurchaseReceivingReturn.supply_price),
            db.func.sum(PurchaseReceivingReturn.vat),
            db.func.sum(PurchaseReceivingReturn.total_price)
        ).filter(
            PurchaseReceivingReturn.client_company == client.name
        ).filter(
            PurchaseReceivingReturn.return_date >= start_date
        ).filter(
            PurchaseReceivingReturn.return_date <= end_date
        ).first()
        if not search_return:
            sum_return_price = 0
            sum_return_vat = 0
            sum_return_total_price = 0
        else:
            sum_return_price =  search_return[0] if search_return[0] else 0
            sum_return_vat = search_return[1] if search_return[1] else 0
            sum_return_total_price = search_return[2] if search_return[2] else 0

        search_payment = db.session.query(
            db.func.sum(PurchasePayment.total_price)
        ).filter(
            PurchasePayment.client_company == client.name
        ).filter(
            PurchasePayment.payment_date >= start_date
        ).filter(
            PurchasePayment.payment_date <= end_date
        ).first()

        if not search_payment:
            sum_payment_price = 0
        else:
            sum_payment_price = search_payment[0] if search_payment[0] else 0

        search_statement= db.session.query(
            db.func.sum(PurchaseStatement.vat),
            db.func.sum(PurchaseStatement.vat_adjustment),
        ).filter(
            PurchaseStatement.client_company == client.name
        ).filter(
            PurchaseStatement.statement_date >= start_date
        ).filter(
            PurchaseStatement.statement_date <= end_date
        ).first()

        if not search_statement:
            sum_statement_vat = 0
            sum_statement_vat_abjustment = 0
        else:
            sum_statement_vat =  search_statement[0] if search_statement[0] else 0
            sum_statement_vat_abjustment = search_statement[1] if search_statement[1] else 0

        past_account_receivable = past_receiving_supply_price - past_receiving_return_supply_price - past_payment_price + past_statement_vat
        
        if past_account_receivable == 0 and \
            sum_receiving_price == 0 and sum_receiving_vat == 0 and sum_receiving_total_price == 0 and \
            sum_return_price == 0 and sum_return_vat == 0 and sum_return_total_price == 0 and \
            sum_payment_price == 0 and \
            sum_statement_vat == 0 and sum_statement_vat_abjustment == 0 :
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
            'purchase_price': sum_receiving_price - sum_return_price,
            'vat': sum_statement_vat,
            'vat_adjustment': sum_statement_vat_abjustment,
            'total_price': sum_receiving_price - sum_return_price + sum_statement_vat,
            'payment_price': sum_payment_price,
            'account_receivable': past_account_receivable + sum_receiving_price - sum_return_price - sum_payment_price + sum_statement_vat,
        }
        response['objects'].append(res)
        res_id += 1

    return make_response(response, 200)


def make_purchase_balance_detail_response(response_id, action_date, action_type, number='', client_company='', client_manager = '', past_account_receivable=0, purchase_price=0, vat=0, vat_adjustment=0, total_purchase_price=0, payment_price=0):
    res = {
        'id': response_id,
        'number': number,
        'action_date': action_date,
        'action_type': action_type,
        'company': client_company,
        'manager': client_manager,
        'past_account_receivable': past_account_receivable,
        'purchase_price': purchase_price,
        'vat': vat,
        'vat_adjustment': vat_adjustment,
        'total_purchase_price': total_purchase_price,
        'payment_price': payment_price,
        'group_id': action_date.strftime('%Y-%m')
    }
    return res
