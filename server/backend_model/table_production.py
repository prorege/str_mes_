# -*- coding: utf-8 -*-

print("module [backend_model.table_production.py] loaded")
from datetime import datetime
from sqlalchemy import DDL, event
from backend_model.database import DBManager
from backend_model.table_base import BaseItem, BaseWarehouse
from backend_model.table_common import Companies
from backend_model.table_shipment import ShipmentOrderItem
from backend_model.table_project import ProjectItem, ProjectManagement
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from backend_model.table_purchase import PurchaseOrderPlan, PurchaseOrderPlanItem


db = DBManager.db


class ProductionPlan(db.Model):  # 생산관리 - 생산계획
    __tablename__ = "production_plan"
    __table_args__ = {"comment": "생산관리(생산계획)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    number = db.Column("number", db.String(48), comment="생산계획번호")
    target_date = db.Column("target_date", db.DateTime, comment="생산계획일자")
    department = db.Column("department", db.String(48), comment="담당부서")
    manager = db.Column("manager", db.String(48), comment="담당자")
    note = db.Column("note", db.String(256), comment="참고사항")
    etc = db.Column("etc", db.Text, comment="비고")
    supply_price = db.Column("supply_price", db.BigInteger, comment="공급가")
    vat = db.Column("vat", db.Integer, comment="부가세")
    total_price = db.Column("total_price", db.BigInteger, comment="합계금액")
    fk_company_id = db.Column("fk_company_id", db.Integer, db.ForeignKey(Companies.id), comment="회사 FK")


class ProductionPlanItem1(db.Model):  # 생산관리 - 생산계획 - 생산계획품목
    __tablename__ = "production_plan_item1"
    __table_args__ = {"comment": "생산계획(생산계획품목)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    item_code = db.Column("item_code", db.String(48), db.ForeignKey(BaseItem.item_code, onupdate="CASCADE"), comment="품목코드")
    production_plan_quantity = db.Column("production_plan_quantity", db.Integer, comment="생산계획수량")
    unit_price = db.Column("unit_price", db.Integer, comment="단가")
    supply_price = db.Column("supply_price", db.BigInteger, comment="공급가")
    request_delivery_date = db.Column("request_delivery_date", db.DateTime, comment="요청납기")
    not_measure_requirement = db.Column("not_measure_requirement", db.Integer, server_default="0", comment="미소요량계산수량")
    unordered_quantity = db.Column("unordered_quantity", db.Integer, comment="미작지수량")
    order_number = db.Column("order_number", db.String(48), comment="수주번호")
    order_date = db.Column("order_date", db.DateTime, comment="수주일자")
    purchase_order_plan_number = db.Column("purchase_order_plan_number", db.String(48), comment="발주계획번호")
    client_company = db.Column("client_company", db.String(48), comment="고객업체")
    client_item_number = db.Column("client_item_number", db.String(48), comment="고객사품번")
    end_user = db.Column("end_user", db.String(48), comment="실수요자")
    warehouse_code = db.Column("warehouse_code", db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment="입고창고")
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate='CASCADE'), comment="프로젝트 FK")
    fk_order_item_id = db.Column("fk_order_item_id", db.Integer, db.ForeignKey(ShipmentOrderItem.id), comment="수주품목 FK")
    fk_purchase_order_plan_id = db.Column("fk_purchase_order_plan_id", db.Integer, db.ForeignKey('purchase_order_plan.id'), comment="발주계획 FK")
    fk_purchase_order_plan_item_id = db.Column("fk_purchase_order_plan_item_id", db.Integer, db.ForeignKey('purchase_order_plan_item.id'), comment="발주계획품목 FK")
    fk_production_plan_id = db.Column("fk_production_plan_id", db.Integer, db.ForeignKey(ProductionPlan.id), comment="생산계획 FK")
    project_management = db.relationship('ProjectManagement', foreign_keys=[fk_project_management_id])
    production_plan = db.relationship("ProductionPlan", foreign_keys=[fk_production_plan_id])
    item = db.relationship("BaseItem", foreign_keys=[item_code])
    warehouse = db.relationship("BaseWarehouse", foreign_keys=[warehouse_code])
    order_item = db.relationship("ShipmentOrderItem", foreign_keys=[fk_order_item_id])
    purchase_order_plan = db.relationship("PurchaseOrderPlan", foreign_keys=[fk_purchase_order_plan_id])
    purchase_order_plan_item = db.relationship("PurchaseOrderPlanItem", foreign_keys=[fk_purchase_order_plan_item_id])
    basic_stock = db.relationship("SetupBasicStock", viewonly=True,
        primaryjoin="and_(foreign(ProductionPlanItem1.item_code) == SetupBasicStock.item_code,"
        "foreign(ProductionPlanItem1.warehouse_code) == SetupBasicStock.wh_code)",
    )


