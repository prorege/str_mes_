# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional, Dict

from backend_model.database import DBManager

db = DBManager.db


class LibCostClosingStockMove(object):

    @staticmethod
    def get_stock_move_receiving_item_list(
            end_date: datetime, item_code: Optional[str] = None, warehouse_code: Optional[str] = None
    ) -> list:
        receiving_items = []

        from backend_model.table_stock import StockMoveRelease, StockMoveReleaseItem
        query = db.session.query(
            StockMoveReleaseItem
        ).join(
            StockMoveRelease, StockMoveReleaseItem.stock_move_release
        ).filter(
            StockMoveRelease.target_date <= end_date
        )
        if item_code:
            query = query.filter(
                StockMoveReleaseItem.item_code == item_code
            )
        if warehouse_code:
            query = query.filter(
                StockMoveReleaseItem.in_warehouse == warehouse_code
            )
        query = query.order_by(
            StockMoveRelease.target_date.asc()
        )
        stock_move_receiving_items = query.all()
        
        for item in stock_move_receiving_items:
            receiving_items.append({
                'id': item.id,
                'type': 'StockMoveReleaseItem',
                'receiving_date': item.stock_move_release.target_date,
                'quantity': item.release_quantity,
                'item_code': item.item_code,
                'unit_price':item.unit_price  if warehouse_code == '본사창고' else item.cost_price,
            })
        return receiving_items

    @staticmethod
    def get_stock_move_release_item_list(
            end_date: datetime, item_code: Optional[str] = None, warehouse_code: Optional[str] = None
    ) -> list:
        release_items = []

        from backend_model.table_stock import StockMoveRelease, StockMoveReleaseItem
        query = db.session.query(
            StockMoveReleaseItem
        ).join(
            StockMoveRelease, StockMoveReleaseItem.stock_move_release
        ).filter(
            StockMoveRelease.target_date <= end_date
        )
        if item_code:
            query = query.filter(
                StockMoveReleaseItem.item_code == item_code
            )
        if warehouse_code:
            query = query.filter(
                StockMoveReleaseItem.out_warehouse == warehouse_code
            )
        query = query.order_by(
            StockMoveRelease.target_date.asc()
        )
        stock_move_release_items = query.all()

        for item in stock_move_release_items:
            release_items.append({
                'id': item.id,
                'type': 'StockMoveReleaseItem',
                'release_date': item.stock_move_release.target_date,
                'quantity': item.release_quantity,
                'item_code': item.item_code
            })
        return release_items

    @staticmethod
    def clear_cost_price(start_date, end_date, warehouse_code, item_code):
        from backend_model.table_stock import StockMoveRelease, StockMoveReleaseItem
        _query = db.session.query(
            StockMoveReleaseItem
        ).join(
            StockMoveRelease, StockMoveRelease.id == StockMoveReleaseItem.fk_stock_move_release_id
        ).filter(
            StockMoveRelease.target_date >= start_date
        ).filter(
            StockMoveRelease.target_date <= end_date
        )
        if item_code:
            _query = _query.filter(
                StockMoveReleaseItem.item_code == item_code
            )
        if warehouse_code:
            _query = _query.filter(
                StockMoveReleaseItem.out_warehouse == warehouse_code
            )
        _stock_move_release_items = _query.all()
        for _item in _stock_move_release_items:
            _item.cost_price = None
            _item.total_cost_price = None
        db.session.commit()
