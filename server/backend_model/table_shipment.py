# -*- coding: utf-8 -*-
print("module [backend_model.table_shipment.py] loaded")
from datetime import datetime
from sqlalchemy import DDL, event
from backend_model.database import DBManager
from backend_model.table_base import BaseItem, BaseWarehouse, BaseClient
from backend_model.table_common import Companies
from backend_model.table_project import ProjectItem, ProjectBusiness, ProjectManagement


db = DBManager.db


class ShipmentQuote(db.Model):  # 출하관리 - 견적
    __tablename__ = 'shipment_quote'
    __table_args__ = {
        'comment': '출하관리(견적)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    quote_number = db.Column('quote_number', db.String(48), comment='견적번호')
    quote_date = db.Column('quote_date', db.DateTime, comment='견적일자')
    client_company = db.Column('client_company', db.String(48), comment='고객업체')
    client_manager = db.Column('client_manager', db.String(48), comment='업체담당자')
    quote_department = db.Column('quote_department', db.String(48), comment='견적부서')
    quote_manager = db.Column('quote_manager', db.String(48), comment='견적담당자')
    quote_type = db.Column('quote_type', db.String(48), comment='견적구분')
    vat_type = db.Column('vat_type', db.String(48), comment='부가세구분')
    payment_terms = db.Column('payment_terms', db.String(48), comment='결재조건')
    delivery_date = db.Column('delivery_date', db.String(48), comment='납품기한')
    delivery_place = db.Column('delivery_place', db.String(48), comment='납품장소')
    end_user = db.Column('end_user', db.String(48), comment='원청업체')
    validity_period = db.Column('validity_period', db.String(48), comment="유효기간")
    warranty_period = db.Column('warranty_period', db.String(48), comment="보증기간")
    delivery_terms = db.Column('delivery_terms', db.String(48), comment="인도조건")
    note = db.Column('note', db.String(256), comment='참고사항')
    etc = db.Column('etc', db.Text, comment='비고')
    supply_price = db.Column('supply_price', db.BigInteger, comment='공급가')
    vat = db.Column('vat', db.BigInteger, comment='부가세')
    total_price = db.Column('total_price', db.BigInteger, comment='합계금액')
    order_number = db.Column('order_number', db.String(48), comment='수주번호')
    business_name = db.Column('business_name', db.String(48), comment='영업명')
    confirmed = db.Column('confirmed', db.Boolean, server_default='0', comment='견적 확정 여부')
    fk_previous_quote_id = db.Column('fk_previous_quote_id', db.Integer, db.ForeignKey('shipment_quote.id'), comment='이전견적번호')
    fk_business_id = db.Column('fk_business_id', db.Integer, db.ForeignKey(ProjectBusiness.id, onupdate="CASCADE", ondelete="CASCADE"), comment='영업 FK')
    previous_quote = db.relationship('ShipmentQuote', remote_side=[id])
    business = db.relationship('ProjectBusiness', foreign_keys=[fk_business_id])
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')

class ShipmentQuoteItem(db.Model):  # 출하관리 - 견적 - 견적품목찾기
    __tablename__ = 'shipment_quote_item'
    __table_args__ = {
        'comment': '견적(견적품목)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE'), comment='품목코드')
    quote_quantity = db.Column('quote_quantity', db.Integer, comment='견적수량')
    unit_price = db.Column('unit_price', db.Integer, comment='견적단가')
    sales_unit_price = db.Column('sales_unit_price', db.Integer, comment='영업단가')
    purchase_unit_price = db.Column('purchase_unit_price', db.Integer, comment="구매단가")
    supply_price = db.Column('supply_price', db.BigInteger, comment='견적공급가')
    sales_supply_price = db.Column('sales_supply_price', db.BigInteger, comment='영업공급가')
    dc_rate = db.Column('dc_rate', db.Integer, comment='DC Rate')
    request_delivery_date = db.Column('request_delivery_date', db.DateTime, comment='요청납기')
    client_item_number = db.Column('client_item_number', db.String(48), comment='고객사품번')
    note = db.Column('note', db.String(256), comment='참고사항')
    item_order = db.Column('item_order', db.Integer, comment="순서")
    not_ordered = db.Column('not_ordered', db.Integer, comment='미수주수량')
    warehouse_code = db.Column('warehouse_code', db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment='출고창고')
    fk_parent_id = db.Column("fk_parent_id", db.Integer, db.ForeignKey('shipment_quote_item.id', onupdate='CASCADE', ondelete='CASCADE'), comment="부모 FK")
    fk_quote_id = db.Column('fk_quote_id', db.Integer, db.ForeignKey(ShipmentQuote.id, onupdate='CASCADE', ondelete='CASCADE'), comment='견적 FK')
    quote = db.relationship("ShipmentQuote", foreign_keys=[fk_quote_id])
    parent = db.relationship("ShipmentQuoteItem", remote_side=[id], backref="children")
    item = db.relationship('BaseItem', foreign_keys=[item_code])
    warehouse = db.relationship('BaseWarehouse', foreign_keys=[warehouse_code])
    basic_stock = db.relationship('SetupBasicStock', viewonly=True,
                                  primaryjoin='and_(foreign(ShipmentQuoteItem.item_code) == SetupBasicStock.item_code,'
                                              'foreign(ShipmentQuoteItem.warehouse_code) == SetupBasicStock.wh_code)')

    def serialize(self):
        serialized_data = {
            'id': self.id,
            'created': self.created.isoformat() if self.created else None,
            'item_code': self.item_code,
            'quote_quantity': self.quote_quantity,
            'unit_price': self.unit_price,
            'sales_unit_price': self.sales_unit_price,
            'purchase_unit_price': self.purchase_unit_price,
            'supply_price': self.supply_price,
            'sales_supply_price': self.sales_supply_price,
            'dc_rate': self.dc_rate,
            'request_delivery_date': self.request_delivery_date.isoformat() if self.request_delivery_date else None,
            'client_item_number': self.client_item_number,
            'note': self.note,
            'item_order': self.item_order,
            'not_ordered': self.not_ordered,
            'warehouse_code': self.warehouse_code,
            'fk_parent_id': self.fk_parent_id,
            'fk_quote_id': self.fk_quote_id
        }
        
        if self.children:
            serialized_data['children'] = [child.serialize() for child in self.children]
        
        return serialized_data

    def excel_import_columns(self):
        return dict(
            output=[(self.fk_quote_id, ShipmentQuote, 'quote_number', 'id'), self.item_code, self.quote_quantity, self.unit_price, self.supply_price, self.request_delivery_date,
                    self.client_item_number, self.note, self.warehouse_code],
            key=[self.id]
        )


