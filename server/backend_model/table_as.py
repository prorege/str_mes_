# -*- coding: utf-8 -*-

print("module [backend_model.table_as.py] loaded")

from datetime import datetime
from sqlalchemy import DDL, event
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
    expense_description = db.Column('expense_description', db.String(64), comment='경비내역')
    expense_amount = db.Column('expense_amount', db.BigInteger, comment='예정소요경비')
    excution_amount = db.Column('excution_amount', db.BigInteger, comment='소요경비')
    plan_amount = db.Column('plan_amount', db.Float, comment='계획소요경비')
    time_amount = db.Column('time_amount', db.BigInteger, comment='시간')
    day_amount = db.Column('day_amount', db.Float, comment='일수')
    vat_type = db.Column('vat_type', db.String(48), comment='부가세구분')
    vat = db.Column('vat', db.Integer, comment='부가세')
    expense_source = db.Column('expense_source', db.String(64), comment='지출처')
    expense_date = db.Column('expense_date', db.DateTime, comment='지출일자')
    register = db.Column('register', db.String(48), comment='등록자')
    modify_register = db.Column('modify_register', db.String(48), comment='수정자')
    modify_date = db.Column('modify_date', db.DateTime, comment='수정일자')
    fk_as_result_id = db.Column('fk_as_result_id', db.Integer, db.ForeignKey(AsResult.id, ondelete='CASCADE', onupdate='CASCADE'), comment='A/S처리 FK')
    as_result = db.relationship('AsResult', foreign_keys=[fk_as_result_id])