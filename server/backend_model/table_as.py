# -*- coding: utf-8 -*-

print("module [backend_model.table_as.py] loaded")

from datetime import datetime
from sqlalchemy import DDL, event, text
from backend_model.database import DBManager
from backend_model.table_common import Companies
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from backend_model.table_project import ProjectManagement
from backend_model.table_base import BaseItem

db = DBManager.db   

class AsReceipt(db.Model):
    __tablename__ = 'as_receipt'
    __table_args__ = {'comment': 'A/S접수'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    receipt_number = db.Column('receipt_number', db.String(48), comment='접수번호')
    receipt_manager = db.Column('receipt_manager', db.String(48), comment='접수 담당자')
    receipt_detail = db.Column('receipt_detail', db.String(512), comment='접수 내용')
    department = db.Column('department', db.String(48), comment='등록부서')
    manager = db.Column('manager', db.String(48), comment='등록담당자')
    client_manager = db.Column('client_manager', db.String(48), comment='고객사  담당자')
    client_manager_phone = db.Column('client_manager_phone', db.String(48), comment='고객사 담당자 연락처')
    receipt_date = db.Column('receipt_date', db.DateTime, comment='접수일자')
    paid_type = db.Column('paid_type', db.String(48), comment='유무상 구분')
    closing_yn = db.Column('closing_yn', db.Boolean, server_default='0', comment='종결여부')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate='CASCADE'), comment='프로젝트 FK')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id, onupdate='CASCADE'), comment='회사 FK')
    project_management = db.relationship('ProjectManagement', foreign_keys=[fk_project_management_id])


class AsReceiptItem(db.Model):
    __tablename__ = 'as_receipt_item'
    __table_args__ = {'comment': '(A/S접수) 담당자 지정'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    manager = db.Column('manager', db.String(48), comment='담당자')
    manager_phone = db.Column('manager_phone', db.String(48), comment='담당자 연락처')
    fk_as_receipt_id = db.Column('fk_as_receipt_id', db.Integer, db.ForeignKey(AsReceipt.id, onupdate='CASCADE', ondelete='CASCADE'), comment='A/S접수 FK')
    as_receipt = db.relationship('AsReceipt', foreign_keys=[fk_as_receipt_id])


class AsResult(db.Model):
    __tablename__ = 'as_result'
    __table_args__ = {'comment': 'A/S처리'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    result_number = db.Column('result_number', db.String(48), comment='A/S처리번호')
    result_date = db.Column('result_date', db.DateTime, comment='A/S처리일자')
    result_department = db.Column('result_department', db.String(48), comment='처리부서')
    result_manager = db.Column('result_manager', db.String(48), comment='처리담당자')
    result_manager_check = db.Column('result_manager_check', db.String(48), comment='처리담당자 확인')
    result_detail = db.Column('result_detail', db.String(512), comment='처리내용')
    result_price = db.Column('result_price', db.Integer, comment='A/S처리비용')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate='CASCADE'), comment='프로젝트관리 FK')
    fk_as_receipt_id = db.Column('fk_as_receipt_id', db.Integer, db.ForeignKey(AsReceipt.id, onupdate='CASCADE', ondelete='CASCADE'), comment='A/S접수 FK')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id, onupdate='CASCADE'), comment='회사 FK')
    project_management = db.relationship('ProjectManagement', foreign_keys=[fk_project_management_id])
    as_receipt = db.relationship('AsReceipt', foreign_keys=[fk_as_receipt_id])

