# -*- coding: utf-8 -*-
print("module [backend.api_production] loaded")

import math
from backend import manager, check_token
from backend_model.table_production import *
from backend_model.table_base import BaseBOM
from backend_model.table_setup import SetupBasicStock
from backend_model.table_stock import StockMoveRequest, StockMoveRequestItem
from backend_model.table_purchase import PurchaseOrderPlan, PurchaseOrderPlanItem
from backend_lib.lib_base import LibBaseBom
from backend_lib.lib_common import LibCommon
from backend_lib.lib_production import LibProductionPlan, LibProductionPlanItem1, LibMeasureRequirement, \
    LibMeasureRequirementItem1, LibWorkOrder, LibWorkOrderItem1, LibPerformanceRegistration, \
    LibPerformanceRegistrationItem1, LibPerformanceRegistrationItem2, \
    LibProcessPerformanceRegistration

db = DBManager.db
# REST API(s) available :
#  - /api/v1/login
#  - /api/v1/logout


manager.create_api(ProductionPlan,
                   url_prefix='/api/mes/v1/production',
                   collection_name='production_plan',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibProductionPlan.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(ProductionPlanItem1,
                   url_prefix='/api/mes/v1/production',
                   collection_name='production_plan_item1',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibProductionPlanItem1.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token, LibProductionPlanItem1.delete_single_preprocessor]
                   },
                   postprocessors={
                       'GET_MANY': [LibProductionPlanItem1.get_many_postprocessor]
                   })

manager.create_api(MeasureRequirement,
                   url_prefix='/api/mes/v1/production',
                   collection_name='measure_requirement',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibMeasureRequirement.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })

manager.create_api(MeasureRequirementItem1,
                   url_prefix='/api/mes/v1/production',
                   collection_name='measure_requirement_item1',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibMeasureRequirementItem1.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(MeasureRequirementItem2,
                   url_prefix='/api/mes/v1/production',
                   collection_name='measure_requirement_item2',
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


manager.create_api(WorkOrder,
                   url_prefix='/api/mes/v1/production',
                   collection_name='work_order',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibWorkOrder.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(WorkOrderItem1,
                   url_prefix='/api/mes/v1/production',
                   collection_name='work_order_item1',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibWorkOrderItem1.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token, LibWorkOrderItem1.delete_single_preprocessor]
                   },
                   postprocessors={
                       'GET_MANY': [LibWorkOrderItem1.get_many_postprocessor],
                       'POST': [LibWorkOrderItem1.post_postprocessor]
                   })


manager.create_api(WorkOrderItem2,
                   url_prefix='/api/mes/v1/production',
                   collection_name='work_order_item2',
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


manager.create_api(PerformanceRegistration,
                   url_prefix='/api/mes/v1/production',
                   collection_name='performance_registration',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibPerformanceRegistration.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(PerformanceRegistrationItem1,
                   url_prefix='/api/mes/v1/production',
                   collection_name='performance_registration_item1',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibPerformanceRegistrationItem1.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token, LibPerformanceRegistrationItem1.delete_single_preprocessor]
                   },
                   postprocessors={
                       'GET_MANY': [LibPerformanceRegistrationItem1.get_many_postprocessor],
                       'POST': [LibPerformanceRegistrationItem1.post_postprocessor],
                       'PATCH_SINGLE': [LibPerformanceRegistrationItem1.patch_single_postprocessor]
                   })


manager.create_api(PerformanceRegistrationItem2,
                   url_prefix='/api/mes/v1/production',
                   collection_name='performance_registration_item2',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token, LibPerformanceRegistrationItem2.patch_single_preprocessor],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(ProcessPerformanceRegistration,
                   url_prefix='/api/mes/v1/production',
                   collection_name='process_performance_registration',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [LibProcessPerformanceRegistration.post_preprocessor],
                       'PATCH_SINGLE': [],
                       'GET_SINGLE': [],
                       'GET_MANY': [],
                       'DELETE_SINGLE': []
                   },
                   postprocessors={
                       'GET_MANY': [LibProcessPerformanceRegistration.get_many_postprocessor]
                   })