class WorkOrder(db.Model):  # 생산관리 - 작업지시
    __tablename__ = "work_order"
    __table_args__ = {"comment": "생산관리(작업지시)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    number = db.Column("number", db.String(48), comment="작업지시번호")
    target_date = db.Column("target_date", db.DateTime, comment="작지일자")
    department = db.Column("department", db.String(48), comment="담당부서")
    manager = db.Column("manager", db.String(48), comment="담당자")
    note = db.Column("note", db.String(256), comment="참고사항")
    etc = db.Column("etc", db.Text, comment="비고")
    stock_move_request_number = db.Column("stock_move_request_number", db.String(48), comment="이동요청번호")
    closing_yn = db.Column("closing_yn", db.Boolean, default=0, comment="종결여부")
    fk_company_id = db.Column("fk_company_id", db.Integer, db.ForeignKey(Companies.id), comment="회사 FK")
    
ProjectItem.work_order = db.relationship('WorkOrder', viewonly=True, primaryjoin='foreign(ProjectItem.fk_work_order_id) == WorkOrder.id')

class WorkOrderItem1(db.Model):  # 생산관리 - 작업지시 - 작업지시
    __tablename__ = "work_order_item1"
    __table_args__ = {"comment": "작업지시(작업지시품목)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    item_code = db.Column("item_code", db.String(48), db.ForeignKey(BaseItem.item_code, onupdate="CASCADE"), comment="품목코드")
    required_quantity = db.Column("required_quantity", db.Integer, server_default="0", comment="작업지시수량")
    bom_yn = db.Column("bom_yn", db.Boolean, server_default="0", comment="BOM여부")
    production_plan_number = db.Column("production_plan_number", db.String(48), comment="생산계획번호")
    request_delivery_date = db.Column("request_delivery_date", db.DateTime, comment="요청납기")
    unproduced_quantity = db.Column("unproduced_quantity", db.Integer, server_default="0", comment="미생산수량")
    order_number = db.Column("order_number", db.String(48), comment="수주번호")
    client_company = db.Column("client_company", db.String(48), comment="고객업체")
    client_item_number = db.Column("client_item_number", db.String(48), comment="고객사품번")
    end_user = db.Column("end_user", db.String(48), comment="실수요자")
    end_yn = db.Column("end_yn", db.Boolean, server_default="0", comment="종료")
    warehouse_code = db.Column("warehouse_code", db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment="입고창고")
    fk_plan_item_id = db.Column("fk_plan_item_id", db.Integer, db.ForeignKey(ProductionPlanItem1.id), comment="생산계획품목 FK")
    fk_project_item_id = db.Column('fk_project_item_id', db.Integer, db.ForeignKey(ProjectItem.id), comment="프로젝트아이템 FK")
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id), comment="프로젝트 FK")
    fk_work_order_id = db.Column("fk_work_order_id", db.Integer, db.ForeignKey(WorkOrder.id, onupdate="CASCADE", ondelete="CASCADE"), comment="작업지시 FK")
    item = db.relationship("BaseItem", foreign_keys=[item_code])
    warehouse = db.relationship("BaseWarehouse", foreign_keys=[warehouse_code])
    work_order = db.relationship("WorkOrder", foreign_keys=[fk_work_order_id])
    plan_item = db.relationship("ProductionPlanItem1", foreign_keys=[fk_plan_item_id])
    project_item = db.relationship("ProjectItem", foreign_keys=[fk_project_item_id])
    project_management = db.relationship("ProjectManagement", foreign_keys=[fk_project_management_id])
    order = db.relationship("ShipmentOrder", viewonly=True, primaryjoin="foreign(WorkOrderItem1.order_number) == ShipmentOrder.order_number")
    basic_stock = db.relationship("SetupBasicStock", viewonly=True,
        primaryjoin="and_(foreign(WorkOrderItem1.item_code) == SetupBasicStock.item_code,"
        "foreign(WorkOrderItem1.warehouse_code) == SetupBasicStock.wh_code)",
    )


