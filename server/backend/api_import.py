# -*- coding: utf-8 -*-
from flask import make_response
from flask_restful import reqparse

from backend import manager
from backend import app, check_token
from backend_lib.lib_import import *
from backend_model.table_import import *

from decimal import Decimal

print("module [backend.api_import] loaded")

db = DBManager.db


manager.create_api(ImportPurchaseOrder,
                   url_prefix='/api/mes/v1/import',
                   collection_name='purchase_order',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibImportPurchaseOrder.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(ImportPurchaseOrderItem,
                   url_prefix='/api/mes/v1/import',
                   collection_name='purchase_order_item',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token, LibImportPurchaseOrderItem.delete_single_preprocessor]
                   })

manager.create_api(ImportShipment,
                   url_prefix='/api/mes/v1/import',
                   collection_name='shipment',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibImportShipment.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(ImportShipmentItem,
                   url_prefix='/api/mes/v1/import',
                   collection_name='shipment_item',
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

manager.create_api(ImportClearance,
                   url_prefix='/api/mes/v1/import',
                   collection_name='clearance',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibImportClearance.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(ImportClearanceItem,
                   url_prefix='/api/mes/v1/import',
                   collection_name='clearance_item',
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

manager.create_api(ImportCredit,
                   url_prefix='/api/mes/v1/import',
                   collection_name='credit',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibImportCredit.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(ImportCreditItem,
                   url_prefix='/api/mes/v1/import',
                   collection_name='credit_item',
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

manager.create_api(ImportApproval,
                   url_prefix='/api/mes/v1/import',
                   collection_name='approval',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibImportApproval.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(ImportApprovalItem,
                   url_prefix='/api/mes/v1/import',
                   collection_name='approval_item',
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

manager.create_api(ImportApprovalCost,
                   url_prefix='/api/mes/v1/import',
                   collection_name='approval_cost',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibImportApprovalCost.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(ImportApprovalCostItem,
                   url_prefix='/api/mes/v1/import',
                   collection_name='approval_cost_item',
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

manager.create_api(ImportClearanceCost,
                   url_prefix='/api/mes/v1/import',
                   collection_name='clearance_cost',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibImportClearanceCost.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(ImportClearanceCostItem,
                   url_prefix='/api/mes/v1/import',
                   collection_name='clearance_cost_item',
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


@app.route("/api/mes/v1/import_cost", methods=["POST"])
def import_cost():
    parser = reqparse.RequestParser()
    parser.add_argument("clearance_id", type=str, location="json")
    args = parser.parse_args()

    clearance_id = args['clearance_id']

    from backend_model.table_import import ImportClearance, ImportClearanceItem
    clearance = db.session.query(
        ImportClearance
    ).filter(
        ImportClearance.id == clearance_id
    ).first()
    if not clearance:
        return make_response({'error': 'clearance not exist'}, 400)

    clearance_items = db.session.query(
        ImportClearanceItem
    ).filter(
        ImportClearanceItem.fk_import_clearance_id == clearance_id
    ).all()
    if not clearance_items:
        return make_response({'error': 'clearance_items not exist'}, 400)

    from backend_model.table_import import ImportShipment
    shipment = db.session.query(
        ImportShipment
    ).filter(
        ImportShipment.shipment_number == clearance_items[0].import_shipment_number
    ).first()
    if not shipment:
        return make_response({'error': 'shipment not exist'}, 400)

    from backend_model.table_import import ImportApprovalCost, ImportApprovalCostItem
    approval_cost = db.session.query(
        ImportApprovalCost
    ).filter(
        ImportApprovalCost.fk_import_shipment_id == shipment.id
    ).first()
    if not approval_cost:
        return make_response({'error': 'approval_cost not exist'}, 400)

    # 수입결재비용의 CABLE CHARGE, OPEN CHARGE의 합을 구한다
    approval_cost_cable_charges = db.session.query(
        ImportApprovalCostItem
    ).filter(
        ImportApprovalCostItem.fk_import_approval_cost_id == approval_cost.id
    ).filter(
        ImportApprovalCostItem.account_type == 'CABLE CHARGE'
    ).all()
    if not approval_cost_cable_charges:
        return make_response({'error': 'approval_cost_cable_charges not exist'}, 400)

    approval_cost_open_charges = db.session.query(
        ImportApprovalCostItem
    ).filter(
        ImportApprovalCostItem.fk_import_approval_cost_id == approval_cost.id
    ).filter(
        ImportApprovalCostItem.account_type == 'OPEN CHARGE'
    ).all()
    if not approval_cost_open_charges:
        return make_response({'error': 'approval_cost_open_charges not exist'}, 400)

    total_charges = Decimal(0)
    for cable_charge in approval_cost_cable_charges:
        total_charges += cable_charge.amount
    for open_charge in approval_cost_open_charges:
        total_charges += open_charge.amount

    # 수입통관비용의 공급가와 수입결재비용의 합을 구한다
    from backend_model.table_import import ImportClearanceCost
    clearance_cost = db.session.query(
        ImportClearanceCost
    ).filter(
        ImportClearanceCost.fk_import_clearance_id == clearance_id
    ).first()
    if not clearance_cost:
        return make_response({'error': 'clearance_cost not exist'}, 400)

    temp_price = total_charges + clearance_cost.supply_price
    print(total_charges)
    print(clearance_cost.supply_price)

    total_won_amount = Decimal(clearance.total_price_won)
    for clearance_item in clearance_items:
        cost_rate = clearance_item.won_amount / total_won_amount
        distribution_amount = temp_price * cost_rate
        cost_price = (clearance_item.won_amount + distribution_amount) / clearance_item.qty
        clearance_item.cost_rate = cost_rate
        clearance_item.cost_price = cost_price
    db.session.commit()

    response = {
        'id': clearance_id
    }

    return make_response(response, 200)