class ShipmentQuoteItem2(db.Model):  # 출하관리 - 견적 - 견적품목입력
    __tablename__ = 'shipment_quote_item2'
    __table_args__ = {
        'comment': '견적(견적품목입력)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), comment='품목코드')
    item_name = db.Column('item_name', db.String(128), comment='품명(견적품목입력에서사용)')
    item_standard = db.Column('item_standard', db.String(48), comment='규격(견적품목입력에서사용)')
    item_detail = db.Column('item_detail', db.String(48), comment='품목설명(견적품목입력에서사용)')
    unit = db.Column('unit', db.String(10), comment='단위(견적품목입력에서사용)')
    quote_quantity = db.Column('quote_quantity', db.Integer, comment='견적수량')
    unit_price = db.Column('unit_price', db.Integer, comment='단가')
    supply_price = db.Column('supply_price', db.BigInteger, comment='공급가')
    request_delivery_date = db.Column('request_delivery_date', db.DateTime, comment='요청납기')
    client_item_number = db.Column('client_item_number', db.String(48), comment='고객사품번')
    note = db.Column('note', db.String(256), comment='참고사항')
    project_number = db.Column('project_number', db.String(48), comment='프로젝트번호')
    warehouse_code = db.Column('warehouse_code', db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment='출고창고')
    fk_quote_id = db.Column('fk_quote_id', db.Integer, db.ForeignKey(ShipmentQuote.id, onupdate='CASCADE', ondelete='CASCADE'), comment='견적 FK')
    quote = db.relationship("ShipmentQuote", foreign_keys=[fk_quote_id])
    warehouse = db.relationship('BaseWarehouse', foreign_keys=[warehouse_code])


class ShipmentQuoteManual(db.Model):  # 출하관리 - 견적
    __tablename__ = 'shipment_quote_manual'
    __table_args__ = {
        'comment': '출하관리(견적 수기)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    quote_number = db.Column('quote_number', db.String(48), comment='견적번호')
    quote_date = db.Column('quote_date', db.DateTime, comment='견적일자')
    client_company = db.Column('client_company', db.String(48), comment='고객업체')
    client_manager = db.Column('client_manager', db.String(48), comment='업체담당자')
    quote_department = db.Column('quote_department', db.String(48), comment='견적부서')
    quote_manager = db.Column('quote_manager', db.String(48), comment='견적담당자')
    quote_type = db.Column('quote_type', db.String(48), comment='견적구분')
    vat_type = db.Column('vat_type', db.String(48), comment='부가세구분')
    payment_terms = db.Column('payment_terms', db.String(48), comment='결재조건')
    delivery_date = db.Column('delivery_date', db.DateTime, comment='납품기한')
    delivery_place = db.Column('delivery_place', db.String(48), comment='납품장소')
    previous_quote_number = db.Column('previous_quote_number', db.String(48), comment='이전견적번호')
    project_number = db.Column('project_number', db.String(48), comment='프로젝트번호')
    end_user = db.Column('end_user', db.String(48), comment='End User')
    note = db.Column('note', db.String(256), comment='참고사항')
    etc = db.Column('etc', db.Text, comment='비고')
    supply_price = db.Column('supply_price', db.BigInteger, comment='공급가')
    vat = db.Column('vat', db.BigInteger, comment='부가세')
    total_price = db.Column('total_price', db.BigInteger, comment='합계금액')
    order_number = db.Column('order_number', db.String(48), comment='수주번호')
    confirmed = db.Column('confirmed', db.Boolean, server_default='0', comment='견적 확정 여부')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')


class ShipmentQuoteManualItem(db.Model):  # 출하관리 - 견적(수기) - 견적품목입력
    __tablename__ = 'shipment_quote_manual_item'
    __table_args__ = {
        'comment': '견적(견적(수기)품목입력)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), comment='품목코드')
    item_name = db.Column('item_name', db.String(128), comment='품명(견적품목입력에서사용)')
    item_standard = db.Column('item_standard', db.String(48), comment='규격(견적품목입력에서사용)')
    item_detail = db.Column('item_detail', db.String(48), comment='품목설명(견적품목입력에서사용)')
    unit = db.Column('unit', db.String(10), comment='단위(견적품목입력에서사용)')
    quote_quantity = db.Column('quote_quantity', db.Integer, comment='견적수량')
    unit_price = db.Column('unit_price', db.Integer, comment='견적단가')
    sales_unit_price = db.Column('sales_unit_price', db.Integer, comment='영업단가')
    supply_price = db.Column('supply_price', db.BigInteger, comment='견적공급가')
    sales_supply_price = db.Column('sales_supply_price', db.BigInteger, comment='영업공급가')
    dc_rate = db.Column('dc_rate', db.Integer, comment='DC Rate')
    request_delivery_date = db.Column('request_delivery_date', db.DateTime, comment='요청납기')
    client_item_number = db.Column('client_item_number', db.String(48), comment='고객사품번')
    note = db.Column('note', db.String(256), comment='참고사항')
    project_number = db.Column('project_number', db.String(48), comment='프로젝트번호')
    not_ordered = db.Column('not_ordered', db.Integer, comment='미수주수량')
    warehouse_code = db.Column('warehouse_code', db.String(48), comment='출고창고')
    fk_quote_id = db.Column('fk_quote_id', db.Integer, db.ForeignKey(ShipmentQuoteManual.id, onupdate='CASCADE', ondelete='CASCADE'), comment='견적 FK')
    quote = db.relationship("ShipmentQuoteManual", foreign_keys=[fk_quote_id])


class ShipmentOrder(db.Model):  # 출하관리 - 수주
    __tablename__ = 'shipment_order'
    __table_args__ = {
        'comment': '출하관리(수주)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    order_number = db.Column('order_number', db.String(48), comment='수주번호')
    order_date = db.Column('order_date', db.DateTime, comment='수주일자')
    client_company = db.Column('client_company', db.String(48), comment='고객업체')
    client_manager = db.Column('client_manager', db.String(48), comment='업체담당자')
    client_manager_phone = db.Column('client_manager_phone', db.String(48), comment='담당연락처')
    order_department = db.Column('order_department', db.String(48), comment='수주부서')
    order_manager = db.Column('order_manager', db.String(48), comment='수주담당자')
    order_type = db.Column('order_type', db.String(48), comment='수주구분')
    vat_type = db.Column('vat_type', db.String(48), comment='부가세구분')
    payment_terms = db.Column('payment_terms', db.String(48), comment='결재조건')
    delivery_date = db.Column('delivery_date', db.DateTime, comment='납품기한')
    delivery_place = db.Column('delivery_place', db.String(256), comment='납품장소')
    client_order_number = db.Column('client_order_number', db.String(48), comment='고객발주번호')
    end_user = db.Column('end_user', db.String(48), comment='End User')
    transport = db.Column('transport', db.String(256), comment='운송구분')
    note = db.Column('note', db.String(256), comment='참고사항')
    etc = db.Column('etc', db.Text, comment='비고')
    supply_price = db.Column('supply_price', db.BigInteger, comment='공급가')
    vat = db.Column('vat', db.BigInteger, comment='부가세')
    total_price = db.Column('total_price', db.BigInteger, comment='합계금액')
    release_number = db.Column('release_number', db.String(48), comment='출고번호')
    confirmed = db.Column('confirmed', db.Boolean, server_default='0', comment='수주 확정 여부')
    approve = db.Column('approve', db.Boolean, server_default='0', comment='수주 승인 여부')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id), comment="프로젝트 FK")
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')
    project_management = db.relationship("ProjectManagement", foreign_keys=[fk_project_management_id])


class ShipmentOrderItem(db.Model):  # 출하관리 - 수주 - 수주품목
    __tablename__ = 'shipment_order_item'
    __table_args__ = {'comment': '수주(수주품목)'}
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE'), comment='품목코드')
    order_quantity = db.Column('order_quantity', db.Integer, comment='수주수량')
    assign_quantity = db.Column('assign_quantity', db.Integer, comment='할당수량')
    produce_plan_quantity = db.Column('produce_plan_quantity', db.Integer, server_default='0', comment='생산계획수량')
    not_produce_plan_quantity = db.Column('not_produce_plan_quantity', db.Integer, server_default='0', comment='생산계획 미처리 수량')
    unit_price = db.Column('unit_price', db.Integer, comment='단가')
    supply_price = db.Column('supply_price', db.BigInteger, comment='공급가')
    request_delivery_date = db.Column('request_delivery_date', db.DateTime, comment='요청납기')
    warehouse_code = db.Column('warehouse_code', db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment='출고창고')
    not_shipped = db.Column('not_shipped', db.Integer, comment='미출고')
    quote_number = db.Column('quote_number', db.String(48), comment='견적번호')
    client_item_number = db.Column('client_item_number', db.String(48), comment='고객사품번')
    note = db.Column('note', db.String(256), comment='참고사항')
    closing_yn = db.Column('closing_yn', db.Boolean, server_default='0', comment='종결여부')
    fk_order_id = db.Column('fk_order_id', db.Integer, db.ForeignKey(ShipmentOrder.id, onupdate='CASCADE'), comment='수주 FK')
    fk_quote_item_id = db.Column('fk_quote_item_id', db.Integer, db.ForeignKey(ShipmentQuoteItem.id), comment='견적품목 FK')
    fk_project_item_id = db.Column('fk_project_item_id', db.Integer, db.ForeignKey(ProjectItem.id), comment='프로젝트품목 FK')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id))
    order = db.relationship("ShipmentOrder", foreign_keys=[fk_order_id], lazy='joined')
    item = db.relationship('BaseItem', foreign_keys=[item_code])
    warehouse = db.relationship('BaseWarehouse', foreign_keys=[warehouse_code])
    project_management = db.relationship("ProjectManagement", foreign_keys=[fk_project_management_id])
    quote_item = db.relationship('ShipmentQuoteItem', foreign_keys=[fk_quote_item_id])
    basic_stock = db.relationship('SetupBasicStock', viewonly=True,
                                  primaryjoin='and_(foreign(ShipmentOrderItem.item_code) == SetupBasicStock.item_code,'
                                              'foreign(ShipmentOrderItem.warehouse_code) == SetupBasicStock.wh_code)')
    client = db.relationship(
        'BaseClient',
        secondary="join(ShipmentOrder, BaseClient, ShipmentOrder.client_company == BaseClient.name)",
        primaryjoin="ShipmentOrderItem.fk_order_id == ShipmentOrder.id",
        secondaryjoin="foreign(ShipmentOrder.client_company) == BaseClient.name",
        uselist=False,
        viewonly=True,
    )


