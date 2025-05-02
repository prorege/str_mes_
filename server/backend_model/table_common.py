# -*- coding: utf-8 -*-

print("module [backend_model.table_common.py] loaded")
from datetime import datetime
from backend_model.database import DBManager
from sqlalchemy.dialects.mysql import MEDIUMTEXT

db = DBManager.db


class Companies(db.Model):  # 기업
    __tablename__ = 'companies'
    __table_args__ = {
        'comment': '기업'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    name = db.Column('name', db.String(48), comment='업체명')
    address = db.Column('address', db.String(256), comment='주소')
    zip_code = db.Column('zip_code', db.String(10), comment='우편번호')
    phone = db.Column('phone', db.String(30), comment='대표전화번호')
    fax = db.Column('fax', db.String(30), comment='팩스번호')
    email = db.Column('email', db.String(48), comment='대표 이메일')
    homepage = db.Column('homepage', db.String(48), comment='홈페이지')
    bill_manager = db.Column('bill_manager', db.String(48), comment='계산서 담당자')
    bill_email = db.Column('bill_email', db.String(48), comment='계산서 이메일')
    system_start_date = db.Column('system_start_date', db.DateTime, comment='시스템 시작일')
    basic_stock_date = db.Column('basic_stock_date', db.DateTime, comment='기초 재고 등록일')
    basic_balance_date = db.Column('basic_balance_date', db.DateTime, comment='기초 잔액 등록일')
    logo = db.Column('logo', MEDIUMTEXT, comment='업체 로고')
    corp_number = db.Column('corp_number', db.String(24), comment='법인번호')
    business_number = db.Column('business_number', db.String(24), comment='사업자번호')
    ceo_name = db.Column('ceo_name', db.String(48), comment='대표자명')
    business_status = db.Column('business_status', db.String(48), comment='업태')
    business_sector = db.Column('business_sector', db.String(48), comment='종목')
    name_en = db.Column('name_en', db.String(48), comment='업체명(영문)')
    ceo_name_en = db.Column('ceo_name_en', db.String(48), comment='대표자명(영문)')
    phone_en = db.Column('phone_en', db.String(30), comment='전화번호(국제)')
    fax_en = db.Column('fax_en', db.String(30), comment='팩스번호(국제)')
    address_en = db.Column('address_en', db.String(256), comment='주소(영문)')
    register_id = db.Column('register_id', db.String(48), comment='최초등록자')
    modify_id = db.Column('modify_id', db.String(48), comment='최종수정자')
    last_updated_date = db.Column('last_updated_date', db.DateTime, comment='최종수정일자')


class Users(db.Model):  # 사용자/관리자
    __tablename__ = 'users'
    __table_args__ = {
        'comment': '사용자'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    user_id = db.Column('user_id', db.String(48), comment='사용자 ID')
    user_pw = db.Column('user_pw', db.String(256), comment='사용자 비밀번호')
    user_name = db.Column('user_name', db.String(48), comment='사용자 이름')
    user_type = db.Column('user_type', db.Integer, default=2, comment='사용자 유형')
    user_status = db.Column('user_status', db.Integer, default=1, comment='사용자 상태')
    phone = db.Column('phone', db.String(30), comment='전화번호')
    email = db.Column('email', db.String(48), comment='이메일주소')
    token = db.Column('token', db.String(128), comment='로그인토큰')
    last_logon_time = db.Column('last_logon_time', db.DateTime, comment='마지막 접속시간')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사테이블 FK')

    def serialize(self):
        json = {
            # property (a)
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_type": self.user_type,
            "user_status": self.user_status,
            "phone": self.phone,
            "email": self.email,
            "token": self.token,
            "last_logon_time": self.last_logon_time,
            "fk_company_id": self.fk_company_id
        }
        return json


class AccessHistory(db.Model):  # 접속 이력 테이블
    __tablename__ = 'access_history'
    __table_args__ = {
        'comment': '접속 이력'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    user_id = db.Column('user_id', db.String(48), comment='유저 ID')
    type = db.Column('type', db.Boolean, comment='로그인 유형')
    update_time = db.Column('update_time', db.DateTime, comment='사용자 접속 시간')
    ip_addr = db.Column('ip_addr', db.String(20), comment='사용자 접속 IP')
    os_ver = db.Column('os_ver', db.String(20), comment='사용자 접속 OS 버전')
    browser_ver = db.Column('browser_ver', db.String(20), comment='사용자 접속 브라우져 버전')
    fk_user_id = db.Column('fk_user_id', db.Integer, db.ForeignKey(Users.id), comment='사용자테이블 FK')
    user = db.relationship('Users')
