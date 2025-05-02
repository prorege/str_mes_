# -*- coding: utf-8 -*-

import math
import datetime
from decimal import Decimal
from flask import make_response, jsonify, request, json, send_from_directory
from flask_restful import reqparse

from sqlalchemy import or_

from backend import app, manager, check_token
from backend_model.table_cost import *
from backend_lib.cost.lib_cost_statistics import LibCostStatistics

print("module [backend.api_cost] loaded")

db = DBManager.db
# REST API(s) available :
#  - /api/v1/login
#  - /api/v1/logout


manager.create_api(CostClosingHistory,
                   url_prefix='/api/mes/v1/cost',
                   collection_name='closing',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })
@app.route("/api/mes/v1/cost/produce-sales-cost-status")
def produce_sales_cost_status():
    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        return make_response(jsonify('No Parameters'), 400)

    start_date = parameter_dict['start']
    end_date = parameter_dict['end']

    from backend_model.table_shipment import ShipmentRelease, ShipmentReleaseItem, ShipmentReleaseReturn, ShipmentReleaseReturnItem
    from backend_model.table_base import BaseItem
    from sqlalchemy import func, extract, text
    response = {'objects': [], 'result': ''}
    shipmentRelease = db.session.query(
         func.DATE_FORMAT(ShipmentRelease.release_date, '%Y-%m').label('date'),
         BaseItem.item_code,
         BaseItem.main_category,
         BaseItem.item_name,
         ShipmentReleaseItem.unit_price,
         db.func.sum(ShipmentReleaseItem.release_quantity).label('total_quantity'),
         db.func.sum(ShipmentReleaseItem.unit_price * ShipmentReleaseItem.release_quantity).label('total_price'),
    ).join(
        ShipmentRelease, ShipmentRelease.id == ShipmentReleaseItem.fk_release_id
    ).join(
        BaseItem, ShipmentReleaseItem.item_code == BaseItem.item_code
    ).filter(
        ShipmentReleaseItem.release.has(ShipmentRelease.release_date >= start_date)
    ).filter(
        ShipmentReleaseItem.release.has(ShipmentRelease.release_date <= end_date)
    ).group_by(
        extract('month', ShipmentRelease.release_date),
        ShipmentReleaseItem.unit_price,
        ShipmentReleaseItem.item_code
    )
    shipmentReleaseReturn = db.session.query(
        func.DATE_FORMAT(ShipmentReleaseReturn.return_date, '%Y-%m').label('date'),
        BaseItem.item_code,
        BaseItem.main_category,
        BaseItem.item_name,
        ShipmentReleaseReturnItem.unit_price,
        -(db.func.sum(ShipmentReleaseReturnItem.return_quantity).label('total_quantity')),
        -(db.func.sum(ShipmentReleaseReturnItem.unit_price * ShipmentReleaseReturnItem.return_quantity).label('total_price')),
    ).join(
        ShipmentReleaseReturn, ShipmentReleaseReturnItem.fk_release_return_id == ShipmentReleaseReturn.id
    ).join(
        BaseItem, ShipmentReleaseReturnItem.item_code == BaseItem.item_code
    ).filter(
        ShipmentReleaseReturnItem.release_return.has(ShipmentReleaseReturn.return_date >= start_date)
    ).filter(
        ShipmentReleaseReturnItem.release_return.has(ShipmentReleaseReturn.return_date <= end_date)
    ).group_by(
        extract('month', ShipmentReleaseReturn.return_date),
        ShipmentReleaseReturnItem.unit_price,
        ShipmentReleaseReturnItem.item_code,
    )

    result_date = shipmentRelease.union(shipmentReleaseReturn).order_by(
        text('date ASC'), 
        BaseItem.main_category.asc(),
        BaseItem.item_code.asc()
    ).all()

    release_item_code_list = [item.item_code for item in result_date]

    # # 검색기간내 출고품목들의 Prent_id(Bom_id), item_id, item_code, type list
    from backend_model.table_base import BaseBOM, BaseBOMLink, BaseItem
    bom_products = db.session.query(
        BaseBOMLink.parent_id,
        BaseBOM.item_id,
        BaseItem.item_code,
        BaseItem.asset_type,
        BaseItem.main_category,
    ).join(
        BaseBOM, BaseBOM.id == BaseBOMLink.parent_id
    ).join(
        BaseItem, BaseItem.id == BaseBOM.item_id
    ).filter(
        BaseItem.item_code.in_(release_item_code_list)
    ).group_by(
        BaseBOMLink.parent_id
    ).all()

    item_code_detail = {}
    for product in bom_products:

        bom_children = get_bom_children(bom_parent_id=product.parent_id)

        #자재원가
        part_cost = calculate_part_cost(bom_children=bom_children)

        from backend_model.table_base import BaseBOM, BaseItem, BaseBOMProcess
        from sqlalchemy import cast, Numeric
        bom_processes = db.session.query(
            BaseItem.item_code,
            cast(BaseBOMProcess.price * BaseBOMProcess.ct, Numeric(10, 2)).label('total_price'),
            BaseBOMProcess.ct,
        ).join(
            BaseBOM, BaseBOM.id == BaseBOMProcess.bom_id
        ).join(
            BaseItem, BaseItem.id == BaseBOM.item_id
        ).filter(
            BaseBOMProcess.bom_id == product.parent_id
        ).filter(
            BaseBOMProcess.ct.isnot(None), BaseBOMProcess.ct != 0
        ).first()
 
        labor_cost = Decimal('0.00')
        ct = Decimal('0.00')
        if bom_processes:
            labor_cost = bom_processes[1]
            ct = bom_processes[2]
        item_code_detail[product.item_code] = [part_cost, labor_cost, ct]
        
    uid = 0
    for release_item in result_date:
        item_code = release_item.item_code
        detail = item_code_detail.get(item_code)
        part_cost = Decimal('0.00'),
        labor_cost = Decimal('0.00'),
        ct = Decimal('0.00')
        if detail:
            part_cost = detail[0],
            labor_cost = detail[1],
            ct = detail[2]

        response['objects'].append({
            'id': uid,
            'date': release_item.date,
            'item_code': release_item.item_code,
            'main_category': release_item.main_category,
            'item_name': release_item.item_name,
            'sales_price': release_item.unit_price,
            'total_quantity': release_item.total_quantity,
            'total_price': release_item.total_price,
            'part_cost': part_cost,
            'labor_cost': labor_cost,
            'ct': ct
        })
        uid += 1
    return make_response(response, 200)
