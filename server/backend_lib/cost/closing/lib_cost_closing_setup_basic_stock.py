# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional, Dict

from backend_model.database import DBManager

db = DBManager.db


class LibCostClosingSetupBasicStock(object):

    @staticmethod
    def get_basic_stock_item_list(
            item_code: Optional[str] = None, warehouse_code: Optional[str] = None
    ) -> list:
        _receiving_items = []

        from backend_model.table_setup import SetupBasicStock
        _query = db.session.query(
            SetupBasicStock
        ).filter(
            SetupBasicStock.basic_stock > 0
        )
        if item_code:
            _query = _query.filter(
                SetupBasicStock.item_code == item_code
            )
        if warehouse_code:
            _query = _query.filter(
                SetupBasicStock.wh_code == warehouse_code
            )
        _basic_stock_items = _query.all()

        for _item in _basic_stock_items:
            _receiving_items.append({
                'id': _item.id,
                'type': 'SetupBasicStock',
                'receiving_date': datetime.strptime('2000-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
                'quantity': _item.basic_stock,
                'item_code': _item.item_code,
                'unit_price': _item.item_unit_price
            })
        return _receiving_items
