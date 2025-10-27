# -*- coding: utf-8 -*-

print("module [backend_model.table_project.py] loaded")
from datetime import datetime
from sqlalchemy import DDL, event
from backend_model.database import DBManager
from backend_model.table_common import Companies
from backend_model.table_base import BaseItem, BaseWarehouse
db = DBManager.db

class ProjectBusiness(db.Model): # 프로젝트 - 영업관리
    __tablename__ = 'project_business'
    __table_args__ = {
        'comment': '영업관리(영업등록)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    business_number = db.Column('business_number', db.String(64), comment='영업번호')
    business_name = db.Column('business_name', db.String(128), comment='영업건명')
    business_date = db.Column('business_date', db.DateTime, default=datetime.now, comment='영업일자')
    client_company = db.Column('client_company', db.String(128), comment='계약업체명')
    client_manager = db.Column('client_manager', db.String(48), comment='업체담당자')
    contract_company = db.Column('contract_company', db.String(48), comment='수요기관')
    business_department = db.Column('business_department', db.String(48), comment='담당부서')
    business_manager = db.Column('business_manager', db.String(48), comment='당사담당자')
    business_type = db.Column('business_type', db.String(48), comment='영업구분')
    classification = db.Column('classification', db.String(48), comment='종목')
    delivery_type = db.Column('delivery_type', db.String(48), comment='납품형태')
    location = db.Column('location', db.String(48), comment='지역')
    registration_closing_date = db.Column('registration_closing_date', db.DateTime, comment='등록마감')
    bid_closing_date = db.Column('bid_closing_date', db.DateTime, comment='투찰마감')
    business_status = db.Column('business_status', db.String(48), comment='현재단계')
    completion_date = db.Column('completion_date', db.DateTime, comment='준공일자')
    business_progress = db.Column('business_progress', db.String(48), comment='진행현황')
    business_important = db.Column('business_important', db.String(48), comment='중요')
    contract_type = db.Column('contract_type', db.String(48), comment='계약유형')
    gross_profit = db.Column('gross_profit', db.BigInteger, comment='매출총이익')
    gross_profit_rate = db.Column('gross_profit_rate', db.Float, comment='매출총이익률')
    operating_profit = db.Column('operating_profit', db.BigInteger, comment='순수익')
    operating_profit_rate = db.Column('operating_profit_rate', db.Float, comment='순수익률')
    business_amount = db.Column('business_amount', db.BigInteger, comment='영업금액')   
    rate = db.Column('rate', db.Float, comment='요율')
    modify_manager = db.Column('modify_manager', db.String(48), comment='최종수정자')
    modify_date = db.Column('modify_date', db.DateTime, comment='최종수정일자')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, comment="프로젝트 FK")
    project = db.relationship('ProjectManagement', viewonly=True, primaryjoin='foreign(ProjectBusiness.fk_project_management_id) == ProjectManagement.id')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')
    project_yn = db.Column('project_yn', db.Boolean, comment = "프로젝트여부")
    
    def excel_import_columns(self):
        return dict(
            output=[
                self.business_number,
                self.business_name,
                self.client_company,
                self.classification,
                self.registration_closing_date,
                self.bid_closing_date,
                self.business_amount,
            ],
            key=[self.business_number],
        )

