# -*- coding: utf-8 -*-

from sqlalchemy import DDL, event
from datetime import datetime
from backend_model.database import DBManager
from backend_model.table_project import ProjectManagement
print("module [backend_model.table_stock.py] loaded")

db = DBManager.db


class StockEtc(db.Model):  # 재고관리 - 기타입출고
    from backend_model.table_common import Companies

    __tablename__ = 'stock_etc'
    __table_args__ = {'comment': '재고관리(기타입출고)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    number = db.Column('number', db.String(48), comment='기타입출고 번호')
    target_date = db.Column('target_date', db.DateTime, comment='입출고 일자')
    department = db.Column('department', db.String(48), comment='담당부서')
    manager = db.Column('manager', db.String(48), comment='담당자')
    note = db.Column('note', db.String(256), comment='참고사항')
    etc = db.Column('etc', db.Text, comment='비고')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')


class StockEtcItem(db.Model):  # 재고관리 - 기타입출고 - 품목
    from backend_model.table_base import BaseItem, BaseWarehouse

    __tablename__ = 'stock_etc_item'
    __table_args__ = {'comment': '기타입출고(품목)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    type = db.Column('type', db.String(48), comment='구분')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE'), comment='품목코드')
    quantity = db.Column('quantity', db.Integer, server_default='0', comment='수량')
    unit_price = db.Column('unit_price', db.Numeric(10, 2), server_default='0', comment='단가')
    cost_price = db.Column('cost_price', db.Numeric(10, 2), server_default='0', comment='원가')
    total_cost_price = db.Column('total_cost_price', db.Numeric(20, 4), server_default='0', comment='원가합계')
    supply_price = db.Column('supply_price', db.Numeric(20, 2), server_default='0', comment='금액')
    warehouse_code = db.Column('warehouse_code', db.ForeignKey(BaseWarehouse.wh_code), comment='입출고창고')
    inout_type = db.Column('inout_type', db.String(48), comment='입출고유형')
    note = db.Column('note', db.String(256), comment='참고')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id))
    fk_stock_etc_id = db.Column('fk_stock_etc_id', db.Integer, db.ForeignKey(StockEtc.id), comment='기타입출고 FK')
    project_management = db.relationship("ProjectManagement", foreign_keys=[fk_project_management_id])
    stock_etc = db.relationship("StockEtc", foreign_keys=[fk_stock_etc_id])
    item = db.relationship('BaseItem', foreign_keys=[item_code])
    warehouse = db.relationship('BaseWarehouse', foreign_keys=[warehouse_code])
    basic_stock = db.relationship('SetupBasicStock', viewonly=True,
                                  primaryjoin='and_(foreign(StockEtcItem.item_code) == SetupBasicStock.item_code,'
                                              'foreign(StockEtcItem.warehouse_code) == SetupBasicStock.wh_code)')


class StockMoveRequest(db.Model):  # 재고관리 - 재고이동요청
    from backend_model.table_common import Companies

    __tablename__ = 'stock_move_request'
    __table_args__ = {'comment': '재고관리(재고이동요청)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    number = db.Column('number', db.String(48), comment='이동요청 번호')
    target_date = db.Column('target_date', db.DateTime, comment='요청 일자')
    department = db.Column('department', db.String(48), comment='담당부서')
    manager = db.Column('manager', db.String(48), comment='담당자')
    note = db.Column('note', db.String(256), comment='참고사항')
    etc = db.Column('etc', db.Text, comment='비고')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')


class StockMoveRequestItem(db.Model):  # 재고관리 - 재고이동요청 - 품목
    from backend_model.table_base import BaseItem, BaseWarehouse
    from backend_model.table_production import WorkOrder, WorkOrderItem2

    __tablename__ = 'stock_move_request_item'
    __table_args__ = {'comment': '재고이동요청(품목)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE'), comment='품목코드')
    quantity = db.Column('quantity', db.Numeric(10, 2), comment='수량')
    unit_price = db.Column('unit_price', db.Numeric(10, 2), comment='단가')
    unit = db.Column('unit', db.String(10), comment='단위')
    supply_price = db.Column('price', db.BigInteger, comment='금액')
    client_company = db.Column("client_company", db.String(48), comment="주공급업체")
    out_warehouse = db.Column('out_warehouse', db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment='출고창고')
    in_warehouse = db.Column('in_warehouse', db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment='입고창고')
    note = db.Column('note', db.String(256), comment='참고')
    asset_type = db.Column('asset_type', db.String(48), comment='자산구분')
    not_shipped = db.Column('not_shipped', db.Integer, comment='미출고수량')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id), comment="프로젝트 FK")
    fk_work_order_id = db.Column('fk_work_order_id', db.Integer, db.ForeignKey(WorkOrder.id), comment='작업지시 FK')
    fk_work_order_item_id = db.Column('fk_work_order_item_id', db.Integer, db.ForeignKey(WorkOrderItem2.id), comment='작업지시품목 FK')
    fk_stock_move_request_id = db.Column('fk_stock_move_request_id', db.Integer, db.ForeignKey(StockMoveRequest.id, onupdate='CASCADE', ondelete='CASCADE'), comment='재고이동 FK')
    project_management = db.relationship("ProjectManagement", foreign_keys=[fk_project_management_id])
    item = db.relationship('BaseItem', foreign_keys=[item_code])
    stock_move_request = db.relationship("StockMoveRequest", foreign_keys=[fk_stock_move_request_id])
    warehouse_release = db.relationship('BaseWarehouse', foreign_keys=[out_warehouse])
    warehouse_receive = db.relationship('BaseWarehouse', foreign_keys=[in_warehouse])
    work_order = db.relationship('WorkOrder', foreign_keys=[fk_work_order_id])


