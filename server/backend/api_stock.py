# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from flask import request, jsonify, make_response
from flask_restful import reqparse

from backend import app, manager, check_token
from backend_lib.lib_stock import *


print("module [backend.api_stock] loaded")

db = DBManager.db
# REST API(s) available :
#  - /api/v1/login
#  - /api/v1/logout


manager.create_api(StockEtc,
                   url_prefix='/api/mes/v1/stock',
                   collection_name='stock_etc',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibStockEtc.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(StockEtcItem,
                   url_prefix='/api/mes/v1/stock',
                   collection_name='stock_etc_item',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibStockEtcItem.post_preprocessor],
                       'PATCH_SINGLE': [check_token, LibStockEtcItem.patch_single_preprocessor],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(StockMoveRequest,
                   url_prefix='/api/mes/v1/stock',
                   collection_name='stock_move_request',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibStockMoveRequest.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(StockMoveRequestItem,
                   url_prefix='/api/mes/v1/stock',
                   collection_name='stock_move_request_item',
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
                       'GET_MANY':[LibStockMoveRequestItem.get_many_postprocessor]
                   })


manager.create_api(StockMoveRelease,
                   url_prefix='/api/mes/v1/stock',
                   collection_name='stock_move_release',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibStockMoveRelease.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(StockMoveReleaseItem,
                   url_prefix='/api/mes/v1/stock',
                   collection_name='stock_move_release_item',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibStockMoveReleaseItem.post_preprocessor],
                       'PATCH_SINGLE': [check_token, LibStockMoveReleaseItem.patch_single_preprocessor],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   },
                   postprocessors={
                       'GET_MANY': [LibStockMoveReleaseItem.get_many_postprocessor],
                       'POST': [LibStockMoveReleaseItem.post_postprocessor],
                       'PATCH_SINGLE': [LibStockMoveReleaseItem.patch_single_postprocessor]
                   })