class ProjectBusinessProgress(db.Model): # 프로젝트 - 영업관리 - 진행현황목록
    __tablename__ = 'project_business_progress'
    __table_args__ = {
        'comment': '영업관리(영업진행현황)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    progress_date = db.Column('progress_date', db.DateTime, comment='진행일자')
    client_manager = db.Column('client_manager', db.String(48), comment='업체담당자')
    progress_method = db.Column('progress_method', db.String(48), comment='진행방법')
    note = db.Column('note', db.String(128), comment='내용')
    fk_business_id = db.Column('fk_business_id', db.Integer, db.ForeignKey(ProjectBusiness.id, onupdate="CASCADE", ondelete="CASCADE"), comment='영업 FK')
    business = db.relationship('ProjectBusiness', foreign_keys=[fk_business_id], lazy='joined')

class ProjectBusinessQuote(db.Model): # 프로젝트 - 영업관리 - 견적현황
    __tablename__ = 'project_business_quote'
    __table_args__ = {
        'comment': '영업관리(견적현황)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    quote_date = db.Column('quote_date', db.DateTime, comment='견적일자')
    quote_manager = db.Column('quote_manager', db.String(48), comment='담당자')
    note = db.Column('note', db.String(256), comment='참고사항')
    file_name = db.Column('file_name', db.String(64), comment='첨부파일')
    file_path = db.Column('file_path', db.String(256), comment='첨부파일경로')
    fk_business_id = db.Column('fk_business_id', db.Integer, db.ForeignKey(ProjectBusiness.id, onupdate="CASCADE", ondelete="CASCADE"), comment='영업 FK')
    business = db.relationship('ProjectBusiness', foreign_keys=[fk_business_id], lazy='joined')


class ProjectBusinessNote(db.Model): # 프로젝트 - 영업관리 - 참고사항목록
    __tablename__ = 'project_business_note'
    __table_args__ = {
        'comment': '영업관리(영업참고사항)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    note_date = db.Column('note_date', db.DateTime, comment='등록일자')
    note_manager = db.Column('note_manager', db.String(48), comment='등록자')
    note_detail = db.Column('note_detail', db.String(256), comment='상세내용')
    fk_business_id = db.Column('fk_business_id', db.Integer, db.ForeignKey(ProjectBusiness.id, onupdate="CASCADE", ondelete="CASCADE"), comment='영업 FK')
    Business = db.relationship('ProjectBusiness', foreign_keys=[fk_business_id], lazy='joined')
    
class ProjectBusinessCost(db.Model): # 프로젝트 - 영업관리 - 원가검토
    __tablename__ = 'project_business_cost'
    __table_args__ = {
        'comment': '영업관리(원가검토)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_order = db.Column('item_order', db.Integer, comment='순서')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE'), comment='품목코드')
    quote_quantity = db.Column('quote_quantity', db.Numeric(11, 1), comment='견적수량')
    quote_unit_price = db.Column('quote_unit_price', db.BigInteger, comment='견적단가')
    quote_supply_price = db.Column('quote_supply_price', db.BigInteger, comment='견적공급가')
    purchase_unit_price = db.Column('purchase_unit_price', db.BigInteger, comment='구매단가')
    purchase_supply_price = db.Column('purchase_supply_price', db.BigInteger, comment='구매공급가')
    dc_rate = db.Column('dc_rate', db.Integer, comment='DC Rate')
    etc = db.Column('etc', db.Text, comment='비고')
    fk_business_id = db.Column('fk_business_id', db.Integer, db.ForeignKey(ProjectBusiness.id, onupdate="CASCADE", ondelete="CASCADE"), comment='영업 FK')
    business = db.relationship('ProjectBusiness', foreign_keys=[fk_business_id], lazy='joined')
    item = db.relationship('BaseItem', foreign_keys=[item_code])

class ProjectBusinessBasic(db.Model): # 프로젝트 - 영업관리 - 기초자료
    __tablename__ = 'project_business_basic'
    __table_args__ = {
        'comment': '영업관리(기초자료)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    basic_date = db.Column('basic_date', db.DateTime, comment='일자')
    basic_manager = db.Column('basic_manager', db.String(48), comment='담당자')
    note = db.Column('note', db.String(256), comment='참고사항')
    file_name = db.Column('file_name', db.String(64), comment='첨부파일')
    file_path = db.Column('file_path', db.String(256), comment='첨부파일경로')
    fk_business_id = db.Column('fk_business_id', db.Integer, db.ForeignKey(ProjectBusiness.id, onupdate="CASCADE", ondelete="CASCADE"), comment='영업 FK')
    business = db.relationship('ProjectBusiness', foreign_keys=[fk_business_id], lazy='joined')

class ProjectManagement(db.Model):  # 프로젝트관리 - 프로젝트
    __tablename__ = 'project_management'
    __table_args__ = {
        'comment': '프로젝트관리(프로젝트)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    contract_begin_date = db.Column('contract_begin_date', db.DateTime, comment='계약기간(시작)')
    contract_end_date = db.Column('contract_end_date', db.DateTime, comment='계약기간(종료)')
    project_number = db.Column('project_number', db.String(64), comment='프로젝트번호')
    project_name = db.Column('project_name', db.String(64), comment='프로젝트명')
    project_date = db.Column('project_date', db.DateTime, comment='등록 일자')
    order_company = db.Column('order_company', db.String(48), comment='계약업체')
    contract_company = db.Column('contract_company', db.String(48), comment='수요기관')
    project_department = db.Column('project_department', db.String(48), comment='등록부서')
    project_manager = db.Column('project_manager', db.String(48), comment='등록담당자')
    contract_date = db.Column('contract_date', db.DateTime, comment='계약일자')
    defect_end_date = db.Column('defect_end_date', db.DateTime, comment='하자만기')
    # contract_amount = db.Column('contract_amount', db.BigInteger, comment='원청금액')
    commencement_date = db.Column('commencement_date', db.Date, comment='착공일자')
    contract_vat_type = db.Column('contract_vat_type', db.String(48), comment='원청금액부가세구분')
    completion_date = db.Column('completion_date', db.DateTime, comment='준공일자')
    defect_period = db.Column('defect_period', db.String(48), comment='하자기간')
    company_amount = db.Column('company_amount', db.BigInteger, comment='계약금액')
    company_vat_type = db.Column('company_vat_type', db.String(48), comment='계약금액부가세구분')
    non_invoice = db.Column('non_invoice', db.Integer, comment='미계산서')
    subcontracting_rate = db.Column('subcontracting_rate', db.String(48), comment='하도급률')
    progress_status = db.Column('progress_status', db.String(48), comment='진행단계')
    project_important = db.Column('project_important', db.String(48), comment='중요')
    location = db.Column('location', db.String(48), comment='현장주소')
    total_progress = db.Column('total_progress', db.Integer, comment='일정관리 전체진행률')
    modify_manager = db.Column('modify_manager', db.String(48), comment='최종수정자')
    modify_date = db.Column('modify_date', db.DateTime, comment='최종수정일자')
    fk_business_id = db.Column('fk_business_id', db.Integer, db.ForeignKey(ProjectBusiness.id), comment='영업 FK')
    fk_excution_plan_id = db.Column('fk_excution_plan_id', db.Integer, comment='실행계획 FK')
    business = db.relationship('ProjectBusiness', foreign_keys=[fk_business_id])
    excution_plan = db.relationship('ProjectExcutionPlan', viewonly=True, primaryjoin='foreign(ProjectManagement.fk_excution_plan_id) == ProjectExcutionPlan.id')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')
    excution_yn = db.Column('excution_yn', db.Boolean, comment = "실행계획여부")
class ProjectItem(db.Model):  # 프로젝트 - 계약품목
    __tablename__ = 'project_item'
    __table_args__ = {
        'comment': '프로젝트(계약품목)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    quantity = db.Column('quantity', db.Integer, comment='수량')
    not_ordered = db.Column('not_ordered', db.Integer, comment="미수주수량")
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE'), comment='품목코드')
    fk_shipment_order_id = db.Column('fk_shipment_order_id', db.Integer, comment='수주 FK')
    fk_work_order_id = db.Column('fk_work_order_id', db.Integer, comment='작업지시 FK')
    fk_shipment_quote_item_id = db.Column('fk_shipment_quote_item_id', db.Integer, comment="견적 품목 FK")
    fk_business_cost_id = db.Column('fk_business_cost_id', db.Integer, db.ForeignKey(ProjectBusinessCost.id, onupdate="CASCADE", ondelete="CASCADE"), comment="원가검토 FK")
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate="CASCADE", ondelete="CASCADE"), comment='프로젝트관리 FK')
    shipment_order = db.relationship('ShipmentOrder', viewonly=True, primaryjoin='foreign(ProjectItem.fk_shipment_order_id) == ShipmentOrder.id')
    item = db.relationship('BaseItem', foreign_keys=[item_code])
    shipment_quote_item = db.relationship('ShipmentQuoteItem', viewonly=True, primaryjoin='foreign(ProjectItem.fk_shipment_quote_item_id) == ShipmentQuoteItem.id')
    project_management = db.relationship("ProjectManagement", foreign_keys=[fk_project_management_id])
    business_cost = db.relationship('ProjectBusinessCost', foreign_keys=[fk_business_cost_id])
class ProjectParticipant(db.Model): #프로젝트 - 참여직원
    __tabename__ = 'project_participation'
    __table_args__ = {
        'comment' : '프로젝트(참여직원)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    project_manager = db.Column('project_manager', db.String(48), comment='담당자')
    job_type = db.Column('job_type', db.String(48), comment='직무유형')
    note = db.Column('note', db.String(48), comment='내용')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate="CASCADE", ondelete="CASCADE"), comment='프로젝트관리 FK')
    project_management = db.relationship('ProjectManagement', foreign_keys=[fk_project_management_id])

class ProjectCompany(db.Model): # 프로젝트 - 관련업체
    __tabename__ = 'project_company'
    __table_args__ = {
        'comment' : '프로젝트(관련업체)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    company_name = db.Column('company_name', db.String(48), comment='업체명')
    company_type = db.Column('company_type', db.String(48), comment='업체구분')
    company_manager = db.Column('company_manager', db.String(48), comment='담당자')
    company_manager_phone = db.Column('company_manager_phone', db.String(48), comment='연락처')
    note = db.Column('note', db.String(256), comment='참고사항')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate="CASCADE", ondelete="CASCADE"), comment='프로젝트관리 FK')
    project_management = db.relationship('ProjectManagement', foreign_keys=[fk_project_management_id])

class ProjectDocument(db.Model):  # 프로젝트 - 계약자료
    __tablename__ = 'project_document'
    __table_args__ = {
        'comment': '프로젝트(계약자료)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    document_number = db.Column('document_number', db.String(128), comment='문서번호')
    document_name = db.Column('document_name', db.String(128), comment='문서명')
    note = db.Column('note', db.String(256), comment='참고사항')
    file_name = db.Column('file_name', db.String(64), comment='파일명')
    file_path = db.Column('file_path', db.String(256), comment='파일저장경로')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate="CASCADE", ondelete="CASCADE"), comment='프로젝트관리 FK')
    project_management = db.relationship("ProjectManagement", foreign_keys=[fk_project_management_id])

