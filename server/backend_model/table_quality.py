# -*- coding: utf-8 -*-

print("module [backend_model.table_quality.py] loaded")
from datetime import datetime
from sqlalchemy import DDL, event
from backend_model.database import DBManager
from backend_model.table_common import Companies
from backend_model.table_base import BaseItem
from backend_model.table_production import WorkOrder, PerformanceRegistration, PerformanceRegistrationItem1
from backend_model.table_purchase import PurchasePreReceivingItem
from sqlalchemy.dialects.mysql import MEDIUMTEXT
db = DBManager.db


class QualityManagement(db.Model):  # 품질관리 - 검사등록관리
    __tablename__ = 'quality_management'
    __table_args__ = {
        'comment': '품질관리(검사등록관리)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    qa_number = db.Column('qa_number', db.String(48), comment='검사번호')
    qa_date = db.Column('qa_date', db.DateTime, comment='검사일자')
    equipment = db.Column('equipment', db.String(48), comment='설비')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE'), comment='품목코드')
    item_name = db.Column('item_name', db.String(128), comment='품명')
    standard = db.Column('standard', db.String(48), comment='규격')
    qa_manager = db.Column('qa_manager', db.String(48), comment='검사자')
    test_type = db.Column('test_type', db.String(48), comment='검사구분')
    ref_number = db.Column('ref_number', db.String(48), comment='가입고번호/작지번호')
    qa_count = db.Column('qa_count', db.Integer, comment='검사횟수')
    process_name = db.Column('process_name', db.String(48), comment='공정명')
    worker = db.Column('worker', db.String(48), comment='작업자')
    lot_no = db.Column('lot_no', db.String(48), comment='LOT No.')
    qa_standard_path = db.Column('qa_standard_path', db.String(48), comment='검사기준서이미지 경로')
    process_quantity = db.Column('process_quantity', db.Integer, comment='공정수량')
    bad_quantity = db.Column('bad_quantity', db.Integer, comment='불량수량')
    good_quantity = db.Column('good_quantity', db.Integer, comment='양품수량')
    action_quantity = db.Column('action_quantity', db.Integer, comment='재작업수량')
    fk_prereceiving_item = db.Column('fk_prereceiving_item', db.Integer, db.ForeignKey(PurchasePreReceivingItem.id, onupdate='CASCADE', ondelete='RESTRICT'), comment='가입고품목 FK')
    fk_performance_registration_item = db.Column('fk_performance_registration_item', db.Integer, db.ForeignKey(PerformanceRegistrationItem1.id, onupdate='CASCADE', ondelete='RESTRICT'), comment='생산입고품목 FK')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')
    item = db.relationship('BaseItem', uselist=False)


class NonConformanceAction(db.Model):  # 품질관리 - 부적합조치
    __tablename__ = 'non_conformance_action'
    __table_args__ = {
        'comment': '품질관리(부적합조치)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    done = db.Column('done', db.Boolean, default=False, comment='조치완료')
    lot_no = db.Column('lot_no', db.String(48), comment='LOT No.')
    product_code = db.Column('product_code', db.String(48), comment='제품코드')
    product_name = db.Column('product_name', db.String(48), comment='제품명')
    process_name = db.Column('process_name', db.String(48), comment='공정명')
    equipment_name = db.Column('equipment_name', db.String(48), comment='설비명')
    qa_manager = db.Column('qa_manager', db.String(48), comment='검사자')
    bad_type = db.Column('bad_type', db.String(48), comment='불량유형')
    bad_reason = db.Column('bad_reason', db.String(255), comment='불량사유')
    bad_quantity = db.Column('bad_quantity', db.Integer, comment='불량수량')
    action_quantity = db.Column('action_quantity', db.Integer, comment='재작업수량')
    fk_quality_management_id = db.Column('fk_quality_management_id', db.Integer, db.ForeignKey(QualityManagement.id), comment='검사등록관리 FK')
    fk_work_order_id = db.Column('fk_work_order_id', db.Integer, db.ForeignKey(WorkOrder.id), comment='작업지시 FK')
    fk_performance_id = db.Column('fk_performance_id', db.Integer, db.ForeignKey(PerformanceRegistration.id), comment='생산입고 FK')
    fk_performance_item1_id = db.Column('fk_performance_item1_id', db.Integer, db.ForeignKey(PerformanceRegistrationItem1.id), comment='생산입고품목 FK')
    fk_item_code = db.Column('fk_item_code', db.Integer, db.ForeignKey(BaseItem.id), comment='품목코드 FK')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')
    quality_management = db.relationship("QualityManagement", foreign_keys=[fk_quality_management_id])
    performance = db.relationship("PerformanceRegistration", foreign_keys=[fk_performance_id])
    performance_item = db.relationship("PerformanceRegistrationItem1", foreign_keys=[fk_performance_item1_id])
    work_order = db.relationship("WorkOrder", foreign_keys=[fk_work_order_id])
    item = db.relationship("BaseItem", foreign_keys=[fk_item_code])


class NonConformanceActionItem(db.Model):  # 품질관리 - 부적합조치 항목
    __tablename__ = 'non_conformance_action_item'
    __table_args__ = {
        'comment': '부적합조치(항목)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    action_date = db.Column('action_date', db.DateTime, comment='조치일자')
    action_manager = db.Column('action_manager', db.String(48), comment='조치담당자')
    action_quantity = db.Column('action_quantity', db.Integer, comment='조치수량')
    action_detail = db.Column('action_detail', db.String(256), comment='조치내용')
    note = db.Column('note', db.String(256), comment='적요')
    action_checker = db.Column('action_checker', db.String(48), comment='조치확인자')
    confirm_date = db.Column('confirm_date', db.DateTime, comment='확인일자')
    fk_non_conformance_action_id = db.Column('fk_non_conformance_action_id', db.Integer, db.ForeignKey(NonConformanceAction.id), comment='부적합조치 FK')


class MeasuringEquipment(db.Model):  # 품질관리 - 측정장비
    __tablename__ = 'measuring_equipment'
    __table_args__ = {
        'comment': '품질관리(측정장비)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    equipment_code = db.Column('equipment_code', db.String(48), comment='장비코드')
    equipment_name = db.Column('equipment_name', db.String(48), comment='장비명')
    manufacturer = db.Column('manufacturer', db.String(48), comment='제조원')
    purchase_date = db.Column('purchase_date', db.DateTime, comment='구입일자')
    correction_date = db.Column('correction_date', db.DateTime, comment='교정일자')
    correction_interval = db.Column('correction_interval', db.Integer, comment='교정주기')
    alarm_date = db.Column('alarm_date', db.DateTime, comment='알림기준일')
    model_name = db.Column('model_name', db.String(48), comment='모델명')
    serial_number = db.Column('serial_number', db.String(48), comment='시리얼번호')
    note = db.Column('note', db.String(256), comment='적요')
    file_attachments = db.Column('file_attachments', db.String(256), comment='첨부파일')
    file_correction = db.Column('file_correction', db.String(256), comment='첨부파일')
    file_receipt = db.Column('file_receipt', db.String(256), comment='첨부파일')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')


class QAStandard(db.Model):  # 품질관리 - 검사기준
    __tablename__ = 'qa_standard'
    __table_args__ = {
        'comment': '품질관리(검사기준)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    qa_type = db.Column('qa_type', db.String(24), comment='검사구분')
    qa_item = db.Column('qa_item', db.String(24), comment='검사항목')
    qa_standard = db.Column('qa_standard', db.String(10), comment='검사규격')
    measurement_unit = db.Column('measurement_unit', db.String(10), comment='측정단위')
    tolerance_plus = db.Column('tolerance_plus', db.Integer, comment='공차(+)')
    tolerance_minus = db.Column('tolerance_minus', db.Integer, comment='공차(-)')
    qa_method = db.Column('qa_method', db.String(48), comment='검사방법')
    input_type = db.Column('input_type', db.String(48), comment='입력구분')
    qa_count = db.Column('qa_count', db.Integer, comment='검사횟수')
    qa_image = db.Column('qa_img_path', MEDIUMTEXT, comment='이미지등록')
    fk_base_item_id = db.Column('fk_base_item_id', db.Integer, db.ForeignKey(BaseItem.id, onupdate="CASCADE",ondelete="CASCADE"), comment='품목 FK')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')


# ----------------------------------------------------------------------------------------------------------------------
# CREATE TRIGGER

# 검사등록관리 삭제 시
after_quality_management_delete = DDL('''
DROP TRIGGER IF EXISTS after_quality_management_delete;
CREATE TRIGGER after_quality_management_delete
AFTER DELETE ON quality_management
FOR EACH ROW
BEGIN
    IF OLD.fk_prereceiving_item IS NOT NULL THEN
        UPDATE purchase_prereceiving_item 
        SET check_yn = 0, check_quantity = 0, bad_quantity = 0, good_quantity = 0
        WHERE id = OLD.fk_prereceiving_item;
    END IF;
    
    IF OLD.fk_performance_registration_item IS NOT NULL THEN
        UPDATE performance_registration_item1
        SET check_yn = 0, check_quantity = 0, bad_quantity = 0, good_quantity = 0, action_quantity = 0
        WHERE id = OLD.fk_performance_registration_item;
    END IF;
END;''')
event.listen(QualityManagement.__table__, 'after_create', after_quality_management_delete)

# ----------------------------------------------------------------------------------------------------------------------
