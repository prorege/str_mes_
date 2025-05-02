# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import DDL, event
from backend_model.database import DBManager
from backend_model.table_base import BaseItem, BaseWarehouse
from backend_model.table_common import Companies

print("module [backend_model.table_import.py] loaded")

db = DBManager.db


class ExportSalesOrder(db.Model):  # 수출관리 - 수주
    __tablename__ = 'export_sales_order'
    __table_args__ = {
        'comment': '수출관리(수주)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    order_number = db.Column('order_number', db.String(48), comment='OrderNo (수주번호)')
    order_date = db.Column('order_date', db.DateTime, comment='OrderDate (수주일자)')
    client_company = db.Column('client_company', db.String(48), comment='Buyer')
    client_manager = db.Column('client_manager', db.String(48), comment='BuyerContact')
    order_department = db.Column('order_department', db.String(48), comment='OwnerDept')
    order_manager = db.Column('order_manager', db.String(48), comment='Member')
    payment_terms = db.Column('payment_terms', db.String(48), comment='PayTerms (결재조건)')
    vat_type = db.Column('vat_type', db.String(48), comment='PriceTerms (가격조건)')
    origin = db.Column('origin', db.String(48), comment='Origin (원산지)')
    ship_port = db.Column('ship_port', db.String(48), comment='ShipPort (수송항구)')
    currency = db.Column('currency', db.String(48), comment='Currency (통화종류)')
    exrate = db.Column('exrate', db.Numeric(10,2), default=0, comment='ExRate (환율)')
    order_type = db.Column('order_type', db.String(48), comment='OrderType')
    supply_price = db.Column('supply_price', db.BigInteger, comment='공급가')
    vat = db.Column('vat', db.BigInteger, comment='부가세')
    total_price = db.Column('total_price', db.BigInteger, comment='합계금액')
    etc = db.Column('etc', db.Text, comment='Remark (참고사항)')
    confirmed = db.Column('confirmed', db.Boolean, server_default='0', comment='수주 확정 여부')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id, onupdate='CASCADE', ondelete='CASCADE'), comment='회사 FK')


class ExportSalesOrderItem(db.Model):  # 수출관리 - 수주 - 수주품목
    __tablename__ = 'export_sales_order_item'
    __table_args__ = {
        'comment': '수출관리(수주품목)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE', ondelete='SET NULL'), comment='ItemCode')
    order_quantity = db.Column('order_quantity', db.Integer, comment='Qty (수량)')
    unit_price = db.Column('unit_price', db.Numeric(14,4), default=0, comment='ExportPrice (수출단가)')
    supply_price = db.Column('supply_price', db.Numeric(14,4), server_default="0", comment='Amount (총금액)')
    request_delivery_date = db.Column('request_delivery_date', db.DateTime, comment='Req Date')
    contact_delivery_date = db.Column('contact_delivery_date', db.DateTime, comment='Con Date')
    assign_quantity = db.Column('assign_quantity', db.Integer, comment='할당수량')
    not_shipped = db.Column('not_shipped', db.Integer, comment='미선적량')
    lot = db.Column("lot", db.String(48), comment="LOT NO (생산주차)")
    warehouse_code = db.Column('warehouse_code', db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment='출고창고')
    fk_export_sales_order_id = db.Column('fk_export_sales_order_id', db.Integer, db.ForeignKey(ExportSalesOrder.id), comment='수주 Fk')
    export_order= db.relationship("ExportSalesOrder", foreign_keys=[fk_export_sales_order_id])
    item = db.relationship("BaseItem", foreign_keys=[item_code])
    warehouse = db.relationship('BaseWarehouse', foreign_keys=[warehouse_code])
    basic_stock = db.relationship('SetupBasicStock', viewonly=True,
                                  primaryjoin='and_(foreign(ExportSalesOrderItem.item_code) == SetupBasicStock.item_code,'
                                              'foreign(ExportSalesOrderItem.warehouse_code) == SetupBasicStock.wh_code)')

    def excel_import_columns(self):
        return dict(
            output=[self.item_code, self.lot, self.order_quantity, self.unit_price],
            key=[self.item_code]
        )


class ExportCommInvoice(db.Model):  # 수출관리 - 출고
    __tablename__ = 'export_comm_invoice'
    __table_args__ = {
        'comment': '수출관리(출고)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    invoice_number = db.Column('invoice_number', db.String(48), comment='Invoice No (선적번호)')
    invoice_date = db.Column('invoice_date', db.DateTime, comment='Invoice Date (선적일자)')
    ship_date = db.Column('ship_date', db.DateTime, comment='ShipDate')
    sale_date = db.Column('sale_date', db.DateTime, comment='SaleDate (출고일자)')
    client_company = db.Column('client_company', db.String(48), comment='Buyer')
    client_manager = db.Column('client_manager', db.String(48), comment='Buyer Contact')
    invoice_department = db.Column('invoice_department', db.String(48), comment='Owner Dept')
    invoice_manager = db.Column('invoice_manager', db.String(48), comment='Member')
    currency = db.Column('currency', db.String(48), comment='Currency')
    exrate = db.Column('exrate', db.Numeric(10,2), default=0, comment='ExRate')
    etc = db.Column('etc', db.Text, comment='비고')
    supply_price = db.Column('supply_price', db.BigInteger, comment='공급가')
    vat = db.Column('vat', db.BigInteger, comment='부가세')
    vat_type = db.Column('vat_type', db.String(48), comment='부가세구분')
    total_price = db.Column('total_price', db.BigInteger, comment='합계금액')
    confirmed = db.Column('confirmed', db.Boolean, server_default='0', comment='출고 확정 여부')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id, onupdate='CASCADE', ondelete='CASCADE'), comment='회사 FK')