class ProjectReceipt(db.Model):  # 프로젝트 - AS접수및결과
    __tablename__ = 'project_receipt'
    __table_args__ = {
        'comment': '프로젝트(AS접수및결과)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    request_date = db.Column('request_date', db.DateTime, default=datetime.now, comment='요청일자')
    request_company = db.Column('request_company', db.String(48), comment='요청업체')
    request_manager = db.Column('request_manager', db.String(48), comment='AS요청자')
    problem = db.Column('problem', db.String(128), comment='AS증상')
    materials = db.Column('materials', db.String(128), comment='준비자재')
    equipment = db.Column('equipment', db.String(128), comment='투입장비')
    involved_people = db.Column('involved_people', db.String(128), comment='투입인원')
    involved_price = db.Column('involved_price', db.Integer, comment='투입비용')
    involved_price_detail = db.Column('involved_price_detail', db.String(256), comment='투입비용세부')
    result = db.Column('result', db.String(128), comment='조치결과')
    reason = db.Column('reason', db.String(256), comment='원인')
    note = db.Column('note', db.String(256), comment='개선요청사항')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate="CASCADE", ondelete="CASCADE"), comment='프로젝트관리 FK')
    project_management = db.relationship("ProjectManagement", foreign_keys=[fk_project_management_id])