class ShipmentRelease(db.Model):  # 출하관리 - 출고
    __tablename__ = 'shipment_release'
    __table_args__ = {
        'comment': '출하관리(출고)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    release_number = db.Column('release_number', db.String(48), comment='출고번호')
    release_date = db.Column('release_date', db.DateTime, comment='출고일자')
    client_company = db.Column('client_company', db.String(48), comment='고객업체')
    client_manager = db.Column('client_manager', db.String(48), comment='업체담당자')
    client_manager_phone = db.Column('client_manager_phone', db.String(48), comment='담당연락처')
    release_department = db.Column('release_department', db.String(48), comment='출고부서')
    release_manager = db.Column('release_manager', db.String(48), comment='출고담당자')
    release_type = db.Column('release_type', db.String(48), comment='출고구분')
    vat_type = db.Column('vat_type', db.String(48), comment='부가세구분')
    payment_terms = db.Column('payment_terms', db.String(48), comment='결재조건')
    delivery_date = db.Column('delivery_date', db.DateTime, comment='납품기한')
    delivery_place = db.Column('delivery_place', db.String(256), comment='납품장소')
    client_order_number = db.Column('client_order_number', db.String(48), comment='고객발주번호')
    end_user = db.Column('end_user', db.String(48), comment='End User')
    transport = db.Column('transport', db.String(256), comment='운송구분')
    note = db.Column('note', db.String(256), comment='참고사항')
    etc = db.Column('etc', db.Text, comment='비고')
    supply_price = db.Column('supply_price', db.BigInteger, comment='공급가')
    vat = db.Column('vat', db.BigInteger, comment='부가세')
    total_price = db.Column('total_price', db.BigInteger, comment='합계금액')
    confirmed = db.Column('confirmed', db.Boolean, server_default='0', comment='출고 확정 여부')
    sales_number = db.Column('sales_number', db.String(48), comment='계산서번호')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate='CASCADE'), comment="프로젝트 FK")
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')
    project_management = db.relationship('ProjectManagement', foreign_keys=[fk_project_management_id])


