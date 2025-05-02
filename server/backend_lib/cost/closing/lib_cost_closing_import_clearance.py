# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional, Dict

from backend_model.database import DBManager

db = DBManager.db


class LibCostClosingImportClearance(object):

    @staticmethod
    def get_import_clearance_item_list(
            end_date: datetime, item_code: Optional[str] = None, warehouse_code: Optional[str] = None
    ) -> list:
        receiving_items = []

        from backend_model.table_import import ImportClearance, ImportClearanceItem
        query = db.session.query(
            ImportClearanceItem
        ).join(
            ImportClearance, ImportClearanceItem.import_clearance
        ).filter(
            ImportClearance.clearance_date <= end_date
        )
        if item_code:
            query = query.filter(
                ImportClearanceItem.item_code == item_code
            )
        if warehouse_code:
            query = query.filter(
                ImportClearanceItem.warehouse_code == warehouse_code
            )
        query = query.order_by(
            ImportClearance.clearance_date.asc()
        )
        import_items = query.all()

        for item in import_items:
            receiving_items.append({
                'id': item.id,
                'type': 'ImportClearanceItem',
                'receiving_date': item.import_clearance.clearance_date,
                'quantity': item.qty,
                'item_code': item.item_code,
                'unit_price': item.cost_price 
            })
        return receiving_items
