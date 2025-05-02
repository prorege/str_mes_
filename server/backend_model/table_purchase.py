# -*- coding: utf-8 -*-

print("module [backend_model.table_purchase.py] loaded")
from datetime import datetime
from sqlalchemy import DDL, event
from backend_model.database import DBManager
from backend_model.table_base import BaseItem, BaseWarehouse
from backend_model.table_common import Companies
from backend_model.table_production import MeasureRequirementItem2
from backend_model.table_project import ProjectExcutionPlanItem, ProjectManagement, ProjectExcutionPlanSubcontract

db = DBManager.db


class PurchaseOrderPlan(db.Model):  # 구매관리 - 발주계획
    __tablename__ = 'purchase_order_plan'
    __table_args__ = {'comment': '구매관리(발주계획)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    order_plan_number = db.Column('order_plan_number', db.String(48), comment='발주계획번호')
    order_plan_date = db.Column('order_plan_date', db.DateTime, comment='발주계획일자')
    order_plan_department = db.Column('order_plan_department', db.String(48), comment='발주계획부서')
    order_plan_manager = db.Column('order_plan_manager', db.String(48), comment='발주계획담당자')
    order_type = db.Column('order_type', db.String(48), comment='발주구분')
    note = db.Column('note', db.String(256), comment='참고사항')
    etc = db.Column('etc', db.Text, comment='비고')
    supply_price = db.Column('supply_price', db.BigInteger, comment='공급가')
    vat = db.Column('vat', db.Integer, comment='부가세')
    total_price = db.Column('total_price', db.BigInteger, comment='합계금액')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id, onupdate='CASCADE', ondelete='CASCADE'), comment='회사 FK')


class PurchaseOrderPlanItem(db.Model):  # 구매관리 - 발주계획 - 발주계획품목
    from backend_model.table_shipment import ShipmentOrderItem
    
    __tablename__ = 'purchase_order_plan_item'
    __table_args__ = {'comment': '발주계획(발주계획품목)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE', ondelete='SET NULL'), comment='품목코드')
    order_plan_quantity = db.Column('order_plan_quantity', db.Integer, comment='발주계획수량')
    unit_price = db.Column('unit_price', db.Numeric(10, 2), comment='단가')
    supply_price = db.Column('supply_price', db.Numeric(20, 2), comment='공급가')
    request_delivery_date = db.Column('request_delivery_date', db.DateTime, comment='요청납기')
    unordered_quantity = db.Column('unordered_quantity', db.Integer, comment='미발주수량')
    not_produce_plan_quantity = db.Column('not_produce_plan_quantity', db.Integer, comment='미생산계획수량')
    order_number = db.Column('order_number', db.String(48), comment='수주번호')
    order_date = db.Column('order_date', db.DateTime, comment='수주일자')
    main_supplier = db.Column('main_supplier', db.String(48), comment='주공급업체')
    client_item_number = db.Column('client_item_number', db.String(48), comment='고객사품번')
    end_user = db.Column('end_user', db.String(48), comment='실수요자')
    delivery_date = db.Column('delivery_date', db.DateTime, comment='납기일자')
    warehouse_code = db.Column('warehouse_code', db.String(48), db.ForeignKey(BaseWarehouse.wh_code, onupdate='CASCADE', ondelete='SET NULL'), comment='입고창고')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate='CASCADE'), comment="프로젝트 FK")
    fk_shipment_order_item_id = db.Column('fk_shipment_order_item_id', db.Integer, db.ForeignKey(ShipmentOrderItem.id, onupdate='CASCADE', ondelete='RESTRICT'), comment='수주품목 FK')
    fk_purchase_order_plan_id = db.Column('fk_purchase_order_plan_id', db.Integer, db.ForeignKey(PurchaseOrderPlan.id, onupdate='CASCADE', ondelete='CASCADE'), comment='발주계획 FK')
    fk_measure_requirement_item2_id = db.Column('fk_measure_requirement_item2_id', db.Integer, db.ForeignKey(MeasureRequirementItem2.id, onupdate='CASCADE', ondelete='RESTRICT'), comment='소요량계산품목2 FK')
    project_management = db.relationship('ProjectManagement', foreign_keys=[fk_project_management_id])
    order_plan = db.relationship("PurchaseOrderPlan", foreign_keys=[fk_purchase_order_plan_id])  # 발주계획
    measure_requirement_item2 = db.relationship("MeasureRequirementItem2", foreign_keys=[fk_measure_requirement_item2_id])  # 생산관리 - 소요량계산품목
    item = db.relationship("BaseItem", foreign_keys=[item_code])
    warehouse = db.relationship('BaseWarehouse', foreign_keys=[warehouse_code])
    basic_stock = db.relationship('SetupBasicStock', viewonly=True,
                                  primaryjoin='and_(foreign(PurchaseOrderPlanItem.item_code) == SetupBasicStock.item_code,'
                                              'foreign(PurchaseOrderPlanItem.warehouse_code) == SetupBasicStock.wh_code)')


class PurchaseOrder(db.Model):  # 구매관리 - 발주
    __tablename__ = 'purchase_order'
    __table_args__ = {'comment': '구매관리(발주)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    order_number = db.Column('order_number', db.String(48), comment='발주번호')
    order_date = db.Column('order_date', db.DateTime, comment='발주일자')
    client_company = db.Column('client_company', db.String(48), comment='공급업체')
    client_manager = db.Column('client_manager', db.String(48), comment='업체담당자')
    client_manager_email = db.Column('client_manager_email', db.String(96), comment='업체담당자 이메일')
    order_department = db.Column('order_department', db.String(48), comment='발주부서')
    order_manager = db.Column('order_manager', db.String(48), comment='발주담당자')
    order_manager_email = db.Column('order_manager_email', db.String(96), comment='발주담당자 이메일')
    order_type = db.Column('order_type', db.String(48), comment='발주구분')
    vat_type = db.Column('vat_type', db.String(48), comment='부가세구분')
    payment_terms = db.Column('payment_terms', db.String(48), comment='결재조건')
    delivery_date = db.Column('delivery_date', db.DateTime, comment='납품기한')
    delivery_place = db.Column('delivery_place', db.String(48), comment='납품장소')
    ref_number = db.Column('ref_number', db.String(48), comment='무상수리기간')
    end_user = db.Column('end_user', db.String(48), comment='EndUser')
    note = db.Column('note', db.String(256), comment='참고사항')
    etc = db.Column('etc', db.Text, comment='비고')
    supply_price = db.Column('supply_price', db.BigInteger, comment='공급가')
    vat = db.Column('vat', db.Integer, comment='부가세')
    total_price = db.Column('total_price', db.BigInteger, comment='합계금액')
    confirmed = db.Column('confirmed', db.Boolean, server_default='0', comment='발주확정 여부')
    confirmed_manager = db.Column('confirmed_manager', db.String(48), comment='발주확정 관리자')
    confirmed_date = db.Column('confirmed_date', db.DateTime, comment='발주확정 일자')
    approve = db.Column('approve', db.Boolean, server_default='0', comment='발주승인 여부')
    approve_manager = db.Column('approve_manager', db.String(48), comment='발주승인 관리자')
    approve_date = db.Column('approve_date', db.DateTime, comment='발주승인 일자')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate='CASCADE'), comment="프로젝트 FK")
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id, onupdate='CASCADE', ondelete='CASCADE'), comment='회사 FK')
    project_management = db.relationship('ProjectManagement', foreign_keys=[fk_project_management_id])