class ProjectSchedule(db.Model):  # 프로젝트 - 일정관리
    __tablename__ = 'project_schedule'
    __table_args__ = {
        'comment': '프로젝트(일정관리)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    title = db.Column('title', db.String(48), comment='스케쥴')
    start_date = db.Column('start_date', db.DateTime, comment='스케시작일')
    end_date = db.Column('end_date', db.DateTime, comment='스케쥴종료일')
    progress_percent = db.Column('progress_percent', db.Integer, comment='진행률')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id), comment='프로젝트관리 FK')


class ProjectNotice(db.Model):  # 프로젝트 - 공지사항
    __tablename__ = 'project_notice'
    __table_args__ = {
        'comment': '프로젝트(공지사항)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    title = db.Column('title', db.String(48), comment='파일명')
    start_date = db.Column('start_date', db.DateTime, comment='공지시작일')
    end_date = db.Column('end_date', db.DateTime, comment='공지종료일')
    important = db.Column('important', db.Boolean, comment='중요여부')
    content_html = db.Column('content_html', db.Text, comment='내용')
    register_id = db.Column('register_id', db.String(48), comment='최초등록자')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')
    user = db.relationship('Users', viewonly=True, primaryjoin='foreign(ProjectNotice.register_id) == Users.user_id')


class ProjectExcutionPlan(db.Model): # 프로젝트 - 실행계획
    __tablename__ = 'project_excution_plan'
    __table_args__ = {
        'comment': '실행계획'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    excution_plan_number = db.Column('excution_plan_number', db.String(64), comment='실행계획번호')
    excution_plan_date = db.Column('excution_plan_date', db.DateTime, comment='등록일자')
    excution_plan_department = db.Column('excution_plan_department', db.String(48), comment='담당부서')
    excution_plan_manager = db.Column('excution_plan_manager', db.String(48), comment='담당자')
    approval_status = db.Column('approval_status', db.String(48), comment='결재상태')
    reject_reason = db.Column('reject_reason', db.String(64), comment='반려사유')
    contract_amount = db.Column('contract_amount', db.BigInteger, comment='계약금액')
    expect_amount = db.Column('expect_amount', db.BigInteger, comment='예정금액')
    excution_amount = db.Column('excution_amount', db.BigInteger, comment='실행금액')
    business_completion_amount = db.Column('business_completion_amount', db.BigInteger, comment='사업완료금액')
    contract_to_expect_rate = db.Column('contract_to_expect_rate', db.Float, comment='계약대비예정률')
    expect_to_excution_rate = db.Column('expect_to_excution_rate', db.Float, comment='예정대비실행률')
    contract_to_excution_rate = db.Column('contract_to_excution_rate', db.Float, comment='계약대비실행률')
    modify_manager = db.Column('modify_manager', db.String(48), comment='최종수정자')
    modify_date = db.Column('modify_date', db.DateTime, comment='최종수정일자')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate="CASCADE", ondelete="CASCADE"), comment='프로젝트관리 FK')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')
    project_management = db.relationship("ProjectManagement", foreign_keys=[fk_project_management_id])