@app.route("/api/mes/v1/cost/profit-stock-status", methods=['GET'])
def profit_stock_get():
    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        return make_response(jsonify('No Parameters'), 400)

    start_date = parameter_dict['start']
    end_date = parameter_dict['end']

    from backend_model.table_shipment import ShipmentRelease, ShipmentReleaseItem, ShipmentReleaseReturn, ShipmentReleaseReturnItem
    from backend_model.table_base import BaseItem

    response = {'objects': [], 'result': ''}

    shipmentRelease = db.session.query(
         ShipmentReleaseItem,
         db.func.sum(ShipmentReleaseItem.release_quantity),
         db.func.sum(ShipmentReleaseItem.unit_price * ShipmentReleaseItem.release_quantity),
    ).join(
        BaseItem, ShipmentReleaseItem.item_code == BaseItem.item_code
    ).filter(
        ShipmentReleaseItem.release.has(ShipmentRelease.release_date >= start_date)
    ).filter(
        ShipmentReleaseItem.release.has(ShipmentRelease.release_date <= end_date)
    ).group_by(
        ShipmentReleaseItem.item_code
    ).order_by(
        BaseItem.main_category.asc()
    ).order_by(
        ShipmentReleaseItem.item_code.asc()
    )
    
    shipmentReleaseReturn = db.session.query(
        ShipmentReleaseReturnItem.item_code,
        db.func.sum(ShipmentReleaseReturnItem.return_quantity),
        db.func.sum(ShipmentReleaseReturnItem.unit_price * ShipmentReleaseReturnItem.return_quantity)
    ).filter(
        ShipmentReleaseReturnItem.release_return.has(ShipmentReleaseReturn.return_date >= start_date)
    ).filter(
        ShipmentReleaseReturnItem.release_return.has(ShipmentReleaseReturn.return_date <= end_date)
    ).group_by(
        ShipmentReleaseReturnItem.item_code
    ).all()

    return_item_list = {item[0] : [item[1], item[2]] for item in shipmentReleaseReturn}

    shipment_release_items = shipmentRelease.all()

    release_item_code_list = [item[0].item_code for item in shipment_release_items]
  
    bom_products = get_bom_from_item_list(item_code_list=release_item_code_list)

    dict_bom_products = {product.parent_id: product for product in bom_products}

    item_code_in_cost_price = {product.item_code: calculate_produce_total_cost(product, dict_bom_products) for product in bom_products}

    uid = 0
    for release_item in shipment_release_items:
        item_code = release_item[0].item_code
        return_item_data = return_item_list.get(item_code)
        if return_item_data:
            return_item_total_quantity = return_item_data[0]
            return_item_total_price = return_item_data[1]
        else:
            return_item_total_quantity = 0
            return_item_total_price = 0
        response['objects'].append({
            'id': uid,
            'item_code': release_item[0].item_code,
            'main_category': release_item[0].item.main_category,
            'item_name': release_item[0].item.item_name,
            'item_standard': release_item[0].item.item_standard,
            'total_quantity': release_item[1] - return_item_total_quantity,
            'total_price': release_item[2] - return_item_total_price,
            'cost_price': item_code_in_cost_price.get(release_item[0].item_code, release_item[0].item.purchase_price)
        })
        uid += 1

    return make_response(response, 200)

