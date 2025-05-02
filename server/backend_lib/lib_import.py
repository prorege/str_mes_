# -*- coding: utf-8 -*-

from backend_model.table_import import *

db = DBManager.db


class LibImportPurchaseOrder(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'order_number', ImportPurchaseOrder, ImportPurchaseOrder.order_number, '/import/purchase-order')


class LibImportPurchaseOrderItem(object):
    @staticmethod
    def delete_single_preprocessor(instance_id=None, **kw):
        from backend_lib.lib_util import LibUtil
        LibUtil.check_exist_connected_data(ImportShipmentItem, ImportShipmentItem.fk_import_purchase_order_item_id, instance_id)


class LibImportShipment(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'shipment_number', ImportShipment, ImportShipment.shipment_number, '/import/shipment')


class LibImportClearance(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'clearance_number', ImportClearance, ImportClearance.clearance_number, '/import/clearance')


class LibImportClearanceItem(object):
    @staticmethod
    def get_total_receiving_quantity_by_item_code_query(use_count, item_code, warehouse_code, start_date=None, end_date=None):
        if use_count:
            query = db.session.query(
                db.func.sum(ImportClearanceItem.qty)
            )
        else:
            query = db.session.query(
                ImportClearance.clearance_number,
                ImportClearance.clearance_date,
                ImportClearance.supplier,
                ImportClearanceItem.qty,
                ImportClearanceItem.cost_price
            )
        query = query.join(
            ImportClearance, ImportClearanceItem.fk_import_clearance_id == ImportClearance.id
        ).filter(
            ImportClearanceItem.item_code == item_code
        ).filter(
            ImportClearanceItem.warehouse_code == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                ImportClearance.clearance_date >= start_date
            ).filter(
                ImportClearance.clearance_date <= end_date
            )
        elif end_date:
            query = query.filter(
                ImportClearance.clearance_date < end_date
            )
        return query

    @staticmethod
    def get_total_receiving_quantity_by_item_code(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibImportClearanceItem.get_total_receiving_quantity_by_item_code_query(use_count=True,
                                                                                       item_code=item_code,
                                                                                       warehouse_code=warehouse_code,
                                                                                       start_date=start_date,
                                                                                       end_date=end_date)
        receiving_quantity = query.first()[0]
        receiving_quantity = 0 if not receiving_quantity else receiving_quantity
        return receiving_quantity

    @staticmethod
    def get_all_receiving_item_for_statistics(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibImportClearanceItem.get_total_receiving_quantity_by_item_code_query(use_count=False,
                                                                                       item_code=item_code,
                                                                                       warehouse_code=warehouse_code,
                                                                                       start_date=start_date,
                                                                                       end_date=end_date)
        release_items = query.all()
        return release_items

    @staticmethod
    def get_total_receiving_price_by_item_code(item_code: str, warehouse_code: str, start_date=None, end_date=None) -> int:
        query = db.session.query(
            db.func.sum(ImportClearanceItem.qty * ImportClearanceItem.won_price)
        ).join(
            ImportClearance, ImportClearanceItem.fk_import_clearance_id == ImportClearance.id
        ).filter(
            ImportClearanceItem.item_code == item_code
        ).filter(
            ImportClearanceItem.warehouse_code == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                ImportClearance.clearance_date >= start_date
            ).filter(
                ImportClearance.clearance_date <= end_date
            )
        elif end_date:
            query = query.filter(
                ImportClearance.clearance_date < end_date
            )
        receiving_price = query.first()[0]
        receiving_price = 0 if not receiving_price else receiving_price
        return receiving_price


class LibImportCredit(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'credit_number', ImportCredit, ImportCredit.credit_number, '/import/credit')


class LibImportApproval(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'approval_number', ImportApproval, ImportApproval.approval_number, '/import/approval')


class LibImportApprovalCost(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'approval_cost_number', ImportApprovalCost, ImportApprovalCost.approval_cost_number, '/import/approval-cost')


class LibImportClearanceCost(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'clearance_cost_number', ImportClearanceCost, ImportClearanceCost.clearance_cost_number, '/import/clearance-cost')