class WorkOrderItem2(db.Model):  # 생산관리 - 작업지시 - 필요자재
    __tablename__ = "work_order_item2"
    __table_args__ = {"comment": "작업지시(필요자재)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    item_code = db.Column("item_code", db.String(48), db.ForeignKey(BaseItem.item_code, onupdate="CASCADE"), comment="품목코드")
    required_quantity = db.Column("required_quantity", db.Numeric(10, 2), server_default="0", comment="필요수량")
    delivery_request_quantity = db.Column("delivery_request_quantity", db.Numeric(10, 2), server_default="0", comment="출고요청수량")
    request_delivery_date = db.Column("request_delivery_date", db.DateTime, comment="요청납기")
    uninput_quantity = db.Column("uninput_quantity", db.Integer, server_default="0", comment="미출고수량")
    client_company = db.Column("client_company", db.String(48), comment="주공급업체")
    warehouse_code = db.Column("warehouse_code", db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment="출고창고")
    in_warehouse_code = db.Column("in_warehouse_code", db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment="입고창고")
    fk_work_order_id = db.Column("fk_work_order_id", db.Integer, db.ForeignKey(WorkOrder.id, onupdate="CASCADE", ondelete="CASCADE"), comment="작업지시 FK")
    item = db.relationship("BaseItem", foreign_keys=[item_code])
    warehouse = db.relationship("BaseWarehouse", foreign_keys=[warehouse_code])
    in_warehouse = db.relationship("BaseWarehouse", foreign_keys=[in_warehouse_code])
    work_order = db.relationship("WorkOrder", foreign_keys=[fk_work_order_id])
    basic_stock = db.relationship("SetupBasicStock", viewonly=True,
        primaryjoin="and_(foreign(WorkOrderItem2.item_code) == SetupBasicStock.item_code,"
        "foreign(WorkOrderItem2.warehouse_code) == SetupBasicStock.wh_code)",
    )


class MeasureRequirement(db.Model):  # 생산관리 - 소요량계산
    __tablename__ = "measure_requirement"
    __table_args__ = {"comment": "생산관리(소요량계산)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    number = db.Column("number", db.String(48), comment="생산계획번호")
    target_date = db.Column("target_date", db.DateTime, comment="생산계획일자")
    department = db.Column("department", db.String(48), comment="담당부서")
    manager = db.Column("manager", db.String(48), comment="담당자")
    note = db.Column("note", db.String(256), comment="참고사항")
    etc = db.Column("etc", db.Text, comment="비고")
    supply_price = db.Column("supply_price", db.BigInteger, comment="공급가")
    vat = db.Column("vat", db.Integer, comment="부가세")
    total_price = db.Column("total_price", db.BigInteger, comment="합계금액")
    purchase_order_plan_number = db.Column("purchase_order_plan_number", db.String(48), comment="발주계획번호")
    closing_yn = db.Column("closing_yn", db.Boolean, default=0, comment="종결여부")
    fk_company_id = db.Column("fk_company_id", db.Integer, db.ForeignKey(Companies.id), comment="회사 FK")


class MeasureRequirementItem1(db.Model):  # 생산관리 - 소요량계산 - 생산계획품목
    __tablename__ = "measure_requirement_item1"
    __table_args__ = {"comment": "소요량계산(소요량등록품목)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    item_code = db.Column("item_code", db.String(48), db.ForeignKey(BaseItem.item_code, onupdate="CASCADE"), comment="품목코드")
    production_plan_quantity = db.Column("production_plan_quantity", db.Integer, comment="생산계획수량")
    unit_price = db.Column("unit_price", db.Integer, comment="단가")
    supply_price = db.Column("supply_price", db.BigInteger, comment="공급가")
    request_delivery_date = db.Column("request_delivery_date", db.DateTime, comment="요청납기")
    unordered_quantity = db.Column("unordered_quantity", db.Integer, comment="미작지수량")
    order_number = db.Column("order_number", db.String(48), comment="수주번호")
    order_date = db.Column("order_date", db.DateTime, comment="수주일자")
    purchase_order_plan_number = db.Column("purchase_order_plan_number", db.String(48), comment="발주계획번호")
    client_company = db.Column("client_company", db.String(48), comment="고객업체")
    client_item_number = db.Column("client_item_number", db.String(48), comment="고객사품번")
    end_user = db.Column("end_user", db.String(48), comment="실수요자")
    warehouse_code = db.Column("warehouse_code", db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment="입고창고")
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate='CASCADE'), comment="프로젝트 FK")
    fk_plan_item_id = db.Column("fk_plan_item_id", db.Integer, db.ForeignKey(ProductionPlanItem1.id), comment="생산계획품목 FK")
    fk_work_order_item_id = db.Column("fk_work_order_item_id", db.Integer, db.ForeignKey(WorkOrderItem1.id), comment="작업지시품목 FK")
    fk_measure_requirement_id = db.Column("fk_measure_requirement_id", db.Integer, db.ForeignKey(MeasureRequirement.id), comment="소요량계산 FK")
    project_management = db.relationship('ProjectManagement', foreign_keys=[fk_project_management_id])
    item = db.relationship("BaseItem", foreign_keys=[item_code])
    warehouse = db.relationship("BaseWarehouse", foreign_keys=[warehouse_code])
    plan_item = db.relationship("ProductionPlanItem1", foreign_keys=[fk_plan_item_id])
    work_order_item = db.relationship("WorkOrderItem1", foreign_keys=[fk_work_order_item_id])
    measure_requirement = db.relationship("MeasureRequirement", foreign_keys=[fk_measure_requirement_id])
    basic_stock = db.relationship("SetupBasicStock", viewonly=True,
        primaryjoin="and_(foreign(MeasureRequirementItem1.item_code) == SetupBasicStock.item_code,"
        "foreign(MeasureRequirementItem1.warehouse_code) == SetupBasicStock.wh_code)",
    )


class MeasureRequirementItem2(db.Model):  # 생산관리 - 소요량계산 - 소요량계산품목
    __tablename__ = "measure_requirement_item2"
    __table_args__ = {"comment": "소요량계산(소요량계산품목)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    item_code = db.Column("item_code", db.String(48), db.ForeignKey(BaseItem.item_code, onupdate="CASCADE"), comment="품목코드")
    requirement_quantity = db.Column("requirement_quantity", db.Numeric(12, 2), comment="소요량")
    order_plan_quantity = db.Column("order_plan_quantity", db.Integer, comment="발주계획량")
    unordered_plan_quantity = db.Column("unordered_plan_quantity", db.Integer, comment="미발주계획수량")
    unit_price = db.Column("unit_price", db.Numeric(10, 2), comment="단가")
    supply_price = db.Column("supply_price", db.BigInteger, comment="공급가")
    client_company = db.Column("client_company", db.String(48), comment="공급업체")
    delivery_date = db.Column("delivery_date", db.DateTime, comment="납기일자")
    order_number = db.Column("order_number", db.String(48), comment="수주번호")
    end_user = db.Column("end_user", db.String(48), comment="실수요자")
    warehouse_code = db.Column("warehouse_code", db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment="입고창고")
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate='CASCADE'), comment="프로젝트 FK")
    fk_measure_requirement_id = db.Column("fk_measure_requirement_id", db.Integer, db.ForeignKey(MeasureRequirement.id), comment="소요량계산 FK")
    project_management = db.relationship('ProjectManagement', foreign_keys=[fk_project_management_id])
    item = db.relationship("BaseItem", foreign_keys=[item_code])
    warehouse = db.relationship("BaseWarehouse", foreign_keys=[warehouse_code])
    measure_requirement = db.relationship("MeasureRequirement", foreign_keys=[fk_measure_requirement_id])
    basic_stock = db.relationship("SetupBasicStock", viewonly=True,
        primaryjoin="and_(foreign(MeasureRequirementItem2.item_code) == SetupBasicStock.item_code,"
        "foreign(MeasureRequirementItem2.warehouse_code) == SetupBasicStock.wh_code)",
    )


