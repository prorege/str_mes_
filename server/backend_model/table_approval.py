# -*- coding: utf-8 -*-

print("module [backend_model.table_approval.py] loaded")

from datetime import datetime
from sqlalchemy import DDL, event
from backend_model.database import DBManager
from backend_model.table_common import Companies
from sqlalchemy.dialects.mysql import MEDIUMTEXT

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
