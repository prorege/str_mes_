# -*- coding: utf-8 -*-

import os
import base64
from uuid import uuid4
from pathlib import Path
from backend_model.database import DBManager

db = DBManager.db


class LibUtil(object):
    @staticmethod
    def check_exist_connected_data(connected_table, fk_column, instance_id):
        item = db.session.query(connected_table).filter(fk_column == instance_id).first()
        if item:
            from backend_lib.lib_exception import MesException
            MesException.raise_exist_connected_data()
            
    @staticmethod
    def check_item_code_exist_connected_data(connected_table, instance_id):
        from backend_model.table_base import BaseItem
        item = db.session.query(connected_table).join(
            BaseItem, BaseItem.id == instance_id
        ).filter(
            BaseItem.item_code == connected_table.item_code
        ).all()
        if item:
            return True
        else:
            return False

    @staticmethod
    def base64_to_file(base64str, save_path):
        imgtype, imgbody = base64str.split(';')
        imgtype, ext = imgtype.rsplit('/')
        imgbody = imgbody.replace('base64,', '')
        filename = str(uuid4()) + '.' + ext

        img_bytes = base64.b64decode(imgbody)
        Path(save_path).mkdir(parents=True, exist_ok=True)

        with open(os.path.join(save_path, filename), 'wb') as f:
            f.write(img_bytes)

        return filename

    @staticmethod
    def calculate_price(vat_type, quantity, unit_price):
        import math
        if vat_type == '별도':
            supply_price = int(quantity) * int(unit_price)
            vat = math.floor(supply_price * 0.1)
            total_price = int(supply_price) + int(vat)
        elif vat_type == '포함':
            total_price = int(quantity) * int(unit_price)
            supply_price = round(total_price * 10 / 11)
            vat = int(total_price) - int(supply_price)
        elif vat_type == '영세':
            supply_price = int(quantity) * int(unit_price)
            vat = 0
            total_price = int(supply_price)
        else:
            supply_price = int(quantity) * int(unit_price)
            vat = 0
            total_price = int(supply_price)
        return {'supply_price': supply_price, 'vat': vat, 'total_price': total_price}

    @staticmethod
    def ceil(value: float, decimal_index: int) -> float:
        import math
        temp = 10 ** (decimal_index - 1)
        return math.ceil(value * temp) / temp
