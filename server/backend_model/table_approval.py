# -*- coding: utf-8 -*-

print("module [backend_model.table_approval.py] loaded")

from datetime import datetime
from sqlalchemy import DDL, event
from backend_model.database import DBManager
from backend_model.table_common import Companies
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from backend_model.table_base import BaseEmployee
from backend_model.table_project import ProjectBusiness

db = DBManager.db

class ApprovalManagement(db.Model):
    __tablename__ = 'approval_management'
    __table_args__ = {'comment': '전자결재관리'}

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    request_date = db.Column("request_date", db.DateTime, comment="요청일자")
    request_number = db.Column("request_number", db.String(48), comment="요청번호")
    request_path = db.Column("request_path", db.String(256), comment="요청경로")
    request_path_id = db.Column("request_path_id", db.Integer, comment="요청경로ID")
    request_name = db.Column("request_name", db.String(48), comment="요청자")
    approval_leader = db.Column("approval_leader", db.String(48), comment="결재팀장")
    approval_status = db.Column("approval_status", db.String(48), comment="결재상태")
    reject_reason = db.Column("reject_reason", db.String(256), comment="반려사유")
    approval_date = db.Column("approval_date", db.DateTime, comment="결재일자")


class ApprovalDocument(db.Model):
    __tablename__ = 'approval_document'
    __table_args__ = {"comment": "결재 문서"}

    id = db.Column('id', db.Integer, primary_key=True)
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    document_number = db.Column('document_number', db.String(48), comment='문서번호')
    document_name = db.Column('document_name', db.String(128), comment='문서명')
    document_path = db.Column('document_path', db.String(256), comment='문서경로')
    max_line = db.Column('max_line', db.Integer, comment='최대결재선')
    register = db.Column('register', db.String(48), comment='등록자')
    register_date = db.Column('register_date', db.DateTime, comment='등록일자')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')
    approval_line =db.relationship('ApprovalLine', lazy='dynamic')


class Approval(db.Model):
    __tablename__ = 'approval'
    __table_args__ = {"comment": "결재"}

    id = db.Column('id', db.Integer, primary_key=True)
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    approval_number = db.Column('approval_number', db.String(48), comment='상신번호')
    approval_date = db.Column('approval_date', db.DateTime, comment='상신일자')
    approval_status = db.Column('approval_status', db.String(48), comment='상신상황')
    approval_reason = db.Column('approval_reason', db.String(48), comment='반려사유')
    closing_yn = db.Column('closing_yn', db.Boolean, server_default='0', comment='종결여부')
    approval_result_date = db.Column('approval_result_date', db.DateTime, comment='결재처리일자')
    register = db.Column('register', db.String(48), comment='작성자')
    title = db.Column('title', db.String(96), comment='제목')
    content = db.Column('content', db.Text, comment='내용')
    etc = db.Column('etc', db.Text, comment='비고')
    fk_business_id = db.Column('fk_business_id', db.Integer, db.ForeignKey(ProjectBusiness.id), comment='영업 FK')
    fk_document_id = db.Column('fk_document_id', db.Integer, db.ForeignKey(ApprovalDocument.id), comment='문서 FK')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')
    approval_document = db.relationship('ApprovalDocument', foreign_keys=[fk_document_id])
    approval_attachment = db.relationship('ApprovalAttachment', lazy='dynamic')
    approval_line_result = db.relationship('ApprovalLineResult', lazy='dynamic')

class ApprovalAttachment(db.Model):
    __tablename__ = 'approval_attachment'
    __table_args__ = {"comment": "결재 첨부문서"}

    id = db.Column('id', db.Integer, primary_key=True)
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    file_name = db.Column('file_name', db.String(48), comment='파일명')
    file_path = db.Column('file_path', db.String(256), comment='파일경로')
    fk_approval_id = db.Column('fk_approval_id', db.Integer, db.ForeignKey(Approval.id), comment='결재 FK')
    approval = db.relationship('Approval', foreign_keys=[fk_approval_id])

class ApprovalLine(db.Model):
    __tablename__ = 'approval_line'
    __table_args__ = {"comment": "결재 결재선"}

    id = db.Column('id', db.Integer, primary_key=True)
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    manager = db.Column('manager', db.String(48), comment='상신자')
    line_order = db.Column('line_order', db.Integer, comment='결재순서')
    approval_manager = db.Column('approval_manager', db.String(48), comment='결재자')
    fk_document_id = db.Column('fk_document_id', db.Integer, db.ForeignKey(ApprovalDocument.id), comment='문서 FK')

class ApprovalLineResult(db.Model):
    __tablename__ = 'approval_line_result'
    __table_args__ = {"comment": "결재 결재선 결과"}

    id = db.Column('id', db.Integer, primary_key=True)
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    approval_manager = db.Column('approval_manager', db.String(48), comment='결재자')
    approval_result = db.Column('approval_result', db.String(48), comment='결재결과')
    approval_reason = db.Column('approval_reason', db.String(48), comment='반려사유')
    approval_date = db.Column('approval_date', db.DateTime, comment='결재일자')
    closing_yn = db.Column('closing_yn', db.Boolean, server_default='0', comment='종결여부')
    fk_approval_line_id = db.Column('fk_approval_line_id', db.Integer, db.ForeignKey(ApprovalLine.id), comment='결재선 FK')
    fk_approval_id = db.Column('fk_approval_id', db.Integer, db.ForeignKey(Approval.id), comment='결재 FK')
    approval_line = db.relationship('ApprovalLine', foreign_keys=[fk_approval_line_id])
    approval = db.relationship('Approval', foreign_keys=[fk_approval_id])