class StockMoveRelease(db.Model):  # 재고관리 - 재고이동출고
    from backend_model.table_common import Companies

    __tablename__ = 'stock_move_release'
    __table_args__ = {'comment': '재고관리(재고이동출고)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    number = db.Column('number', db.String(48), comment='이동출고 번호')
    target_date = db.Column('target_date', db.DateTime, comment='요청 일자')
    department = db.Column('department', db.String(48), comment='담당부서')
    manager = db.Column('manager', db.String(48), comment='담당자')
    note = db.Column('note', db.String(256), comment='참고사항')
    etc = db.Column('etc', db.Text, comment='비고')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')


class StockMoveReleaseItem(db.Model):  # 재고관리 - 재고이동출고 - 품목
    from backend_model.table_base import BaseItem, BaseWarehouse
    from backend_model.table_production import WorkOrder

    __tablename__ = 'stock_move_release_item'
    __table_args__ = {'comment': '재고이동출고(품목)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE'), comment='품목코드')
    request_quantity = db.Column('request_quantity', db.Numeric(10, 2), comment='요청수량')
    release_quantity = db.Column('release_quantity', db.Integer, comment='출고수량')
    unit_price = db.Column('unit_price', db.Numeric(10, 2), comment='단가')
    cost_price = db.Column('cost_price', db.Numeric(10, 2), server_default='0', comment='원가')
    total_cost_price = db.Column('total_cost_price', db.Numeric(20, 4), server_default='0', comment='원가합계')
    unit = db.Column('unit', db.String(10), comment='단위')
    supply_price = db.Column('price', db.BigInteger, comment='금액')
    client_company = db.Column("client_company", db.String(48), comment="주공급업체")
    out_warehouse = db.Column('out_warehouse', db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment='출고창고')
    in_warehouse = db.Column('in_warehouse', db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment='입고창고')
    note = db.Column('note', db.String(48), comment='참고')
    asset_type = db.Column('asset_type', db.String(48), comment='자산구분')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id))
    fk_stock_move_release_id = db.Column('fk_stock_move_release_id', db.Integer, db.ForeignKey(StockMoveRelease.id), comment='재고이동출고 FK')
    fk_stock_move_request_item_id = db.Column('fk_stock_move_request_item_id', db.Integer, db.ForeignKey(StockMoveRequestItem.id), comment='재고이동요청품목 FK')
    fk_work_order_id = db.Column('fk_work_order_id', db.Integer, db.ForeignKey(WorkOrder.id), comment='작업지시 FK')
    project_management = db.relationship("ProjectManagement", foreign_keys=[fk_project_management_id])
    item = db.relationship('BaseItem', foreign_keys=[item_code])
    stock_move_release = db.relationship("StockMoveRelease", foreign_keys=[fk_stock_move_release_id])
    warehouse_release = db.relationship('BaseWarehouse', foreign_keys=[out_warehouse])
    warehouse_receive = db.relationship('BaseWarehouse', foreign_keys=[in_warehouse])
    work_order = db.relationship('WorkOrder', foreign_keys=[fk_work_order_id])