class ShipmentReleaseItem(db.Model):  # 출하관리 - 출고 - 출고품목
    __tablename__ = 'shipment_release_item'
    __table_args__ = {
        'comment': '출고(출고품목)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE'), comment='품목코드')
    order_quantity = db.Column('order_quantity', db.Integer, server_default='0', comment='수주수량')
    release_quantity = db.Column('release_quantity', db.Integer, server_default='0', comment='출고수량')
    unit_price = db.Column('unit_price', db.Integer, server_default='0', comment='단가')
    cost_price = db.Column('cost_price', db.Numeric(10, 2), server_default='0', comment='원가')
    total_cost_price = db.Column('total_cost_price', db.Numeric(20, 4), server_default='0', comment='원가합계')
    request_delivery_date = db.Column('request_delivery_date', db.DateTime, comment='요청납기')
    non_invoice = db.Column('non_invoice', db.Integer, server_default='0', comment='미계산서')
    warehouse_code = db.Column('warehouse_code', db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment='출고창고')
    order_number = db.Column('order_number', db.String(48), comment='수주번호')
    lot_number = db.Column('lot_number', db.String(48), comment='출고 LOT번호')
    client_item_number = db.Column('client_item_number', db.String(48), comment='고객사품번')
    note = db.Column('note', db.String(256), comment='참고사항')
    closing_yn = db.Column('closing_yn', db.Boolean, server_default='0', comment='종결여부')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate='CASCADE'), comment="프로젝트 FK")
    fk_release_id = db.Column('fk_release_id', db.Integer, db.ForeignKey(ShipmentRelease.id, onupdate='CASCADE'), comment='출고 FK')
    fk_order_item_id = db.Column('fk_order_item_id', db.Integer, db.ForeignKey(ShipmentOrderItem.id), comment='수주품목 FK')
    project_management = db.relationship('ProjectManagement', foreign_keys=[fk_project_management_id])
    release = db.relationship("ShipmentRelease", foreign_keys=[fk_release_id])
    order_item = db.relationship("ShipmentOrderItem", foreign_keys=[fk_order_item_id])
    item = db.relationship('BaseItem', foreign_keys=[item_code])
    warehouse = db.relationship('BaseWarehouse', foreign_keys=[warehouse_code])
    basic_stock = db.relationship('SetupBasicStock', viewonly=True,
                                  primaryjoin='and_(foreign(ShipmentReleaseItem.item_code) == SetupBasicStock.item_code,'
                                              'foreign(ShipmentReleaseItem.warehouse_code) == SetupBasicStock.wh_code)')
    client = db.relationship(
        'BaseClient',
        secondary="join(ShipmentRelease, BaseClient, ShipmentRelease.client_company == BaseClient.name)",
        primaryjoin="ShipmentReleaseItem.fk_release_id == ShipmentRelease.id",
        secondaryjoin="foreign(ShipmentRelease.client_company) == BaseClient.name",
        uselist=False,
        viewonly=True,
    )


