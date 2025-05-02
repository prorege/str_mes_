# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional, Dict

from backend_model.database import DBManager

db = DBManager.db


class LibCostClosingPurchaseReceivingReturn(object):

    @staticmethod
    def get_purchase_receiving_return_item_list(
            end_date: datetime, item_code: Optional[str] = None, warehouse_code: Optional[str] = None
    ) -> list:
        release_items = []

        from backend_model.table_purchase import PurchaseReceivingReturn, PurchaseReceivingReturnItem
        query = db.session.query(
            PurchaseReceivingReturnItem
        ).join(
            PurchaseReceivingReturn, PurchaseReceivingReturnItem.receiving_return
        ).filter(
            PurchaseReceivingReturn.return_date <= end_date
        )
        if item_code:
            query = query.filter(
                PurchaseReceivingReturnItem.item_code == item_code
            )
        if warehouse_code:
            query = query.filter(
                PurchaseReceivingReturnItem.warehouse_code == warehouse_code
            )
        query = query.order_by(
            PurchaseReceivingReturn.return_date.asc()
        )
        return_items = query.all()

        for item in return_items:
            release_items.append({
                'id': item.id,
                'type': 'PurchaseReceivingReturnItem',
                'release_date': item.receiving_return.return_date,
                'quantity': item.return_quantity,
                'item_code': item.item_code
            })
        return release_items

    @staticmethod
    def clear_cost_price(start_date, end_date, warehouse_code, item_code):
        from backend_model.table_purchase import PurchaseReceivingReturn, PurchaseReceivingReturnItem
        query = db.session.query(
            PurchaseReceivingReturnItem
        ).join(
            PurchaseReceivingReturn, PurchaseReceivingReturn.id == PurchaseReceivingReturnItem.fk_receiving_return_id
        ).filter(
            PurchaseReceivingReturn.return_date >= start_date
        ).filter(
            PurchaseReceivingReturn.return_date <= end_date
        )
        if item_code:
            query = query.filter(
                PurchaseReceivingReturnItem.item_code == item_code
            )
        if warehouse_code:
            query = query.filter(
                PurchaseReceivingReturnItem.warehouse_code == warehouse_code
            )
        purchase_receiving_return_items = query.all()
        for item in purchase_receiving_return_items:
            item.cost_price = None
            item.total_cost_price = None
        db.session.commit()