class PurchaseOrderItem(db.Model):  # 구매관리 - 발주 - 발주품목
    __tablename__ = 'purchase_order_item'
    __table_args__ = {'comment': '발주(발주품목)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE', ondelete='SET NULL'), comment='품목코드')
    order_quantity = db.Column('order_quantity', db.Integer, comment='발주수량')
    unit_price = db.Column('unit_price', db.Numeric(12, 4), comment='단가')
    expect_unit_price = db.Column('expect_unit_price', db.Integer, comment='예정단가')
    supply_price = db.Column('supply_price', db.Numeric(20, 2), comment='공급가')
    request_delivery_date = db.Column('request_delivery_date', db.DateTime, comment='요청납기')
    fixed_delivery_date = db.Column('fixed_delivery_date', db.DateTime, comment='확정납기')
    not_shipped = db.Column('not_shipped', db.Integer, comment='미입고수량')
    order_plan_number = db.Column('order_plan_number', db.String(48), comment='발주계획번호')
    client_item_number = db.Column('client_item_number', db.String(48), comment='공급사품번')
    note = db.Column('note', db.String(256), comment='참고사항')
    closing_yn = db.Column('closing_yn', db.Boolean, comment='종결여부')
    check_yn = db.Column('check_yn', db.Boolean, comment='검수완료여부')
    warehouse_code = db.Column('warehouse_code', db.String(48), db.ForeignKey(BaseWarehouse.wh_code, onupdate='CASCADE', ondelete='SET NULL'), comment='입고창고')
    fk_order_plan_item_id = db.Column('fk_order_plan_item_id', db.Integer, db.ForeignKey(PurchaseOrderPlanItem.id), comment='발주계획 품목 FK')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate='CASCADE'), comment="프로젝트 FK")
    fk_excution_plan_item_id = db.Column('fk_excution_plan_item_id', db.Integer, db.ForeignKey(ProjectExcutionPlanItem.id, onupdate='CASCADE'), comment='실행계획 품목 FK')
    fk_excution_plan_subcontract_id = db.Column('fk_excution_plan_subcontract_id', db.Integer, db.ForeignKey(ProjectExcutionPlanSubcontract.id, onupdate='CASCADE'), comment='실행계획 외주공사 FK')
    fk_purchase_order_id = db.Column('fk_purchase_order_id', db.Integer, db.ForeignKey(PurchaseOrder.id, onupdate='CASCADE'), comment='발주 FK')
    order = db.relationship("PurchaseOrder", foreign_keys=[fk_purchase_order_id])
    order_plan_item = db.relationship("PurchaseOrderPlanItem", foreign_keys=[fk_order_plan_item_id])
    project_management = db.relationship('ProjectManagement', foreign_keys=[fk_project_management_id])
    excution_plan_item = db.relationship('ProjectExcutionPlanItem', foreign_keys=[fk_excution_plan_item_id])
    excution_plan_subcontract = db.relationship('ProjectExcutionPlanSubcontract', foreign_keys=[fk_excution_plan_subcontract_id])
    item = db.relationship("BaseItem", foreign_keys=[item_code])
    warehouse = db.relationship('BaseWarehouse', foreign_keys=[warehouse_code])
    basic_stock = db.relationship('SetupBasicStock', viewonly=True,
                                  primaryjoin='and_(foreign(PurchaseOrderItem.item_code) == SetupBasicStock.item_code,'
                                              'foreign(PurchaseOrderItem.warehouse_code) == SetupBasicStock.wh_code)')

ProjectExcutionPlanItem.purchase_order_item = db.relationship('PurchaseOrderItem', uselist=False)
ProjectExcutionPlanSubcontract.purchase_order_item = db.relationship('PurchaseOrderItem', uselist=False)

class PurchasePreReceiving(db.Model):  # 구매관리 - 가입고
    __tablename__ = 'purchase_prereceiving'
    __table_args__ = {'comment': '구매관리(가입고)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    prereceiving_number = db.Column('prereceiving_number', db.String(48), comment='가입고번호')
    prereceiving_date = db.Column('prereceiving_date', db.DateTime, comment='가입고일자')
    client_company = db.Column('client_company', db.String(48), comment='공급업체')
    client_manager = db.Column('client_manager', db.String(48), comment='업체담당자')
    receiving_department = db.Column('receiving_department', db.String(48), comment='입고부서')
    receiving_manager = db.Column('receiving_manager', db.String(48), comment='입고담당자')
    receiving_type = db.Column('receiving_type', db.String(48), comment='입고구분')
    vat_type = db.Column('vat_type', db.String(48), comment='부가세구분')
    payment_terms = db.Column('payment_terms', db.String(48), comment='결재조건')
    delivery_date = db.Column('delivery_date', db.DateTime, comment='납품기한')
    delivery_place = db.Column('delivery_place', db.String(48), comment='납품장소')
    ref_number = db.Column('ref_number', db.String(48), comment='무상수리기간')
    end_user = db.Column('end_user', db.String(48), comment='EndUser')
    note = db.Column('note', db.String(256), comment='참고사항')
    etc = db.Column('etc', db.Text, comment='비고')
    supply_price = db.Column('supply_price', db.BigInteger, comment='공급가')
    vat = db.Column('vat', db.Integer, comment='부가세')
    total_price = db.Column('total_price', db.BigInteger, comment='합계금액')
    confirmed = db.Column('confirmed', db.Boolean, server_default='0', comment='입고 확정 여부')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate='CASCADE'), comment="프로젝트 FK")
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id, onupdate='CASCADE', ondelete='CASCADE'), comment='회사 FK')
    project_management = db.relationship('ProjectManagement', foreign_keys=[fk_project_management_id])

class PurchasePreReceivingItem(db.Model):  # 구매관리 - 가입고 - 입고품목
    __tablename__ = 'purchase_prereceiving_item'
    __table_args__ = {'comment': '가입고(가입고품목)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE', ondelete='SET NULL'), comment='품목코드')
    order_quantity = db.Column('order_quantity', db.Integer, comment='발주수량')
    prereceiving_quantity = db.Column('prereceiving_quantity', db.Integer, comment='가입고수량')
    unit_price = db.Column('unit_price', db.Numeric(13, 5), comment='단가')
    supply_price = db.Column('supply_price', db.Numeric(20, 2), comment='공급가')
    request_delivery_date = db.Column('request_delivery_date', db.DateTime, comment='요청납기')
    order_number = db.Column('order_number', db.String(48), comment='발주번호')
    client_item_number = db.Column('client_item_number', db.String(48), comment='공급사품번')
    note = db.Column('note', db.String(256), comment='참고사항')
    check_quantity = db.Column('check_quantity', db.Integer, comment='검수수량')
    bad_quantity = db.Column('bad_quantity', db.Integer, comment='불량수량')
    good_quantity = db.Column('good_quantity', db.Integer, comment='양품수량')
    not_shipped = db.Column('not_shipped', db.Integer, comment='미입고수량')
    lot_number = db.Column('lot_number', db.String(48), comment='LOT번호')
    check_yn = db.Column('check_yn', db.Boolean, comment='검수완료')
    warehouse_code = db.Column('warehouse_code', db.String(48), db.ForeignKey(BaseWarehouse.wh_code, onupdate='CASCADE', ondelete='SET NULL'), comment='입고창고')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate='CASCADE'), comment="프로젝트 FK")
    fk_prereceiving_id = db.Column('fk_prereceiving_id', db.Integer, db.ForeignKey(PurchasePreReceiving.id, onupdate='CASCADE'), comment='가입고 FK')
    fk_order_item_id = db.Column('fk_order_item_id', db.Integer, db.ForeignKey(PurchaseOrderItem.id), comment='발주 품목 FK')
    project_management = db.relationship('ProjectManagement', foreign_keys=[fk_project_management_id])
    order_item = db.relationship("PurchaseOrderItem", foreign_keys=[fk_order_item_id])
    prereceiving = db.relationship("PurchasePreReceiving", foreign_keys=[fk_prereceiving_id])
    item = db.relationship("BaseItem", foreign_keys=[item_code])
    warehouse = db.relationship('BaseWarehouse', foreign_keys=[warehouse_code])
    basic_stock = db.relationship('SetupBasicStock', viewonly=True,
                                  primaryjoin='and_(foreign(PurchasePreReceivingItem.item_code) == SetupBasicStock.item_code,'
                                              'foreign(PurchasePreReceivingItem.warehouse_code) == SetupBasicStock.wh_code)')


