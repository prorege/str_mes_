# -*- coding: utf-8 -*-

print("module [backend_model.table_qr.py] loaded")
from datetime import datetime
from backend_model.database import DBManager
from backend_model.table_common import Companies
from backend_model.table_base import BaseItem
db = DBManager.db


class QRManagement(db.Model):  # QR관리
    __tablename__ = 'qr_management'
    __table_args__ = {
        'comment': 'QR관리'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate="CASCADE"), comment='품목코드')
    item_name = db.Column('item_name', db.String(128), comment='품명')
    standard = db.Column('standard', db.String(48), comment='규격')
    lot_no = db.Column('lot_no', db.String(48), comment='Lot No')
    warehouse = db.Column('warehouse', db.String(48), comment='창고')
    transaction_type = db.Column('transaction_type', db.String(48), comment='거래구분')
    asset_type = db.Column('asset_type', db.String(48), comment='자산구분')
    stock_number = db.Column('stock_number', db.String(48), comment='입고번호')
    delivery_date = db.Column('delivery_date', db.DateTime, comment='입고일자')
    quantity = db.Column('quantity', db.Integer, comment='수량')
    unit = db.Column('unit', db.String(10), comment='단위')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')


class LOTManagement(db.Model):  # LOT관리
    __tablename__ = 'lot_management'
    __table_args__ = {
        'comment': 'LOT관리'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    menu_name = db.Column('menu_name', db.String(48), comment='메뉴명')
    register_number = db.Column('register_number', db.String(48), comment='등록번호')
    lot_date = db.Column('lot_date', db.DateTime, comment='일자')
    lot_no = db.Column('lot_no', db.String(48), comment='Lot No')
    process_name = db.Column('process_name', db.String(48), comment='공정명')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate="CASCADE"), comment='품목코드')
    good_quantity = db.Column('good_quantity', db.Integer, comment='양품수량')
    bad_quantity = db.Column('bad_quantity', db.Integer, comment='불량수량')
    unit = db.Column('unit', db.String(10), comment='단위')
    receiving_quantity = db.Column('receiving_quantity', db.Integer, comment='입고수량')
    release_quantity = db.Column('release_quantity', db.Integer, comment='출고수량')
    company_name = db.Column('company_name', db.String(48), comment='업체명')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')

