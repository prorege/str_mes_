# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional, Dict

from backend_model.database import DBManager

db = DBManager.db


class LibCostClosingShipmentReleaseReturn(object):

    @staticmethod
    def get_release_return_item_list(
            end_date: datetime, item_code: Optional[str] = None, warehouse_code: Optional[str] = None
    ) -> list:
        receiving_items = []

        from backend_model.table_shipment import ShipmentReleaseReturn, ShipmentReleaseReturnItem
        query = db.session.query(
            ShipmentReleaseReturnItem
        ).join(
            ShipmentReleaseReturn, ShipmentReleaseReturnItem.release_return
        ).filter(
            ShipmentReleaseReturn.return_date <= end_date
        )
        if item_code:
            query = query.filter(
                ShipmentReleaseReturnItem.item_code == item_code
            )
        if warehouse_code:
            query = query.filter(
                ShipmentReleaseReturnItem.warehouse_code == warehouse_code
            )
        query = query.order_by(
            ShipmentReleaseReturn.return_date.asc()
        )
        return_items = query.all()

        for item in return_items:
            receiving_items.append({
                'id': item.id,
                'type': 'ShipmentReleaseReturnItem',
                'receiving_date': item.release_return.return_date,
                'quantity': item.return_quantity,
                'item_code': item.item_code,
                'unit_price': item.cost_price,
                'release_item_id': item.fk_release_item_id
            })
        return receiving_items
