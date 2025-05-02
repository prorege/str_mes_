# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional, Dict

from backend_model.database import DBManager

db = DBManager.db


class LibCostClosingStockEtc(object):

    @staticmethod
    def get_stock_etc_receiving_item_list(
            end_date: datetime, item_code: Optional[str] = None, warehouse_code: Optional[str] = None
    ) -> list:
        receiving_items = []

        from backend_model.table_stock import StockEtc, StockEtcItem
        query = db.session.query(
            StockEtcItem
        ).join(
            StockEtc, StockEtcItem.stock_etc
        ).filter(
            StockEtc.target_date <= end_date
        ).filter(
            StockEtcItem.type == '입고'
        )
        if item_code:
            query = query.filter(
                StockEtcItem.item_code == item_code
            )
        if warehouse_code:
            query = query.filter(
                StockEtcItem.warehouse_code == warehouse_code
            )
        query = query.order_by(
            StockEtc.target_date.asc()
        )
        stock_etc_receiving_items = query.all()

        for item in stock_etc_receiving_items:
            receiving_items.append({
                'id': item.id,
                'type': 'StockEtcItem',
                'receiving_date': item.stock_etc.target_date,
                'quantity': item.quantity,
                'item_code': item.item_code,
                'unit_price': item.unit_price
            })
        return receiving_items

    @staticmethod
    def get_stock_etc_release_item_list(
            end_date: datetime, item_code: Optional[str] = None, warehouse_code: Optional[str] = None
    ) -> list:
        release_items = []

        from backend_model.table_stock import StockEtc, StockEtcItem
        query = db.session.query(
            StockEtcItem
        ).join(
            StockEtc, StockEtcItem.stock_etc
        ).filter(
            StockEtcItem.type == '출고'
        ).filter(
            StockEtc.target_date <= end_date
        )
        if item_code:
            query = query.filter(
                StockEtcItem.item_code == item_code
            )
        if warehouse_code:
            query = query.filter(
                StockEtcItem.warehouse_code == warehouse_code
            )
        query = query.order_by(
            StockEtc.target_date.asc()
        )
        stock_etc_release_items = query.all()

        for item in stock_etc_release_items:
            release_items.append({
                'id': item.id,
                'type': 'StockEtcItem',
                'release_date': item.stock_etc.target_date,
                'quantity': item.quantity,
                'item_code': item.item_code
            })
        return release_items

    @staticmethod
    def clear_cost_price(start_date, end_date, warehouse_code, item_code):
        from backend_model.table_stock import StockEtc, StockEtcItem
        _query = db.session.query(
            StockEtcItem
        ).join(
            StockEtc, StockEtc.id == StockEtcItem.fk_stock_etc_id
        ).filter(
            StockEtc.target_date >= start_date
        ).filter(
            StockEtc.target_date <= end_date
        )
        if item_code:
            _query = _query.filter(
                StockEtcItem.item_code == item_code
            )
        if warehouse_code:
            _query = _query.filter(
                StockEtcItem.warehouse_code == warehouse_code
            )
        _stock_etc_items = _query.all()
        for _item in _stock_etc_items:
            _item.cost_price = None
            _item.total_cost_price = None
        db.session.commit()
