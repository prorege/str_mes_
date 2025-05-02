# -*- coding: utf-8 -*-

from datetime import datetime
from backend_model.database import DBManager

print("module [backend_model.table_production.py] loaded")

db = DBManager.db


class CostClosingHistory(db.Model):  # 원가마감이력
    from backend_model.table_common import Companies
    from backend_model.table_base import BaseWarehouse

    __tablename__ = 'cost_closing_history'
    __table_args__ = {'comment': '원가관리(원가마감이력)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    start_date = db.Column('start_date', db.DateTime, comment='시작시간')
    end_date = db.Column('end_date', db.DateTime, comment='종료시간')
    manager = db.Column('manager', db.String(48), comment='담당자')
    closed = db.Column("closed", db.Boolean, server_default='1', comment="원가마감 적용 여부")
    applied = db.Column("applied", db.Boolean, server_default='0', comment="마감재고 원가 적용 여부")
    warehouse_code = db.Column("warehouse_code", db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment="마감창고")
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사테이블 FK')

    warehouse = db.relationship("BaseWarehouse", foreign_keys=[warehouse_code])