class ShipmentReleaseReturn(db.Model):  # 출하관리 - 출고반품
    __tablename__ = 'shipment_release_return'
    __table_args__ = {
        'comment': '출하관리(출고반품)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    return_number = db.Column('return_number', db.String(48), comment='반품번호')
    return_date = db.Column('return_date', db.DateTime, comment='반품일자')
    client_company = db.Column('client_company', db.String(48), comment='고객업체')
    client_manager = db.Column('client_manager', db.String(48), comment='업체담당자')
    return_department = db.Column('return_department', db.String(48), comment='반품부서')
    return_manager = db.Column('return_manager', db.String(48), comment='반품담당자')
    return_type = db.Column('return_type', db.String(48), comment='반품구분')
    vat_type = db.Column('vat_type', db.String(48), comment='부가세구분')
    etc = db.Column('etc', db.Text, comment='비고')
    supply_price = db.Column('supply_price', db.BigInteger, server_default='0', comment='공급가')
    vat = db.Column('vat', db.BigInteger, server_default='0', comment='부가세')
    total_price = db.Column('total_price', db.BigInteger, server_default='0', comment='합계금액')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')


class ShipmentReleaseReturnItem(db.Model):  # 출하관리 - 출고반품 - 품목
    __tablename__ = 'shipment_release_return_item'
    __table_args__ = {
        'comment': '출고반품(출고반품품목)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE'), comment='품목코드')
    release_quantity = db.Column('release_quantity', db.Integer, server_default='0', comment='출고수량')
    return_quantity = db.Column('return_quantity', db.Integer, server_default='0', comment='반품수량')
    non_invoice = db.Column('non_invoice', db.Integer, server_default='0', comment='미계산서')
    unit_price = db.Column('unit_price', db.Numeric(10, 2), server_default='0.00', comment='단가')
    cost_price = db.Column('cost_price', db.Numeric(10, 2), comment='원가')
    supply_price = db.Column('supply_price', db.BigInteger, server_default='0', comment='공급가')
    request_delivery_date = db.Column('request_delivery_date', db.DateTime, comment='요청납기')
    warehouse_code = db.Column('warehouse_code', db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment='입고창고')
    return_reason = db.Column('return_reason', db.String(256), comment='반품사유')
    fk_release_id = db.Column('fk_release_id', db.Integer, db.ForeignKey(ShipmentRelease.id, onupdate='CASCADE'), comment='출고 FK')
    fk_release_item_id = db.Column('fk_release_item_id', db.Integer, db.ForeignKey(ShipmentReleaseItem.id), comment='출고품목 FK')
    fk_release_return_id = db.Column('fk_release_return_id', db.Integer, db.ForeignKey(ShipmentReleaseReturn.id, onupdate='CASCADE'), comment='출고반품 FK')
    release = db.relationship("ShipmentRelease", foreign_keys=[fk_release_id])
    release_item = db.relationship("ShipmentReleaseItem", foreign_keys=[fk_release_item_id])
    release_return = db.relationship("ShipmentReleaseReturn", foreign_keys=[fk_release_return_id])
    item = db.relationship('BaseItem', foreign_keys=[item_code])
    warehouse = db.relationship('BaseWarehouse', foreign_keys=[warehouse_code])
    basic_stock = db.relationship('SetupBasicStock', viewonly=True,
                                  primaryjoin='and_(foreign(ShipmentReleaseReturnItem.item_code) == SetupBasicStock.item_code,'
                                              'foreign(ShipmentReleaseReturnItem.warehouse_code) == SetupBasicStock.wh_code)')


class ShipmentSalesStatement(db.Model):  # 출하관리 - 매출계산서
    __tablename__ = 'shipment_sales_statement'
    __table_args__ = {
        'comment': '출하관리(매출계산서)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    sales_number = db.Column('sales_number', db.String(48), comment='계산서번호')
    sales_date = db.Column('sales_date', db.DateTime, comment='발행일자')
    client_company = db.Column('client_company', db.String(48), comment='고객업체')
    client_manager = db.Column('client_manager', db.String(48), comment='업체담당자')
    sales_department = db.Column('sales_department', db.String(48), comment='매출부서')
    sales_manager = db.Column('sales_manager', db.String(48), comment='매출담당자')
    tax_rate = db.Column('tax_rate', db.String(48), comment='세율')
    sales_type = db.Column('sales_type', db.String(48), comment='계산서유형')
    approval_type = db.Column('approval_type', db.String(48), comment='결재유형')
    publish_type = db.Column('publish_type', db.String(48), comment='발행구분')
    office_type = db.Column('office_type', db.String(48), comment='본지점구분')
    etc = db.Column('etc', db.Text, comment='비고')
    vat_type = db.Column('vat_type', db.String(48), comment='부가세구분')
    vat = db.Column('vat', db.BigInteger, comment='부가세')
    vat_adjustment = db.Column('vat_adjustment', db.BigInteger, server_default='0', comment='부가세보정')
    supply_price = db.Column('supply_price', db.BigInteger, comment='공급가')
    total_price = db.Column('total_price', db.BigInteger, comment='합계금액')
    not_deposit = db.Column('not_deposit', db.BigInteger, comment='미입금')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')


class ShipmentSalesStatementItem(db.Model):  # 출하관리 - 매출계산서품목
    __tablename__ = 'shipment_sales_statement_item'
    __table_args__ = {
        'comment': '매출계산서(매출계산서품목)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE'), comment='품목코드')
    statement_item = db.Column('statement_item', db.String(48), comment='계산서품목')
    quantity = db.Column('quantity', db.Integer, comment='수량')
    unit_price = db.Column('unit_price', db.Integer, comment='단가')
    not_deposit = db.Column('not_deposit', db.BigInteger, comment='미입금')
    vat = db.Column('vat', db.BigInteger, comment='부가세')
    supply_price = db.Column('supply_price', db.BigInteger, comment='공급가')
    total_price = db.Column('total_price', db.BigInteger, comment='합계금액')
    note = db.Column('note', db.Text, comment='추가설명')
    release_number = db.Column('release_number', db.String(48), comment='출고번호')
    release_return_number = db.Column('release_return_number', db.String(48), comment='출고반품번호')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate='CASCADE'), comment="프로젝트 FK")
    fk_sales_id = db.Column('fk_sales_id', db.Integer, db.ForeignKey(ShipmentSalesStatement.id, onupdate='CASCADE'), comment='계산서 FK')
    fk_release_item_id = db.Column('fk_release_item_id', db.Integer, db.ForeignKey(ShipmentReleaseItem.id, onupdate='CASCADE'), comment='출고품목 FK')
    fk_release_return_item_id = db.Column('fk_release_return_item_id', db.Integer, db.ForeignKey(ShipmentReleaseReturnItem.id, onupdate='CASCADE'), comment='출고반품품목 FK')
    project_management = db.relationship('ProjectManagement', foreign_keys=[fk_project_management_id])
    item = db.relationship('BaseItem', foreign_keys=[item_code])
    sales = db.relationship("ShipmentSalesStatement", foreign_keys=[fk_sales_id])
    client = db.relationship(
        'BaseClient',
        secondary="join(ShipmentSalesStatement, BaseClient, ShipmentSalesStatement.client_company == BaseClient.name)",
        primaryjoin="ShipmentSalesStatementItem.fk_sales_id == ShipmentSalesStatement.id",
        secondaryjoin="foreign(ShipmentSalesStatement.client_company) == BaseClient.name",
        uselist=False,
        viewonly=True,
    )