class StockCorrection(db.Model):  # 재고관리 - 재고보정
    from backend_model.table_common import Companies

    __tablename__ = 'stock_correction'
    __table_args__ = {'comment': '재고관리(재고보정)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    number = db.Column('number', db.String(48), comment='기타입출고 번호')
    target_date = db.Column('target_date', db.DateTime, comment='입출고 일자')
    department = db.Column('department', db.String(48), comment='담당부서')
    manager = db.Column('manager', db.String(48), comment='담당자')
    note = db.Column('note', db.String(256), comment='참고사항')
    etc = db.Column('etc', db.Text, comment='비고')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')


class StockCorrectionItem(db.Model):  # 재고관리 - 재고보정 - 품목
    from backend_model.table_base import BaseItem, BaseWarehouse
    from backend_model.table_export import ExportCommInvoice, ExportCommInvoiceItem

    __tablename__ = 'stock_correction_item'
    __table_args__ = {'comment': '재고보정(품목)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    type = db.Column('type', db.String(48), comment='구분')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE'), comment='품목코드')
    quantity = db.Column('quantity', db.Integer, comment='수량')
    unit_price = db.Column('unit_price', db.Integer, comment='단가')
    supply_price = db.Column('supply_price', db.BigInteger, comment='금액')
    warehouse_code = db.Column('warehouse_code', db.ForeignKey(BaseWarehouse.wh_code), comment='보정창고')
    correction_type = db.Column('correction_type', db.String(48), comment='보정유형')
    note = db.Column('note', db.String(256), comment='참고')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id))
    fk_stock_correction_id = db.Column('fk_stock_correction_id', db.Integer, db.ForeignKey(StockCorrection.id), comment='재고보정 FK')
    fk_export_comm_invoice_id = db.Column('fk_export_comm_invoice_id', db.Integer, db.ForeignKey(ExportCommInvoice.id), comment='comm-invoice FK')
    fk_export_comm_invoice_item_id = db.Column('fk_export_comm_invoice_item_id', db.Integer, db.ForeignKey(ExportCommInvoiceItem.id), comment='comm-invoice item FK')
    project_management = db.relationship("ProjectManagement", foreign_keys=[fk_project_management_id])
    stock_correction = db.relationship("StockCorrection", foreign_keys=[fk_stock_correction_id])
    export_comm_invoice = db.relationship("ExportCommInvoice", foreign_keys=[fk_export_comm_invoice_id])
    export_comm_invoice_item = db.relationship("ExportCommInvoiceItem", foreign_keys=[fk_export_comm_invoice_item_id])
    item = db.relationship('BaseItem', foreign_keys=[item_code])
    warehouse = db.relationship('BaseWarehouse', foreign_keys=[warehouse_code])
    basic_stock = db.relationship('SetupBasicStock', viewonly=True,
                                  primaryjoin='and_(foreign(StockCorrectionItem.item_code) == SetupBasicStock.item_code,'
                                              'foreign(StockEtcItem.warehouse_code) == SetupBasicStock.wh_code)')


# ----------------------------------------------------------------------------------------------------------------------
# CREATE STORED PROCEDURE

# 재고이동출고품목의 출고수량 합계 가져오기
proc_get_stock_move_release_item_total_release_quantity = DDL('''
DROP PROCEDURE IF EXISTS proc_get_stock_move_release_item_total_release_quantity;
CREATE PROCEDURE `proc_get_stock_move_release_item_total_release_quantity`(
    IN `id` INT,
    OUT `sum` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '재고이동출고품목의 출고수량 합계 가져오기'
BEGIN
    SET sum = (SELECT SUM(release_quantity)
               FROM stock_move_release_item
               WHERE fk_stock_move_request_item_id = id
               GROUP BY fk_stock_move_request_item_id);
    IF sum IS NULL THEN
        SET sum = 0;
    ENd IF;
END
''')
event.listen(StockMoveReleaseItem.__table__, 'after_create', proc_get_stock_move_release_item_total_release_quantity)