class AsResultItem(db.Model):
    __tablename__ = 'as_result_item'
    __table_args__ = {'comment': '(A/S처리) 사용자재'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE', ondelete='SET NULL'), comment='품목코드')
    item_quantity = db.Column('item_quantity', db.Integer, comment='수량')
    unit_price = db.Column('unit_price', db.Numeric(12, 2), comment='단가')
    supply_price = db.Column('supply_price', db.Numeric(14, 2), comment='공급가')
    etc = db.Column('etc', db.String(512), comment='비고')
    fk_as_result_id = db.Column('fk_as_result_id', db.Integer, db.ForeignKey(AsResult.id, onupdate='CASCADE', ondelete='CASCADE'), comment='A/S처리 FK')
    as_result = db.relationship('AsResult', foreign_keys=[fk_as_result_id])
    item = db.relationship("BaseItem", foreign_keys=[item_code])
    
class AsResultAttachment(db.Model):
    __tablename__ = 'as_result_attachment'
    __table_args__ = {'comment': '(A/S처리) 첨부파일'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    file_name = db.Column('file_name', db.String(256), comment='파일명')
    file_path = db.Column('file_path', db.String(256), comment='파일경로')
    fk_as_result_id = db.Column('fk_as_result_id', db.Integer, db.ForeignKey(AsResult.id, onupdate='CASCADE', ondelete='CASCADE'), comment='A/S처리 FK')
    as_result = db.relationship('AsResult', foreign_keys=[fk_as_result_id])

class AsResultExpense(db.Model):
    __tablename__ = 'as_result_expense'
    __table_args__ = {'comment': '(A/S처리) 비용'}
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    expense_date = db.Column('expense_date', db.DateTime, comment='지출일자')
    register = db.Column('register', db.String(48), comment='등록자')
    expense_description = db.Column('expense_description', db.String(64), comment='경비항목')
    expense_amount = db.Column('expense_amount', db.BigInteger, comment='금액')
    etc = db.Column('etc', db.String(512), comment='비고')
    fk_as_result_id = db.Column('fk_as_result_id', db.Integer, db.ForeignKey(AsResult.id, ondelete='CASCADE', onupdate='CASCADE'), comment='A/S처리 FK')
    as_result = db.relationship('AsResult', foreign_keys=[fk_as_result_id])


class AsReceiptResultStatus(db.Model):
    __tablename__ = 'v_as_receipt_result_status'
    __table_args__ = {'comment': 'A/S 접수-처리 현황'}
    
    # AsReceipt 
    receipt_id = db.Column('receipt_id', db.Integer, comment='접수 ID')
    receipt_number = db.Column('receipt_number', db.String(48), comment='접수번호')
    receipt_manager = db.Column('receipt_manager', db.String(48), comment='접수 담당자')
    receipt_detail = db.Column('receipt_detail', db.String(512), comment='접수 내용')
    receipt_date = db.Column('receipt_date', db.DateTime, comment='접수일자')
    paid_type = db.Column('paid_type', db.String(48), comment='유무상 구분')
    closing_yn = db.Column('closing_yn', db.Boolean, comment='종결여부')
    
    # AsResult 
    result_id = db.Column('result_id', db.Integer, comment='처리 ID')
    result_number = db.Column('result_number', db.String(48), comment='A/S처리번호')
    result_date = db.Column('result_date', db.DateTime, comment='A/S처리일자')
    result_manager = db.Column('result_manager', db.String(48), comment='처리담당자')
    result_detail = db.Column('result_detail', db.String(512), comment='처리내용')
    result_price = db.Column('result_price', db.Integer, comment='A/S처리비용')
    
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, comment='프로젝트 FK')
    fk_company_id = db.Column('fk_company_id', db.Integer, comment='회사 FK')
    
    # ProjectManagement  
    project_number = db.Column('project_number', db.String(48), comment='프로젝트번호')
    project_name = db.Column('project_name', db.String(128), comment='프로젝트명')
    contract_company = db.Column('contract_company', db.String(128), comment='수요기관')
    
    __mapper_args__ = {
        'primary_key': [receipt_id, result_id]
    }


create_as_receipt_result_status = DDL("""
DROP VIEW IF EXISTS v_as_receipt_result_status;
CREATE OR REPLACE VIEW v_as_receipt_result_status AS
SELECT 
    ar.id as receipt_id,
    ar.receipt_number, -- 접수번호
    ar.receipt_date, -- 접수일자
    ar.receipt_manager, -- 접수담당자
    ar.receipt_detail, -- 접수내용
    ar.paid_type, -- 유무상구분
    ar.closing_yn,
    ars.id as result_id,
    ars.result_number, -- A/S처리번호
    ars.result_date, -- A/S처리일자
    ars.result_manager, -- A/S처리담당자
    ars.result_detail, -- A/S처리내용
    ars.result_price, -- A/S처리비용
    ar.fk_project_management_id,
    ar.fk_company_id,
    pm.project_number, -- 프로젝트번호
    pm.project_name, -- 프로젝트명
    pm.contract_company -- 수요기관
FROM as_receipt ar
LEFT JOIN as_result ars ON ar.id = ars.fk_as_receipt_id
LEFT JOIN project_management pm ON ar.fk_project_management_id = pm.id
""")

event.listen(AsReceiptResultStatus.__table__, 'after_create', create_as_receipt_result_status.execute_if(dialect='mysql'))