class ShipmentDeposit(db.Model):  # 출하관리 - 입금
    __tablename__ = 'shipment_deposit'
    __table_args__ = {
        'comment': '출하관리(입금)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    deposit_number = db.Column('deposit_number', db.String(48), comment='입금번호')
    deposit_date = db.Column('deposit_date', db.DateTime, comment='입금일자')
    client_company = db.Column('client_company', db.String(48), comment='고객업체')
    client_manager = db.Column('client_manager', db.String(48), comment='업체담당자')
    deposit_department = db.Column('deposit_department', db.String(48), comment='영업부서')
    deposit_manager = db.Column('deposit_manager', db.String(48), comment='영업담당자')
    total_price = db.Column('total_price', db.Numeric(20, 4), server_default='0', comment="입금합계금액")
    etc = db.Column('etc', db.Text, comment='비고')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')


class ShipmentDepositItem(db.Model):  # 출하관리 - 입금내역
    __tablename__ = 'shipment_deposit_item'
    __table_args__ = {
        'comment': '출하관리(입금내역)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    price = db.Column('price', db.BigInteger, comment='금액')
    deposit_type = db.Column('deposit_type', db.String(48), comment='입금형태')
    etc = db.Column('etc', db.Text, comment='입금적요')
    fk_deposit_id = db.Column('fk_deposit_id', db.Integer, db.ForeignKey(ShipmentDeposit.id, onupdate='CASCADE'), comment='입금 FK')
    fk_sales_id = db.Column('fk_sales_id', db.Integer, db.ForeignKey(ShipmentSalesStatement.id, onupdate='CASCADE'), comment='매출계산서 FK')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate='CASCADE'), comment="프로젝트 FK")
    project_management = db.relationship('ProjectManagement', foreign_keys=[fk_project_management_id])
    deposit = db.relationship("ShipmentDeposit", foreign_keys=[fk_deposit_id])
    sales = db.relationship("ShipmentSalesStatement", foreign_keys=[fk_sales_id])
    client = db.relationship(
        'BaseClient',
        secondary="join(ShipmentDeposit, BaseClient, ShipmentDeposit.client_company == BaseClient.name)",
        primaryjoin="ShipmentDepositItem.fk_deposit_id == ShipmentDeposit.id",
        secondaryjoin="foreign(ShipmentDeposit.client_company) == BaseClient.name",
        uselist=False,
        viewonly=True,
    )


