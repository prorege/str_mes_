# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional, Dict

from backend_model.database import DBManager

db = DBManager.db


class LibCostClosingPurchaseReceiving(object):

    @staticmethod
    def get_purchase_receiving_item_list(
            end_date: datetime, item_code: Optional[str] = None, warehouse_code: Optional[str] = None
    ) -> list:
        receiving_items = []

        from backend_model.table_purchase import PurchaseReceiving, PurchaseReceivingItem
        query = db.session.query(
            PurchaseReceivingItem
        ).join(
            PurchaseReceiving, PurchaseReceivingItem.receiving
        ).filter(
            PurchaseReceiving.receiving_date2 <= end_date
        )
        if item_code:
            query = query.filter(
                PurchaseReceivingItem.item_code == item_code
            )
        if warehouse_code:
            query = query.filter(
                PurchaseReceivingItem.warehouse_code == warehouse_code
            )
        query = query.order_by(
            PurchaseReceiving.receiving_date2.asc()
        )
        purchase_receiving_items = query.all()

        for item in purchase_receiving_items:
            receiving_items.append({
                'id': item.id,
                'type': 'PurchaseReceivingItem',
                'receiving_date': item.receiving.receiving_date2,
                'quantity': item.receiving_quantity,
                'item_code': item.item_code,
                'unit_price': item.unit_price
            })
        return receiving_items