class PerformanceRegistration(db.Model):  # 생산관리 - 생산입고
    __tablename__ = "performance_registration"
    __table_args__ = {"comment": "생산관리(생산입고)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    number = db.Column("number", db.String(48), comment="생산입고번호")
    target_date = db.Column("target_date", db.DateTime, comment="생산일자")
    department = db.Column("department", db.String(48), comment="담당부서")
    manager = db.Column("manager", db.String(48), comment="담당자")
    note = db.Column("note", db.String(256), comment="참고사항")
    etc = db.Column("etc", db.Text, comment="비고")
    closing_yn = db.Column("closing_yn", db.Boolean, default=0, comment="종결여부")
    fk_company_id = db.Column("fk_company_id", db.Integer, db.ForeignKey(Companies.id), comment="회사 FK")


class PerformanceRegistrationItem1(db.Model):  # 생산관리 - 생산입고 - 생산입고
    __tablename__ = "performance_registration_item1"
    __table_args__ = {"comment": "생산입고(생산입고품목)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    item_code = db.Column("item_code", db.String(48), db.ForeignKey(BaseItem.item_code, onupdate="CASCADE"), comment="품목코드")
    work_order_quantity = db.Column("work_order_quantity", db.Integer, server_default="0", comment="작업지시수량")
    production_receiving_quantity = db.Column("production_receiving_quantity", db.Integer, server_default="0", comment="생산입고수량")
    check_quantity = db.Column("check_quantity", db.Integer, server_default="0", comment="검수수량")
    bad_quantity = db.Column("bad_quantity", db.Integer, server_default="0", comment="불량수량")
    action_quantity = db.Column("action_quantity", db.Integer, server_default="0", comment="재작업수량")
    good_quantity = db.Column("good_quantity", db.Integer, server_default="0", comment="양품수량")
    unit_price = db.Column("unit_price", db.Numeric(10, 2), server_default="0", comment="단가")
    check_yn = db.Column("check_yn", db.Boolean, server_default="0", comment="검수완료")
    work_order_number = db.Column("work_order_number", db.String(48), comment="작지번호")
    request_delivery_date = db.Column("request_delivery_date", db.DateTime, comment="요청납기")
    order_number = db.Column("order_number", db.String(48), comment="수주번호")
    lot = db.Column("lot", db.String(48), comment="생산주차")
    client_company = db.Column("client_company", db.String(48), comment="고객업체")
    client_item_number = db.Column("client_item_number", db.String(48), comment="고객사품번")
    end_user = db.Column("end_user", db.String(48), comment="실수요자")
    warehouse_code = db.Column("warehouse_code", db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment="입고창고")
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate='CASCADE'), comment="프로젝트 FK")
    fk_performance_registration_id = db.Column("fk_performance_registration_id", db.Integer, db.ForeignKey(PerformanceRegistration.id, onupdate="CASCADE"), comment="생산입고 FK")
    fk_work_order_item = db.Column("fk_work_order_item", db.Integer, db.ForeignKey(WorkOrderItem1.id), comment="작업지시품목 FK")
    project_management = db.relationship('ProjectManagement', foreign_keys=[fk_project_management_id])
    item = db.relationship("BaseItem", foreign_keys=[item_code])
    warehouse = db.relationship("BaseWarehouse", foreign_keys=[warehouse_code])
    work_order_item = db.relationship("WorkOrderItem1", foreign_keys=[fk_work_order_item])
    performance_registration = db.relationship("PerformanceRegistration", foreign_keys=[fk_performance_registration_id])
    order = db.relationship("ShipmentOrder", viewonly=True, primaryjoin="foreign(PerformanceRegistrationItem1.order_number) == ShipmentOrder.order_number")
    work_order = db.relationship("WorkOrder", viewonly=True, primaryjoin="foreign(PerformanceRegistrationItem1.work_order_number) == WorkOrder.number")
    basic_stock = db.relationship("SetupBasicStock", viewonly=True,
        primaryjoin="and_(foreign(PerformanceRegistrationItem1.item_code) == SetupBasicStock.item_code,"
        "foreign(PerformanceRegistrationItem1.warehouse_code) == SetupBasicStock.wh_code)",
    )