@app.route("/api/mes/v2/apply_cost", methods=["POST"])
def apply_cost_v2():
    from backend_lib.cost.lib_cost_closing import LibCostClosing

    parser = reqparse.RequestParser()
    parser.add_argument("history_id", type=str, location="json")
    parser.add_argument("start_date", type=str, location="json")
    parser.add_argument("end_date", type=str, location="json")
    parser.add_argument("item_code", type=str, location="json")
    parser.add_argument("warehouse_code", type=str, location="json")
    args = parser.parse_args()

    history_id = args['history_id']
    start_date = datetime.strptime(args['start_date'], '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(args['end_date'], '%Y-%m-%d %H:%M:%S')
    base_item_code = args['item_code']
    warehouse_code = args['warehouse_code']

    # 마감 기간 내 출고가 있는 모든 품목을 검색
    from backend_model.table_setup import SetupBasicStock
    query = db.session.query(SetupBasicStock)
    if warehouse_code and warehouse_code != '':
        query = query.filter(SetupBasicStock.wh_code == warehouse_code)
    if base_item_code and base_item_code != '':
        query = query.filter(SetupBasicStock.item_code == base_item_code)
    query = query.order_by(SetupBasicStock.item_code.asc())
    basic_stock_list = query.all()
    item_code_list = [basic_stock.item_code for basic_stock in basic_stock_list]
    release_datas = LibCostClosing.get_cost_release_quantity_n_price_list(
        item_code_list=item_code_list, warehouse_code=warehouse_code, start_date=start_date, end_date=end_date
    )
    for _release in release_datas:
        if _release.cost_price is None or _release.cost_price == 0:
            if _release.item_code in item_code_list:
                item_code_list.remove(_release.item_code)

    # 각 품목의 마감 원가 계산
    calculated_items = calculate_closing_cost(
        basic_stock_list=basic_stock_list,
        item_code_list=item_code_list,
        warehouse_code=warehouse_code,
        start_date=start_date,
        end_date=end_date
    )

    # 계산된 마감 원가를 품목의 매입가로 할당
    for _item_code, _item in sorted(calculated_items.items()):
        if _item['release_stock'] <= 0:
            continue
        if _item['closing_stock'] <= 0:
            query = db.session.query(
                SetupBasicStock
            ).filter(
                SetupBasicStock.item_code == _item_code
            )
            if warehouse_code and warehouse_code != '':
                query = query.filter(SetupBasicStock.wh_code == warehouse_code)
            basic_stock = query.first()
            if basic_stock:
                receiving_datas = LibCostClosing.get_cost_receiving_quantity_n_price_list(
                    item_code_list=[_item_code], warehouse_code=warehouse_code, start_date=start_date, end_date=end_date
                )
                if receiving_datas:
                    sum_stock = 0
                    sum_price = 0
                    for receiving in receiving_datas:
                        sum_stock += receiving.purchase_receiving_quantity + \
                                     receiving.stock_etc_receiving_quantity + \
                                     receiving.stock_move_receiving_quantity + \
                                     receiving.produce_receiving_quantity + \
                                     receiving.release_return_quantity + \
                                     receiving.import_clearance_quantity
                        sum_price += receiving.purchase_receiving_price + \
                                     receiving.stock_etc_receiving_price + \
                                     receiving.stock_move_receiving_price + \
                                     receiving.produce_receiving_price + \
                                     receiving.release_return_price + \
                                     receiving.import_clearance_price

                    price = Decimal(math.trunc((sum_price / sum_stock) * 100)) / Decimal(100)
                    update_base_item_purchase_price(item_code=_item_code, purchase_price=price)
            continue
        if _item['closing_price'] <= 0:
            continue

        price = Decimal(math.trunc((_item['closing_price'] / _item['closing_stock']) * 100)) / Decimal(100)
        update_base_item_purchase_price(item_code=_item_code, purchase_price=price)

    # 마감 기간 내 생산입고가 있는 품목 중 BOM이 생성되어 있는 품목의 제조원가를 품목의 매입가로 할당
    item_code_list = get_performance_registration_item_list_in_period(
        item_code=base_item_code, warehouse_code=warehouse_code, start_date=start_date, end_date=end_date)
    
    bom_child_bom_id_list = get_bom_child_item_list(item_code_list=item_code_list)
    child_bom_products = get_bom_from_item_list_in_child_bom_id(bom_child_bom_id_list=bom_child_bom_id_list)

    dict_child_bom_products = {}
    for _product in child_bom_products:
        dict_child_bom_products[_product.parent_id] = _product

    for _product in child_bom_products:
        produce_total_cost = calculate_produce_total_cost(product=_product, dict_bom_products=dict_child_bom_products)
        update_base_item_purchase_price(item_id=_product.item_id, purchase_price=produce_total_cost)

    bom_products = get_bom_from_item_list(item_code_list=item_code_list)

    dict_bom_products = {}
    for _product in bom_products:
        dict_bom_products[_product.parent_id] = _product

    update_item_list = []
    for _product in bom_products:
        produce_total_cost = calculate_produce_total_cost(product=_product, dict_bom_products=dict_bom_products)
        update_base_item_purchase_price(item_id=_product.item_id, purchase_price=produce_total_cost)
        update_item_list.append(_product.item_code)

    # 마감 기간 내 생산입고가 있는 품목 중 BOM이 생성되어 있는 품목의 제조원가를 생산입고 품목의 단가로 할당
    update_performance_registration_item1_cost_price(update_item_list=update_item_list,
                                                     warehouse_code=warehouse_code,
                                                     start_date=start_date,
                                                     end_date=end_date)

    # 마감 기간 내 출고가 있는 모든 품목의 출고 원가를 계산하여 할당 (원가마감)
    cost_closing(item_code=base_item_code, warehouse_code=warehouse_code, start_date=start_date, end_date=end_date)

    # 마감 기간 내 생산입고가 있는 품목의 마감 원가를 계산
    calculated_items = calculate_closing_cost(
        basic_stock_list=basic_stock_list,
        item_code_list=item_code_list,
        warehouse_code=warehouse_code,
        start_date=start_date,
        end_date=end_date
    )

    # 계산된 마감 원가를 품목의 매입가로 할당
    for _item_code, _item in sorted(calculated_items.items()):
        if _item['release_stock'] <= 0:
            continue
        if _item['closing_stock'] <= 0:
            query = db.session.query(
                SetupBasicStock
            ).filter(
                SetupBasicStock.item_code == _item_code
            )
            if warehouse_code and warehouse_code != '':
                query = query.filter(SetupBasicStock.wh_code == warehouse_code)
            basic_stock = query.first()
            if basic_stock:
                receiving_datas = LibCostClosing.get_cost_receiving_quantity_n_price_list(
                    item_code_list=[_item_code], warehouse_code=warehouse_code, start_date=start_date, end_date=end_date
                )
                if receiving_datas:
                    sum_stock = 0
                    sum_price = 0
                    for receiving in receiving_datas:
                        sum_stock += receiving.purchase_receiving_quantity + \
                                     receiving.stock_etc_receiving_quantity + \
                                     receiving.stock_move_receiving_quantity + \
                                     receiving.produce_receiving_quantity + \
                                     receiving.release_return_quantity + \
                                     receiving.import_clearance_quantity
                        sum_price += receiving.purchase_receiving_price + \
                                     receiving.stock_etc_receiving_price + \
                                     receiving.stock_move_receiving_price + \
                                     receiving.produce_receiving_price + \
                                     receiving.release_return_price + \
                                     receiving.import_clearance_price

                    price = Decimal(math.trunc((sum_price / sum_stock) * 100)) / Decimal(100)
                    update_base_item_purchase_price(item_code=_item_code, purchase_price=price)
            continue
        if _item['closing_price'] <= 0:
            continue

        price = Decimal(math.trunc((_item['closing_price'] / _item['closing_stock']) * 100)) / Decimal(100)
        update_base_item_purchase_price(item_code=_item_code, purchase_price=price)

    # 원가마감 히스토리에 마감재고원가적용 true로 업데이트
    LibCostClosing.set_cost_closing_history_applied(history_id)

    return make_response('success', 200)


@app.route("/api/mes/v2/close_cost", methods=["POST"])
def close_cost_v2():
    parser = reqparse.RequestParser()
    parser.add_argument("start_date", type=str, location="json")
    parser.add_argument("end_date", type=str, location="json")
    parser.add_argument("manager", type=str, location="json")
    parser.add_argument("company_id", type=int, location="json")
    parser.add_argument("warehouse_code", type=str, location="json")
    parser.add_argument("item_code", type=str, location="json")
    args = parser.parse_args()

    start_date = datetime.strptime(args['start_date'], '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(args['end_date'], '%Y-%m-%d %H:%M:%S')
    closing_manager = args['manager']
    company_id = args['company_id']
    warehouse_code = args['warehouse_code']
    item_code = args['item_code']

    # 원가 마감
    cost_closing(item_code=item_code, warehouse_code=warehouse_code, start_date=start_date, end_date=end_date)

    # 원가 마감 히스토리 추가
    from backend_lib.cost.lib_cost_closing import LibCostClosing
    closing_item = LibCostClosing.insert_cost_closing_history(
        start_date=start_date, end_date=end_date, manager=closing_manager, company_id=company_id, warehouse_code=warehouse_code
    )
    response = {
        'id': closing_item.id
    }

    return make_response(response, 200)


@app.route("/api/mes/v1/cost/statistics", methods=["GET"])
def cost_statistics_list():
    from backend_model.table_setup import SetupBasicStock

    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        return make_response(jsonify('No Parameters'), 400)

    start_date = datetime.strptime(parameter_dict['start'], '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(parameter_dict['end'], '%Y-%m-%d %H:%M:%S')
    warehouse_name = parameter_dict['wh_name']
    asset_type = parameter_dict['asset_type']
    category = parameter_dict['category']

    response = dict()
    response['objects'] = []
    response['result'] = ''

    # 1. 창고와 자산 구분, 품목 대분류로 품목 리스트를 뽑는다.
    query = db.session.query(SetupBasicStock)
    if warehouse_name and warehouse_name != '':
        query = query.filter(SetupBasicStock.warehouse.has(wh_name=warehouse_name))
    if asset_type and asset_type != '':
        query = query.filter(SetupBasicStock.item.has(asset_type=asset_type))
    if category and category != '':
        query = query.filter(SetupBasicStock.item.has(main_category=category))
    query = query.order_by(SetupBasicStock.item_code.asc())
    basic_stock_list = query.all()
    item_code_list = [basic_stock.item_code for basic_stock in basic_stock_list]

    from backend_lib.lib_base import LibBaseWarehouse
    warehouse = LibBaseWarehouse.get_warehouse_by_name(warehouse_name=warehouse_name)

    items = calculate_closing_cost(
        basic_stock_list=basic_stock_list,
        item_code_list=item_code_list,
        warehouse_code=warehouse.wh_code,
        start_date=start_date,
        end_date=end_date
    )

    for item_code, item in  sorted(items.items()):
        response['objects'].append(item)

    return make_response(response, 200)

@app.route("/api/mes/v1/cost/statistics/item", methods=["POST"])
def cost_statistics_item_warehouse():
    parser = reqparse.RequestParser()
    parser.add_argument("item_code", type=str, location="json")
    parser.add_argument("warehouse_name", type=str, location="json")
    parser.add_argument("start", type=str, location="json")
    parser.add_argument("end", type=str, location="json")
    args = parser.parse_args()

    if len(args) == 0:
        return make_response(jsonify('No Parameters'), 400)

    item_code = args['item_code']
    warehouse_name = args['warehouse_name']
    start_date = args['start']
    end_date = args['end']

    from backend_lib.lib_base import LibBaseWarehouse
    warehouse = LibBaseWarehouse.get_warehouse_by_name(warehouse_name=warehouse_name)
    if not warehouse:
        return make_response(jsonify('Invalid warehouse name'), 400)

    from backend_lib.lib_setup import LibSetupBasicStock
    basic_stock = LibSetupBasicStock.get_basic_stock(item_code=item_code, warehouse_code=warehouse.wh_code)
    if basic_stock is None:
        return make_response(jsonify('basic stock not exist'), 400)

    objects = LibCostStatistics.get_cost_statistics(basic_stock=basic_stock, start_date=start_date, end_date=end_date)
    response = {'objects': sorted(objects, key=(lambda x: x['action_date']))}
    return make_response(response, 200)

@app.route("/api/mes/v1/cost/correction", methods=["GET"])
def cost_correction_list():
    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        return make_response(jsonify('No Parameters'), 400)

    start_date = parameter_dict['start']
    end_date = parameter_dict['end']
    warehouse_name = parameter_dict['wh_name']
    asset_type = parameter_dict['asset_type']
    category = parameter_dict['category']

    response = dict()
    response['objects'] = []
    response['result'] = ''

    from backend_lib.lib_base import LibBaseWarehouse
    warehouse = LibBaseWarehouse.get_warehouse_by_name(warehouse_name=warehouse_name)

    from backend_model.table_shipment import ShipmentRelease, ShipmentReleaseItem

    query = db.session.query(
        ShipmentReleaseItem
    ).filter(
        ShipmentReleaseItem.warehouse_code == warehouse.wh_code
    ).filter(
        ShipmentReleaseItem.release.has(ShipmentRelease.release_date >= start_date)
    ).filter(
        ShipmentReleaseItem.release.has(ShipmentRelease.release_date <= end_date)
    )
    if asset_type:
        query = query.filter(ShipmentReleaseItem.item.has(asset_type=asset_type))
    if category:
        query = query.filter(ShipmentReleaseItem.item.has(main_category=category))
    shipment_release_items = query.all()

    uid = 0
    for release_item in shipment_release_items:
        response['objects'].append({
            'id': uid,
            'item_id': release_item.id,
            'release_date': release_item.release.release_date,
            'release_number': release_item.release.release_number,
            'category': release_item.item.main_category,
            'menu_type': '출고',
            'release_type': release_item.release.release_type,
            'item_code': release_item.item.item_code,
            'item_name': release_item.item.item_name,
            'item_standard': release_item.item.item_standard,
            'release_quantity': release_item.release_quantity,
            'unit_price': release_item.unit_price,
            'cost_price': release_item.cost_price
        })
        uid += 1

    from backend_model.table_stock import StockEtc, StockEtcItem
    query = db.session.query(
        StockEtcItem
    ).filter(
        StockEtcItem.type == '출고'
    ).filter(
        StockEtcItem.warehouse_code == warehouse.wh_code
    ).filter(
        StockEtcItem.stock_etc.has(StockEtc.target_date >= start_date)
    ).filter(
        StockEtcItem.stock_etc.has(StockEtc.target_date <= end_date)
    )
    if asset_type:
        query = query.filter(StockEtcItem.item.has(asset_type=asset_type))
    if category:
        query = query.filter(StockEtcItem.item.has(main_category=category))
    stock_etc_items = query.all()

    for etc_item in stock_etc_items:
        response['objects'].append({
            'id': uid,
            'item_id': etc_item.id,
            'release_date': etc_item.stock_etc.target_date,
            'release_number': etc_item.stock_etc.number,
            'category': etc_item.item.main_category,
            'menu_type': '기타출고',
            'release_type': etc_item.inout_type,
            'item_code': etc_item.item.item_code,
            'item_name': etc_item.item.item_name,
            'item_standard': etc_item.item.item_standard,
            'release_quantity': etc_item.quantity,
            'unit_price': etc_item.unit_price,
            'cost_price': etc_item.cost_price
        })
        uid += 1

    from backend_model.table_stock import StockMoveRelease, StockMoveReleaseItem
    query = db.session.query(
        StockMoveReleaseItem
    ).filter(
        StockMoveReleaseItem.out_warehouse == warehouse.wh_code
    ).filter(
        StockMoveReleaseItem.stock_move_release.has(StockMoveRelease.target_date >= start_date)
    ).filter(
        StockMoveReleaseItem.stock_move_release.has(StockMoveRelease.target_date <= end_date)
    )
    if asset_type:
        query = query.filter(StockMoveReleaseItem.item.has(asset_type=asset_type))
    if category:
        query = query.filter(StockMoveReleaseItem.item.has(main_category=category))
    stock_move_release_items = query.all()

    for move_item in stock_move_release_items:
        response['objects'].append({
            'id': uid,
            'item_id': move_item.id,
            'release_date': move_item.stock_move_release.target_date,
            'release_number': move_item.stock_move_release.number,
            'category': move_item.item.main_category,
            'menu_type': '재고이동출고',
            'release_type': '재고이동출고',
            'item_code': move_item.item.item_code,
            'item_name': move_item.item.item_name,
            'item_standard': move_item.item.item_standard,
            'release_quantity': move_item.release_quantity,
            'unit_price': move_item.unit_price,
            'cost_price': move_item.cost_price
        })
        uid += 1

    return make_response(response, 200)


def calculate_closing_cost(basic_stock_list, item_code_list: list, warehouse_code: str, start_date: datetime, end_date: datetime):
    from backend_lib.cost.lib_cost_closing import LibCostClosing
    # 출고 -------------------------------------------------------------------------------------------------------------
    past_release_datas = LibCostClosing.get_cost_release_quantity_n_price_list(
        item_code_list=item_code_list, warehouse_code=warehouse_code, end_date=start_date
    )

    # 입고 -------------------------------------------------------------------------------------------------------------
    past_receiving_datas = LibCostClosing.get_cost_receiving_quantity_n_price_list(
        item_code_list=item_code_list, warehouse_code=warehouse_code, end_date=start_date
    )
    items = {}  # { item_code: { item info } }
    for past_release in past_release_datas:
        sum_stock = past_release.shipment_release_quantity + \
                    past_release.stock_etc_release_quantity + \
                    past_release.stock_move_release_quantity + \
                    past_release.produce_release_quantity + \
                    past_release.purchase_return_quantity + \
                    past_release.export_comm_invoice_quantity
        sum_price = past_release.shipment_release_price + \
                    past_release.stock_etc_release_price + \
                    past_release.stock_move_release_price + \
                    past_release.produce_release_price + \
                    past_release.purchase_return_price + \
                    past_release.export_comm_invoice_price
        if past_release.item_code in items:
            items[past_release.item_code]['past_stock'] -= sum_stock
            items[past_release.item_code]['past_price'] -= sum_price
        else:
            items[past_release.item_code] = {
                'item_code': past_release.item_code,
                'past_stock': -sum_stock,
                'past_price': -sum_price,
                'release_stock': Decimal(0),
                'release_price': Decimal(0),
                'receiving_stock': Decimal(0),
                'receiving_price': Decimal(0),
            }
    for past_receiving in past_receiving_datas:
        sum_stock = past_receiving.purchase_receiving_quantity + \
                    past_receiving.stock_etc_receiving_quantity + \
                    past_receiving.stock_move_receiving_quantity + \
                    past_receiving.produce_receiving_quantity + \
                    past_receiving.release_return_quantity + \
                    past_receiving.import_clearance_quantity
        sum_price = past_receiving.purchase_receiving_price + \
                    past_receiving.stock_etc_receiving_price + \
                    past_receiving.stock_move_receiving_price + \
                    past_receiving.produce_receiving_price + \
                    past_receiving.release_return_price + \
                    past_receiving.import_clearance_price
        if past_receiving.item_code in items:
            items[past_receiving.item_code]['past_stock'] += sum_stock
            items[past_receiving.item_code]['past_price'] += sum_price
        else:
            items[past_receiving.item_code] = {
                'item_code': past_receiving.item_code,
                'past_stock': sum_stock,
                'past_price': sum_price,
                'release_stock': Decimal(0),
                'release_price': Decimal(0),
                'receiving_stock': Decimal(0),
                'receiving_price': Decimal(0),
            }

    # 출고 -------------------------------------------------------------------------------------------------------------
    release_datas = LibCostClosing.get_cost_release_quantity_n_price_list(
        item_code_list=item_code_list, warehouse_code=warehouse_code, start_date=start_date, end_date=end_date
    )

    # 입고 -------------------------------------------------------------------------------------------------------------
    receiving_datas = LibCostClosing.get_cost_receiving_quantity_n_price_list(
        item_code_list=item_code_list, warehouse_code=warehouse_code, start_date=start_date, end_date=end_date
    )
    for release in release_datas:
        sum_stock = release.shipment_release_quantity + \
                    release.stock_etc_release_quantity + \
                    release.stock_move_release_quantity + \
                    release.produce_release_quantity + \
                    release.purchase_return_quantity + \
                    release.export_comm_invoice_quantity
        sum_price = release.shipment_release_price + \
                    release.stock_etc_release_price + \
                    release.stock_move_release_price + \
                    release.produce_release_price + \
                    release.purchase_return_price + \
                    release.export_comm_invoice_price
        if release.item_code in items:
            items[release.item_code]['release_stock'] += sum_stock
            items[release.item_code]['release_price'] += sum_price
        else:
            items[release.item_code] = {
                'item_code': release.item_code,
                'past_stock': Decimal(0),
                'past_price': Decimal(0),
                'release_stock': sum_stock,
                'release_price': sum_price,
                'receiving_stock': Decimal(0),
                'receiving_price': Decimal(0),
            }
    for receiving in receiving_datas:
        sum_stock = receiving.purchase_receiving_quantity + \
                    receiving.stock_etc_receiving_quantity + \
                    receiving.stock_move_receiving_quantity + \
                    receiving.produce_receiving_quantity + \
                    receiving.release_return_quantity + \
                    receiving.import_clearance_quantity
        sum_price = receiving.purchase_receiving_price + \
                    receiving.stock_etc_receiving_price + \
                    receiving.stock_move_receiving_price + \
                    receiving.produce_receiving_price + \
                    receiving.release_return_price + \
                    receiving.import_clearance_price
        if receiving.item_code in items:
            items[receiving.item_code]['receiving_stock'] += sum_stock
            items[receiving.item_code]['receiving_price'] += sum_price
        else:
            items[receiving.item_code] = {
                'item_code': receiving.item_code,
                'past_stock': Decimal(0),
                'past_price': Decimal(0),
                'release_stock': Decimal(0),
                'release_price': Decimal(0),
                'receiving_stock': sum_stock,
                'receiving_price': sum_price,
            }

    result_id = 0
    for basic_stock in basic_stock_list:
        if not basic_stock.item:
            continue

        if basic_stock.item_code in items:
            items[basic_stock.item_code]['id'] = result_id
            items[basic_stock.item_code]['asset_type'] = basic_stock.item.asset_type  # 자산 구분
            items[basic_stock.item_code]['item_id'] = basic_stock.item.id  # 품목 아이디
            items[basic_stock.item_code]['item_name'] = basic_stock.item.item_name  # 품목 이름
            items[basic_stock.item_code]['item_standard'] = basic_stock.item.item_standard  # 품목 규격
            items[basic_stock.item_code]['available_stock'] = basic_stock.available_stock  # 가용 재고
            items[basic_stock.item_code]['current_stock'] = basic_stock.current_stock  # 현재고
            items[basic_stock.item_code]['safety_stock'] = basic_stock.item.safety_stock  # 안전 재고
            items[basic_stock.item_code]['main_category'] = basic_stock.item.main_category  # 품목 대분류
            items[basic_stock.item_code]['middle_category'] = basic_stock.item.middle_category  # 품목 중분류
            items[basic_stock.item_code]['sub_category'] = basic_stock.item.sub_category  # 품목 소분류
            items[basic_stock.item_code]['past_stock'] += basic_stock.basic_stock  # 이월 재고
            items[basic_stock.item_code]['past_price'] += Decimal(basic_stock.item_price)  # 이월 금액
            # 마감 재고
            items[basic_stock.item_code]['closing_stock'] = items[basic_stock.item_code]['past_stock'] + \
                                                            items[basic_stock.item_code]['receiving_stock'] - \
                                                            items[basic_stock.item_code]['release_stock']
            # 마감 금액
            items[basic_stock.item_code]['closing_price'] = items[basic_stock.item_code]['past_price'] + \
                                                            items[basic_stock.item_code]['receiving_price'] - \
                                                            items[basic_stock.item_code]['release_price']
        else:
            if basic_stock.basic_stock <= 0 and basic_stock.item_price <= 0:
                continue

            items[basic_stock.item_code] = {
                'id': result_id,
                'item_code': basic_stock.item_code,
                'asset_type': basic_stock.item.asset_type,  # 자산 구분
                'item_id': basic_stock.item.id,  # 품목 아이디
                'item_name': basic_stock.item.item_name,  # 품목 이름
                'item_standard': basic_stock.item.item_standard,  # 품목 규격
                'available_stock': basic_stock.available_stock,  # 가용 재고
                'current_stock': basic_stock.current_stock,  # 현재고
                'safety_stock': basic_stock.item.safety_stock,  # 안전 재고
                'main_category': basic_stock.item.main_category,  # 품목 대분류
                'middle_category': basic_stock.item.middle_category,  # 품목 중분류
                'sub_category': basic_stock.item.sub_category,  # 품목 소분류
                'past_stock': basic_stock.basic_stock,  # 이월 재고
                'past_price': Decimal(basic_stock.item_price),  # 이월 금액
                'release_stock': Decimal(0),  # 출고량
                'release_price': Decimal(0),  # 출고 원가 금액
                'receiving_stock': Decimal(0),  # 입고량
                'receiving_price': Decimal(0),  # 입고 금액
                'closing_stock': basic_stock.basic_stock,  # 마감 재고
                'closing_price': Decimal(basic_stock.item_price),  # 마감 금액
            }
        result_id += 1
    return items


def calculate_produce_total_cost(product, dict_bom_products: dict) -> Decimal:
    """
    제조원가 계산
    :return:
    """

    import math

    subfix = get_item_subfix(item_code=product.item_code)
    produce_cost_rate = get_produce_cost_rate(subfix=subfix)

    bom_children = get_bom_children(bom_parent_id=product.parent_id)
    part_cost = calculate_part_cost(bom_children=bom_children)
    product_list = get_bom_products(
        bom_parent_id=product.parent_id, bom_children=bom_children, dict_bom_products=dict_bom_products)

    bom_processes = get_bom_processes(product_list=product_list)
    labor_cost = calculate_labor_cost(bom_processes=bom_processes, product_item_code=product.item_code)
    produce_cost = calculate_produce_cost(subfix=subfix, part_cost=part_cost, labor_cost=labor_cost, produce_cost_rate=produce_cost_rate)

    produce_total_cost = part_cost + labor_cost + produce_cost

    return Decimal(math.trunc(produce_total_cost * 100)) / Decimal('100')


def get_bom_children(bom_parent_id: int):
    from backend_model.table_base import BaseBOM, BaseBOMLink, BaseItem
    bom_children = db.session.query(
        BaseBOMLink.child_id,
        BaseBOMLink.requirement,
        BaseBOM.item_id,
        BaseItem.item_code,
        BaseItem.purchase_price,
    ).join(
        BaseBOM, BaseBOM.id == BaseBOMLink.child_id
    ).join(
        BaseItem, BaseItem.id == BaseBOM.item_id
    ).filter(
        BaseBOMLink.parent_id == bom_parent_id
    ).all()
    return bom_children


def get_bom_products(bom_parent_id: int, bom_children, dict_bom_products: dict) -> list:
    product_list = [bom_parent_id]
    for bom_child in bom_children:
        if bom_child.child_id in dict_bom_products:
            product_list.append(bom_child.child_id)
    return product_list


def get_bom_processes(product_list: list):
    from backend_model.table_base import BaseBOM, BaseItem, BaseBOMProcess
    bom_processes = db.session.query(
        BaseBOMProcess.id,
        BaseBOMProcess.price,
        BaseBOMProcess.ct,
        BaseItem.item_code,
        BaseItem.asset_type
    ).join(
        BaseBOM, BaseBOM.id == BaseBOMProcess.bom_id
    ).join(
        BaseItem, BaseItem.id == BaseBOM.item_id
    ).filter(
        BaseBOMProcess.bom_id.in_(product_list)
    ).all()
    return bom_processes


def calculate_part_cost(bom_children) -> Decimal:
    import math

    part_cost = Decimal('0.0')
    for bom_child in bom_children:
        part_cost = Decimal(f'{part_cost}') + \
                    (Decimal(f'{bom_child.purchase_price}') * Decimal(f'{bom_child.requirement}'))
    part_cost = Decimal(math.floor(part_cost * Decimal(100))) / Decimal(100)
    return part_cost


def calculate_labor_cost(bom_processes, product_item_code: str) -> Decimal:
    import math
    labor_cost = Decimal('0.0')
    for process in bom_processes:
        if not process.price or not process.ct:
            continue
        if product_item_code == process.item_code:
            labor_cost = Decimal(f'{labor_cost}') + Decimal(f'{process.price}') * Decimal(f'{process.ct}')
        elif process.asset_type == '제품':
            labor_cost = Decimal(f'{labor_cost}') + Decimal(f'{process.price}') * Decimal(f'{process.ct}')
    labor_cost = math.floor(labor_cost * Decimal(100)) / Decimal(100)
    return labor_cost


def calculate_produce_cost(subfix: str, part_cost: Decimal, labor_cost: Decimal, produce_cost_rate: int) -> Decimal:
    import math
    if subfix == '/HS':
        produce_cost = Decimal(f'{labor_cost}') * (Decimal(f'{produce_cost_rate}') / Decimal('100'))
    else:
        produce_cost = (Decimal(f'{part_cost}') + Decimal(f'{labor_cost}')) * (
                    Decimal(f'{produce_cost_rate}') / Decimal('100'))
    produce_cost = math.floor(produce_cost * Decimal(100)) / Decimal(100)
    return produce_cost


def get_item_subfix(item_code: str) -> str:
    import re
    pattern = re.compile(r'/(C|HS|MO|O|V)')
    matches = pattern.findall(item_code)
    if matches and len(matches) > 0:
        subfix = f'/{matches[0]}'
    else:
        subfix = ''
    return subfix


def get_produce_cost_rate(subfix: str) -> int:
    from backend_model.table_setup import SetupProduceCost
    setup_produce_cost = db.session.query(
        SetupProduceCost
    ).filter(
        SetupProduceCost.year == datetime.now().strftime('%Y')
    ).filter(
        SetupProduceCost.subfix == subfix
    ).first()
    return setup_produce_cost.produce_cost_rate


def update_base_item_purchase_price(item_id: int = None, item_code: str = None, purchase_price: Decimal = 0):
    from backend_model.table_base import BaseItem
    query = db.session.query(BaseItem)
    if item_id is not None:
        query = query.filter(BaseItem.id == item_id)
    if item_code is not None:
        query = query.filter(BaseItem.item_code == item_code)
    base_item = query.first()
    base_item.purchase_price = purchase_price
    db.session.commit()


def get_performance_registration_item_list_in_period(item_code: str, warehouse_code: str, start_date: datetime, end_date: datetime) -> list:
    from backend_model.table_production import PerformanceRegistration, PerformanceRegistrationItem1
    query = db.session.query(
        PerformanceRegistrationItem1.item_code
    ).join(
        PerformanceRegistration,
        PerformanceRegistrationItem1.fk_performance_registration_id == PerformanceRegistration.id
    )
    if item_code is not None:
        query = query.filter(PerformanceRegistrationItem1.item_code == item_code)
    query = query.filter(
        PerformanceRegistrationItem1.warehouse_code == warehouse_code
    ).filter(
        PerformanceRegistration.target_date >= start_date
    ).filter(
        PerformanceRegistration.target_date <= end_date
    ).group_by(
        PerformanceRegistrationItem1.item_code
    )
    receiving_items = query.all()
    item_code_list = [item.item_code for item in receiving_items]
    return item_code_list


def get_bom_from_item_list(item_code_list: list):
    from backend_model.table_base import BaseBOM, BaseBOMLink, BaseItem
    bom_products = db.session.query(
        BaseBOMLink.parent_id,
        BaseBOM.item_id,
        BaseItem.item_code,
        BaseItem.asset_type,
    ).join(
        BaseBOM, BaseBOM.id == BaseBOMLink.parent_id
    ).join(
        BaseItem, BaseItem.id == BaseBOM.item_id
    ).filter(
        BaseItem.item_code.in_(item_code_list)
    ).group_by(
        BaseBOMLink.parent_id
    ).all()
    return bom_products

def get_bom_from_item_list_in_child_bom_id(bom_child_bom_id_list: list):
    from backend_model.table_base import BaseBOM, BaseBOMLink, BaseItem
    child_bom_products = db.session.query(
        BaseBOMLink.parent_id,
        BaseBOM.item_id,
        BaseItem.item_code,
        BaseItem.asset_type,
    ).join(
        BaseBOM, BaseBOM.id == BaseBOMLink.parent_id
    ).join(
        BaseItem, BaseItem.id == BaseBOM.item_id
    ).filter(
        BaseBOMLink.parent_id.in_(bom_child_bom_id_list)
    ).group_by(
        BaseBOMLink.parent_id
    ).all()
    return child_bom_products

def get_bom_child_item_list(item_code_list: list):
    from backend_model.table_base import BaseBOM, BaseBOMLink, BaseItem
    query = db.session.query(
        BaseBOMLink.child_id,
    ).join(
        BaseBOM, BaseBOM.id == BaseBOMLink.parent_id
    ).join(
        BaseItem, BaseItem.id == BaseBOM.item_id
    ).filter(
        BaseItem.item_code.in_(item_code_list)
    ).distinct()
    return query.all()

def update_performance_registration_item1_cost_price(update_item_list: [], warehouse_code: str, start_date: datetime, end_date: datetime):
    from backend_model.table_base import BaseItem
    from backend_model.table_production import PerformanceRegistration, PerformanceRegistrationItem1
    items = db.session.query(
        PerformanceRegistration, PerformanceRegistrationItem1, BaseItem
    ).join(
        PerformanceRegistration,
        PerformanceRegistration.id == PerformanceRegistrationItem1.fk_performance_registration_id
    ).join(
        BaseItem, BaseItem.item_code == PerformanceRegistrationItem1.item_code
    ).filter(
        PerformanceRegistration.target_date >= start_date
    ).filter(
        PerformanceRegistration.target_date <= end_date
    ).filter(
        PerformanceRegistrationItem1.warehouse_code == warehouse_code
    ).filter(
        PerformanceRegistrationItem1.item_code.in_(update_item_list)
    ).all()
    for item in items:
        item.PerformanceRegistrationItem1.unit_price = item.BaseItem.purchase_price
        db.session.commit()


def cost_closing(item_code: str, warehouse_code: str, start_date: datetime, end_date: datetime):
    # 기간 내의 모든 출고 품목의 원가를 null로 초기화
    from backend_lib.cost.lib_cost_closing import LibCostClosing
    LibCostClosing.clear_cost_price(
        start_date=start_date, end_date=end_date, item_code=item_code, warehouse_code=warehouse_code
    )

    # 입고 품목 리스트
    receiving_items = LibCostClosing.get_receiving_item_list(
        end_date=end_date, item_code=item_code, warehouse_code=warehouse_code
    )
    # 입고일로 정렬 및 품목 코드로 분류
    sorted_receiving_items = LibCostClosing.sort_item_dict_in_list(receiving_items, 'receiving_date')
    dict_receiving_items = LibCostClosing.classify_by_item_code(sorted_receiving_items)

    # 출고 품목 리스트
    release_items = LibCostClosing.get_release_item_list(
        end_date=end_date, item_code=item_code, warehouse_code=warehouse_code
    )
    # 출고일로 정렬 및 품목 코드로 분류
    sorted_release_items = LibCostClosing.sort_item_dict_in_list(release_items, 'release_date')
    dict_release_items = LibCostClosing.classify_by_item_code(sorted_release_items)

    for item_code, release_list in dict_release_items.items():
        if item_code in dict_receiving_items:
            receiving_list = dict_receiving_items[item_code].copy()
        else:  # 출고 품목에는 있으나 입고 품목에는 없는 경우
            continue

        for release_item in release_list:
            if release_item['quantity'] <= 0:  # 출고 수량이 0 이하면 계산하지 않는다
                continue
            cost_price, total_cost_price = LibCostClosing.calculate_cost_price(release_item['quantity'], receiving_list)
            if cost_price is None:  # 입고량보다 출고량이 많은 경우
                break
            if release_item['release_date'] < start_date:  # 출고일이 시작일보다 빠르면 업데이트하지 않는다
                continue
            LibCostClosing.update_cost_price(release_item['type'], release_item['id'], cost_price, total_cost_price)
