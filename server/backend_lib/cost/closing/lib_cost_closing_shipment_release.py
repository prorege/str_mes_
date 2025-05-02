# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional, Dict

from backend_model.database import DBManager

db = DBManager.db


class LibCostClosingShipmentRelease(object):

    @staticmethod
    def get_shipment_release_item_list(
            end_date: datetime, item_code: Optional[str] = None, warehouse_code: Optional[str] = None
    ) -> list:
        release_items = []

        from backend_model.table_shipment import ShipmentRelease, ShipmentReleaseItem
        query = db.session.query(
            ShipmentReleaseItem
        ).join(
            ShipmentRelease, ShipmentReleaseItem.release
        ).filter(
            ShipmentRelease.release_date <= end_date
        )
        if item_code:
            query = query.filter(
                ShipmentReleaseItem.item_code == item_code
            )
        if warehouse_code:
            query = query.filter(
                ShipmentReleaseItem.warehouse_code == warehouse_code
            )
        query = query.order_by(
            ShipmentRelease.release_date.asc()
        )
        shipment_release_items = query.all()

        for item in shipment_release_items:
            release_items.append({
                'id': item.id,
                'type': 'ShipmentReleaseItem',
                'release_date': item.release.release_date,
                'quantity': item.release_quantity,
                'item_code': item.item_code
            })
        return release_items

    @staticmethod
    def clear_cost_price(start_date, end_date, warehouse_code, item_code):
        from backend_model.table_shipment import ShipmentRelease, ShipmentReleaseItem
        _query = db.session.query(
            ShipmentReleaseItem
        ).join(
            ShipmentRelease, ShipmentReleaseItem.fk_release_id == ShipmentRelease.id
        ).filter(
            ShipmentRelease.release_date >= start_date
        ).filter(
            ShipmentRelease.release_date <= end_date
        )
        if item_code:
            _query = _query.filter(
                ShipmentReleaseItem.item_code == item_code
            )
        if warehouse_code:
            _query = _query.filter(
                ShipmentReleaseItem.warehouse_code == warehouse_code
            )
        _shipment_release_items = _query.all()
        for _item in _shipment_release_items:
            _item.cost_price = None
            _item.total_cost_price = None
        db.session.commit()