class PerformanceRegistrationItem2(db.Model):  # 생산관리 - 생산입고 - 자재소모
    __tablename__ = "performance_registration_item2"
    __table_args__ = {"comment": "생산입고(자재소모)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    item_code = db.Column("item_code", db.String(48), db.ForeignKey(BaseItem.item_code, onupdate="CASCADE"), comment="품목코드")
    material_quantity = db.Column("material_quantity", db.Integer, server_default="0", comment="자재소모수량")
    cost_price = db.Column("cost_price", db.Numeric(10, 2), server_default="0", comment="원가")
    total_cost_price = db.Column("total_cost_price", db.Numeric(20, 4), server_default="0", comment="원가합계")
    warehouse_code = db.Column("warehouse_code", db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment="자재소모창고")
    fk_performance_registration_id = db.Column("fk_performance_registration_id", db.Integer, db.ForeignKey(PerformanceRegistration.id, onupdate="CASCADE"), comment="생산입고 FK")
    item = db.relationship("BaseItem", foreign_keys=[item_code])
    warehouse = db.relationship("BaseWarehouse", foreign_keys=[warehouse_code])
    performance_registration = db.relationship("PerformanceRegistration", foreign_keys=[fk_performance_registration_id])
    basic_stock = db.relationship("SetupBasicStock", viewonly=True,
        primaryjoin="and_(foreign(PerformanceRegistrationItem2.item_code) == SetupBasicStock.item_code,"
        "foreign(PerformanceRegistrationItem2.warehouse_code) == SetupBasicStock.wh_code)",
    )


class ProcessPerformanceRegistration(db.Model):  # 생산관리 - 공정실적등록
    __tablename__ = "process_performance_registration"
    __table_args__ = {"comment": "공정실적등록(공정실적등록품목)"}
    number = db.Column("number", db.String(48), primary_key=True, comment="실적번호")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    item_code = db.Column("item_code", db.String(48), db.ForeignKey(BaseItem.item_code, onupdate="CASCADE"), comment="품목코드")
    worker = db.Column("worker", db.String(48), comment="작업자")
    process_tag = db.Column("process_tag", db.String(20), comment="생산주차")
    process_quantity = db.Column("process_quantity", db.Integer, comment="작업수량")
    bad_quantity = db.Column("bad_quantity", db.Integer, comment="불량수량")
    work_start_time = db.Column("work_start_time", db.String(6), comment="작업시작시간")
    work_end_time = db.Column("work_end_time", db.String(6), comment="작업종료시간")
    work_rest_time = db.Column("work_rest_time", db.String(6), comment="작업휴게시간")
    order_number = db.Column("order_number", db.String(48), comment="작업지시번호")
    fk_project_management_id = db.Column('fk_project_management_id', db.Integer, db.ForeignKey(ProjectManagement.id, onupdate='CASCADE'), comment="프로젝트 FK")
    fk_process_id = db.Column("fk_process_id", db.Integer, db.ForeignKey("base_process.id"), comment="공정관리 ID FK")
    fk_work_order_item = db.Column("fk_work_order_item", db.Integer, db.ForeignKey(WorkOrderItem1.id), comment="작업지시품목 FK")
    fk_company_id = db.Column("fk_company_id", db.Integer, db.ForeignKey(Companies.id), comment="회사 FK")
    project_management = db.relationship('ProjectManagement', foreign_keys=[fk_project_management_id])
    item = db.relationship("BaseItem", foreign_keys=[item_code])
    work_order_item = db.relationship("WorkOrderItem1", foreign_keys=[fk_work_order_item])
    process = db.relationship("BaseProcess", foreign_keys=[fk_process_id])
    work_order = db.relationship("WorkOrder", foreign_keys=[order_number], viewonly=True, primaryjoin="ProcessPerformanceRegistration.order_number == WorkOrder.number")


class ProcessMaterialConsumption(db.Model):  # 생산관리 - 자재소모등록
    __tablename__ = "process_material_consumption"
    __table_args__ = {"comment": "공정실적등록(공정실적품목자재)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    lot_number = db.Column("lot_number", db.String(48), nullable=False, comment="자재LOT번호")
    item_code = db.Column("item_code", db.String(48), db.ForeignKey(BaseItem.item_code, onupdate="CASCADE"), nullable=False, comment="품목코드")
    quantity = db.Column("quantity", db.Numeric(10, 2), default=0, comment="투입수량")
    process_number = db.Column("process_number", db.String(48), db.ForeignKey(ProcessPerformanceRegistration.number, onupdate="CASCADE"), nullable=False, comment="생산실적번호")
    item = db.relationship("BaseItem", foreign_keys=[item_code])
    process_performance_registration = db.relationship("ProcessPerformanceRegistration", foreign_keys=[process_number])


# ----------------------------------------------------------------------------------------------------------------------
# CREATE STORED PROCEDURE

# 생산계획의 생산계획수량 합계 가져오기
proc_get_production_plan_item_total_plan_quantity = DDL(
    """
DROP PROCEDURE IF EXISTS proc_get_production_plan_item_total_plan_quantity;
CREATE PROCEDURE `proc_get_production_plan_item_total_plan_quantity`(
    IN `orderItemId` INT,
    OUT `quantity` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '생산계획의 생산계획수량 합계 가져오기'
BEGIN
    SET quantity = (SELECT SUM(production_plan_quantity)
                    FROM production_plan_item1
                    WHERE fk_order_item_id = orderItemId
                    GROUP BY fk_order_item_id);
    IF quantity IS NULL THEN
        SET quantity = 0;
    ENd IF;
END
"""
)
event.listen(
    ProductionPlanItem1.__table__,
    "after_create",
    proc_get_production_plan_item_total_plan_quantity,
)

proc_get_production_plan_item_total_plan_quantity2 = DDL(
    """
DROP PROCEDURE IF EXISTS proc_get_production_plan_item_total_plan_quantity2;
CREATE PROCEDURE `proc_get_production_plan_item_total_plan_quantity2`(
    IN `purchaseOrderPlanItemId` INT,
    OUT `quantity` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '생산계획의 생산계획수량 합계 가져오기'
BEGIN
    SET quantity = (SELECT SUM(production_plan_quantity)
                    FROM production_plan_item1
                    WHERE fk_purchase_order_plan_item_id = purchaseOrderPlanItemId
                    GROUP BY fk_purchase_order_plan_item_id);
    IF quantity IS NULL THEN
        SET quantity = 0;
    ENd IF;
END
"""
)
event.listen(ProductionPlanItem1.__table__, "after_create", proc_get_production_plan_item_total_plan_quantity2)

# 소요량계산의 생산계획수량 합계 가져오기
proc_get_measure_requirement_item1_total_plan_quantity = DDL(
    """
DROP PROCEDURE IF EXISTS proc_get_measure_requirement_item1_total_plan_quantity;
CREATE PROCEDURE `proc_get_measure_requirement_item1_total_plan_quantity`(
    IN `planItemId` INT,
    OUT `quantity` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '소요량계산의 생산계획수량 합계 가져오기'
BEGIN
    SET quantity = (SELECT SUM(production_plan_quantity)
                    FROM measure_requirement_item1
                    WHERE fk_plan_item_id = planItemId
                    GROUP BY fk_plan_item_id);
    IF quantity IS NULL THEN
        SET quantity = 0;
    ENd IF;
END
"""
)
event.listen(
    MeasureRequirementItem1.__table__,
    "after_create",
    proc_get_measure_requirement_item1_total_plan_quantity,
)

# 작업지시품목의 작업지시수량 합계 가져오기
proc_get_work_order_item1_total_required_quantity = DDL(
    """
DROP PROCEDURE IF EXISTS proc_get_work_order_item1_total_required_quantity;
CREATE PROCEDURE `proc_get_work_order_item1_total_required_quantity`(
    IN `planItemId` INT,
    OUT `sumRequired` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '작업지시품목의 작업지시수량 합계 가져오기'
BEGIN
    SET sumRequired = (SELECT SUM(required_quantity)
                       FROM work_order_item1
                       WHERE fk_plan_item_id = planItemId
                       GROUP BY fk_plan_item_id);
    IF sumRequired IS NULL THEN
        SET sumRequired = 0;
    ENd IF;
END
"""
)
event.listen(
    WorkOrderItem1.__table__,
    "after_create",
    proc_get_work_order_item1_total_required_quantity,
)

# 생산계획 품목 미소요량계산 수량 업데이트
proc_update_production_plan_item_not_mea_req_quantity = DDL(
    """
DROP PROCEDURE IF EXISTS proc_update_production_plan_item_not_mea_req_quantity;
CREATE PROCEDURE `proc_update_production_plan_item_not_mea_req_quantity`(
    IN `planItemId` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '생산계획 품목 미소요량계산 수량 업데이트'
BEGIN
    CALL proc_get_measure_requirement_item1_total_plan_quantity(planItemId, @quantity);

    UPDATE production_plan_item1
    SET not_measure_requirement = production_plan_quantity - @quantity
    WHERE id = planItemId;
END
"""
)
event.listen(
    ProductionPlanItem1.__table__,
    "after_create",
    proc_update_production_plan_item_not_mea_req_quantity,
)

# 작업지시품목의 미생산수량 업데이트
proc_update_work_order_item1_unproduced_quantity = DDL(
    """
DROP PROCEDURE IF EXISTS proc_update_work_order_item1_unproduced_quantity;
CREATE PROCEDURE `proc_update_work_order_item1_unproduced_quantity`(
    IN `work_order_item1_id` INT
)
LANGUAGE SQL
NOT DETERMINISTIC
CONTAINS SQL
SQL SECURITY DEFINER
COMMENT '작업지시품목의 미생산수량을 업데이트한다'
BEGIN
    DECLARE produce_quantity INT;
    DECLARE total_quantity INT;
    DECLARE unproduce_quantity INT;
    
    SELECT SUM(production_receiving_quantity) INTO produce_quantity
    FROM performance_registration_item1
    WHERE fk_work_order_item = work_order_item1_id
    GROUP BY fk_work_order_item;
    
    SELECT required_quantity INTO total_quantity
    FROM work_order_item1
    WHERE id = work_order_item1_id
    LIMIT 1;
    
    IF produce_quantity IS NULL THEN
        SET produce_quantity = 0;
    END IF;
    
    SET unproduce_quantity = total_quantity - produce_quantity;
    IF unproduce_quantity < 0 THEN
        SET unproduce_quantity = 0;
    END IF;
    
    UPDATE work_order_item1
    SET unproduced_quantity = unproduce_quantity
    WHERE id = work_order_item1_id;
END
"""
)
event.listen(
    PerformanceRegistrationItem1.__table__,
    "after_create",
    proc_update_work_order_item1_unproduced_quantity,
)


# ----------------------------------------------------------------------------------------------------------------------
# CREATE TRIGGER

# 생산계획 삭제 시 품목 삭제
before_production_plan_delete = DDL(
    """
CREATE TRIGGER before_production_plan_delete 
BEFORE DELETE ON production_plan
FOR EACH ROW
BEGIN
    DELETE FROM production_plan_item1 WHERE fk_production_plan_id = OLD.id;
END;"""
)
event.listen(ProductionPlan.__table__, "after_create", before_production_plan_delete)

# 생산계획 품목 추가
after_production_plan_item_insert = DDL(
    """
DROP TRIGGER IF EXISTS after_production_plan_item_insert;
CREATE TRIGGER after_production_plan_item_insert
AFTER INSERT ON production_plan_item1
FOR EACH ROW
BEGIN
    # 수주품목 생산계획미처리수량 업데이트
    IF NEW.fk_order_item_id IS NOT NULL
    THEN
        CALL proc_update_shipment_order_item_not_production_plan_quantity(NEW.fk_order_item_id);
    END IF;
    
    # 발주계획 미생산계획수량 업데이트
    IF NEW.fk_purchase_order_plan_item_id IS NOT NULL
    THEN
        CALL proc_update_purchase_order_plan_item_not_produce(NEW.fk_purchase_order_plan_item_id);
    END IF;
END;"""
)
event.listen(
    ProductionPlanItem1.__table__, "after_create", after_production_plan_item_insert
)

# 생산계획 품목 업데이트
after_production_plan_item_update = DDL(
    """
DROP TRIGGER IF EXISTS after_production_plan_item_update;
CREATE TRIGGER after_production_plan_item_update
AFTER UPDATE ON production_plan_item1
FOR EACH ROW
BEGIN
    # 수주품목 생산계획미처리수량 업데이트
    IF NEW.fk_order_item_id IS NOT NULL
    THEN
        CALL proc_update_shipment_order_item_not_production_plan_quantity(NEW.fk_order_item_id);
    END IF;
    
    # 발주계획 미생산계획수량 업데이트
    IF NEW.fk_purchase_order_plan_item_id IS NOT NULL
    THEN
        CALL proc_update_purchase_order_plan_item_not_produce(NEW.fk_purchase_order_plan_item_id);
    END IF;
END;"""
)
event.listen(
    ProductionPlanItem1.__table__, "after_create", after_production_plan_item_update
)

# 생산계획 품목 삭제
after_production_plan_item_delete = DDL(
    """
DROP TRIGGER IF EXISTS after_production_plan_item_delete;
CREATE TRIGGER after_production_plan_item_delete
AFTER DELETE ON production_plan_item1
FOR EACH ROW
BEGIN
    # 수주품목 생산계획미처리수량 업데이트
    IF OLD.fk_order_item_id IS NOT NULL
    THEN
        CALL proc_update_shipment_order_item_not_production_plan_quantity(OLD.fk_order_item_id);
    END IF;
    
    # 발주계획 미생산계획수량 업데이트
    IF OLD.fk_purchase_order_plan_item_id IS NOT NULL
    THEN
        CALL proc_update_purchase_order_plan_item_not_produce(OLD.fk_purchase_order_plan_item_id);
    END IF;
END;"""
)
event.listen(
    ProductionPlanItem1.__table__, "after_create", after_production_plan_item_delete
)

# 소요량계산 삭제 시 품목 삭제
before_measure_requirement_delete = DDL(
    """
CREATE TRIGGER before_measure_requirement_delete 
BEFORE DELETE ON measure_requirement
FOR EACH ROW
BEGIN
    DELETE FROM measure_requirement_item1 WHERE fk_measure_requirement_id = OLD.id;
    DELETE FROM measure_requirement_item2 WHERE fk_measure_requirement_id = OLD.id;
END;"""
)
event.listen(
    MeasureRequirement.__table__, "after_create", before_measure_requirement_delete
)

# 소요량계산 품목1 추가
after_measure_requirement_item_insert = DDL(
    """
DROP TRIGGER IF EXISTS after_measure_requirement_item_insert;
CREATE TRIGGER after_measure_requirement_item_insert
AFTER INSERT ON measure_requirement_item1
FOR EACH ROW
BEGIN
    # 생산계획품목 미소요량계산 수량 업데이트
    IF NEW.fk_plan_item_id IS NOT NULL
    THEN
        CALL proc_update_production_plan_item_not_mea_req_quantity(NEW.fk_plan_item_id);
    END IF;
END;"""
)
event.listen(
    MeasureRequirementItem1.__table__,
    "after_create",
    after_measure_requirement_item_insert,
)

# 소요량계산 품목1 업데이트
after_measure_requirement_item_update = DDL(
    """
DROP TRIGGER IF EXISTS after_measure_requirement_item_update;
CREATE TRIGGER after_measure_requirement_item_update
AFTER UPDATE ON measure_requirement_item1
FOR EACH ROW
BEGIN
    # 생산계획품목 미소요량계산 수량 업데이트
    IF NEW.fk_plan_item_id IS NOT NULL
    THEN
        CALL proc_update_production_plan_item_not_mea_req_quantity(NEW.fk_plan_item_id);
    END IF;
END;"""
)
event.listen(
    MeasureRequirementItem1.__table__,
    "after_create",
    after_measure_requirement_item_update,
)

# 소요량계산 품목1 삭제
after_measure_requirement_item_delete = DDL(
    """
DROP TRIGGER IF EXISTS after_measure_requirement_item_delete;
CREATE TRIGGER after_measure_requirement_item_delete
AFTER DELETE ON measure_requirement_item1
FOR EACH ROW
BEGIN
    # 생산계획품목 미소요량계산 수량 업데이트
    IF OLD.fk_plan_item_id IS NOT NULL
    THEN
        CALL proc_update_production_plan_item_not_mea_req_quantity(OLD.fk_plan_item_id);
    END IF;
END;"""
)
event.listen(
    MeasureRequirementItem1.__table__,
    "after_create",
    after_measure_requirement_item_delete,
)

# 작업지시 삭제
before_work_order_delete = DDL(
    """
CREATE TRIGGER before_work_order_delete 
BEFORE DELETE ON work_order
FOR EACH ROW
BEGIN
    # 작업지시품목1 삭제
    DELETE FROM work_order_item2 WHERE fk_work_order_id = OLD.id;
    # 작업지시품목2 삭제
    DELETE FROM work_order_item1 WHERE fk_work_order_id = OLD.id;
END;"""
)
event.listen(WorkOrder.__table__, "after_create", before_work_order_delete)

# 작업지시품목1 업데이트
after_work_order_item1_update = DDL(
    """
CREATE TRIGGER after_work_order_item1_update
AFTER UPDATE ON work_order_item1
FOR EACH ROW
BEGIN
    # 생산계획 미작지수량 업데이트
    IF OLD.fk_plan_item_id IS NOT NULL THEN
        CALL proc_get_work_order_item1_total_required_quantity(OLD.fk_plan_item_id, @sumRequired);

        UPDATE production_plan_item1
        SET unordered_quantity = production_plan_quantity - @sumRequired
        WHERE id = OLD.fk_plan_item_id;
    END IF;
END;"""
)
event.listen(WorkOrderItem1.__table__, "after_create", after_work_order_item1_update)

# 작업지시품목1 삭제
after_work_order_item1_delete = DDL(
    """
CREATE TRIGGER after_work_order_item1_delete 
AFTER DELETE ON work_order_item1
FOR EACH ROW
BEGIN
    # 생산계획 미작지수량 업데이트
    IF OLD.fk_plan_item_id IS NOT NULL THEN
        CALL proc_get_work_order_item1_total_required_quantity(OLD.fk_plan_item_id, @sumRequired);

        UPDATE production_plan_item1
        SET unordered_quantity = production_plan_quantity - @sumRequired
        WHERE id = OLD.fk_plan_item_id;
    END IF;

    IF OLD.fk_project_item_id IS NOT NULL THEN
        UPDATE project_item
        SET fk_work_order_id = NULL
        WHERE id = OLD.fk_project_item_id;
    END IF;
END;"""
)
event.listen(WorkOrderItem1.__table__, "after_create", after_work_order_item1_delete)

# 생산입고 삭제 시 품목 삭제
before_performance_registration_delete = DDL(
    """
DROP TRIGGER IF EXISTS before_performance_registration_delete;
CREATE TRIGGER before_performance_registration_delete 
BEFORE DELETE ON performance_registration
FOR EACH ROW
BEGIN
    DELETE FROM performance_registration_item1 WHERE fk_performance_registration_id = OLD.id;
    DELETE FROM performance_registration_item2 WHERE fk_performance_registration_id = OLD.id;
END;"""
)
event.listen(
    PerformanceRegistration.__table__,
    "after_create",
    before_performance_registration_delete,
)

# 생산입고1(생산입고) 삭제 시 작업지시품목의 미생산수량, 가용재고, 현재고 업데이트
after_performance_registration_item1_delete = DDL(
    """
DROP TRIGGER IF EXISTS after_performance_registration_item1_delete;
CREATE TRIGGER after_performance_registration_item1_delete 
AFTER DELETE ON performance_registration_item1
FOR EACH ROW
BEGIN
    IF OLD.fk_work_order_item IS NOT NULL
    THEN
        CALL proc_update_work_order_item1_unproduced_quantity(OLD.fk_work_order_item);
    END IF;

    UPDATE setup_basic_stock
    SET current_stock = current_stock - OLD.good_quantity, 
        available_stock = available_stock - OLD.good_quantity
    WHERE item_code = OLD.item_code AND wh_code = OLD.warehouse_code;
END;"""
)
event.listen(
    PerformanceRegistrationItem1.__table__,
    "after_create",
    after_performance_registration_item1_delete,
)

# 생산입고2(자재소모) 삭제 시 현재고, 가용재고 되돌리기
after_performance_registration_item2_delete = DDL(
    """
DROP TRIGGER IF EXISTS after_performance_registration_item2_delete;
CREATE TRIGGER after_performance_registration_item2_delete 
AFTER DELETE ON performance_registration_item2
FOR EACH ROW
BEGIN
    UPDATE setup_basic_stock
    SET current_stock = current_stock + OLD.material_quantity, 
        available_stock = available_stock + OLD.material_quantity
    WHERE item_code = OLD.item_code AND wh_code = OLD.warehouse_code;
END;"""
)
event.listen(
    PerformanceRegistrationItem2.__table__,
    "after_create",
    after_performance_registration_item2_delete,
)