# 재고이동출고품목의 출고수량 합계 가져오기
proc_get_stock_correction_item_total_quantity = DDL('''
DROP PROCEDURE IF EXISTS proc_get_stock_correction_item_total_quantity;
CREATE PROCEDURE `proc_get_stock_correction_item_total_quantity`(
    IN `id` INT,
    OUT `sum` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '재고보정품목의 수량 합계 가져오기'
BEGIN
    SET sum = (SELECT SUM(quantity)
               FROM stock_correction_item
               WHERE fk_export_comm_invoice_item_id = id
               GROUP BY fk_export_comm_invoice_item_id);
    IF sum IS NULL THEN
        SET sum = 0;
    ENd IF;
END
''')
event.listen(StockCorrectionItem.__table__, 'after_create', proc_get_stock_correction_item_total_quantity)


# ----------------------------------------------------------------------------------------------------------------------
# CREATE TRIGGER

# 기타입출고 삭제
before_stock_etc_delete = DDL('''
DROP TRIGGER IF EXISTS before_stock_etc_delete;
CREATE TRIGGER before_stock_etc_delete 
BEFORE DELETE ON stock_etc
FOR EACH ROW
BEGIN
    # 기타입출고품목 삭제
    DELETE FROM stock_etc_item WHERE fk_stock_etc_id = OLD.id;
END;''')
event.listen(StockEtc.__table__, 'after_create', before_stock_etc_delete)

# 기타입출고품목 삭제
after_stock_etc_item_delete = DDL('''
DROP TRIGGER IF EXISTS after_stock_etc_item_delete;
CREATE TRIGGER after_stock_etc_item_delete 
AFTER DELETE ON stock_etc_item
FOR EACH ROW
BEGIN
    # 재고 업데이트
    IF OLD.type = '입고' THEN
        UPDATE setup_basic_stock
        SET current_stock = current_stock - OLD.quantity, 
            available_stock = available_stock - OLD.quantity
        WHERE item_code = OLD.item_code AND wh_code = OLD.warehouse_code;
    ELSE
        UPDATE setup_basic_stock
        SET current_stock = current_stock + OLD.quantity, 
            available_stock = available_stock + OLD.quantity
        WHERE item_code = OLD.item_code AND wh_code = OLD.warehouse_code;
    END IF;
END;''')
event.listen(StockEtcItem.__table__, 'after_create', after_stock_etc_item_delete)

# 재고이동요청 삭제
before_stock_move_request_delete = DDL('''
DROP TRIGGER IF EXISTS before_stock_move_request_delete;
CREATE TRIGGER before_stock_move_request_delete 
BEFORE DELETE ON stock_move_request
FOR EACH ROW
BEGIN
    # 재고이동요청품목 삭제
    DELETE FROM stock_move_request_item WHERE fk_stock_move_request_id = OLD.id;
END;''')
event.listen(StockMoveRequest.__table__, 'after_create', before_stock_move_request_delete)

# 재고이동요청 삭제
after_stock_move_request_delete = DDL('''
DROP TRIGGER IF EXISTS after_stock_move_request_delete;
CREATE TRIGGER after_stock_move_request_delete 
AFTER DELETE ON stock_move_request
FOR EACH ROW
BEGIN
    # 작업지시의 재고이동요청번호 삭제
    UPDATE work_order
    SET stock_move_request_number = NULL, closing_yn = 0
    WHERE stock_move_request_number = OLD.number;
END;''')
event.listen(StockMoveRequest.__table__, 'after_create', after_stock_move_request_delete)

# 재고이동요청품목 업데이트
after_stock_move_request_item_update = DDL('''
DROP TRIGGER IF EXISTS after_stock_move_request_item_update;
CREATE TRIGGER after_stock_move_request_item_update
AFTER UPDATE ON stock_move_request_item
FOR EACH ROW
BEGIN
    # 작업지시품목2 미출고수량 업데이트
    IF OLD.fk_work_order_item_id IS NOT NULL THEN
        UPDATE work_order_item2
        SET uninput_quantity = NEW.not_shipped
        WHERE id = OLD.fk_work_order_item_id;
    END IF;
END;''')
event.listen(StockMoveRequestItem.__table__, 'after_create', after_stock_move_request_item_update)

# 재고이동출고 삭제
before_stock_move_release_delete = DDL('''
DROP TRIGGER IF EXISTS before_stock_move_release_delete;
CREATE TRIGGER before_stock_move_release_delete 
BEFORE DELETE ON stock_move_release
FOR EACH ROW
BEGIN
    # 재고이동출고품목 삭제
    DELETE FROM stock_move_release_item WHERE fk_stock_move_release_id = OLD.id;
END;''')
event.listen(StockMoveRelease.__table__, 'after_create', before_stock_move_release_delete)