class ShipmentLend(db.Model):  # 출하관리 - 가출고
    __tablename__ = 'shipment_lend'
    __table_args__ = {
        'comment': '가출고'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    lend_number = db.Column('lend_number', db.String(48), comment='가출고번호')
    lend_date = db.Column('lend_date', db.DateTime, comment='가출고일자')
    lend_manager = db.Column('lend_manager', db.String(48), comment='가출고담당자')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE'), comment='품목코드')
    quantity = db.Column('quantity', db.Integer, comment='가출고수량')
    not_retrieved_quantity = db.Column('not_retrieved_quantity', db.Integer, comment='미회수수량')
    client_company = db.Column('client_company', db.String(48), comment='업체')
    note = db.Column('note', db.String(256), comment='참고사항')
    etc = db.Column('etc', db.String(256), comment='비고')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')
    item = db.relationship('BaseItem', foreign_keys=[item_code])


class ShipmentRetrieve(db.Model):  # 출하관리 - 가출고회수
    __tablename__ = 'shipment_retrieve'
    __table_args__ = {
        'comment': '가출고회수'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    retrieve_number = db.Column('retrieve_number', db.String(48), comment='회수번호')
    retrieve_date = db.Column('retrieve_date', db.DateTime, comment='회수일자')
    retrieve_manager = db.Column('retrieve_manager', db.String(48), comment='회수담당자')
    quantity = db.Column('quantity', db.Integer, comment='회수수량')
    etc = db.Column('etc', db.String(256), comment='비고')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE'), comment='품목코드')
    fk_lend_id = db.Column('fk_lend_id', db.Integer, db.ForeignKey(ShipmentLend.id), comment='가출고 FK')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')
    item = db.relationship('BaseItem', foreign_keys=[item_code])
    lend = db.relationship('ShipmentLend', foreign_keys=[fk_lend_id])


# ----------------------------------------------------------------------------------------------------------------------
# CREATE STORED PROCEDURE

# 수주 품목 생산계획미처리 수량 업데이트
proc_update_shipment_order_item_not_production_plan_quantity = DDL('''
DROP PROCEDURE IF EXISTS proc_update_shipment_order_item_not_production_plan_quantity;
CREATE PROCEDURE `proc_update_shipment_order_item_not_production_plan_quantity`(
    IN `orderItemId` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '매출계산서 미입금 업데이트'
BEGIN
    CALL proc_get_production_plan_item_total_plan_quantity(orderItemId, @quantity);

    UPDATE shipment_order_item
    SET not_produce_plan_quantity = produce_plan_quantity - @quantity
    WHERE id = orderItemId;
END
''')
event.listen(ShipmentOrderItem.__table__, 'after_create', proc_update_shipment_order_item_not_production_plan_quantity)

# 입금품목의 입금액 합계 가져오기
proc_get_shipment_deposit_item_total_price = DDL('''
DROP PROCEDURE IF EXISTS proc_get_shipment_deposit_item_total_price;
CREATE PROCEDURE `proc_get_shipment_deposit_item_total_price`(
    IN `salesId` INT,
    OUT `sumPrice` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '입금품목의 입금액 합계 가져오기'
BEGIN
    SET sumPrice = (SELECT SUM(price)
                    FROM shipment_deposit_item
                    WHERE fk_sales_id = salesId
                    GROUP BY fk_sales_id);
    IF sumPrice IS NULL THEN
        SET sumPrice = 0;
    END IF;
END
''')
event.listen(ShipmentDepositItem.__table__, 'after_create', proc_get_shipment_deposit_item_total_price)

# 매출계산서 미입금 업데이트
proc_update_shipment_sales_statement_not_deposit = DDL('''
DROP PROCEDURE IF EXISTS proc_update_shipment_sales_statement_not_deposit;
CREATE PROCEDURE `proc_update_shipment_sales_statement_not_deposit`(
    IN `salesId` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '매출계산서 미입금 업데이트'
BEGIN
    CALL proc_get_shipment_deposit_item_total_price(salesId, @sumPrice);
    
    UPDATE shipment_sales_statement
    SET not_deposit = total_price - @sumPrice
    WHERE id = salesId;
END
''')
event.listen(ShipmentSalesStatement.__table__, 'after_create', proc_update_shipment_sales_statement_not_deposit)


# ----------------------------------------------------------------------------------------------------------------------
# CREATE TRIGGER

# 수주 삭제
before_shipment_order_delete = DDL('''
DROP TRIGGER IF EXISTS before_shipment_order_delete;
CREATE TRIGGER before_shipment_order_delete
BEFORE DELETE ON shipment_order
FOR EACH ROW
BEGIN
    # 수주품목 삭제
    DELETE FROM shipment_order_item WHERE fk_order_id = OLD.id;
    
    # 견적에서 가져온 경우 견적의 수주번호를 NULL로 설정
    UPDATE shipment_quote 
    SET order_number = NULL
    WHERE order_number = OLD.order_number;
END;''')
event.listen(ShipmentOrder.__table__, 'after_create', before_shipment_order_delete)

# 수주품목 삭제
after_shipment_order_item_delete = DDL('''
DROP TRIGGER IF EXISTS after_shipment_order_item_delete;
CREATE TRIGGER after_shipment_order_item_delete
AFTER DELETE ON shipment_order_item
FOR EACH ROW
BEGIN
    # 가용재고 업데이트
    UPDATE setup_basic_stock
    SET available_stock = available_stock + OLD.assign_quantity
    WHERE item_code = OLD.item_code AND wh_code = OLD.warehouse_code;
    
    # 프로젝트품목에서 가져온 경우 프로젝트품목의 미수주수량 복구
    IF OLD.fk_project_item_id IS NOT NULL THEN
        UPDATE project_item
        SET not_ordered = not_ordered + OLD.order_quantity,
            fk_shipment_order_id = NULL
        WHERE id = OLD.fk_project_item_id;
    END IF;
    
    # 견적품목에서 가져온 경우 견적품목의 미수주수량 복구
    IF OLD.fk_quote_item_id IS NOT NULL THEN
        UPDATE shipment_quote_item
        SET not_ordered = not_ordered + OLD.order_quantity
        WHERE id = OLD.fk_quote_item_id;
    END IF;
END;''')
event.listen(ShipmentOrderItem.__table__, 'after_create', after_shipment_order_item_delete)

# 출고 삭제
before_shipment_release_delete = DDL('''
DROP TRIGGER IF EXISTS before_shipment_release_delete;
CREATE TRIGGER before_shipment_release_delete
BEFORE DELETE ON shipment_release
FOR EACH ROW
BEGIN
    # 출고품목 삭제
    DELETE FROM shipment_release_item WHERE fk_release_id = OLD.id;
    
    # 수주에서 가져온 경우 수주의 출고번호를 NULL로 설정
    UPDATE shipment_order
    SET release_number = NULL
    WHERE release_number = OLD.release_number;
END;''')
event.listen(ShipmentRelease.__table__, 'after_create', before_shipment_release_delete)

# 출고품목 업데이트
after_shipment_release_item_update = DDL('''
DROP TRIGGER IF EXISTS after_shipment_release_item_update;
CREATE TRIGGER after_shipment_release_item_update
AFTER UPDATE ON shipment_release_item
FOR EACH ROW
BEGIN
    # 출고반품품목의 반품원가 업데이트
	IF NEW.cost_price is NULL THEN
		UPDATE shipment_release_return_item
		SET cost_price = NULL
		WHERE fk_release_item_id = NEW.id;
	ELSEIF OLD.cost_price IS NULL THEN
		UPDATE shipment_release_return_item
        SET cost_price = NEW.cost_price
        WHERE fk_release_item_id = NEW.id;
	ELSE
    	IF NEW.cost_price != OLD.cost_price THEN
	        UPDATE shipment_release_return_item
	        SET cost_price = NEW.cost_price
	        WHERE fk_release_item_id = NEW.id;
	    END IF;
    END IF;
END;''')
event.listen(ShipmentReleaseItem.__table__, 'after_create', after_shipment_release_item_update)

# 출고품목 삭제
after_shipment_release_item_delete = DDL('''
DROP TRIGGER IF EXISTS after_shipment_release_item_delete;
CREATE TRIGGER after_shipment_release_item_delete
AFTER DELETE ON shipment_release_item
FOR EACH ROW
BEGIN
    # 수주품목에서 가져온 경우 수주품목의 미출고 수량 복구
    IF OLD.fk_order_item_id IS NOT NULL
    THEN
        UPDATE shipment_order_item
        SET not_shipped = not_shipped + OLD.release_quantity,
            assign_quantity = assign_quantity + OLD.release_quantity
        WHERE id = OLD.fk_order_item_id;
    END IF;

    # 현재고, 가용재고 업데이트
    UPDATE setup_basic_stock
    SET current_stock = current_stock + OLD.release_quantity
    WHERE item_code = OLD.item_code AND wh_code = OLD.warehouse_code;
    
    UPDATE setup_basic_stock
    SET available_stock = current_stock
    WHERE item_code = OLD.item_code AND wh_code = OLD.warehouse_code AND available_stock > current_stock;
    
    UPDATE setup_basic_stock
    SET available_stock = 0
    WHERE item_code = OLD.item_code AND wh_code = OLD.warehouse_code AND available_stock < 0;
END;''')
event.listen(ShipmentReleaseItem.__table__, 'after_create', after_shipment_release_item_delete)

# 매출계산서 삭제
before_shipment_sales_delete = DDL('''
DROP TRIGGER IF EXISTS before_shipment_sales_delete;
CREATE TRIGGER before_shipment_sales_delete
BEFORE DELETE ON shipment_sales_statement
FOR EACH ROW
BEGIN
    # 매출계산서품목 삭제
    DELETE FROM shipment_sales_statement_item WHERE fk_sales_id = OLD.id;

    # 출고에서 가져온 경우 출고의 매출계산서번호를 NULL로 설정
    UPDATE shipment_release
    SET sales_number = NULL
    WHERE sales_number = OLD.sales_number;
END;''')
event.listen(ShipmentSalesStatement.__table__, 'after_create', before_shipment_sales_delete)

# 매출계산서품목 삭제
after_shipment_sales_item_delete = DDL('''
DROP TRIGGER IF EXISTS after_shipment_sales_item_delete;
CREATE TRIGGER after_shipment_sales_item_delete
AFTER DELETE ON shipment_sales_statement_item
FOR EACH ROW
BEGIN
    # 출고품목에서 가져온 경우 출고품목의 미계산서 수량 복구
    IF OLD.fk_release_item_id IS NOT NULL
    THEN
        UPDATE shipment_release_item
        SET non_invoice = non_invoice + OLD.quantity
        WHERE id = OLD.fk_release_item_id;
    END IF;
    
    # 출고반품품목에서 가져온 경우 출고반품품목의 미계산서 수량 복구
    IF OLD.fk_release_return_item_id IS NOT NULL
    THEN
        UPDATE shipment_release_return_item
        SET non_invoice = non_invoice + OLD.quantity
        WHERE id = OLD.fk_release_return_item_id;
    END IF;
    IF OLD.fk_project_management_id IS NOT NULL
    THEN
        UPDATE project_management
        SET non_invoice = non_invoice + OLD.supply_price
        WHERE id = OLD.fk_project_management_id;
    END IF;
END;''')
event.listen(ShipmentSalesStatementItem.__table__, 'after_create', after_shipment_sales_item_delete)

# 입금 삭제
before_shipment_deposit_delete = DDL('''
DROP TRIGGER IF EXISTS before_shipment_deposit_delete;
CREATE TRIGGER before_shipment_deposit_delete
BEFORE DELETE ON shipment_deposit
FOR EACH ROW
BEGIN
    # 입금품목 삭제
    DELETE FROM shipment_deposit_item WHERE fk_deposit_id = OLD.id;
END;''')
event.listen(ShipmentDeposit.__table__, 'after_create', before_shipment_deposit_delete)

# 입금품목 삭제
after_shipment_deposit_item_delete = DDL('''
DROP TRIGGER IF EXISTS after_shipment_deposit_item_delete;
CREATE TRIGGER after_shipment_deposit_item_delete
AFTER DELETE ON shipment_deposit_item
FOR EACH ROW
BEGIN
    # 매출계산서 미입금 업데이트
    CALL proc_update_shipment_sales_statement_not_deposit(OLD.fk_sales_id);
END;''')
event.listen(ShipmentDepositItem.__table__, 'after_create', after_shipment_deposit_item_delete)

# 가출고회수 삭제 시 가출고 미회수수량 업데이트
after_shipment_retrieve_delete = DDL('''
DROP TRIGGER IF EXISTS after_shipment_retrieve_delete;
CREATE TRIGGER after_shipment_retrieve_delete
AFTER DELETE ON shipment_retrieve
FOR EACH ROW
BEGIN
    DECLARE total_quantity INT;
    DECLARE retrieved_quantity INT;
    DECLARE not_retrieved_quantity INT;
    
    SELECT SUM(quantity) INTO retrieved_quantity
    FROM shipment_retrieve
    WHERE fk_lend_id = OLD.fk_lend_id
    GROUP BY fk_lend_id;
    
    SELECT quantity INTO total_quantity
    FROM shipment_lend
    WHERE id = OLD.fk_lend_id
    LIMIT 1;
    
    IF retrieved_quantity IS NULL THEN
        SET retrieved_quantity = 0;
    END IF;
    
    SET not_retrieved_quantity = total_quantity - retrieved_quantity;
    IF not_retrieved_quantity < 0 THEN
        SET not_retrieved_quantity = 0;
    END IF;
    
    UPDATE shipment_lend 
    SET not_retrieved_quantity = not_retrieved_quantity
    WHERE id = OLD.fk_lend_id;
END;''')
event.listen(ShipmentRetrieve.__table__, 'after_create', after_shipment_retrieve_delete)

# 출고반품 삭제
before_shipment_release_return_delete = DDL('''
DROP TRIGGER IF EXISTS before_shipment_release_return_delete;
CREATE TRIGGER before_shipment_release_return_delete
BEFORE DELETE ON shipment_release_return
FOR EACH ROW
BEGIN
    # 출고반품품목 삭제
    DELETE FROM shipment_release_return_item WHERE fk_release_return_id = OLD.id;
END;''')
event.listen(ShipmentReleaseReturn.__table__, 'after_create', before_shipment_release_return_delete)

# ----------------------------------------------------------------------------------------------------------------------