class ProjectExcutionPlanItem(db.Model): # 프로젝트 - 실행계획 - 주요자재
    __tablename__ = 'project_excution_plan_item'
    __table_args__ = {
        'comment': '실행계획(주요자재)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE'), comment='품목코드')
    main_supplier = db.Column('main_supplier', db.String(48), comment='구매처')
    excution_plan_quantity = db.Column('excution_plan_quantity', db.Integer, comment='수량')
    not_excution_plan_quantity = db.Column('not_excution_plan_quantity', db.Integer, comment='미수량')
    assign_quantity = db.Column('assign_quantity', db.Integer, comment='할당수량')
    purchase_unit_price = db.Column('purchase_unit_price', db.Integer, comment='발주단가')
    unit_price = db.Column('unit_price', db.Integer, comment='단가')
    supply_price = db.Column('supply_price', db.BigInteger, comment='공급가')
    purchase_supply_price = db.Column('purchase_supply_price', db.BigInteger, comment='발주공급가')
    delivery_price = db.Column('delivery_price', db.Integer, comment='배송비')
    vat_type = db.Column('vat_type', db.String(48), comment='부가세구분')
    vat = db.Column('vat', db.Integer, comment='부가세')
    closing_yn = db.Column('closing_yn', db.Boolean, server_default='0', comment='종결여부')
    confirmed = db.Column('confirmed', db.Boolean, server_default='0', comment='발주확정')
    delivery_require = db.Column('delivery_require', db.Integer, comment='납기소요')
    delivery_date = db.Column('delivery_date', db.DateTime, comment='납기일자')
    order_date = db.Column('order_date', db.DateTime, comment='발주일자')
    order_date_modify = db.Column('order_date_modify', db.DateTime, comment='변경납기일자')
    note = db.Column('note', db.String(256), comment='비고')
    warehouse_code = db.Column('warehouse_code', db.String(48), db.ForeignKey(BaseWarehouse.wh_code, onupdate='CASCADE', ondelete='SET NULL'), comment='입고창고')
    register = db.Column('register', db.String(48), comment='등록자')
    modify_register = db.Column('modify_register', db.String(48), comment='수정자')
    modify_date = db.Column('modify_date', db.DateTime, comment='수정일자')
    fk_project_item_id = db.Column('fk_project_item_id', db.Integer, db.ForeignKey(ProjectItem.id, onupdate="CASCADE"), comment="프로젝트 품목 FK")
    fk_project_excution_plan_id = db.Column('fk_project_excution_plan_id', db.Integer, db.ForeignKey(ProjectExcutionPlan.id), comment='실행계획 FK')
    project_excution_plan = db.relationship('ProjectExcutionPlan', foreign_keys=[fk_project_excution_plan_id])
    item = db.relationship('BaseItem', foreign_keys=[item_code])
    warehouse = db.relationship('BaseWarehouse', foreign_keys=[warehouse_code])
    basic_stock = db.relationship('SetupBasicStock', viewonly=True,
                                  primaryjoin='and_(foreign(ProjectExcutionPlanItem.item_code) == SetupBasicStock.item_code,'
                                              'foreign(ProjectExcutionPlanItem.warehouse_code) == SetupBasicStock.wh_code)')