class ExportCommInvoiceItem(db.Model):  # 수출관리 - 출고 - 출고품목
    __tablename__ = 'export_comm_invoice_item'
    __table_args__ = { 'comment': '수출관리(출고품목)' }

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE', ondelete='SET NULL'), comment='품목코드')
    order_quantity = db.Column('order_quantity', db.Integer, server_default='0', comment='Qty (수주수량)')
    invoice_quantity = db.Column('invoice_quantity', db.Integer, server_default='0', comment='출고수량')
    unit_price = db.Column('unit_price', db.Numeric(14,4), server_default='0', comment='ExportPrice (수출단가)')
    supply_price = db.Column('supply_price', db.Numeric(14,4), server_default="0", comment='Amount (총금액)')
    cost_price = db.Column('cost_price', db.Numeric(10, 2), server_default='0', comment='원가')
    total_cost_price = db.Column('total_cost_price', db.Numeric(20, 4), server_default='0', comment='원가합계')
    request_delivery_date = db.Column('request_delivery_date', db.DateTime, comment='Req Date')
    contact_delivery_date = db.Column('contact_delivery_date', db.DateTime, comment='Con Date')
    non_invoice = db.Column('non_invoice', db.Integer, server_default='0', comment='미계산서')
    not_received = db.Column('not_received', db.Integer, server_default='0', comment='미입고')
    lot = db.Column("lot", db.String(48), comment="생산주차")
    warehouse_code = db.Column('warehouse_code', db.String(48), db.ForeignKey(BaseWarehouse.wh_code, onupdate='CASCADE', ondelete='SET NULL'), comment='출고창고')
    order_number = db.Column('order_number', db.String(48), comment='수주번호')
    fk_export_sales_order_item_id = db.Column('fk_export_sales_order_item_id', db.Integer, db.ForeignKey(ExportSalesOrderItem.id), comment='수주 품목 Fk')
    fk_export_comm_invoice_id = db.Column('fk_export_comm_invoice_id', db.Integer, db.ForeignKey(ExportCommInvoice.id), comment='출고 Fk')

    export_comm_invoice = db.relationship("ExportCommInvoice", foreign_keys=[fk_export_comm_invoice_id])
    export_sales_order_item = db.relationship("ExportSalesOrderItem", foreign_keys=[fk_export_sales_order_item_id])
    item = db.relationship("BaseItem", foreign_keys=[item_code])
    warehouse = db.relationship('BaseWarehouse', foreign_keys=[warehouse_code])
    basic_stock = db.relationship('SetupBasicStock', viewonly=True,
                                  primaryjoin='and_(foreign(ExportCommInvoiceItem.item_code) == SetupBasicStock.item_code,'
                                              'foreign(ExportCommInvoiceItem.warehouse_code) == SetupBasicStock.wh_code)')


# ----------------------------------------------------------------------------------------------------------------------
# CREATE TRIGGER

# 수주 삭제 시 수주품목 삭제
before_export_sales_order_delete = DDL('''
CREATE TRIGGER before_export_sales_order_delete
BEFORE DELETE ON export_sales_order
FOR EACH ROW
BEGIN
    DELETE FROM export_sales_order_item WHERE fk_export_sales_order_id = OLD.id;
END;''')
event.listen(ExportSalesOrder.__table__, 'after_create', before_export_sales_order_delete)

# 출고 삭제 시 출고품목 삭제
before_export_comm_invoice_delete = DDL('''
CREATE TRIGGER before_export_comm_invoice_delete
BEFORE DELETE ON export_comm_invoice
FOR EACH ROW
BEGIN
    DELETE FROM export_comm_invoice_item WHERE fk_export_comm_invoice_id = OLD.id;
END;''')
event.listen(ExportCommInvoice.__table__, 'after_create', before_export_comm_invoice_delete)

# 출고품목 삭제
after_export_comm_invoice_item_delete = DDL('''
DROP TRIGGER IF EXISTS after_export_comm_invoice_item_delete;
CREATE TRIGGER after_export_comm_invoice_item_delete
AFTER DELETE ON export_comm_invoice_item
FOR EACH ROW
BEGIN
    # 수주품목에서 가져온 경우 수주품목의 미출고 수량 복구
    IF OLD.fk_export_sales_order_item_id IS NOT NULL
    THEN
        UPDATE export_sales_order_item
        SET not_shipped = not_shipped + OLD.invoice_quantity
        WHERE id = OLD.fk_export_sales_order_item_id;
    END IF;

    # 현재고, 가용재고 업데이트
    UPDATE setup_basic_stock
    SET current_stock = current_stock + OLD.invoice_quantity, 
        available_stock = available_stock + OLD.invoice_quantity
    WHERE item_code = OLD.item_code AND wh_code = OLD.warehouse_code;
    
    UPDATE setup_basic_stock
    SET available_stock = current_stock
    WHERE item_code = OLD.item_code AND wh_code = OLD.warehouse_code AND available_stock > current_stock;
    
    UPDATE setup_basic_stock
    SET available_stock = 0
    WHERE item_code = OLD.item_code AND wh_code = OLD.warehouse_code AND available_stock < 0;
END;''')
event.listen(ExportCommInvoiceItem.__table__, 'after_create', after_export_comm_invoice_item_delete)