class PurchaseReceiving(db.Model):  # 구매관리 - 입고
    __tablename__ = 'purchase_receiving'
    __table_args__ = {'comment': '구매관리(입고)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    receiving_number = db.Column('receiving_number', db.String(48), comment='입고번호')
    receiving_date = db.Column('receiving_date', db.DateTime, comment='수불일자')  # 수불일자로 변경
    receiving_date2 = db.Column('receiving_date2', db.DateTime, comment='입고일자')
    client_company = db.Column('client_company', db.String(48), comment='공급업체')
    client_manager = db.Column('client_manager', db.String(48), comment='업체담당자')
    receiving_department = db.Column('receiving_department', db.String(48), comment='입고부서')
    receiving_manager = db.Column('receiving_manager', db.String(48), comment='입고담당자')
    receiving_type = db.Column('receiving_type', db.String(48), comment='입고구분')
    vat_type = db.Column('vat_type', db.String(48), comment='부가세구분')
    payment_terms = db.Column('payment_terms', db.String(48), comment='결재조건')
    delivery_date = db.Column('delivery_date', db.DateTime, comment='납품기한')
    delivery_place = db.Column('delivery_place', db.String(48), comment='납품장소')
    ref_number = db.Column('ref_number', db.String(48), comment='무상수리기간')
    end_user = db.Column('end_user', db.String(48), comment='EndUser')
    note = db.Column('note', db.String(256), comment='참고사항')
    etc = db.Column('etc', db.Text, comment='비고')
    supply_price = db.Column('supply_price', db.BigInteger, comment='공급가')
    vat = db.Column('vat', db.Integer, comment='부가세')
    total_price = db.Column('total_price', db.BigInteger, comment='합계금액')
    confirmed = db.Column('confirmed', db.Boolean, server_default='0', comment='입고 확정 여부')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate='CASCADE'), comment="프로젝트 FK")
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id, onupdate='CASCADE', ondelete='CASCADE'), comment='회사 FK')
    project_management = db.relationship('ProjectManagement', foreign_keys=[fk_project_management_id])


class PurchaseReceivingItem(db.Model):  # 구매관리 - 입고 - 입고품목
    __tablename__ = 'purchase_receiving_item'
    __table_args__ = {'comment': '입고(입고품목)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE', ondelete='SET NULL'), comment='품목코드')
    order_quantity = db.Column('order_quantity', db.Integer, comment='발주수량')
    receiving_quantity = db.Column('receiving_quantity', db.Integer, comment='입고수량')
    unit_price = db.Column('unit_price', db.Numeric(13, 5), comment='단가')
    supply_price = db.Column('supply_price', db.Numeric(20, 2), comment='공급가')
    non_invoice = db.Column('non_invoice', db.Integer , comment='미계산서')
    request_delivery_date = db.Column('request_delivery_date', db.DateTime, comment='요청납기')
    order_number = db.Column('order_number', db.String(48), comment='발주번호')
    client_item_number = db.Column('client_item_number', db.String(48), comment='공급사품번')
    note = db.Column('note', db.String(256), comment='참고사항')
    closing_yn = db.Column('closing_yn', db.Boolean, comment='종결여부')
    warehouse_code = db.Column('warehouse_code', db.String(48), db.ForeignKey(BaseWarehouse.wh_code, onupdate='CASCADE', ondelete='SET NULL'), comment='입고창고')
    lot_number = db.Column('lot_number', db.String(48), comment='LOT번호')
    supplier_lot_number = db.Column('supplier_lot_number', db.String(48), comment='공급처LOT번호')
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate='CASCADE'), comment="프로젝트 FK")
    fk_receiving_id = db.Column('fk_receiving_id', db.Integer, db.ForeignKey(PurchaseReceiving.id, onupdate='CASCADE'), comment='입고 FK')
    fk_order_item_id = db.Column('fk_order_item_id', db.Integer, db.ForeignKey(PurchaseOrderItem.id), comment='발주 품목 FK')
    fk_purchase_order_id = db.Column('fk_purchase_order_id', db.Integer, db.ForeignKey(PurchaseOrder.id), comment='발주 FK')
    fk_prereceiving_id = db.Column('fk_prereceiving_id', db.Integer, db.ForeignKey(PurchasePreReceiving.id), comment='가입고 FK')
    fk_prereceiving_item_id = db.Column('fk_prereceiving_item_id', db.Integer, db.ForeignKey(PurchasePreReceivingItem.id), comment='가입고 품목 FK')
    project_management = db.relationship('ProjectManagement', foreign_keys=[fk_project_management_id])
    order_item = db.relationship("PurchaseOrderItem", foreign_keys=[fk_order_item_id])
    receiving = db.relationship("PurchaseReceiving", foreign_keys=[fk_receiving_id])
    item = db.relationship("BaseItem", foreign_keys=[item_code])
    warehouse = db.relationship('BaseWarehouse', foreign_keys=[warehouse_code])
    prereceiving = db.relationship('PurchasePreReceiving', foreign_keys=[fk_prereceiving_id])
    order = db.relationship('PurchaseOrder', foreign_keys=[fk_purchase_order_id])
    prereceiving_item = db.relationship('PurchasePreReceivingItem', foreign_keys=[fk_prereceiving_item_id])
    basic_stock = db.relationship('SetupBasicStock', viewonly=True,
                                  primaryjoin='and_(foreign(PurchaseReceivingItem.item_code) == SetupBasicStock.item_code,'
                                              'foreign(PurchaseReceivingItem.warehouse_code) == SetupBasicStock.wh_code)')