class ProjectExcutionPlanSubcontract(db.Model): # 프로젝트 - 실행계획 - 외주공사
    __tablename__ = 'project_excution_plan_subcontract'
    __table_args__ = {
        'comment': '실행계획(외주공사)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    subcontract_name = db.Column('subcontract_name', db.String(64), comment='공사명')
    subcontract_company = db.Column('subcontract_company', db.String(48), comment='공사업체')
    expect_amount = db.Column('expect_amount', db.BigInteger, comment='예정금액')
    purchase_unit_price = db.Column('purchase_unit_price', db.Integer, comment='발주단가')
    vat_type = db.Column('vat_type', db.String(48), comment='부가세구분')
    vat = db.Column('vat', db.Integer, comment='부가세')
    closing_yn = db.Column('closing_yn', db.Boolean, server_default='0', comment='종결여부')
    start_date = db.Column('start_date', db.DateTime, comment='시작일자')
    end_date = db.Column('end_date', db.DateTime, comment='종료일자')
    contract_document = db.Column('contract_document', db.String(256), comment='계약서')
    contract_document_path = db.Column('contract_document_path', db.String(256), comment='계약서경로')
    estimate_document = db.Column('estimate_document', db.String(256), comment='견적서')
    estimate_document_path = db.Column('estimate_document_path', db.String(256), comment='견적서경로')    
    contract_performance_bond = db.Column('contract_performance_bond', db.String(256), comment='계약이행증권')
    contract_performance_bond_path = db.Column('contract_performance_bond_path', db.String(256), comment='계약이행증권경로')
    defect_liability_bond = db.Column('defect_liability_bond', db.String(256), comment='하자이행증권')
    defect_liability_bond_path = db.Column('defect_liability_bond_path', db.String(256), comment='하자이행증권경로')
    register = db.Column('register', db.String(48), comment='등록자')
    modify_register = db.Column('modify_register', db.String(48), comment='수정자')
    modify_date = db.Column('modify_date', db.DateTime, comment='수정일자')
    fk_project_excution_plan_id = db.Column('fk_project_excution_plan_id', db.Integer, db.ForeignKey(ProjectExcutionPlan.id, ondelete='CASCADE', onupdate='CASCADE'), comment='실행계획 FK')
    project_excution_plan = db.relationship('ProjectExcutionPlan', foreign_keys=[fk_project_excution_plan_id])


class ProjectExcutionPlanExpense(db.Model): # 프로젝트 - 실행계획 - 경비
    __tablename__ = 'project_excution_plan_expense'
    __table_args__ = {
        'comment': '실행계획(경비)'
    }
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
    fk_project_excution_plan_id = db.Column('fk_project_excution_plan_id', db.Integer, db.ForeignKey(ProjectExcutionPlan.id, ondelete='CASCADE', onupdate='CASCADE'), comment='실행계획 FK')
    project_excution_plan = db.relationship('ProjectExcutionPlan', foreign_keys=[fk_project_excution_plan_id])

class ProjectBusinessTripLog(db.Model): # 프로젝트 - 출장 / 외근 관리 
    __tablename__ = 'project_business_trip_log'
    __table_args__ = {
        'comment': '출장/외근 관리'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    manager = db.Column('manager', db.String(48), comment='담당자')
    companion = db.Column('companion', db.String(96), comment='동행자')
    trip_type = db.Column('trip_type', db.String(48), comment='구분')
    trip_start_date = db.Column('trip_start_date', db.DateTime, comment='시작날짜')
    trip_end_date = db.Column('trip_end_date', db.DateTime, comment='종료날짜')
    note = db.Column('note', db.String(256), comment='내용')
    stopover = db.Column('stopover', db.String(96), comment='경유지')
    vehicle = db.Column('vehicle', db.String(48), comment='운행차량')
    project_name = db.Column('project_name', db.String(96), comment='프로젝트명')

class ProjectHappyCall(db.Model):  # 프로젝트 - 해피콜관리
    __tablename__ = 'project_happy_call'
    __table_args__ = {
        'comment': '프로젝트(해피콜관리)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    call_date = db.Column('call_date', db.DateTime, default=datetime.now, comment='일자')
    client_company = db.Column('client_company', db.String(48), comment='업체명')
    manager = db.Column('manager', db.String(48), comment='담당자')
    result = db.Column('result', db.String(48), comment='해피콜결과')
    satisfaction = db.Column('satisfaction', db.String(48), comment='만족도')
    note = db.Column('note', db.String(128), comment='고객객요청사항')
    register = db.Column('register', db.String(48), comment='등록자')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate="CASCADE"), comment='프로젝트관리 FK')
    project_management = db.relationship("ProjectManagement", foreign_keys=[fk_project_management_id])


class ProjectDailyLog(db.Model): # 프로젝트 - 일지등록
    __tablename__ = 'project_daily_log'
    __table_args__ = {
        'comment': '프로젝트(일지등록)'
    }   
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    log_date = db.Column('log_date', db.DateTime, comment='일자')
    work_type = db.Column('work_type', db.String(48), comment='업무유형')
    content = db.Column('content', db.String(256), comment='업무내용')
    attachment = db.Column('attachment', db.String(256), comment='첨부파일')
    attachment_path = db.Column('attachment_path', db.String(256), comment='첨부파일경로')
    register = db.Column('register', db.String(48), comment='등록자')
    register_date = db.Column('register_date', db.DateTime, comment='등록일자')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate="CASCADE", ondelete="CASCADE"), comment='프로젝트관리 FK')
    project_management = db.relationship("ProjectManagement", foreign_keys=[fk_project_management_id])