manager.create_api(ProcessMaterialConsumption,
                   url_prefix='/api/mes/v1/production',
                   collection_name='process_material_consumption',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   results_per_page=0,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


import datetime
from backend import app
from flask import make_response, jsonify, request, json, send_from_directory
from flask_restless import ProcessingException
from flask_restful import reqparse
from urllib.parse import urlparse


@app.route("/api/mes/v1/update-mea-req", methods=["POST"])
def update_mea_req():
    parser = reqparse.RequestParser()
    parser.add_argument("mea_req_id", type=int, location="json")
    parser.add_argument("warehouse_code", type=str, location="json")
    args = parser.parse_args()

    # 소요량계산2(소요량계산)을 모두 삭제한다
    delete_items = MeasureRequirementItem2.query.filter(
        MeasureRequirementItem2.fk_measure_requirement_id == args['mea_req_id']
    ).all()
    for delete_item in delete_items:
        db.session.delete(delete_item)
    db.session.commit()

    # 소요량계산1(생산계획)을 가져온다
    measure_items = db.session.query(
        MeasureRequirementItem1
    ).filter(
        MeasureRequirementItem1.fk_measure_requirement_id == args['mea_req_id']
    ).all()
    
    item_code_fied_items= {}
    for item in measure_items:
        params = [{
            'id': item.item.id,
            'count': item.production_plan_quantity
        }]
        leaf = LibBaseBom.find_bom(params)
        item_code_fied_items.update({bom_id: item_code_fied_items.get(bom_id, 0) + quantity for bom_id, quantity in leaf.items()})
    for bom_id, quantity in item_code_fied_items.items():
        bom = db.session.query(BaseBOM).filter(BaseBOM.id == bom_id).first()
        basic_stock = db.session.query(
            SetupBasicStock
        ).filter(
            SetupBasicStock.item_code == bom.item.item_code
        ).filter(
            SetupBasicStock.wh_code == args['warehouse_code']
        ).first()
        
        available_stock = 0
        if basic_stock:
            available_stock = basic_stock.available_stock
        
        plan_quantity = math.ceil(quantity) + bom.item.safety_stock - available_stock
        if plan_quantity < 0:
            plan_quantity = 0
        else:
            if bom.item.moq > 0:
                mul = int(int(plan_quantity) / int(bom.item.moq))
                if plan_quantity % bom.item.moq > 0:
                    mul += 1
                plan_quantity = bom.item.moq * mul
    
        from backend_lib.lib_base import LibBaseClient
        client_company = None
 
        client = LibBaseClient.get_main_client_company_by_item(bom.item.item_code)
  
        if client:
            client_company = client.name

        req = MeasureRequirementItem2(
                    item_code=bom.item.item_code,
                    requirement_quantity=quantity,
                    order_plan_quantity=plan_quantity,
                    unordered_plan_quantity=plan_quantity,
                    unit_price=bom.item.purchase_price,
                    supply_price=plan_quantity * round(bom.item.purchase_price),
                    client_company=client_company,
                    warehouse_code=args['warehouse_code'],
                    fk_measure_requirement_id=args['mea_req_id']
                )
        db.session.add(req)
    db.session.commit()
    # -- 수주별, 프로젝트 별 소요량 계산식
    #     classified_items = {}
    #     order_number = item.order_number
    #     if not order_number:
    #         order_number = 'null'
    #     project_number = item.project_number
    #     if not project_number:
    #         project_number = 'null'
    #     end_user = item.end_user
    #     if not end_user:
    #         end_user = 'null'

    #     if order_number in classified_items:
    #         if project_number in classified_items[order_number]:
    #             if end_user in classified_items[order_number][project_number]:
    #                 classified_items[order_number][project_number][end_user].append(item)
    #             else:
    #                 classified_items[order_number][project_number][end_user] = [item]
    #         else:
    #             classified_items[order_number][project_number] = {}
    #             classified_items[order_number][project_number][end_user] = [item]
    #     else:
    #         classified_items[order_number] = {}
    #         classified_items[order_number][project_number] = {}
    #         classified_items[order_number][project_number][end_user] = [item]

    # for order_number, classify_order_number in classified_items.items():
    #     for project_number, classify_project_number in classify_order_number.items():
    #         for end_user, classify_end_user in classify_project_number.items():
    #             params = [{
    #                 'id': item.item.id,
    #                 'count': item.production_plan_quantity
    #             } for item in classify_end_user]
    #             leaf = LibBaseBom.find_bom(params)
    #             bom_list = []
    #             item_code_list = []
    #             for bom_id, quantity in leaf.items():
    #                 bom = db.session.query(BaseBOM).filter(BaseBOM.id == bom_id).first()
    #                 bom_list.append({
    #                     'bom': bom,
    #                     'quantity': quantity
    #                 })
    #                 item_code_list.append(bom.item.item_code)
    #             for bom in bom_list:
    #                 basic_stock = db.session.query(
    #                     SetupBasicStock
    #                 ).filter(
    #                     SetupBasicStock.item_code == bom['bom'].item.item_code
    #                 ).filter(
    #                     SetupBasicStock.wh_code == args['warehouse_code']
    #                 ).first()

    #                 available_stock = 0
    #                 if basic_stock:
    #                     available_stock = basic_stock.available_stock

    #                 plan_quantity = bom['quantity'] + bom['bom'].item.safety_stock - available_stock
    #                 if plan_quantity < 0:
    #                     plan_quantity = 0
    #                 else:
    #                     if bom['bom'].item.moq > 0:
    #                         mul = int(int(plan_quantity) / int(bom['bom'].item.moq))
    #                         if plan_quantity % bom['bom'].item.moq > 0:
    #                             mul += 1
    #                         plan_quantity = bom['bom'].item.moq * mul
    #                 if order_number == 'null':
    #                     order_number = None
    #                 if project_number == 'null':
    #                     project_number = None
    #                 if end_user == 'null':
    #                     end_user = None

    #                 from backend_lib.lib_base import LibBaseClient
    #                 client_company = None
    #                 print(bom['bom'].item.item_code)
    #                 client = LibBaseClient.get_main_client_company_by_item(bom['bom'].item.item_code)
    #                 print(client)
    #                 if client:
    #                     client_company = client.name

    #                 req = MeasureRequirementItem2(
    #                     item_code=bom['bom'].item.item_code,
    #                     requirement_quantity=bom['quantity'],
    #                     order_plan_quantity=plan_quantity,
    #                     unordered_plan_quantity=plan_quantity,
    #                     unit_price=bom['bom'].item.purchase_price,
    #                     supply_price=plan_quantity * round(bom['bom'].item.purchase_price),
    #                     order_number=order_number,
    #                     project_number=project_number,
    #                     end_user=end_user,
    #                     client_company=client_company,
    #                     warehouse_code=args['warehouse_code'],
    #                     fk_measure_requirement_id=args['mea_req_id']
    #                 )
    #                 db.session.add(req)
    # db.session.commit()
    return make_response('success', 200)


@app.route("/api/mes/v1/export-mea-req", methods=["POST"])
def export_mea_req():
    parser = reqparse.RequestParser()
    parser.add_argument("mea_req_id", type=int, location="json")
    parser.add_argument("company_id", type=int, location="json")
    args = parser.parse_args()

    req = db.session.query(
        MeasureRequirement
    ).filter(
        MeasureRequirement.id == args['mea_req_id']
    ).first()

    req_items = db.session.query(
        MeasureRequirementItem2
    ).filter(
        MeasureRequirementItem2.fk_measure_requirement_id == args['mea_req_id']
    ).all()
    if len(req_items) > 0:
        # 발주계획 추가하기
        order_plan_number = LibCommon.create_item_number(PurchaseOrderPlan, PurchaseOrderPlan.order_plan_number,
                                                         '/purchase/order-plan', 'ORDERPLAN', req.fk_company_id)
        order_plan = PurchaseOrderPlan(
            order_plan_number=order_plan_number,
            order_plan_date=datetime.datetime.now(),
            order_plan_department=req.department,
            order_plan_manager=req.manager,
            fk_company_id=args['company_id']
        )
        db.session.add(order_plan)

        req.purchase_order_plan_number = order_plan_number
        req.closing_yn = 1
        db.session.commit()

        supply_price = 0
        for item in req_items:
            order_date = None
            if item.order_number:
                from backend_model.table_shipment import ShipmentOrder
                order = db.session.query(
                    ShipmentOrder
                ).filter(
                    ShipmentOrder.order_number == item.order_number
                ).first()
                if order:
                    order_date = order.order_date

            plan_item = PurchaseOrderPlanItem(
                item_code=item.item_code,
                order_plan_quantity=item.unordered_plan_quantity,
                unit_price=item.unit_price,
                supply_price=item.unordered_plan_quantity * item.unit_price,
                unordered_quantity=item.unordered_plan_quantity,
                main_supplier=item.client_company,
                delivery_date=item.delivery_date,
                order_number=item.order_number,
                order_date=order_date,
                end_user=item.end_user,
                warehouse_code=item.warehouse_code,
                fk_project_management_id=item.fk_project_management_id,
                fk_measure_requirement_item2_id=item.id,
                fk_purchase_order_plan_id=order_plan.id
            )
            db.session.add(plan_item)
            supply_price += (item.unordered_plan_quantity * item.unit_price)
        order_plan.supply_price = supply_price
        order_plan.total_price = supply_price
        db.session.commit()
    return make_response('success', 200)


@app.route("/api/mes/v1/update-excution-to-work-order", methods=["POST"])
def update_excution_to_work_order():
    parser = reqparse.RequestParser()
    parser.add_argument("work_order_id", type=int, location="json")
    parser.add_argument("warehouse_code", type=str, location="json")
    parser.add_argument('excution_plan_ids', type=int, action='append')
    args = parser.parse_args()
    
    from backend_model.table_project import ProjectExcutionPlanItem
    from backend_lib.lib_base import LibBaseWarehouse
    default_warehouse = LibBaseWarehouse.get_warehouse_by_name('현장창고')
    valid_items = {}
    item_code_list = []
    plan_items = db.session.query(
        ProjectExcutionPlanItem
    ).filter(
        ProjectExcutionPlanItem.fk_project_excution_plan_id.in_(args['excution_plan_ids'])
    ).all()

    for plan_item in plan_items:
        if plan_item.delivery_primary_quantity <= 0:
            continue
        if plan_item.item_code in valid_items:
            valid_items[plan_item.item_code]['quantity'] += plan_item.delivery_primary_quantity
        else:
            valid_items[plan_item.item_code] = {
                'quantity' : plan_item.delivery_primary_quantity,
                'item' : plan_item.item,
                'client_company' : plan_item.main_supplier,
            }
            item_code_list.append(plan_item.item_code)

    update_req = db.session.query(
        WorkOrderItem2
    ).filter(
        WorkOrderItem2.fk_work_order_id == args['work_order_id']
    ).filter(
        WorkOrderItem2.item_code.in_(item_code_list)
    ).all()

    for _item_code, _item in valid_items.items():
        is_update = False
        for req in update_req:
            if _item_code == req.item_code:
                is_update = True
                req.required_quantity = _item['quantity'],
                req.delivery_request_quantity = _item['quantity'],
                req.uninput_quantity = _item['quantity'],
                req.warehouse_code = args['warehouse_code'],
                req.client_company = _item['client_company'],
                req.in_warehouse_code=default_warehouse.wh_code,
        if is_update is False:
            req = WorkOrderItem2(
                item_code = _item_code,
                required_quantity = _item['quantity'],
                delivery_request_quantity = _item['quantity'],
                uninput_quantity = _item['quantity'],
                client_company =_item['client_company'],
                warehouse_code=args['warehouse_code'],
                in_warehouse_code=default_warehouse.wh_code,
                fk_work_order_id=args['work_order_id']
            )
            db.session.add(req)

    deletes = WorkOrderItem2.query.filter(
        WorkOrderItem2.fk_work_order_id == args['work_order_id']
    ).filter(
        WorkOrderItem2.item_code.notin_(item_code_list)
    ).all()
    for del_item in deletes:
        db.session.delete(del_item)
    db.session.commit()
        
    return make_response('success', 200)

@app.route("/api/mes/v1/update-work-order", methods=["POST"])
def update_work_order():
    parser = reqparse.RequestParser()
    parser.add_argument("work_order_id", type=int, location="json")
    parser.add_argument("warehouse_code", type=str, location="json")
    args = parser.parse_args()

    from backend_lib.lib_util import LibUtil
    from backend_model.table_base import BaseClientItem, BaseClient

    # 작업지시1을 가져온다
    order_items = db.session.query(
        WorkOrderItem1
    ).filter(
        WorkOrderItem1.fk_work_order_id == args['work_order_id']
    ).all()
    # 작업지시1의 품목을 리스트로 만든다
    params = [{
        'id': item.item.id,
        'count': item.unproduced_quantity,
        'warehouse': item.warehouse_code
    } for item in order_items]
    # 작업지시1의 품목 리스트를 이용해 BOM의 필요 자재와 양을 가져온다
    leaf = LibBaseBom.find_bom(params)
    bom_list = []
    item_code_list = []
    for bom_id, quantity in leaf.items():
        bom = db.session.query(BaseBOM).filter(BaseBOM.id == bom_id).first()
        client_item = db.session.query(
            BaseClientItem
        ).filter(
            BaseClientItem.item_code == bom.item.item_code
        ).filter(
            BaseClientItem.main_supplier == 1
        ).first()
        if client_item:
            client = db.session.query(
                BaseClient
            ).filter(
                BaseClient.id == client_item.client_id
            ).first()

            bom_list.append({
                'bom': bom,
                'quantity': LibUtil.ceil(quantity, 3),
                'client_company': client.name
            })
        else:
            bom_list.append({
                'bom': bom,
                'quantity': LibUtil.ceil(quantity, 3),
                'client_company': None
            })
        item_code_list.append(bom.item.item_code)

    from backend_lib.lib_base import LibBaseWarehouse
    default_warehouse = LibBaseWarehouse.get_warehouse_by_name('공장창고')

    # 업데이트할 목록
    update_req = db.session.query(
        WorkOrderItem2
    ).filter(
        WorkOrderItem2.fk_work_order_id == args['work_order_id']
    ).filter(
        WorkOrderItem2.item_code.in_(item_code_list)
    ).all()
    for bom in bom_list:
        is_update = False
        for req in update_req:  # 업데이트
            if bom['bom'].item.item_code == req.item_code:
                is_update = True

                req.required_quantity = bom['quantity']
                req.delivery_request_quantity = bom['quantity']
                req.uninput_quantity = math.ceil(bom['quantity'])
                req.warehouse_code = args['warehouse_code']
                req.client_company = bom['client_company']
        if is_update is False:  # 새로 추가
            req = WorkOrderItem2(
                item_code=bom['bom'].item.item_code,
                required_quantity=bom['quantity'],
                delivery_request_quantity=bom['quantity'],
                uninput_quantity=math.ceil(bom['quantity']),
                client_company=bom['client_company'],
                warehouse_code=args['warehouse_code'],
                in_warehouse_code=default_warehouse.wh_code,
                fk_work_order_id=args['work_order_id']
            )
            db.session.add(req)

    # 삭제할 목록
    deletes = WorkOrderItem2.query.filter(
        WorkOrderItem2.fk_work_order_id == args['work_order_id']
    ).filter(
        WorkOrderItem2.item_code.notin_(item_code_list)
    ).all()
    for del_item in deletes:
        db.session.delete(del_item)
    db.session.commit()

    return make_response('success', 200)


@app.route("/api/mes/v1/export-work-order", methods=["POST"])
def export_work_order():
    parser = reqparse.RequestParser()
    parser.add_argument("work_order_id", type=int, location="json")
    args = parser.parse_args()

    work_order_id = args['work_order_id']
    work_order = db.session.query(
        WorkOrder
    ).filter(
        WorkOrder.id == work_order_id
    ).first()

    work_order_items = db.session.query(
        WorkOrderItem2
    ).filter(
        WorkOrderItem2.fk_work_order_id == work_order_id
    ).all()
    if len(work_order_items) > 0:
        # 재고이동요청추가
        stock_move_number = LibCommon.create_item_number(StockMoveRequest, StockMoveRequest.number,
                                                         '/stock/move-request', 'STKMV', work_order.fk_company_id)
        stock_move = StockMoveRequest(
            number=stock_move_number,
            target_date=datetime.datetime.now(),
            department=work_order.department,
            manager=work_order.manager,
            fk_company_id=work_order.fk_company_id
        )
        db.session.add(stock_move)
        db.session.commit()

        from backend_lib.lib_base import LibBaseWarehouse
        default_warehouse = LibBaseWarehouse.get_warehouse_by_name('현장창고')

        for item in work_order_items:
            stock_item = StockMoveRequestItem(
                item_code=item.item_code,
                quantity=item.delivery_request_quantity,
                unit_price=item.item.purchase_price,
                unit=item.item.unit,
                supply_price=item.delivery_request_quantity * round(item.item.purchase_price),
                client_company=item.client_company,
                out_warehouse=item.warehouse_code,
                in_warehouse=default_warehouse.wh_code,
                asset_type=item.item.asset_type,
                not_shipped=math.ceil(item.delivery_request_quantity),
                fk_work_order_id=work_order_id,
                fk_work_order_item_id=item.id,
                fk_stock_move_request_id=stock_move.id
            )
            db.session.add(stock_item)

        work_order.stock_move_request_number = stock_move_number
        work_order.closing_yn = 1
        db.session.commit()
    return make_response('success', 200)


@app.route("/api/mes/v1/update-perf-reg", methods=["POST"])
def update_performance_registration():  # 자재소모 재계산
    parser = reqparse.RequestParser()
    parser.add_argument("perf_reg_id", type=int, location="json")
    parser.add_argument("warehouse_code", type=str, location="json")
    args = parser.parse_args()

    from backend_lib.lib_setup import LibSetupBasicStock

    # 작업지시1을 가져온다
    register_items = db.session.query(
        PerformanceRegistrationItem1
    ).filter(
        PerformanceRegistrationItem1.fk_performance_registration_id == args['perf_reg_id']
    ).all()
    for reg in register_items:
        # 재고를 업데이트한다
        LibSetupBasicStock.update_stock_by_item_code(reg.item_code, reg.warehouse_code)

    # 생산입고1의 품목을 리스트로 만든다
    params = [{
        'id': item.item.id,
        'count': item.production_receiving_quantity
    } for item in register_items]
    # 생산입고1의 품목 리스트를 이용해 BOM의 필요 자재와 양을 가져온다
    leaf = LibBaseBom.find_bom(params)
    bom_list = []
    item_code_list = []
    for bom_id, quantity in leaf.items():
        bom = db.session.query(BaseBOM).filter(BaseBOM.id == bom_id).first()
        bom_list.append({
            'bom': bom,
            'quantity': quantity
        })
        item_code_list.append(bom.item.item_code)

    # 소모자재 차감
    update_req = db.session.query(
        PerformanceRegistrationItem2
    ).filter(
        PerformanceRegistrationItem2.fk_performance_registration_id == args['perf_reg_id']
    ).all()
    for req in update_req:
        db.session.delete(req)

    from backend_lib.lib_base import LibBaseWarehouse
    default_warehouse = LibBaseWarehouse.get_warehouse_by_name('공장창고')
    warehouse_code = ''
    if default_warehouse:
        warehouse_code = default_warehouse.wh_code

    for bom in bom_list:
        req = PerformanceRegistrationItem2(
            item_code=bom['bom'].item.item_code,
            material_quantity=bom['quantity'],
            warehouse_code=warehouse_code,
            fk_performance_registration_id=args['perf_reg_id']
        )
        db.session.add(req)

        basic_stock = LibSetupBasicStock.get_basic_stock(req.item_code, req.warehouse_code)
        if basic_stock:
            basic_stock.current_stock -= req.material_quantity
            basic_stock.available_stock -= req.material_quantity

            # 마이너스 수불 처리 가능 여부 확인
            from backend_lib.lib_setup import LibSetupControl
            LibSetupControl.check_minus_stock(basic_stock.fk_company_id, basic_stock.current_stock)

    perform = db.session.query(
        PerformanceRegistration
    ).filter(
        PerformanceRegistration.id == args['perf_reg_id']
    ).first()
    if perform:
        perform.closing_yn = 1
    db.session.commit()

    return make_response('success', 200)