class PurchaseReceivingReturn(db.Model):  # 구매관리 - 입고반품
    __tablename__ = 'purchase_receiving_return'
    __table_args__ = {'comment': '입고반품(입고반품)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    return_number = db.Column('return_number', db.String(48), comment='반품번호')
    return_date = db.Column('return_date', db.DateTime, comment='반품일자')
    client_company = db.Column('client_company', db.String(48), comment='공급업체')
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


class PurchaseReceivingReturnItem(db.Model):  # 구매관리 - 입고반품 - 품목
    __tablename__ = 'purchase_receiving_return_item'
    __table_args__ = {'comment': '입고반품(입고반품품목)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE'), comment='품목코드')
    return_quantity = db.Column('return_quantity', db.Integer, server_default='0', comment='반품수량')
    non_invoice = db.Column('non_invoice', db.Integer , comment='미계산서')
    cost_price = db.Column('cost_price', db.Numeric(10, 2), server_default='0', comment='원가')
    total_cost_price = db.Column('total_cost_price', db.Numeric(20, 4), server_default='0', comment='원가합계')
    supply_price = db.Column('supply_price', db.Numeric(20, 2), server_default='0', comment='공급가')
    request_delivery_date = db.Column('request_delivery_date', db.DateTime, comment='요청납기')
    warehouse_code = db.Column('warehouse_code', db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment='출고창고')
    return_reason = db.Column('return_reason', db.String(256), comment='반품사유')
    fk_receiving_id = db.Column('fk_receiving_id', db.Integer, db.ForeignKey(PurchaseReceiving.id, onupdate='CASCADE'), comment='입고 FK')
    fk_receiving_item_id = db.Column('fk_receiving_item_id', db.Integer, db.ForeignKey(PurchaseReceivingItem.id), comment='입고품목 FK')
    fk_receiving_return_id = db.Column('fk_receiving_return_id', db.Integer, db.ForeignKey(PurchaseReceivingReturn.id, onupdate='CASCADE'), comment='입고반품 FK')
    receiving = db.relationship("PurchaseReceiving", foreign_keys=[fk_receiving_id])
    receiving_item = db.relationship("PurchaseReceivingItem", foreign_keys=[fk_receiving_item_id])
    receiving_return = db.relationship("PurchaseReceivingReturn", foreign_keys=[fk_receiving_return_id])
    item = db.relationship('BaseItem', foreign_keys=[item_code])
    warehouse = db.relationship('BaseWarehouse', foreign_keys=[warehouse_code])
    basic_stock = db.relationship('SetupBasicStock', viewonly=True,
                                  primaryjoin='and_(foreign(PurchaseReceivingReturnItem.item_code) == SetupBasicStock.item_code,'
                                              'foreign(PurchaseReceivingReturnItem.warehouse_code) == SetupBasicStock.wh_code)')

class PurchaseStatement(db.Model): # 구매관리 - 매입 계산서
    __tablename__ = 'purchase_statement'
    __table_args__ = {
        'comment': '매입계산서'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    statement_number = db.Column('statement_number', db.String(48), comment='계산서번호')
    statement_date = db.Column('statement_date', db.DateTime, comment='발행일자')
    client_company = db.Column('client_company', db.String(48), comment='고객업체')
    client_manager = db.Column('client_manager', db.String(48), comment='업체담당자')
    statement_department = db.Column('statement_department', db.String(48), comment='매입부서')
    statement_manager = db.Column('statement_manager', db.String(48), comment='매입담당자')
    tax_rate = db.Column('tax_rate', db.String(48), comment='세율')
    statement_type = db.Column('statement_type', db.String(48), comment='계산서유형')
    approval_type = db.Column('approval_type', db.String(48), comment='결재유형')
    publish_type = db.Column('publish_type', db.String(48), comment='발행구분')
    office_type = db.Column('office_type', db.String(48), comment='본지점구분')
    etc = db.Column('etc', db.Text, comment='비고')
    vat_type = db.Column('vat_type', db.String(48), comment='부가세구분')
    vat = db.Column('vat', db.Numeric(12, 2), server_default='0', comment='부가세')
    vat_adjustment = db.Column('vat_adjustment', db.Numeric(12, 2), server_default='0', comment='부가세보정')
    supply_price = db.Column('supply_price', db.Numeric(14, 2), server_default='0', comment='공급가')
    total_price = db.Column('total_price', db.Numeric(14, 2), server_default='0', comment='합계금액')
    not_payment = db.Column('not_payment', db.Numeric(14, 2), server_default='0', comment='미결제')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')


class PurchaseStatementItem(db.Model):  # 구매관리 - 매입계산서품목
    __tablename__ = 'purchase_statement_item'
    __table_args__ = {
        'comment': '매입계산서(매입계산서품목)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE'), comment='품목코드')
    quantity = db.Column('quantity', db.Integer, comment='수량')
    unit_price = db.Column('unit_price', db.Numeric(12, 2), server_default='0', comment='단가')
    vat = db.Column('vat', db.Numeric(12, 2), server_default='0', comment='부가세')
    supply_price = db.Column('supply_price', db.Numeric(14, 2), server_default='0', comment='공급가')
    total_price = db.Column('total_price', db.Numeric(14, 2), server_default='0', comment='합계금액')
    project_number = db.Column('project_number', db.String(48), comment='프로젝트번호')
    note = db.Column('note', db.Text, comment='추가설명')
    receiving_number = db.Column('receiving_number', db.String(48), comment='입고번호')
    return_number = db.Column('return_number', db.String(48), comment='입고반품번호')
    fk_statement_id = db.Column('fk_statement_id', db.Integer, db.ForeignKey(PurchaseStatement.id, onupdate='CASCADE'), comment='계산서 FK')
    fk_order_item_id = db.Column('fk_order_item_id', db.Integer, db.ForeignKey(PurchaseOrder.id, onupdate='CASCADE'), comment='발주품목 FK')
    fk_receiving_item_id = db.Column('fk_receiving_item_id', db.Integer, db.ForeignKey(PurchaseReceivingItem.id, onupdate='CASCADE'), comment='입고품목 FK')
    fk_receiving_return_item_id = db.Column('fk_receiving_return_item_id', db.Integer, db.ForeignKey(PurchaseReceivingReturnItem.id, onupdate='CASCADE'), comment='입고반품품목 FK')
    item = db.relationship('BaseItem', foreign_keys=[item_code])
    statement = db.relationship("PurchaseStatement", foreign_keys=[fk_statement_id])
    # receiving_item = db.relationship('PurchaseReceivingItem', foreign_keys=[fk_receiving_item_id])
    # receiving_return_item = db.relationship('PurchaseReceivingReturnItem', foreign_keys=[fk_receiving_return_item_id])
    receiving = db.relationship(
        "PurchaseReceiving",
        secondary="join(PurchaseReceivingItem, PurchaseReceiving, PurchaseReceivingItem.fk_receiving_id == PurchaseReceiving.id)",
        primaryjoin="PurchaseStatementItem.fk_receiving_item_id == PurchaseReceivingItem.id",
        secondaryjoin="foreign(PurchaseReceivingItem.fk_receiving_id) == PurchaseReceiving.id",
        uselist=False,
        viewonly=True,
    )
    receiving_return = db.relationship(
        "PurchaseReceivingReturn",
        secondary="join(PurchaseReceivingReturnItem, PurchaseReceivingReturn, PurchaseReceivingReturnItem.fk_receiving_return_id == PurchaseReceivingReturn.id)",
        primaryjoin="PurchaseStatementItem.fk_receiving_return_item_id == PurchaseReceivingReturnItem.id",
        secondaryjoin="foreign(PurchaseReceivingReturnItem.fk_receiving_return_id) == PurchaseReceivingReturn.id",
        uselist=False,
        viewonly=True,
    )
    client = db.relationship(
        'BaseClient',
        secondary="join(PurchaseStatement, BaseClient, PurchaseStatement.client_company == BaseClient.name)",
        primaryjoin="PurchaseStatementItem.fk_statement_id == PurchaseStatement.id",
        secondaryjoin="foreign(PurchaseStatement.client_company) == BaseClient.name",
        uselist=False,
        viewonly=True,
    )