class ProjectCostLog(db.Model): # 프로젝트 - 비용관리
    __tablename__ = 'project_cost_log'
    __table_args__ = {
        'comment': '프로젝트(기성관리)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    cost_date = db.Column('cost_date', db.DateTime, comment='일자')
    prev_cost = db.Column('prev_cost', db.BigInteger, comment='전월기성')
    curr_cost = db.Column('curr_cost', db.BigInteger, comment='현재기성')
    cumulative_cost = db.Column('cumulative_cost', db.BigInteger, comment='누적기성')
    remaining_cost = db.Column('remaining_cost', db.Float, comment='잔여기성')
    total_cost_rate = db.Column('total_cost_rate', db.Float, comment='총기성률')
    etc = db.Column('etc', db.String(256), comment='비고')
    register = db.Column('register', db.String(48), comment='등록자')
    register_date = db.Column('register_date', db.DateTime, comment='등록일자')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate="CASCADE", ondelete="CASCADE"), comment='프로젝트관리 FK')
    project_management = db.relationship("ProjectManagement", foreign_keys=[fk_project_management_id])

class ProjectOutCostLog(db.Model): # 프로젝트 - 외주기성관리
    __tablename__ = 'project_out_cost_log'
    __table_args__ = {
        'comment': '프로젝트(외주기성관리)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    cost_date = db.Column('cost_date', db.DateTime, comment='일자')
    prev_cost = db.Column('prev_cost', db.BigInteger, comment='전월기성')
    curr_cost = db.Column('curr_cost', db.BigInteger, comment='현재기성')
    cumulative_cost = db.Column('cumulative_cost', db.BigInteger, comment='누적기성')
    remaining_cost = db.Column('remaining_cost', db.Float, comment='잔여기성')
    total_cost_rate = db.Column('total_cost_rate', db.Float, comment='총기성률')
    etc = db.Column('etc', db.String(256), comment='비고')
    register = db.Column('register', db.String(48), comment='등록자')
    register_date = db.Column('register_date', db.DateTime, comment='등록일자')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate="CASCADE", ondelete="CASCADE"), comment='프로젝트관리 FK')
    project_management = db.relationship("ProjectManagement", foreign_keys=[fk_project_management_id])


class ProjectCompletion(db.Model): # 프로젝트 - 준공관리
    __tablename__ = 'project_completion'
    __table_args__ = {
        'comment': '프로젝트(준공관리)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    completion_date = db.Column('completion_date', db.DateTime, comment='준공일자')
    completion_drawing = db.Column('completion_drawing', db.String(256), comment='준공도면')
    completion_drawing_path = db.Column('completion_drawing_path', db.String(256), comment='준공도면경로')
    completion_manual = db.Column('completion_manual', db.String(256), comment='운영메뉴얼')
    completion_manual_path = db.Column('completion_manual_path', db.String(256), comment='운영메뉴얼경로')
    completion_document = db.Column('completion_document', db.String(256), comment='준공서류')
    completion_document_path = db.Column('completion_document_path', db.String(256), comment='준공서류경로')
    maintenance_manual = db.Column('maintenance_manual', db.String(256), comment='유지보수지침서')
    maintenance_manual_path = db.Column('maintenance_manual_path', db.String(256), comment='유지보수지침서경로')
    defect_guarantee = db.Column('defect_guarantee', db.String(256), comment='하자이행보증증서')
    defect_guarantee_path = db.Column('defect_guarantee_path', db.String(256), comment='하자이행보증증서경로')
    register = db.Column('register', db.String(48), comment='등록자')
    register_date = db.Column('register_date', db.DateTime, comment='등록일자')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate="CASCADE", ondelete="CASCADE"), comment='프로젝트관리 FK')
    project_management = db.relationship("ProjectManagement", foreign_keys=[fk_project_management_id])


class ProjectMaterialApproval(db.Model): # 프로젝트 - 자재승인관리
    __tablename__ = 'project_material_approval'
    __table_args__ = {
        'comment': '프로젝트(자재승인관리)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    document_number = db.Column('document_number', db.String(48), comment='문서번호')
    etc = db.Column('etc', db.String(256), comment='비고')
    file_name = db.Column('file_name', db.String(64), comment='첨부파일')
    file_path = db.Column('file_path', db.String(256), comment='첨부파일경로')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate="CASCADE", ondelete="CASCADE"), comment='프로젝트관리 FK')
    project_management = db.relationship("ProjectManagement", foreign_keys=[fk_project_management_id])

class ProjectConstruction(db.Model): # 프로젝트 - 착공계
    __tablename__ = 'project_construction'
    __table_args__ = {
        'comment': '프로젝트(착공계)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    document_name = db.Column('document_name', db.String(96), comment='문서명')
    reference = db.Column('reference', db.String(48), comment='참조')
    contract_number = db.Column('contract_number', db.String(48), comment='계약번호')
    purchase_number = db.Column('purchase_number', db.String(48), comment='구매번호')
    etc = db.Column('etc', db.String(256), comment='비고')
    file_name = db.Column('file_name', db.String(64), comment='첨부파일')
    file_path = db.Column('file_path', db.String(256), comment='첨부파일경로')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate="CASCADE", ondelete="CASCADE"), comment='프로젝트관리 FK')
    project_management = db.relationship("ProjectManagement", foreign_keys=[fk_project_management_id])