# 재고이동출고품목 삭제
after_stock_move_release_item_delete = DDL('''
DROP TRIGGER IF EXISTS after_stock_move_release_item_delete;
CREATE TRIGGER after_stock_move_release_item_delete 
AFTER DELETE ON stock_move_release_item
FOR EACH ROW
BEGIN
    # 재고이동요청품목의 미출고수량 업데이트
    CALL proc_get_stock_move_release_item_total_release_quantity(OLD.fk_stock_move_request_item_id, @sum);
    
    UPDATE stock_move_request_item
    SET not_shipped = ceil(quantity) - @sum
    WHERE id = OLD.fk_stock_move_request_item_id;

    # 현재고, 가용재고 업데이트
    UPDATE setup_basic_stock
    SET current_stock = current_stock - OLD.release_quantity, 
        available_stock = available_stock - OLD.release_quantity
    WHERE item_code = OLD.item_code AND wh_code = OLD.in_warehouse;
    
    UPDATE setup_basic_stock
    SET current_stock = current_stock + OLD.release_quantity, 
        available_stock = available_stock + OLD.release_quantity
    WHERE item_code = OLD.item_code AND wh_code = OLD.out_warehouse;
END;''')
event.listen(StockMoveReleaseItem.__table__, 'after_create', after_stock_move_release_item_delete)

# 재고보정 삭제
before_stock_correction_delete = DDL('''
DROP TRIGGER IF EXISTS before_stock_correction_delete;
CREATE TRIGGER before_stock_correction_delete 
BEFORE DELETE ON stock_correction
FOR EACH ROW
BEGIN
    # 재고보정품목 삭제
    DELETE FROM stock_correction_item WHERE fk_stock_correction_id = OLD.id;
END;''')
event.listen(StockCorrection.__table__, 'after_create', before_stock_correction_delete)

# 재고보정품목 추가
after_stock_correction_item_insert = DDL('''
DROP TRIGGER IF EXISTS after_stock_correction_item_insert;
CREATE TRIGGER after_stock_correction_item_insert 
AFTER INSERT ON stock_correction_item
FOR EACH ROW
BEGIN
    # comm-invoice의 미입고수량 업데이트
    IF NEW.fk_export_comm_invoice_item_id IS NOT NULL THEN
        CALL proc_get_stock_correction_item_total_quantity(NEW.fk_export_comm_invoice_item_id, @sum);
    
        UPDATE export_comm_invoice_item
        SET not_received = invoice_quantity - @sum
        WHERE id = NEW.fk_export_comm_invoice_item_id;
    END IF;
END;''')
event.listen(StockCorrectionItem.__table__, 'after_create', after_stock_correction_item_insert)

# 재고보정품목 수정
after_stock_correction_item_update = DDL('''
DROP TRIGGER IF EXISTS after_stock_correction_item_update;
CREATE TRIGGER after_stock_correction_item_update 
AFTER UPDATE ON stock_correction_item
FOR EACH ROW
BEGIN
    # comm-invoice의 미입고수량 업데이트
    IF NEW.fk_export_comm_invoice_item_id IS NOT NULL THEN
        CALL proc_get_stock_correction_item_total_quantity(NEW.fk_export_comm_invoice_item_id, @sum);
    
        UPDATE export_comm_invoice_item
        SET not_received = invoice_quantity - @sum
        WHERE id = NEW.fk_export_comm_invoice_item_id;
    END IF;
END;''')
event.listen(StockCorrectionItem.__table__, 'after_create', after_stock_correction_item_update)

# 재고보정품목 삭제
after_stock_correction_item_delete = DDL('''
DROP TRIGGER IF EXISTS after_stock_correction_item_delete;
CREATE TRIGGER after_stock_correction_item_delete 
AFTER DELETE ON stock_correction_item
FOR EACH ROW
BEGIN
    # comm-invoice의 미입고수량 업데이트
    IF OLD.fk_export_comm_invoice_item_id IS NOT NULL THEN
        CALL proc_get_stock_correction_item_total_quantity(OLD.fk_export_comm_invoice_item_id, @sum);
    
        UPDATE export_comm_invoice_item
        SET not_received = invoice_quantity - @sum
        WHERE id = OLD.fk_export_comm_invoice_item_id;
    END IF;
END;''')
event.listen(StockCorrectionItem.__table__, 'after_create', after_stock_correction_item_delete)
