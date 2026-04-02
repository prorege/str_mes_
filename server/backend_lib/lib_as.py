# -*- coding: utf-8 -*-

from decimal import Decimal
from backend_model.database import DBManager
from backend_model.table_as import *
from backend_lib.lib_common import LibCommon
from backend import app
import os

db = DBManager.db

class LibAsReceipt(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        LibCommon.get_item_number(data, 'receipt_number', AsReceipt, AsReceipt.receipt_number, '/as/receipt')


class LibAsResult(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        LibCommon.get_item_number(data, 'result_number', AsResult, AsResult.result_number, '/as/result')

    @staticmethod
    def post_postprocessor(result=None, **kw):
        fk_as_receipt_id = result['fk_as_receipt_id']
        if fk_as_receipt_id is not None and fk_as_receipt_id != '':
            db.session.query(
                AsReceipt
            ).filter(
                AsReceipt.id == fk_as_receipt_id
            ).update({'closing_yn' : True})
            db.session.commit()
    @staticmethod
    def patch_single_preprocessor(instance_id=None, data=None, **kw):
        fk_as_receipt_id = data['fk_as_receipt_id']
        if fk_as_receipt_id is not None and fk_as_receipt_id != '':
            prev_result = db.session.query(
                AsResult
            ).filter(
                AsResult.id == instance_id
            ).first()
            if prev_result:
                if prev_result.fk_as_receipt_id != fk_as_receipt_id:
                    db.session.query(
                        AsReceipt
                    ).filter(
                        AsReceipt.id == prev_result.fk_as_receipt_id
                    ).update({'closing_yn' : False})
                    db.session.commit()
                    db.session.query(
                        AsReceipt
                    ).filter(
                        AsReceipt.id == fk_as_receipt_id
                    ).update({'closing_yn' : True})
                    db.session.commit()

    @staticmethod
    def delete_single_preprocessor(instance_id=None, **kw):
        prev_result = db.session.query(
            AsResult
        ).filter(
            AsResult.id == instance_id
        ).first()
        if prev_result:
            db.session.query(
                AsReceipt
            ).filter(
                AsReceipt.id == prev_result.fk_as_receipt_id
            ).update({'closing_yn' : False})
            db.session.commit()
        attachment = db.session.query(
            AsResultAttachment
        ).filter(
            AsResultAttachment.fk_as_result_id == instance_id
        ).all()
        for item in attachment:
            file_path = os.path.join(app.config['UPLOAD_BASE_DIR'], item.file_path)
            try:
                os.remove(file_path)
            except IsADirectoryError:
                pass

class LibAsResultItem(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_setup import LibSetupBasicStock, LibSetupControl

        if data and 'item_code' in data and 'warehouse_code' in data and 'item_quantity' in data:
            basic_stock = LibSetupBasicStock.get_basic_stock(data['item_code'], data['warehouse_code'])
            if basic_stock is None:
                from backend_lib.lib_exception import MesException
                MesException.raise_not_exist_basic_stock()

            new_current_stock = basic_stock.current_stock - data['item_quantity']
            LibSetupControl.check_minus_stock(basic_stock.fk_company_id, new_current_stock)

            basic_stock.current_stock = new_current_stock
            basic_stock.available_stock = basic_stock.available_stock - data['item_quantity']
            db.session.commit()

    @staticmethod
    def patch_single_preprocessor(instance_id=None, data=None, **kw):
        from backend_lib.lib_setup import LibSetupBasicStock, LibSetupControl

        if data and 'item_quantity' in data:
            item = db.session.query(AsResultItem).filter(AsResultItem.id == instance_id).first()
            if item:
                diff = data['item_quantity'] - item.item_quantity
                if diff != 0:
                    wh = data.get('warehouse_code', item.warehouse_code)
                    basic_stock = LibSetupBasicStock.get_basic_stock(item.item_code, wh)
                    new_current_stock = basic_stock.current_stock - diff
                    LibSetupControl.check_minus_stock(basic_stock.fk_company_id, new_current_stock)

                    basic_stock.current_stock = new_current_stock
                    basic_stock.available_stock = basic_stock.available_stock - diff
                    db.session.commit()

    @staticmethod
    def delete_single_preprocessor(instance_id=None, **kw):
        from backend_lib.lib_setup import LibSetupBasicStock

        item = db.session.query(AsResultItem).filter(AsResultItem.id == instance_id).first()
        if item and item.warehouse_code:
            basic_stock = LibSetupBasicStock.get_basic_stock(item.item_code, item.warehouse_code)
            if basic_stock:
                basic_stock.current_stock += item.item_quantity
                basic_stock.available_stock += item.item_quantity
                db.session.commit()