class ProjectCustomerInformation(db.Model): # 프로젝트 - 고객정보관리
    __tablename__ = 'project_customer_information'
    __table_args__ = {
        'comment': '프로젝트(고객정보관리)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    information_date = db.Column('information_date', db.DateTime, comment='일자')
    manager = db.Column('manager', db.String(48), comment='담당자')
    manager_mobile = db.Column('manager_mobile', db.String(48), comment='담당자 휴대폰')
    manager_email = db.Column('manager_email', db.String(48), comment='담당자 이메일')
    note = db.Column('note', db.String(256), comment='메모사항')
    register = db.Column('register', db.String(48), comment='등록자')
    register_date = db.Column('register_date', db.DateTime, comment='등록일자')
    fk_business_id = db.Column('fk_business_id', db.Integer, db.ForeignKey(ProjectBusiness.id, onupdate="CASCADE", ondelete="CASCADE"), comment='영업 FK')
    project_business = db.relationship("ProjectBusiness", foreign_keys=[fk_business_id])

class ProjectCustomerHistory(db.Model): # 프로젝트 - 고객이력관리
    __tablename__ = 'project_customer_history'
    __table_args__ = {
        'comment': '프로젝트(고객이력관리)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    history_date = db.Column('history_date', db.DateTime, comment='이력일자')
    manager = db.Column('manager', db.String(48), comment='담당자')
    contact_method = db.Column('contact_method', db.String(48), comment='접촉방법')
    note = db.Column('note', db.String(256), comment='메모사항')
    register = db.Column('register', db.String(48), comment='등록자')
    register_date = db.Column('register_date', db.DateTime, comment='등록일자')
    fk_business_id = db.Column('fk_business_id', db.Integer, db.ForeignKey(ProjectBusiness.id, onupdate="CASCADE", ondelete="CASCADE"), comment='영업 FK')
    project_business = db.relationship("ProjectBusiness", foreign_keys=[fk_business_id])
    

#   ----------------------------------------------------------------------------------------------------------------------
# CREATE TRIGGER
    


# ----------------------------------------------------------------------------------------------------------------------
# CREATE STORED PROCEDURE


# ----------------------------------------------------------------------------------------------------------------------
# CREATE TRIGGER

# 실행계획 품목 추가 
# after_project_excution_plan_item_insert = DDL('''
# DROP TRIGGER IF EXISTS after_project_excution_plan_item_insert;
# CREATE TRIGGER after_project_excution_plan_item_insert
# AFTER INSERT ON project_excution_plan_item
# FOR EACH ROW
# BEGIN
#     # 프로젝트 품목 미실행계획 수량 업데이트 
#     IF NEW.fk_project_item_id IS NOT NULL THEN
#              update project_item
#              set not_ordered = 0
#              where project_item.id = NEW.fk_project_item_id;
#     END IF;
# END;''')
# event.listen(ProjectExcutionPlanItem.__table__, 'after_create', after_project_excution_plan_item_insert)

# 실행계획 품목 업데이트 
# after_project_excution_plan_item_delete = DDL('''
# DROP TRIGGER IF EXISTS after_project_excution_plan_item_delete;
# CREATE TRIGGER after_project_excution_plan_item_delete
# AFTER DELETE ON project_excution_plan_item
# FOR EACH ROW
# BEGIN
#     # 프로젝트 품목 미실행계획 수량 업데이트 
#     IF OLD.fk_project_item_id IS NOT NULL THEN
#              update project_item
#              set not_ordered = project_item.quantity
#              where project_item.id = OLD.fk_project_item_id;
#     END IF;
# END;''')
# event.listen(ProjectExcutionPlanItem.__table__, 'after_create', after_project_excution_plan_item_delete)

#실행계획 삭제
before_project_excution_plan_delete = DDL('''
DROP TRIGGER IF EXISTS before_project_excution_plan_delete;
CREATE TRIGGER before_project_excution_plan_delete
BEFORE DELETE ON project_excution_plan
FOR EACH ROW
BEGIN
    # 실행 품목 삭제
    DELETE FROM project_excution_plan_item WHERE fk_project_excution_plan_id = OLD.id;
    DELETE FROM approval_management WHERE request_path_id = OLD.id;
        
END;''')
event.listen(ProjectExcutionPlan.__table__, 'after_create', before_project_excution_plan_delete)