manager.create_api(StockCorrection,
                   url_prefix='/api/mes/v1/stock',
                   collection_name='stock_correction',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibStockCorrection.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(StockCorrectionItem,
                   url_prefix='/api/mes/v1/stock',
                   collection_name='stock_correction_item',
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


@app.route("/api/mes/v1/stock/statistics", methods=["GET"])
def stock_statistics_list():
    from decimal import Decimal
    from backend_model.table_setup import SetupBasicStock

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

    # 1. 창고와 자산구분, 품목대분류로 품목 리스트를 뽑는다.
    query = db.session.query(SetupBasicStock)
    if warehouse_name and warehouse_name != '':
        query = query.filter(SetupBasicStock.warehouse.has(wh_name=warehouse_name))
    if asset_type and asset_type != '':
        query = query.filter(SetupBasicStock.item.has(asset_type=asset_type))
    if category and category != '':
        query = query.filter(SetupBasicStock.item.has(main_category=category))
    basic_stock_list = query.all()

    from backend_lib.lib_base import LibBaseWarehouse
    warehouse = LibBaseWarehouse.get_warehouse_by_name(warehouse_name=warehouse_name)

    item_code_list = [basic_stock.item_code for basic_stock in basic_stock_list]

    from backend_lib.cost.lib_cost_closing import LibCostClosing
    # 출고 -------------------------------------------------------------------------------------------------------------
    past_release_datas = LibCostClosing.get_cost_release_quantity_n_price_list(
        item_code_list=item_code_list, warehouse_code=warehouse.wh_code, end_date=start_date
    )

    # 입고 -------------------------------------------------------------------------------------------------------------
    past_receiving_datas = LibCostClosing.get_cost_receiving_quantity_n_price_list(
        item_code_list=item_code_list, warehouse_code=warehouse.wh_code, end_date=start_date
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
        item_code_list=item_code_list, warehouse_code=warehouse.wh_code, start_date=start_date, end_date=end_date
    )

    # 입고 -------------------------------------------------------------------------------------------------------------
    receiving_datas = LibCostClosing.get_cost_receiving_quantity_n_price_list(
        item_code_list=item_code_list, warehouse_code=warehouse.wh_code, start_date=start_date, end_date=end_date
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

    id = 0
    for basic_stock in basic_stock_list:
        if not basic_stock.item:
            continue

        if basic_stock.item_code in items:
            items[basic_stock.item_code]['id'] = id
            items[basic_stock.item_code]['asset_type'] = basic_stock.item.asset_type  # 자산 구분
            items[basic_stock.item_code]['item_id'] = basic_stock.id  # 품목 아이디
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
                'id': id,
                'item_code': basic_stock.item_code,
                'asset_type': basic_stock.item.asset_type,  # 자산 구분
                'item_id': basic_stock.id,  # 품목 아이디
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
        id += 1

    for item_code, item in sorted(items.items()):
        response['objects'].append(item)

    return make_response(response, 200)


def make_statistics_response(response_id, action_date, inout_type, company='', unit_price=0, past_stock=0, receiving_stock=0, release_stock=0, fk_project_management_id=None, number=''):
    res = {
        'id': response_id,
        'number': number,
        'action_date': action_date.strftime('%Y-%m-%dT00:00:00'),
        'inout_type': inout_type,
        'company': company,
        'unit_price': unit_price,
        'past_stock': past_stock,
        'receiving_stock': receiving_stock,
        'release_stock': release_stock,
        'fk_project_management_id': fk_project_management_id,
        'group_id': action_date.strftime('%Y-%m')
    }
    return res


def stock_statistics(basic_stock, start_date, end_date):
    response = dict()
    response['objects'] = []
    response['result'] = ""

    from backend_model.table_common import Companies
    is_past_stock = True
    company = db.session.query(
        Companies
    ).filter(
        Companies.basic_stock_date < end_date
    ).first()
    if not company:
        is_past_stock = False
    basic_stock_quantity = 0
    if is_past_stock:
        basic_stock_quantity = basic_stock.basic_stock

    # 3. 이월재고 = 기초재고 + 2의 입고량 - 2의 출고량
    from backend_lib.lib_setup import LibSetupBasicStock
    past_release_result = LibSetupBasicStock.get_total_release_quantity(item_code=basic_stock.item_code, warehouse_code=basic_stock.wh_code, end_date=start_date)
    past_receiving_result = LibSetupBasicStock.get_total_receiving_quantity(item_code=basic_stock.item_code, warehouse_code=basic_stock.wh_code, end_date=start_date)
    past_stock = basic_stock_quantity + past_receiving_result['total_receiving_quantity'] - past_release_result['total_release_quantity']

    tmp = datetime.strptime(start_date, '%Y%m%d').date() - timedelta(days=1)
    start_date_one_day_ago = datetime(tmp.year, tmp.month, tmp.day)  # date to datetime
    res_id = 0
    res = make_statistics_response(response_id=res_id,
                                   action_date=start_date_one_day_ago,
                                   inout_type='이월재고',
                                   past_stock=past_stock)
    response['objects'].append(res)

    # 구매관리 - 입고
    from backend_lib.lib_purchase import LibPurchaseReceivingItem
    receiving_list = LibPurchaseReceivingItem.get_all_receiving_item_for_statistics(item_code=basic_stock.item_code,
                                                                                    warehouse_code=basic_stock.wh_code,
                                                                                    start_date=start_date,
                                                                                    end_date=end_date)
    for item in receiving_list:
        res_id += 1
        res = make_statistics_response(response_id=res_id,
                                       number=item.receiving_number,
                                       action_date=item.receiving_date,
                                       inout_type=item.receiving_type,
                                       company=item.client_company,
                                       unit_price=item.unit_price,
                                       receiving_stock=item.receiving_quantity,
                                       fk_project_management_id=item.fk_project_management_id)
        response['objects'].append(res)

    # 재고관리 - 기타입고
    from backend_lib.lib_stock import LibStockEtcItem
    stock_etc_receiving_list = LibStockEtcItem.get_all_receiving_item_for_statistics(
        item_code=basic_stock.item_code,
        warehouse_code=basic_stock.wh_code,
        start_date=start_date, end_date=end_date)
    for item in stock_etc_receiving_list:
        res_id += 1
        res = make_statistics_response(response_id=res_id,
                                       number=item.number,
                                       action_date=item.target_date,
                                       inout_type=item.inout_type,
                                       unit_price=item.unit_price,
                                       receiving_stock=item.quantity,
                                       fk_project_management_id=item.fk_project_management_id)
        response['objects'].append(res)

    # 재고관리 - 재고이동입고
    from backend_lib.lib_stock import LibStockMoveReleaseItem
    stock_move_receiving_list = LibStockMoveReleaseItem.get_all_receiving_item_for_statistics(
        item_code=basic_stock.item_code,
        warehouse_code=basic_stock.wh_code,
        start_date=start_date, end_date=end_date)
    for item in stock_move_receiving_list:
        res_id += 1
        res = make_statistics_response(response_id=res_id,
                                       number=item.number,
                                       action_date=item.target_date,
                                       inout_type='재고이동입고',
                                       company=item.out_warehouse,
                                       unit_price=item.unit_price,
                                       receiving_stock=item.release_quantity,
                                       fk_project_management_id=item.fk_project_management_id)
        response['objects'].append(res)

    # 생산관리 - 생산입고
    from backend_lib.lib_production import LibPerformanceRegistrationItem1
    produce_receiving_list = LibPerformanceRegistrationItem1.get_all_receiving_item_for_statistics(
        item_code=basic_stock.item_code,
        warehouse_code=basic_stock.wh_code,
        start_date=start_date, end_date=end_date)
    for item in produce_receiving_list:
        res_id += 1

        # 수주 업체 표시
        company = LibPerformanceRegistrationItem1.get_shipment_order_company(item.fk_work_order_item)

        res = make_statistics_response(response_id=res_id,
                                       number=item.number,
                                       action_date=item.target_date,
                                       inout_type='생산입고',
                                       company=company,
                                       unit_price=item.unit_price,
                                       receiving_stock=item.good_quantity,
                                       fk_project_management_id=item.fk_project_management_id)
        response['objects'].append(res)

    # 출하관리 - 출고반품
    from backend_lib.lib_shipment import LibShipmentReleaseReturnItem
    release_return_list = LibShipmentReleaseReturnItem.get_all_receiving_item_for_statistics(
        item_code=basic_stock.item_code,
        warehouse_code=basic_stock.wh_code,
        start_date=start_date, end_date=end_date)
    for item in release_return_list:
        res_id += 1
        res = make_statistics_response(response_id=res_id,
                                       number=item.return_number,
                                       action_date=item.return_date,
                                       inout_type=item.return_type,
                                       company=item.client_company,
                                       unit_price=item.unit_price,
                                       receiving_stock=item.return_quantity)
        response['objects'].append(res)

    # 수입관리 - 통관
    from backend_lib.lib_import import LibImportClearanceItem
    import_list = LibImportClearanceItem.get_all_receiving_item_for_statistics(item_code=basic_stock.item_code,
                                                                               warehouse_code=basic_stock.wh_code,
                                                                               start_date=start_date,
                                                                               end_date=end_date)
    for item in import_list:
        res_id += 1
        res = make_statistics_response(response_id=res_id,
                                       number=item.clearance_number,
                                       action_date=item.clearance_date,
                                       inout_type='통관',
                                       company=item.supplier,
                                       unit_price=item.import_price,
                                       receiving_stock=item.qty)
        response['objects'].append(res)

    # 출하관리 - 출고
    from backend_lib.lib_shipment import LibShipmentReleaseItem
    release_list = LibShipmentReleaseItem.get_all_release_item_for_statistics(item_code=basic_stock.item_code,
                                                                              warehouse_code=basic_stock.wh_code,
                                                                              start_date=start_date, end_date=end_date)
    for item in release_list:
        res_id += 1
        res = make_statistics_response(response_id=res_id,
                                       number=item.release_number,
                                       action_date=item.release_date,
                                       inout_type=item.release_type,
                                       company=item.client_company,
                                       unit_price=item.unit_price,
                                       release_stock=item.release_quantity,
                                       fk_project_management_id=item.fk_project_management_id)
        response['objects'].append(res)

    # 재고관리 - 기타출고
    stock_etc_release_list = LibStockEtcItem.get_all_release_item_for_statistics(item_code=basic_stock.item_code,
                                                                                 warehouse_code=basic_stock.wh_code,
                                                                                 start_date=start_date, end_date=end_date)
    for item in stock_etc_release_list:
        res_id += 1
        res = make_statistics_response(response_id=res_id,
                                       number=item.number,
                                       action_date=item.target_date,
                                       inout_type=item.inout_type,
                                       unit_price=item.unit_price,
                                       release_stock=item.quantity,
                                       fk_project_management_id=item.fk_project_management_id)
        response['objects'].append(res)

    # 재고관리 - 재고이동출고
    stock_move_release_list = LibStockMoveReleaseItem.get_all_release_item_for_statistics(item_code=basic_stock.item_code,
                                                                                          warehouse_code=basic_stock.wh_code,
                                                                                          start_date=start_date, end_date=end_date)
    for item in stock_move_release_list:
        res_id += 1
        res = make_statistics_response(response_id=res_id,
                                       number=item.number,
                                       action_date=item.target_date,
                                       inout_type='재고이동출고',
                                       company=item.in_warehouse,
                                       unit_price=item.unit_price,
                                       release_stock=item.release_quantity,
                                       fk_project_management_id=item.fk_project_management_id)
        response['objects'].append(res)

    # 생산관리 자재소모
    from backend_lib.lib_production import LibPerformanceRegistrationItem2
    produce_release_list = LibPerformanceRegistrationItem2.get_all_release_item_for_statistics(item_code=basic_stock.item_code,
                                                                                               warehouse_code=basic_stock.wh_code,
                                                                                               start_date=start_date, end_date=end_date)
    for item in produce_release_list:
        res_id += 1
        res = make_statistics_response(response_id=res_id,
                                       number=item.number,
                                       action_date=item.target_date,
                                       inout_type='자재소모',
                                       release_stock=item.material_quantity)
        response['objects'].append(res)

    # 구매관리 - 입고반품
    from backend_lib.lib_purchase import LibPurchaseReceivingReturnItem
    purchase_return_list = LibPurchaseReceivingReturnItem.get_all_release_item_for_statistics(item_code=basic_stock.item_code,
                                                                                              warehouse_code=basic_stock.wh_code,
                                                                                              start_date=start_date, end_date=end_date)
    for item in purchase_return_list:
        res_id += 1
        res = make_statistics_response(response_id=res_id,
                                       number=item.return_number,
                                       action_date=item.return_date,
                                       inout_type=item.return_type,
                                       company=item.client_company,
                                       unit_price=item.unit_price,
                                       release_stock=item.return_quantity)
        response['objects'].append(res)

    # 수출관리 - 선적
    from backend_lib.lib_export import LibExportCommInvoiceItem
    export_list = LibExportCommInvoiceItem.get_all_release_item_for_statistics(item_code=basic_stock.item_code,
                                                                               warehouse_code=basic_stock.wh_code,
                                                                               start_date=start_date, end_date=end_date)
    for item in export_list:
        res_id += 1
        res = make_statistics_response(response_id=res_id,
                                       number=item.invoice_number,
                                       action_date=item.invoice_date,
                                       inout_type='선적',
                                       company=item.client_company,
                                       unit_price=item.unit_price,
                                       release_stock=item.invoice_quantity)
        response['objects'].append(res)

    response['objects'] = sorted(response['objects'], key=(lambda x: x['action_date']))
    return response


@app.route("/api/mes/v1/stock/statistics/<bs_id>", methods=["GET"])
def stock_statistics_bs_id(bs_id):
    from backend_model.table_setup import SetupBasicStock

    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        return make_response(jsonify('No Parameters'), 400)

    start = parameter_dict['start']
    end = parameter_dict['end']

    bs = db.session.query(SetupBasicStock).filter(SetupBasicStock.id == bs_id).first()
    if bs is None:
        return make_response({}, 404)

    response = stock_statistics(bs, start, end)
    return make_response(response, 200)


@app.route("/api/mes/v1/stock/statistics/item", methods=["POST"])
def stock_statistics_item_warehouse():
    parser = reqparse.RequestParser()
    parser.add_argument("item_code", type=str, location="json")
    parser.add_argument("warehouse_name", type=str, location="json")
    parser.add_argument("start", type=str, location="json")
    parser.add_argument("end", type=str, location="json")
    args = parser.parse_args()
    print(args)

    if len(args) == 0:
        return make_response(jsonify('No Parameters'), 400)

    item_code = args['item_code']
    warehouse_name = args['warehouse_name']
    start = args['start']
    end = args['end']

    from backend_lib.lib_base import LibBaseWarehouse
    warehouse = LibBaseWarehouse.get_warehouse_by_name(warehouse_name=warehouse_name)
    if not warehouse:
        return make_response(jsonify('Invalid warehouse name'), 400)

    from backend_lib.lib_setup import LibSetupBasicStock
    bs = LibSetupBasicStock.get_basic_stock(item_code, warehouse.wh_code)
    if bs is None:
        return make_response(jsonify('basic stock not exist'), 400)

    response = stock_statistics(bs, start, end)
    return make_response(response, 200)


@app.route("/api/mes/v1/stock/search", methods=["POST"])
def stock_search():
    from backend_model.table_setup import SetupBasicStock

    parser = reqparse.RequestParser()
    parser.add_argument("warehouse", type=str, location="json")
    parser.add_argument("asset_type", type=str, location="json")
    args = parser.parse_args()

    from backend_model.table_base import BaseItem
    total_price = 0
    index = 1
    response_items = []
    if args['warehouse'] == '전체':
        joined = db.session.query(
            SetupBasicStock, BaseItem,
            db.func.sum(SetupBasicStock.current_stock).label('total_current_stock'),
            db.func.sum(SetupBasicStock.available_stock).label('total_available_stock')
        ).join(
            BaseItem, SetupBasicStock.item_code == BaseItem.item_code
        )
        if args['asset_type'] != '전체':
            filtered = joined.filter(BaseItem.asset_type == args['asset_type'])
        else:
            filtered = joined
        parent_items = filtered.group_by(SetupBasicStock.item_code).all()
        for parent_item in parent_items:
            if parent_item.total_current_stock == 0:
                continue

            assign_stock = parent_item.total_current_stock - parent_item.total_available_stock
            if assign_stock < 0:
                assign_stock = 0
            response_items.append({
                'id': index,
                'parent_id': None,
                'warehouse': '전체',
                'item_code': parent_item.SetupBasicStock.item_code,
                'current_stock': parent_item.total_current_stock,
                'available_stock': parent_item.total_available_stock,
                'assign_stock': assign_stock,
                'item': {
                    'item_name': parent_item.BaseItem.item_name,
                    'item_standard': parent_item.BaseItem.item_standard,
                    'asset_type': parent_item.BaseItem.asset_type,
                    'safety_stock': parent_item.BaseItem.safety_stock,
                    'main_category': parent_item.BaseItem.main_category,
                    'middle_category': parent_item.BaseItem.middle_category,
                    'sub_category': parent_item.BaseItem.sub_category,
                    'purchase_price': parent_item.BaseItem.purchase_price
                }
            })

            total_price = total_price + (parent_item.total_current_stock * round(parent_item.BaseItem.purchase_price))
            parent_index = index
            index += 1
            child_items = db.session.query(
                SetupBasicStock
            ).filter(
                SetupBasicStock.item_code == parent_item.SetupBasicStock.item_code
            ).all()
            for child_item in child_items:
                if child_item.current_stock == 0:
                    continue
                assign_stock = child_item.current_stock - child_item.available_stock
                if assign_stock < 0:
                    assign_stock = 0
                response_items.append({
                    'id': index,
                    'parent_id': parent_index,
                    'warehouse': child_item.warehouse.wh_name,
                    'item_code': child_item.item_code,
                    'current_stock': child_item.current_stock,
                    'available_stock': child_item.available_stock,
                    'assign_stock': assign_stock,
                    'item': {
                        'item_name': child_item.item.item_name,
                        'item_standard': child_item.item.item_standard,
                        'asset_type': child_item.item.asset_type,
                        'safety_stock': child_item.item.safety_stock,
                        'main_category': child_item.item.main_category,
                        'middle_category': child_item.item.middle_category,
                        'sub_category': child_item.item.sub_category,
                        'purchase_price': child_item.item.purchase_price
                    }
                })
                index += 1
    else:
        joined = db.session.query(
            SetupBasicStock,
            BaseItem,
        ).join(
            BaseItem, SetupBasicStock.item_code == BaseItem.item_code
        ).filter(
            SetupBasicStock.wh_code == args['warehouse']
        )
        if args['asset_type'] != '전체':
            filtered = joined.filter(BaseItem.asset_type == args['asset_type'])
        else:
            filtered = joined
        basic_stocks = filtered.all()
        for basic_stock in basic_stocks:
            if basic_stock.SetupBasicStock.current_stock == 0:
                continue

            assign_stock = basic_stock.SetupBasicStock.current_stock - basic_stock.SetupBasicStock.available_stock
            if assign_stock < 0:
                assign_stock = 0
            response_items.append({
                'id': index,
                'parent_id': None,
                'warehouse': basic_stock.SetupBasicStock.warehouse.wh_name,
                'item_code': basic_stock.SetupBasicStock.item_code,
                'current_stock': basic_stock.SetupBasicStock.current_stock,
                'available_stock': basic_stock.SetupBasicStock.available_stock,
                'assign_stock': assign_stock,
                'item': {
                    'item_name': basic_stock.BaseItem.item_name,
                    'item_standard': basic_stock.BaseItem.item_standard,
                    'asset_type': basic_stock.BaseItem.asset_type,
                    'safety_stock': basic_stock.BaseItem.safety_stock,
                    'main_category': basic_stock.BaseItem.main_category,
                    'middle_category': basic_stock.BaseItem.middle_category,
                    'sub_category': basic_stock.BaseItem.sub_category,
                    'purchase_price': basic_stock.BaseItem.purchase_price
                }
            })
            total_price = total_price + (basic_stock.SetupBasicStock.current_stock * round(basic_stock.BaseItem.purchase_price))
            index += 1
    response = {
        'data': response_items,
        'totalPrice': total_price
    }
    return make_response(response, 200)


@app.route("/api/mes/v1/stock/price", methods=["POST"])
def stock_price():
    from backend_model.table_setup import SetupBasicStock

    parser = reqparse.RequestParser()
    parser.add_argument("warehouse", type=str, location="json")
    parser.add_argument("asset_type", type=str, location="json")
    parser.add_argument("category", type=str, location="json")
    args = parser.parse_args()

    from backend_model.table_base import BaseItem
    total_price = 0
    index = 1
    response_items = []
    if args['warehouse'] == '전체':
        query = db.session.query(
            SetupBasicStock, BaseItem,
            db.func.sum(SetupBasicStock.current_stock).label('total_current_stock'),
            db.func.sum(SetupBasicStock.available_stock).label('total_available_stock')
        ).join(
            BaseItem, SetupBasicStock.item_code == BaseItem.item_code
        )
        if args['asset_type'] != '전체':
            query = query.filter(BaseItem.asset_type == args['asset_type'])
        if args['category'] != '전체':
            query = query.filter(BaseItem.main_category == args['category'])

        parent_items = query.group_by(SetupBasicStock.item_code).all()
        for parent_item in parent_items:
            if parent_item.total_current_stock == 0:
                continue
            if parent_item.BaseItem.purchase_price <= 0:
                continue

            assign_stock = parent_item.total_current_stock - parent_item.total_available_stock
            if assign_stock < 0:
                assign_stock = 0
            response_items.append({
                'id': index,
                'parent_id': None,
                'warehouse': '전체',
                'item_code': parent_item.SetupBasicStock.item_code,
                'current_stock': parent_item.total_current_stock,
                'available_stock': parent_item.total_available_stock,
                'assign_stock': assign_stock,
                'item': {
                    'item_name': parent_item.BaseItem.item_name,
                    'item_standard': parent_item.BaseItem.item_standard,
                    'asset_type': parent_item.BaseItem.asset_type,
                    'safety_stock': parent_item.BaseItem.safety_stock,
                    'main_category': parent_item.BaseItem.main_category,
                    'middle_category': parent_item.BaseItem.middle_category,
                    'sub_category': parent_item.BaseItem.sub_category,
                    'purchase_price': parent_item.BaseItem.purchase_price
                }
            })

            total_price = total_price + (parent_item.total_current_stock * round(parent_item.BaseItem.purchase_price))
            parent_index = index
            index += 1
            child_items = db.session.query(
                SetupBasicStock
            ).filter(
                SetupBasicStock.item_code == parent_item.SetupBasicStock.item_code
            ).all()
            for child_item in child_items:
                if child_item.current_stock == 0:
                    continue
                assign_stock = child_item.current_stock - child_item.available_stock
                if assign_stock < 0:
                    assign_stock = 0
                response_items.append({
                    'id': index,
                    'parent_id': parent_index,
                    'warehouse': child_item.warehouse.wh_name,
                    'item_code': child_item.item_code,
                    'current_stock': child_item.current_stock,
                    'available_stock': child_item.available_stock,
                    'assign_stock': assign_stock,
                    'item': {
                        'item_name': child_item.item.item_name,
                        'item_standard': child_item.item.item_standard,
                        'asset_type': child_item.item.asset_type,
                        'safety_stock': child_item.item.safety_stock,
                        'main_category': child_item.item.main_category,
                        'middle_category': child_item.item.middle_category,
                        'sub_category': child_item.item.sub_category,
                        'purchase_price': child_item.item.purchase_price
                    }
                })
                index = index + 1
    else:
        query = db.session.query(
            SetupBasicStock,
            BaseItem,
        ).join(
            BaseItem, SetupBasicStock.item_code == BaseItem.item_code
        ).filter(
            SetupBasicStock.wh_code == args['warehouse']
        )
        if args['asset_type'] != '전체':
            query = query.filter(BaseItem.asset_type == args['asset_type'])
        if args['category'] != '전체':
            query = query.filter(BaseItem.main_category == args['category'])
        basic_stocks = query.all()
        for basic_stock in basic_stocks:
            if basic_stock.SetupBasicStock.current_stock == 0:
                continue
            if basic_stock.BaseItem.purchase_price <= 0:
                continue

            assign_stock = basic_stock.SetupBasicStock.current_stock - basic_stock.SetupBasicStock.available_stock
            if assign_stock < 0:
                assign_stock = 0
            response_items.append({
                'id': index,
                'parent_id': None,
                'warehouse': basic_stock.SetupBasicStock.warehouse.wh_name,
                'item_code': basic_stock.SetupBasicStock.item_code,
                'current_stock': basic_stock.SetupBasicStock.current_stock,
                'available_stock': basic_stock.SetupBasicStock.available_stock,
                'assign_stock': assign_stock,
                'item': {
                    'item_name': basic_stock.BaseItem.item_name,
                    'item_standard': basic_stock.BaseItem.item_standard,
                    'asset_type': basic_stock.BaseItem.asset_type,
                    'safety_stock': basic_stock.BaseItem.safety_stock,
                    'main_category': basic_stock.BaseItem.main_category,
                    'middle_category': basic_stock.BaseItem.middle_category,
                    'sub_category': basic_stock.BaseItem.sub_category,
                    'purchase_price': basic_stock.BaseItem.purchase_price
                }
            })
            total_price = total_price + (basic_stock.SetupBasicStock.current_stock * round(basic_stock.BaseItem.purchase_price))
            index = index + 1
    response = {
        'data': response_items,
        'totalPrice': total_price
    }
    return make_response(response, 200)