class PurchasePayment(db.Model):  # 구매관리 - 결제
    __tablename__ = 'purchase_payment'
    __table_args__ = {
        'comment': '구매관리(결제)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    payment_number = db.Column('payment_number', db.String(48), comment='결제번호')
    payment_date = db.Column('payment_date', db.DateTime, comment='결제일자')
    client_company = db.Column('client_company', db.String(48), comment='고객업체')
    client_manager = db.Column('client_manager', db.String(48), comment='업체담당자')
    payment_department = db.Column('payment_department', db.String(48), comment='영업부서')
    payment_manager = db.Column('payment_manager', db.String(48), comment='영업담당자')
    total_price = db.Column('total_price', db.Numeric(20, 4), server_default='0', comment="결제합계금액")
    etc = db.Column('etc', db.Text, comment='비고')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')

class PurchasePaymentItem(db.Model):  # 구매관리 - 결제내역
    __tablename__ = 'purchase_payment_item'
    __table_args__ = {
        'comment': '결제(결제내역)'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    price = db.Column('price', db.BigInteger, comment='금액')
    payment_type = db.Column('payment_type', db.String(48), comment='결제형태')
    project_number = db.Column('project_number', db.String(48), comment='프로젝트번호')
    etc = db.Column('etc', db.Text, comment='결제적요')
    fk_payment_id = db.Column('fk_payment_id', db.Integer, db.ForeignKey(PurchasePayment.id, onupdate='CASCADE'), comment='입금 FK')
    fk_statement_id = db.Column('fk_statement_id', db.Integer, db.ForeignKey(PurchaseStatement.id, onupdate='CASCADE'), comment='매입계산서 FK')
    payment = db.relationship("PurchasePayment", foreign_keys=[fk_payment_id])
    statement = db.relationship("PurchaseStatement", foreign_keys=[fk_statement_id])
    client = db.relationship(
        'BaseClient',
        secondary="join(PurchasePayment, BaseClient, PurchasePayment.client_company == BaseClient.name)",
        primaryjoin="PurchasePaymentItem.fk_payment_id == PurchasePayment.id",
        secondaryjoin="foreign(PurchasePayment.client_company) == BaseClient.name",
        uselist=False,
        viewonly=True,
    )

# ----------------------------------------------------------------------------------------------------------------------
# CREATE STORED PROCEDURE

# 가입고품목의 가입고수량 가져오기
proc_get_purchase_prereceiving_item_total_quantity_in_order = DDL('''
DROP PROCEDURE IF EXISTS proc_get_purchase_prereceiving_item_total_quantity_in_order;
CREATE PROCEDURE `proc_get_purchase_prereceiving_item_total_quantity_in_order`(
    IN `orderItemId` INT,
    OUT `sum` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '가입고품목의 가입고수량 가져오기'
BEGIN
    SET sum = (SELECT SUM(prereceiving_quantity)
               FROM purchase_prereceiving_item
               WHERE fk_order_item_id = orderItemId
               GROUP BY fk_order_item_id);
    IF sum IS NULL THEN
        SET sum = 0;
    ENd IF;
END
''')
event.listen(PurchasePreReceivingItem.__table__, 'after_create', proc_get_purchase_prereceiving_item_total_quantity_in_order)


# 발주품목의 미입고수량 업데이트(가입고 품목)
proc_update_purchase_order_item_not_shipped_to_prereceiving = DDL('''
DROP PROCEDURE IF EXISTS proc_update_purchase_order_item_not_shipped_to_prereceiving;
CREATE PROCEDURE `proc_update_purchase_order_item_not_shipped_to_prereceiving`(
    IN `orderItemId` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '발주품목의 미입고수량 업데이트'
BEGIN
    CALL proc_get_purchase_prereceiving_item_total_quantity_in_order(orderItemId, @sum);
        
    UPDATE purchase_order_item
    SET not_shipped = order_quantity - @sum
    WHERE id = orderItemId;
END
''')
event.listen(PurchaseOrderItem.__table__, 'after_create', proc_update_purchase_order_item_not_shipped_to_prereceiving)

# 가입고품목의 미입고수량 업데이트
proc_update_purchase_prereceiving_item_not_shipped = DDL('''
DROP PROCEDURE IF EXISTS proc_update_purchase_prereceiving_item_not_shipped;
CREATE PROCEDURE `proc_update_purchase_prereceiving_item_not_shipped`(
    IN `prereceivingItemId` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '가입고품목의 미입고수량 업데이트'
BEGIN
    CALL proc_get_purchase_receiving_item_total_quantity_in_prereceiving(prereceivingItemId, @sum);

    UPDATE purchase_prereceiving_item
    SET not_shipped = good_quantity - @sum
    WHERE id = prereceivingItemId;
END
''')
event.listen(PurchasePreReceivingItem.__table__, 'after_create', proc_update_purchase_prereceiving_item_not_shipped)

# 발주품목의 미입고수량 업데이트(입고 품목)
proc_update_purchase_order_item_not_shipped_to_receiving = DDL('''
DROP PROCEDURE IF EXISTS proc_update_purchase_order_item_not_shipped_to_receiving;
CREATE PROCEDURE `proc_update_purchase_order_item_not_shipped_to_receiving`(
    IN `orderItemId` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '발주품목의 미입고수량 업데이트'
BEGIN
    CALL proc_get_purchase_receiving_item_total_quantity_in_order(orderItemId, @sum);
        
    UPDATE purchase_order_item
    SET not_shipped = order_quantity - @sum
    WHERE id = orderItemId;
END
''')
event.listen(PurchaseOrderItem.__table__, 'after_create', proc_update_purchase_order_item_not_shipped_to_receiving)


# 입고품목의 입고수량 가져오기(발주 품목)
proc_get_purchase_receiving_item_total_quantity_in_order = DDL('''
DROP PROCEDURE IF EXISTS proc_get_purchase_receiving_item_total_quantity_in_order;
CREATE PROCEDURE `proc_get_purchase_receiving_item_total_quantity_in_order`(
    IN `orderItemId` INT,
    OUT `sum` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '입고품목의 입고수량 가져오기'
BEGIN
    SET sum = (SELECT SUM(receiving_quantity)
               FROM purchase_receiving_item
               WHERE fk_order_item_id = orderItemId
               GROUP BY fk_order_item_id);
    IF sum IS NULL THEN
        SET sum = 0;
    ENd IF;
END
''')
event.listen(PurchaseReceivingItem.__table__, 'after_create', proc_get_purchase_receiving_item_total_quantity_in_order)

# 입고품목의 입고수량 가져오기 (가입고품목)
proc_get_purchase_receiving_item_total_quantity_in_prereceiving = DDL('''
DROP PROCEDURE IF EXISTS proc_get_purchase_receiving_item_total_quantity_in_prereceiving;
CREATE PROCEDURE `proc_get_purchase_receiving_item_total_quantity_in_prereceiving`(
    IN `prereceivingItemId` INT,
    OUT `sum` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '입고품목의 입고수량 가져오기'
BEGIN
    SET sum = (SELECT SUM(receiving_quantity)
               FROM purchase_receiving_item
               WHERE fk_prereceiving_item_id = prereceivingItemId
               GROUP BY fk_prereceiving_item_id);
    IF sum IS NULL THEN
        SET sum = 0;
    ENd IF;
END
''')
event.listen(PurchaseReceivingItem.__table__, 'after_create', proc_get_purchase_receiving_item_total_quantity_in_prereceiving)


# 매입계산서 품목의 계산서수량 가져오기(입고)
proc_get_purchase_statement_item_total_quantity = DDL('''
DROP PROCEDURE IF EXISTS proc_get_purchase_statement_item_total_quantity;
CREATE PROCEDURE `proc_get_purchase_statement_item_total_quantity`(
    IN `receivingItemId` INT,
    OUT `sum` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '매입계산서 품목의 계산서수량 가져오기'
BEGIN
    SET sum = (SELECT SUM(quantity)
               FROM purchase_statement_item
               WHERE fk_receiving_item_id = receivingItemId
               GROUP BY fk_receiving_item_id);
    IF sum IS NULL THEN
        SET sum = 0;
    ENd IF;
END
''')
event.listen(PurchaseStatementItem.__table__, 'after_create', proc_get_purchase_statement_item_total_quantity)


# 매입계산서 품목의 계산서수량 가져오기(입고반품)
proc_get_purchase_statement_item_total_quantity_return = DDL('''
DROP PROCEDURE IF EXISTS proc_get_purchase_statement_item_total_quantity_return;
CREATE PROCEDURE `proc_get_purchase_statement_item_total_quantity_return`(
    IN `receivingReturnItemId` INT,
    OUT `sum` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '매입계산서 품목의 계산서수량 가져오기(입고반품)'
BEGIN
    SET sum = (SELECT SUM(quantity)
               FROM purchase_statement_item
               WHERE fk_receiving_return_item_id = receivingReturnItemId
               GROUP BY fk_receiving_return_item_id);
    IF sum IS NULL THEN
        SET sum = 0;
    ENd IF;
END
''')
event.listen(PurchaseStatementItem.__table__, 'after_create', proc_get_purchase_statement_item_total_quantity_return)


# 결재내역 품목의 총 결재금액 가져오기
proc_get_purchase_payment_item_total_price = DDL('''
DROP PROCEDURE IF EXISTS proc_get_purchase_payment_item_total_price;
CREATE PROCEDURE `proc_get_purchase_payment_item_total_price`(
    IN `statementId` INT,
    OUT `sum` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '매입계산서 품목의 계산서수량 가져오기(입고반품)'
BEGIN
    SET sum = (SELECT SUM(price)
               FROM purchase_payment_item
               WHERE fk_statement_id = statementId
               GROUP BY fk_statement_id);
    IF sum IS NULL THEN
        SET sum = 0;
    ENd IF;
END
''')
event.listen(PurchasePaymentItem.__table__, 'after_create', proc_get_purchase_payment_item_total_price)


# 가입고품목의 미입고수량 업데이트
proc_update_purchase_prereceiving_item_not_shipped = DDL('''
DROP PROCEDURE IF EXISTS proc_update_purchase_prereceiving_item_not_shipped;
CREATE PROCEDURE `proc_update_purchase_prereceiving_item_not_shipped`(
    IN `prereceivingItemId` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '가입고품목의 미입고수량 업데이트'
BEGIN
    CALL proc_get_purchase_receiving_item_total_quantity_in_prereceiving(prereceivingItemId, @sum);

    UPDATE purchase_prereceiving_item
    SET not_shipped = good_quantity - @sum
    WHERE id = prereceivingItemId;
END
''')
event.listen(PurchasePreReceivingItem.__table__, 'after_create', proc_update_purchase_prereceiving_item_not_shipped)


# 입고품목의 미계산수량 업데이트
proc_update_purchase_receiving_item_non_invoice = DDL('''
DROP PROCEDURE IF EXISTS proc_update_purchase_receiving_item_non_invoice;
CREATE PROCEDURE `proc_update_purchase_receiving_item_non_invoice`(
    IN `receivingItemId` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '입고품목의 미계산수량 업데이트'
BEGIN
    CALL proc_get_purchase_statement_item_total_quantity(receivingItemId, @sum);

    UPDATE purchase_receiving_item
    SET non_invoice = receiving_quantity - @sum
    WHERE id = receivingItemId;
END
''')
event.listen(PurchaseReceivingItem.__table__, 'after_create', proc_update_purchase_receiving_item_non_invoice)


# 입고반품 품목의 미계산수량 업데이트
proc_update_purchase_receiving_return_item_non_invoice = DDL('''
DROP PROCEDURE IF EXISTS proc_update_purchase_receiving_return_item_non_invoice;
CREATE PROCEDURE `proc_update_purchase_receiving_return_item_non_invoice`(
    IN `receivingReturnItemId` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '입고반품 품목의 미계산수량 업데이트'
BEGIN
    CALL proc_get_purchase_statement_item_total_quantity_return(receivingReturnItemId, @sum);

    UPDATE purchase_receiving_return_item
    SET non_invoice = return_quantity - @sum
    WHERE id = receivingReturnItemId;
END
''')
event.listen(PurchaseReceivingReturnItem.__table__, 'after_create', proc_update_purchase_receiving_return_item_non_invoice)


# 매입계산서 미결재 업데이트
proc_update_purchase_statement_not_payment = DDL('''
DROP PROCEDURE IF EXISTS proc_update_purchase_statement_not_payment;
CREATE PROCEDURE `proc_update_purchase_statement_not_payment`(
    IN `statementId` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '매입계산서 미결재 업데이트'
BEGIN
    CALL proc_get_purchase_payment_item_total_price(statementId, @sum);

    UPDATE purchase_statement
    SET not_payment = total_price - @sum
    WHERE id = statementId;
END
''')
event.listen(PurchaseStatement.__table__, 'after_create', proc_update_purchase_statement_not_payment)

# 발주계획품목의 미생산계획수량 업데이트
proc_update_purchase_order_plan_item_not_produce = DDL('''
DROP PROCEDURE IF EXISTS proc_update_purchase_order_plan_item_not_produce;
CREATE PROCEDURE `proc_update_purchase_order_plan_item_not_produce`(
    IN `orderPlanItemId` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '발주계획품목의 미생산계획수량 업데이트'
BEGIN
    CALL proc_get_production_plan_item_total_plan_quantity2(orderPlanItemId, @sum);

    UPDATE purchase_order_plan_item
    SET not_produce_plan_quantity = order_plan_quantity - @sum
    WHERE id = orderPlanItemId;
END
''')
event.listen(PurchaseOrderPlanItem.__table__, 'after_create', proc_update_purchase_order_plan_item_not_produce)


# ----------------------------------------------------------------------------------------------------------------------
# CREATE TRIGGER

# 발주 삭제
before_purchase_order_delete = DDL('''
DROP TRIGGER IF EXISTS before_purchase_order_delete;
CREATE TRIGGER before_purchase_order_delete
BEFORE DELETE ON purchase_order
FOR EACH ROW
BEGIN
    # 발주품목 삭제
    DELETE FROM purchase_order_item WHERE fk_purchase_order_id = OLD.id;
END;''')
event.listen(PurchaseOrder.__table__, 'after_create', before_purchase_order_delete)

# 발주 품목 삭제
after_purchase_order_item_delete = DDL('''
DROP TRIGGER IF EXISTS after_purchase_order_item_delete;
CREATE TRIGGER after_purchase_order_item_delete
AFTER DELETE ON purchase_order_item
FOR EACH ROW
BEGIN
    # 발주계획 미발주수량 업데이트
    IF OLD.fk_order_plan_item_id IS NOT NULL
    THEN
        UPDATE purchase_order_plan_item
        SET unordered_quantity = unordered_quantity + OLD.order_quantity
        WHERE id = OLD.fk_order_plan_item_id;
    END IF;
                                       
    # 실행계획 미발주수량 업데이트
    IF OLD.fk_excution_plan_item_id IS NOT NULL 
    THEN
        UPDATE project_excution_plan_item
        SET not_excution_plan_quantity = 
            CASE 
                WHEN (not_excution_plan_quantity + OLD.order_quantity) <= excution_plan_quantity THEN
                    not_excution_plan_quantity + OLD.order_quantity
                ELSE
                    excution_plan_quantity
            END,
            closing_yn = FALSE
        WHERE id = OLD.fk_excution_plan_item_id;
    END IF;
    # 실행계획 외주공사 업데이트
    IF OLD.fk_excution_plan_subcontract_id IS NOT NULL 
    THEN
        UPDATE project_excution_plan_subcontract
        SET closing_yn = FALSE
        WHERE id = OLD.fk_excution_plan_subcontract_id;
    END IF;
    
END;''')
event.listen(PurchaseOrderItem.__table__, 'after_create', after_purchase_order_item_delete)

# 가입고 삭제
before_purchase_prereceiving_delete = DDL('''
DROP TRIGGER IF EXISTS before_purchase_prereceiving_delete;
CREATE TRIGGER before_purchase_prereceiving_delete
BEFORE DELETE ON purchase_prereceiving
FOR EACH ROW
BEGIN
    # 가입고품목 삭제
    DELETE FROM purchase_prereceiving_item WHERE fk_prereceiving_id = OLD.id;
END;''')
event.listen(PurchasePreReceiving.__table__, 'after_create', before_purchase_prereceiving_delete)

# 가입고 품목 추가
after_purchase_prereceiving_item_insert = DDL('''
DROP TRIGGER IF EXISTS after_purchase_prereceiving_item_insert;
CREATE TRIGGER after_purchase_prereceiving_item_insert
AFTER INSERT ON purchase_prereceiving_item
FOR EACH ROW
BEGIN
    # 발주품목 미입고 업데이트
    IF NEW.fk_order_item_id IS NOT NULL
    THEN
        CALL proc_update_purchase_order_item_not_shipped_to_prereceiving(NEW.fk_order_item_id);
    END IF;
END;''')
event.listen(PurchasePreReceivingItem.__table__, 'after_create', after_purchase_prereceiving_item_insert)

# 가입고 품목 업데이트
after_purchase_prereceiving_item_update = DDL('''
DROP TRIGGER IF EXISTS after_purchase_prereceiving_item_update;
CREATE TRIGGER after_purchase_prereceiving_item_update
AFTER UPDATE ON purchase_prereceiving_item
FOR EACH ROW
BEGIN
    # 발주품목 미입고 업데이트
    IF NEW.fk_order_item_id IS NOT NULL
    THEN
        CALL proc_update_purchase_order_item_not_shipped_to_prereceiving(NEW.fk_order_item_id);
    END IF;
END;''')
event.listen(PurchasePreReceivingItem.__table__, 'after_create', after_purchase_prereceiving_item_update)

# 가입고 품목 삭제
after_purchase_prereceiving_item_delete = DDL('''
DROP TRIGGER IF EXISTS after_purchase_prereceiving_item_delete;
CREATE TRIGGER after_purchase_prereceiving_item_delete
AFTER DELETE ON purchase_prereceiving_item
FOR EACH ROW
BEGIN
    # 발주품목 미입고 업데이트
    IF OLD.fk_order_item_id IS NOT NULL
    THEN
        CALL proc_update_purchase_order_item_not_shipped_to_prereceiving(OLD.fk_order_item_id);
    END IF;
END;''')
event.listen(PurchasePreReceivingItem.__table__, 'after_create', after_purchase_prereceiving_item_delete)

# 입고 삭제
before_purchase_receiving_delete = DDL('''
DROP TRIGGER IF EXISTS before_purchase_receiving_delete;
CREATE TRIGGER before_purchase_receiving_delete
BEFORE DELETE ON purchase_receiving
FOR EACH ROW
BEGIN
    # 입고품목 삭제
    DELETE FROM purchase_receiving_item WHERE fk_receiving_id = OLD.id;
END;''')
event.listen(PurchaseReceiving.__table__, 'after_create', before_purchase_receiving_delete)

# 입고 품목 추가
after_purchase_receiving_item_insert = DDL('''
DROP TRIGGER IF EXISTS after_purchase_receiving_item_insert;
CREATE TRIGGER after_purchase_receiving_item_insert
AFTER INSERT ON purchase_receiving_item
FOR EACH ROW
BEGIN
    # 가입고품목의 미입고수량 업데이트
    IF NEW.fk_prereceiving_item_id IS NOT NULL
    THEN
        CALL proc_update_purchase_prereceiving_item_not_shipped(NEW.fk_prereceiving_item_id);
    # 발주품목의 미입고수량 업데이트                         
    ELSEIF NEW.fk_prereceiving_item_id IS NULL AND NEW.fk_order_item_id IS NOT NULL
    THEN
        CALL proc_update_purchase_order_item_not_shipped_to_receiving(NEW.fk_order_item_id);
    END IF;
    
    # 현재고 업데이트
    # CALL proc_update_current_stock(NEW.item_code, NEW.warehouse_code);
    # 가용재고 업데이트
    # CALL proc_update_available_stock(NEW.item_code, NEW.warehouse_code);
END;''')
event.listen(PurchaseReceivingItem.__table__, 'after_create', after_purchase_receiving_item_insert)

# 입고 품목 업데이트
after_purchase_receiving_item_update = DDL('''
DROP TRIGGER IF EXISTS after_purchase_receiving_item_update;
CREATE TRIGGER after_purchase_receiving_item_update
AFTER UPDATE ON purchase_receiving_item
FOR EACH ROW
BEGIN
    # 가입고품목의 미입고수량 업데이트
    IF NEW.fk_prereceiving_item_id IS NOT NULL
    THEN
        CALL proc_update_purchase_prereceiving_item_not_shipped(NEW.fk_prereceiving_item_id);
    # 발주품목의 미입고수량 업데이트                         
    ELSEIF NEW.fk_prereceiving_item_id IS NULL AND NEW.fk_order_item_id IS NOT NULL
    THEN
        CALL proc_update_purchase_order_item_not_shipped_to_receiving(NEW.fk_order_item_id);
    END IF;                               
    # 현재고 업데이트
    # CALL proc_update_current_stock(NEW.item_code, NEW.warehouse_code);
    # 가용재고 업데이트
    # CALL proc_update_available_stock(NEW.item_code, NEW.warehouse_code);
END;''')
event.listen(PurchaseReceivingItem.__table__, 'after_create', after_purchase_receiving_item_update)

# 입고 품목 삭제
after_purchase_receiving_item_delete = DDL('''
DROP TRIGGER IF EXISTS after_purchase_receiving_item_delete;
CREATE TRIGGER after_purchase_receiving_item_delete
AFTER DELETE ON purchase_receiving_item
FOR EACH ROW
BEGIN
    # 가입고품목의 미입고수량 업데이트
    IF OLD.fk_prereceiving_item_id IS NOT NULL
    THEN
        CALL proc_update_purchase_prereceiving_item_not_shipped(OLD.fk_prereceiving_item_id);
    # 발주품목의 미입고수량 업데이트                         
    ELSEIF OLD.fk_prereceiving_item_id IS NULL AND OLD.fk_order_item_id IS NOT NULL
    THEN
        CALL proc_update_purchase_order_item_not_shipped_to_receiving(OLD.fk_order_item_id);
    END IF;
                                           
    # 현재고, 가용재고 업데이트
    UPDATE setup_basic_stock
    SET current_stock = current_stock - OLD.receiving_quantity, 
        available_stock = available_stock - OLD.receiving_quantity
    WHERE item_code = OLD.item_code AND wh_code = OLD.warehouse_code;
    
    UPDATE setup_basic_stock
    SET available_stock = current_stock
    WHERE item_code = OLD.item_code AND wh_code = OLD.warehouse_code AND available_stock > current_stock;
    
    UPDATE setup_basic_stock
    SET available_stock = 0
    WHERE item_code = OLD.item_code AND wh_code = OLD.warehouse_code AND available_stock < 0;
END;''')
event.listen(PurchaseReceivingItem.__table__, 'after_create', after_purchase_receiving_item_delete)

# 입고반품 삭제
before_purchase_receiving_return_delete = DDL('''
DROP TRIGGER IF EXISTS before_purchase_receiving_return_delete;
CREATE TRIGGER before_purchase_receiving_return_delete
BEFORE DELETE ON purchase_receiving_return
FOR EACH ROW
BEGIN
    # 입고반품품목 삭제
    DELETE FROM purchase_receiving_return_item WHERE fk_receiving_return_id = OLD.id;
END;''')
event.listen(PurchaseReceivingReturn.__table__, 'after_create', before_purchase_receiving_return_delete)

# 매입계산서 삭제
before_purchase_statement_delete = DDL('''
DROP TRIGGER IF EXISTS before_purchase_statement_delete;
CREATE TRIGGER before_purchase_statement_delete
BEFORE DELETE ON purchase_statement
FOR EACH ROW
BEGIN
    # 매입계산서 품목 삭제
    DELETE FROM purchase_statement_item WHERE fk_statement_id = OLD.id;
END;''')
event.listen(PurchaseStatementItem.__table__, 'after_create', before_purchase_statement_delete)

# 매입계산서 품목 추가
after_purchase_statement_item_insert = DDL('''
DROP TRIGGER IF EXISTS after_purchase_statement_item_insert;
CREATE TRIGGER after_purchase_statement_item_insert
AFTER INSERT ON purchase_statement_item
FOR EACH ROW
BEGIN
    # 입고품목의 미계산서수량 업데이트
    IF NEW.fk_receiving_item_id IS NOT NULL
    THEN
        CALL proc_update_purchase_receiving_item_non_invoice(NEW.fk_receiving_item_id);
    END IF;
                                           
    # 입고반품 품목의 미계산서수량 업데이트
    IF NEW.fk_receiving_return_item_id IS NOT NULL
    THEN
        CALL proc_update_purchase_receiving_return_item_non_invoice(NEW.fk_receiving_return_item_id);
    END IF;
    
END;''')
event.listen(PurchaseStatementItem.__table__, 'after_create', after_purchase_statement_item_insert)

# 매입계산서 품목 업데이트
after_purchase_statement_item_update = DDL('''
DROP TRIGGER IF EXISTS after_purchase_statement_item_update;
CREATE TRIGGER after_purchase_statement_item_update
AFTER UPDATE ON purchase_statement_item
FOR EACH ROW
BEGIN
    # 입고품목의 미계산수량 업데이트
    IF NEW.fk_receiving_item_id IS NOT NULL
    THEN
        CALL proc_update_purchase_receiving_item_non_invoice(NEW.fk_receiving_item_id);
    END IF;

    # 입고반품 품목의 미계산서수량 업데이트
    IF NEW.fk_receiving_return_item_id IS NOT NULL
    THEN
        CALL proc_update_purchase_receiving_return_item_non_invoice(NEW.fk_receiving_return_item_id);
    END IF;
                                           
END;''')
event.listen(PurchaseStatementItem.__table__, 'after_create', after_purchase_statement_item_update)

# 매입계산서 품목 삭제
after_purchase_statement_item_delete = DDL('''
DROP TRIGGER IF EXISTS after_purchase_statement_item_delete;
CREATE TRIGGER after_purchase_statement_item_delete
AFTER DELETE ON purchase_statement_item
FOR EACH ROW
BEGIN
    # 입고품목의 미계산서수량 업데이트
    IF OLD.fk_receiving_item_id IS NOT NULL
    THEN
        CALL proc_update_purchase_receiving_item_non_invoice(OLD.fk_receiving_item_id);
    END IF;

    # 입고반품 품목의 미계산서수량 업데이트
    IF OLD.fk_receiving_return_item_id IS NOT NULL
    THEN
        CALL proc_update_purchase_receiving_return_item_non_invoice(OLD.fk_receiving_return_item_id);
    END IF;
                        
END;''')
event.listen(PurchaseStatementItem.__table__, 'after_create', after_purchase_statement_item_delete)

# 결재 삭제
before_purchase_payment_delete = DDL('''
DROP TRIGGER IF EXISTS before_purchase_payment_delete;
CREATE TRIGGER before_purchase_payment_delete
BEFORE DELETE ON purchase_payment
FOR EACH ROW
BEGIN
    # 결재 품목 삭제
    DELETE FROM purchase_payment_item WHERE fk_payment_id = OLD.id;
END;''')
event.listen(PurchasePaymentItem.__table__, 'after_create', before_purchase_payment_delete)

# 결재 품목 추가
after_purchase_payment_item_insert = DDL('''
DROP TRIGGER IF EXISTS after_purchase_payment_item_insert;
CREATE TRIGGER after_purchase_payment_item_insert
AFTER INSERT ON purchase_payment_item
FOR EACH ROW
BEGIN
    # 매입계산서 미결재 업데이트
    IF NEW.fk_statement_id IS NOT NULL
    THEN
        CALL proc_update_purchase_statement_not_payment(NEW.fk_statement_id);
    END IF;
    
END;''')
event.listen(PurchasePaymentItem.__table__, 'after_create', after_purchase_payment_item_insert)

# 결재 품목 업데이트
after_purchase_payment_item_update = DDL('''
DROP TRIGGER IF EXISTS after_purchase_payment_item_update;
CREATE TRIGGER after_purchase_payment_item_update
AFTER UPDATE ON purchase_payment_item
FOR EACH ROW
BEGIN
    # 매입계산서 미결재 업데이트
    IF NEW.fk_statement_id IS NOT NULL
    THEN
        CALL proc_update_purchase_statement_not_payment(NEW.fk_statement_id);
    END IF;                             
END;''')
event.listen(PurchasePaymentItem.__table__, 'after_create', after_purchase_payment_item_update)

# 결재 품목 삭제
after_purchase_payment_item_delete = DDL('''
DROP TRIGGER IF EXISTS after_purchase_payment_item_delete;
CREATE TRIGGER after_purchase_payment_item_delete
AFTER DELETE ON purchase_payment_item
FOR EACH ROW
BEGIN
    # 매입계산서 미결재 업데이트
    IF OLD.fk_statement_id IS NOT NULL
    THEN
        CALL proc_update_purchase_statement_not_payment(OLD.fk_statement_id);
    END IF;                             
END;''')
event.listen(PurchasePaymentItem.__table__, 'after_create', after_purchase_payment_item_delete)
