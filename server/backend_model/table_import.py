# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import DDL, event
from backend_model.database import DBManager

print("module [backend_model.table_import.py] loaded")

db = DBManager.db


class ImportPurchaseOrder(db.Model):  # 수입관리 - 발주
    from backend_model.table_common import Companies

    __tablename__ = 'import_purchase_order'
    __table_args__ = {'comment': '수입관리(발주)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    order_number = db.Column('order_number', db.String(48), comment='P/O No (발주번호)')
    order_date = db.Column('order_date', db.DateTime, comment='Order Date (발주일자)')
    supplier = db.Column('supplier', db.String(48), comment='Supplier (공급업체)')
    supplier_contact = db.Column('supplier_contact', db.String(48), comment='Supplier Contact(업체담당자)')
    buyer = db.Column('buyer', db.String(48), comment='Buyer (고객업체)')
    owner_dept = db.Column('owner_dept', db.String(48), comment='OwnerDept (발주부서)')
    member = db.Column('member', db.String(48), comment='Member (발주담당자)')
    pay_terms = db.Column('pay_terms', db.String(48), comment='PayTerms (결재조건)')
    destination = db.Column('destination', db.String(48), comment='Destination (도착지)')
    valid_period = db.Column('valid_period', db.String(48), comment='ValidPeriod (유효기간)')
    delivery = db.Column('delivery', db.String(48), comment='Delivery')
    price_terms = db.Column('price_terms', db.String(48), comment='PriceTerms (가격조건)')
    origin = db.Column('origin', db.String(48), comment='Origin (원산지)')
    ship_port = db.Column('ship_port', db.String(48), comment='ShipPort (수송항구)')
    packing = db.Column('packing', db.String(48), comment='Packing')
    adv_bank = db.Column('adv_bank', db.String(48), comment='AdvBank')
    currency = db.Column('currency', db.String(48), comment='Currency (통화종류)')
    ex_rate = db.Column('ex_rate', db.Numeric(10, 2), server_default='0', comment='ExRate (환율)')
    inspection = db.Column('inspection', db.String(48), comment='Inspection')
    payment = db.Column('payment', db.String(48), comment='PayMent')
    remark = db.Column('remark', db.Text, comment='Remark (참고사항)')
    total_price = db.Column('total_price', db.Numeric(20, 4), server_default='0', comment='합계금액')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id, onupdate='CASCADE', ondelete='CASCADE'), comment='회사 FK')


class ImportPurchaseOrderItem(db.Model):  # 수입관리 - 발주 - 발주품목
    from backend_model.table_base import BaseItem
    from backend_model.table_purchase import PurchaseOrderPlanItem

    __tablename__ = 'import_purchase_order_item'
    __table_args__ = {'comment': '수입관리(발주품목)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE'), comment='품목코드 FK')
    qty = db.Column('qty', db.Integer, server_default='0', comment='Qty (수량)')
    import_price = db.Column('import_price', db.Numeric(20, 4), server_default='0', comment='ImportPrice (수입단가)')
    amount = db.Column('amount', db.Numeric(20, 4), server_default='0', comment='Amount (총금액)')
    req_date = db.Column('req_date', db.DateTime, comment='Req Date (요청 일자)')
    con_date = db.Column('con_date', db.DateTime, comment='Con Date (확인 일자)')
    net_price = db.Column('net_price', db.Numeric(20, 4), server_default='0', comment='NetPrice')
    end_user = db.Column('end_user', db.String(48), comment='EndUser')
    not_lc = db.Column('not_lc', db.Integer, server_default='0', comment='미LC')
    not_shipment = db.Column('not_shipment', db.Integer, server_default='0', comment='미선적')
    order_plan_number = db.Column('order_plan_number', db.String(48), comment='발주계획번호')
    fk_order_plan_item_id = db.Column('fk_order_plan_item_id', db.Integer, db.ForeignKey(PurchaseOrderPlanItem.id), comment='발주계획 품목 FK')
    fk_import_order_id = db.Column('fk_import_order_id', db.Integer, db.ForeignKey(ImportPurchaseOrder.id, onupdate='CASCADE'), comment='발주 FK')

    item = db.relationship("BaseItem", foreign_keys=[item_code])
    import_order = db.relationship("ImportPurchaseOrder", foreign_keys=[fk_import_order_id])
    order_plan_item = db.relationship("PurchaseOrderPlanItem", foreign_keys=[fk_order_plan_item_id])


class ImportShipment(db.Model):  # 수입관리 - 입고(선적)
    from backend_model.table_common import Companies

    __tablename__ = 'import_shipment'
    __table_args__ = {'comment': '수입관리(입고)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    shipment_number = db.Column('shipment_number', db.String(48), comment='Invoice No (선적번호)')
    shipment_date = db.Column('shipment_date', db.DateTime, comment='Invoice Date (선적일자)')
    supplier = db.Column('supplier', db.String(48), comment='Supplier (공급업체)')
    buyer = db.Column('buyer', db.String(48), comment='Buyer (고객업체)')
    validity = db.Column('validity', db.String(48), comment='Validity (유효기간)')
    pay_terms = db.Column('pay_terms', db.String(48), comment='PayTerms (결재조건)')
    destination = db.Column('destination', db.String(48), comment='Destination (도착지)')
    delivery = db.Column('delivery', db.String(48), comment='Delivery')
    price_terms = db.Column('price_terms', db.String(48), comment='PriceTerms (가격조건)')
    origin = db.Column('origin', db.String(48), comment='Origin (원산지)')
    ship_port = db.Column('ship_port', db.String(48), comment='ShipPort (배송지)')
    packing = db.Column('packing', db.String(48), comment='Packing (포장)')
    adv_bank = db.Column('adv_bank', db.String(48), comment='AdvBank')
    currency = db.Column('currency', db.String(48), comment='Currency (환종)')
    ex_rate = db.Column('ex_rate', db.Numeric(10, 2), server_default='0', comment='ExRate (환율)')
    inspection = db.Column('inspection', db.String(48), comment='Inspection')
    payment = db.Column('payment', db.String(48), comment='Payment')
    remark = db.Column('remark', db.Text, comment='Remark (참고사항)')
    total_price = db.Column('total_price', db.Numeric(20, 2), server_default='0', comment='합계금액')
    fk_purchase_order_id = db.Column('fk_purchase_order_id', db.Integer, db.ForeignKey(ImportPurchaseOrder.id, onupdate='CASCADE'), comment='발주 FK')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id, onupdate='CASCADE', ondelete='CASCADE'), comment='회사 FK')

    purchase_order = db.relationship("ImportPurchaseOrder", foreign_keys=[fk_purchase_order_id])


class ImportShipmentItem(db.Model):  # 수입관리 - 입고 - 입고품목
    from backend_model.table_base import BaseItem

    __tablename__ = 'import_shipment_item'
    __table_args__ = {'comment': '수입관리(입고품목)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE'), comment='품목코드')
    qty = db.Column('qty', db.Integer, server_default='0', comment='Qty (수량)')
    import_price = db.Column('import_price', db.Numeric(10, 5), server_default='0', comment='Import Price (수입단가)')
    amount = db.Column('amount', db.Numeric(10, 2), server_default='0', comment='Amount (총금액)')
    req_date = db.Column('req_date', db.DateTime, comment='Req Date')
    con_date = db.Column('con_date', db.DateTime, comment='Con Date')
    closing_yn = db.Column('closing_yn', db.Boolean, server_default='0', comment='종결여부')
    end_user = db.Column('end_user', db.String(48), comment='End User')
    not_clearance = db.Column('not_clearance', db.Integer, server_default='0', comment='미통관')
    not_publish = db.Column('not_publish', db.Integer, server_default='0', comment='미발행')
    fk_import_shipment_id = db.Column('fk_import_shipment_id', db.Integer, db.ForeignKey(ImportShipment.id, onupdate='CASCADE'), comment='입고 FK')
    fk_import_purchase_order_item_id = db.Column('fk_import_purchase_order_item_id', db.Integer, db.ForeignKey(ImportPurchaseOrderItem.id), comment='발주 품목 FK')

    item = db.relationship("BaseItem", foreign_keys=[item_code])
    shipment = db.relationship("ImportShipment", foreign_keys=[fk_import_shipment_id])
    import_purchase_order_item = db.relationship("ImportPurchaseOrderItem", foreign_keys=[fk_import_purchase_order_item_id])


class ImportClearance(db.Model):  # 수입관리 - 통관관리
    from backend_model.table_common import Companies

    __tablename__ = 'import_clearance'
    __table_args__ = {'comment': '수입관리(통관관리)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    clearance_number = db.Column('clearance_number', db.String(48), comment='통관번호')
    clearance_date = db.Column('clearance_date', db.DateTime, comment='통관일자')
    clearance_department = db.Column('clearance_department', db.String(48), comment='부서')
    member = db.Column('member', db.String(48), comment='담당자')
    supplier = db.Column('supplier', db.String(48), comment='Supplier (공급업체)')
    buyer = db.Column('buyer', db.String(48), comment='Buyer (고객업체)')
    currency = db.Column('currency', db.String(48), comment='Currency (통화)')
    ex_rate = db.Column('ex_rate', db.Numeric(10, 2), server_default='0', comment='ExRate(환율)')
    remark = db.Column('remark', db.Text, comment='Remark (참고사항)')
    total_price_import = db.Column('total_price_import', db.Numeric(20, 2), server_default='0', comment='import price 합계')
    total_price_won = db.Column('total_price_won', db.BigInteger, server_default='0', comment='won price 합계')
    total_price_cost = db.Column('total_price_cost', db.Numeric(20, 2), server_default='0', comment='원가 원화 합계금액')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id, onupdate='CASCADE', ondelete='CASCADE'), comment='회사 FK')


class ImportClearanceItem(db.Model):  # 수입관리 - 통관관리 - 통관품목
    from backend_model.table_base import BaseItem, BaseWarehouse

    __tablename__ = 'import_clearance_item'
    __table_args__ = {'comment': '수입관리(통관관리품목)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE'), comment='품목코드')
    item_name = db.Column('item_name', db.String(48), comment='ItemName (품명)')
    qty = db.Column('qty', db.Integer, server_default='0', comment='Qty (수량)')
    import_price = db.Column('import_price', db.Numeric(10, 5), server_default='0', comment='ImportPrice (수입단가)')
    amount = db.Column('amount', db.Numeric(10, 2), server_default='0', comment='Amount (총금액)')
    won_price = db.Column('won_price', db.BigInteger, server_default='0', comment='WonPrice')
    won_amount = db.Column('won_amount', db.BigInteger, server_default='0', comment='WonAmount')
    cost_price = db.Column('cost_price', db.Numeric(20, 4), server_default='0', comment='CostPrice')
    cost_rate = db.Column('cost_rate', db.Numeric(10, 3), server_default='0', comment='CostRate')
    import_shipment_number = db.Column('import_shipment_number', db.String(48), comment='선적번호')
    warehouse_code = db.Column('warehouse_code', db.String(48), db.ForeignKey(BaseWarehouse.wh_code, onupdate='CASCADE', ondelete='SET NULL'), comment='입고창고')
    fk_import_shipment_item_id = db.Column('fk_import_shipment_item_id', db.Integer, db.ForeignKey(ImportShipmentItem.id, onupdate='CASCADE'), comment='수입입고(선적) 품목 Fk')
    fk_import_clearance_id = db.Column('fk_import_clearance_id', db.Integer, db.ForeignKey(ImportClearance.id, onupdate='CASCADE'), comment='통관관리 Fk')

    item = db.relationship("BaseItem", foreign_keys=[item_code])
    warehouse = db.relationship('BaseWarehouse', foreign_keys=[warehouse_code])
    import_clearance = db.relationship("ImportClearance", foreign_keys=[fk_import_clearance_id])
    import_shipment_item = db.relationship("ImportShipmentItem", foreign_keys=[fk_import_shipment_item_id])
    basic_stock = db.relationship('SetupBasicStock', viewonly=True,
                                  primaryjoin='and_(foreign(ImportClearanceItem.item_code) == SetupBasicStock.item_code,'
                                              'foreign(ImportClearanceItem.warehouse_code) == SetupBasicStock.wh_code)')


class ImportCredit(db.Model):  # 수입관리 - 입고계산서
    from backend_model.table_common import Companies

    __tablename__ = 'import_credit'
    __table_args__ = {'comment': '수입관리(입고계산서)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    credit_number = db.Column('credit_number', db.String(48), comment='Credit No')
    work_day = db.Column('work_day', db.DateTime, comment='Work Day')
    supplier = db.Column('supplier', db.String(48), comment='Supplier (공급업체)')
    department = db.Column('department', db.String(48), comment='Department (담당부서)')
    employee = db.Column('employee', db.String(48), comment='Employee (담당사원)')
    due_day = db.Column('due_day', db.DateTime, comment='Due Day')
    credit_type = db.Column('credit_type', db.String(48), comment='Credit type')
    tax = db.Column('tax', db.Integer, comment='Tax')
    excute_day = db.Column('excute_day', db.DateTime, comment='Excute Day')
    currency = db.Column('currency', db.String(48), comment='Currency (환종)')
    remark = db.Column('remark', db.Text, comment='Remark (참고사항)')
    total_price = db.Column('total_price', db.Float, server_default='0', comment='합계금액')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id, onupdate='CASCADE', ondelete='CASCADE'), comment='회사 FK')


class ImportCreditItem(db.Model):  # 수입관리 - 입고계산서 - 입고계산서품목
    __tablename__ = 'import_credit_item'
    __table_args__ = {'comment': '수입관리(입고계산서품목)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    amount = db.Column('amount', db.Float, server_default='0', comment='Amount (총금액)')
    fk_import_credit_id = db.Column('fk_import_credit_id', db.Integer, db.ForeignKey(ImportCredit.id, onupdate='CASCADE'), comment='입고계산서 Fk')
    fk_import_shipment_id = db.Column('fk_import_shipment_id', db.Integer, db.ForeignKey(ImportShipment.id, onupdate='CASCADE'), comment='수입입고(선적) FK')

    credit = db.relationship('ImportCredit', foreign_keys=[fk_import_credit_id])
    shipment = db.relationship('ImportShipment', foreign_keys=[fk_import_shipment_id])


class ImportApproval(db.Model):  # 수입관리 - 결재등록
    from backend_model.table_common import Companies

    __tablename__ = 'import_approval'
    __table_args__ = {'comment': '수입관리(결재등록)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    approval_number = db.Column('approval_number', db.String(48), comment='결재번호')
    approval_date = db.Column('approval_date', db.DateTime, comment='결재일')
    supplier = db.Column('supplier', db.String(48), comment='공급업체')
    department = db.Column('department', db.String(48), comment='담당부서')
    member = db.Column('member', db.String(48), comment='담당자')
    approval_type = db.Column('approval_type', db.String(48), comment='결재유형')
    currency = db.Column('currency', db.String(48), comment='환종')
    remark = db.Column('remark', db.Text, comment='비고')
    total_price = db.Column('total_price', db.Float, server_default='0', comment='합계금액')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')


class ImportApprovalItem(db.Model):  # 수입관리 - 결재등록 - 품목
    __tablename__ = 'import_approval_item'
    __table_args__ = {'comment': '수입관리(결재등록품목)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    amount = db.Column('amount', db.Float, server_default='0', comment='금액')
    remark = db.Column('remark', db.Text, comment='비고')
    briefs = db.Column('briefs', db.Text, comment='적요')
    fk_import_approval_id = db.Column('fk_import_approval_id', db.Integer, db.ForeignKey(ImportApproval.id, onupdate='CASCADE'), comment='결재등록 FK')
    fk_import_shipment_id = db.Column('fk_import_shipment_id', db.Integer, db.ForeignKey(ImportShipment.id, onupdate='CASCADE'), comment='입고 FK')
    fk_import_credit_id = db.Column('fk_import_credit_id', db.Integer, db.ForeignKey(ImportCredit.id, onupdate='CASCADE'), comment='계산서 FK')
    fk_import_credit_item_id = db.Column('fk_import_credit_item_id', db.Integer, db.ForeignKey(ImportCreditItem.id, onupdate='CASCADE'), comment='계산서 품목 FK')

    approval = db.relationship("ImportApproval", foreign_keys=[fk_import_approval_id])
    shipment = db.relationship("ImportShipment", foreign_keys=[fk_import_shipment_id])
    credit = db.relationship("ImportCredit", foreign_keys=[fk_import_credit_id])
    credit_item = db.relationship("ImportCreditItem", foreign_keys=[fk_import_credit_item_id])


class ImportApprovalCost(db.Model):  # 수입관리 - 결재비용
    from backend_model.table_common import Companies

    __tablename__ = 'import_approval_cost'
    __table_args__ = {'comment': '수입관리(결재비용)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    approval_cost_number = db.Column('approval_cost_number', db.String(48), comment='결재비용번호')
    approval_cost_date = db.Column('approval_cost_date', db.DateTime, comment='발행일')
    cost_type = db.Column('cost_type', db.String(48), comment='비용구분')
    supplier = db.Column('supplier', db.String(48), comment='Supplier')
    department = db.Column('department', db.String(48), comment='담당부서')
    member = db.Column('member', db.String(48), comment='담당자')
    amount = db.Column('amount', db.Numeric(10, 2), server_default='0', comment='Amount')
    currency = db.Column('currency', db.String(48), comment='Currency')
    ex_rate = db.Column('ex_rate', db.Numeric(10, 2), server_default='0', comment='ExRate')
    won_amount = db.Column('won_amount', db.Numeric(20, 2), server_default='0', comment='Won Amount')
    remark = db.Column('remark', db.Text, comment='비고')
    total_price = db.Column('total_price', db.Numeric(20, 2), server_default='0', comment='합계 금액')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')
    fk_import_shipment_id = db.Column('fk_import_shipment_id', db.Integer, db.ForeignKey(ImportShipment.id), comment='입고 FK')

    shipment = db.relationship("ImportShipment", foreign_keys=[fk_import_shipment_id])


class ImportApprovalCostItem(db.Model):  # 수입관리 - 결재비용 - 품목
    __tablename__ = 'import_approval_cost_item'
    __table_args__ = {'comment': '수입관리(결재비용품목)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    account_type = db.Column('account_type', db.String(48), comment='계정과목')
    briefs = db.Column('briefs', db.String(48), comment='적요')
    supplier = db.Column('supplier', db.String(48), comment='공급업체')
    amount = db.Column('amount', db.Numeric(20, 2), server_default='0', comment='금액')
    payment_method = db.Column('payment_method', db.String(48), comment='지불방법')
    remark = db.Column('remark', db.Text, comment='비고')
    fk_import_shipment_id = db.Column('fk_import_shipment_id', db.Integer, db.ForeignKey(ImportShipment.id, onupdate='CASCADE'), comment='수입입고(선적) FK')
    fk_import_approval_cost_id = db.Column('fk_import_approval_cost_id', db.Integer, db.ForeignKey(ImportApprovalCost.id, onupdate='CASCADE'), comment='결재비용 FK')

    shipment = db.relationship("ImportShipment", foreign_keys=[fk_import_shipment_id])
    approval_cost = db.relationship("ImportApprovalCost", foreign_keys=[fk_import_approval_cost_id])


class ImportClearanceCost(db.Model):  # 수입관리 - 통관비용
    from backend_model.table_common import Companies

    __tablename__ = 'import_clearance_cost'
    __table_args__ = {'comment': '수입관리(통관비용)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    clearance_cost_number = db.Column('clearance_cost_number', db.String(48), comment='통관비용번호')
    clearance_cost_date = db.Column('clearance_cost_date', db.DateTime, comment='통관비용일자')
    cost_type = db.Column('cost_type', db.String(48), comment='비용구분')
    supplier = db.Column('supplier', db.String(48), comment='Supplier')
    department = db.Column('department', db.String(48), comment='담당부서')
    member = db.Column('member', db.String(48), comment='담당자')
    amount = db.Column('amount', db.Numeric(10, 2), server_default='0', comment='Amount')
    currency = db.Column('currency', db.String(48), comment='Currency')
    ex_rate = db.Column('ex_rate', db.Numeric(10, 2), server_default='0', comment='ExRate')
    won_amount = db.Column('won_amount', db.BigInteger, server_default='0', comment='Won Amount')
    remark = db.Column('remark', db.Text, comment='비고')
    supply_price = db.Column('supply_price', db.Numeric(20, 2), server_default='0', comment='공급가')
    vat = db.Column('vat', db.Numeric(20, 2), server_default='0', comment='부가세')
    total_price = db.Column('total_price', db.Numeric(20, 2), server_default='0', comment='합계 금액')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사 FK')
    fk_import_clearance_id = db.Column('fk_import_clearance_id', db.Integer, db.ForeignKey(ImportClearance.id), comment='통관 FK')

    clearance = db.relationship("ImportClearance", foreign_keys=[fk_import_clearance_id])


class ImportClearanceCostItem(db.Model):  # 수입관리 - 통관비용 - 품목
    from backend_model.table_base import BaseItem

    __tablename__ = 'import_clearance_cost_item'
    __table_args__ = {'comment': '수입관리(통관비용품목)'}

    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    item_code = db.Column('item_code', db.String(48), db.ForeignKey(BaseItem.item_code, onupdate='CASCADE'), comment='품목코드')
    account_type = db.Column('account_type', db.String(48), comment='계정과목')
    briefs = db.Column('briefs', db.String(48), comment='적요')
    supplier = db.Column('supplier', db.String(48), comment='공급업체')
    supply_price = db.Column('supply_price', db.Numeric(20, 2), server_default='0', comment='공급가')
    vat = db.Column('vat', db.Numeric(10, 2), server_default='0', comment='부가세')
    amount = db.Column('amount', db.Numeric(20, 2), server_default='0', comment='금액')
    payment_method = db.Column('payment_method', db.String(48), comment='지불방법')
    remark = db.Column('remark', db.Text, comment='비고')
    fk_import_clearance_id = db.Column('fk_import_clearance_id', db.Integer, db.ForeignKey(ImportClearance.id, onupdate='CASCADE'), comment='통관 FK')
    fk_import_clearance_cost_id = db.Column('fk_import_clearance_cost_id', db.Integer, db.ForeignKey(ImportClearanceCost.id, onupdate='CASCADE'), comment='수입통관비용 FK')

    item = db.relationship('BaseItem', foreign_keys=[item_code])
    clearance_cost = db.relationship("ImportClearanceCost", foreign_keys=[fk_import_clearance_cost_id])
    import_clearance = db.relationship("ImportClearance", foreign_keys=[fk_import_clearance_id])


# ----------------------------------------------------------------------------------------------------------------------
# CREATE STORED PROCEDURE

# 선적 품목에서 발주 품목 아이디로 선적 수량 합계 가져오기
proc_get_import_shipment_item_total_quantity = DDL('''
DROP PROCEDURE IF EXISTS proc_get_import_shipment_item_total_quantity;
CREATE PROCEDURE `proc_get_import_shipment_item_total_quantity`(
    IN `orderItemId` INT,
    OUT `sumQuantity` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '선적 품목에서 발주 품목 아이디로 선적 수량 합계 가져오기'
BEGIN
    SET sumQuantity = (SELECT SUM(qty)
                       FROM import_shipment_item
                       WHERE fk_import_purchase_order_item_id = orderItemId
                       GROUP BY fk_import_purchase_order_item_id);
    IF sumQuantity IS NULL THEN
        SET sumQuantity = 0;
    ENd IF;
END
''')
event.listen(ImportShipmentItem.__table__, 'after_create', proc_get_import_shipment_item_total_quantity)

# 발주 품목의 미선적 수량 업데이트
proc_update_import_purchase_order_item_not_shipment = DDL('''
DROP PROCEDURE IF EXISTS proc_update_import_purchase_order_item_not_shipment;
CREATE PROCEDURE `proc_update_import_purchase_order_item_not_shipment`(
    IN `orderItemId` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '발주 품목의 미선적 수량 업데이트'
BEGIN
    # 발주 품목 아이디로 선적 수량 합계 가져오기
    CALL proc_get_import_shipment_item_total_quantity(orderItemId, @sumQuantity);
    # 발주 품목의 미선적 수량 업데이트
    UPDATE import_purchase_order_item
    SET not_shipment = qty - @sumQuantity
    WHERE id = orderItemId AND not_shipment != (qty - @sumQuantity);
END
''')
event.listen(ImportPurchaseOrderItem.__table__, 'after_create', proc_update_import_purchase_order_item_not_shipment)

# 통관에서 회사 아이디 가져오기
proc_get_import_clearance_company_id = DDL('''
DROP PROCEDURE IF EXISTS proc_get_import_clearance_company_id;
CREATE PROCEDURE `proc_get_import_clearance_company_id`(
    IN `clearanceId` INT,
    OUT `companyId` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '통관에서 회사 아이디 가져오기'
BEGIN
    SELECT fk_company_id INTO companyId
    FROM import_clearance
    WHERE id = clearanceId;
END
''')
event.listen(ImportClearance.__table__, 'after_create', proc_get_import_clearance_company_id)

# 통관 품목에서 선적 품목 아이디로 통관 수량 합계 가져오기
proc_get_import_clearance_item_total_quantity = DDL('''
DROP PROCEDURE IF EXISTS proc_get_import_clearance_item_total_quantity;
CREATE PROCEDURE `proc_get_import_clearance_item_total_quantity`(
    IN `shipmentItemId` INT,
    OUT `sumQuantity` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '통관 품목에서 선적 품목 아이디로 통관 수량 합계 가져오기'
BEGIN
    SET sumQuantity = (SELECT SUM(qty)
                       FROM import_clearance_item
                       WHERE fk_import_shipment_item_id = shipmentItemId
                       GROUP BY fk_import_shipment_item_id);
    IF sumQuantity IS NULL THEN
        SET sumQuantity = 0;
    ENd IF;
END
''')
event.listen(ImportClearanceItem.__table__, 'after_create', proc_get_import_clearance_item_total_quantity)

# 선적 품목의 미통관 수량 업데이트
proc_update_import_shipment_item_not_clearance = DDL('''
DROP PROCEDURE IF EXISTS proc_update_import_shipment_item_not_clearance;
CREATE PROCEDURE `proc_update_import_shipment_item_not_clearance`(
    IN `shipmentItemId` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '선적 품목의 미통관 수량 업데이트'
BEGIN
    # 선적 품목 아이디로 통관 수량 합계 가져오기
    CALL proc_get_import_clearance_item_total_quantity(shipmentItemId, @sumQuantity);
    # 선적 품목의 미통관 수량 업데이트
    UPDATE import_shipment_item
    SET not_clearance = qty - @sumQuantity
    WHERE id = shipmentItemId AND not_clearance != (qty - @sumQuantity);
END
''')
event.listen(ImportShipmentItem.__table__, 'after_create', proc_update_import_shipment_item_not_clearance)

# ----------------------------------------------------------------------------------------------------------------------
# CREATE TRIGGER

# 발주 삭제
before_import_purchase_order_delete = DDL('''
DROP TRIGGER IF EXISTS before_import_purchase_order_delete;
CREATE TRIGGER before_import_purchase_order_delete
BEFORE DELETE ON import_purchase_order
FOR EACH ROW
BEGIN
    # 발주 품목 삭제
    DELETE FROM import_purchase_order_item WHERE fk_import_order_id = OLD.id;
END;''')
event.listen(ImportPurchaseOrder.__table__, 'after_create', before_import_purchase_order_delete)

# 선적 삭제
before_import_shipment_delete = DDL('''
DROP TRIGGER IF EXISTS before_import_shipment_delete;
CREATE TRIGGER before_import_shipment_delete
BEFORE DELETE ON import_shipment
FOR EACH ROW
BEGIN
    # 선적 품목 삭제
    DELETE FROM import_shipment_item WHERE fk_import_shipment_id = OLD.id;
END;''')
event.listen(ImportShipment.__table__, 'after_create', before_import_shipment_delete)

# 선적 품목 추가
after_import_shipment_item_insert = DDL('''
DROP TRIGGER IF EXISTS after_import_shipment_item_insert;
CREATE TRIGGER after_import_shipment_item_insert
AFTER INSERT ON import_shipment_item
FOR EACH ROW
BEGIN
    # 발주 품목 미선적 수량 업데이트
    CALL proc_update_import_purchase_order_item_not_shipment(NEW.fk_import_purchase_order_item_id);
END;''')
event.listen(ImportShipmentItem.__table__, 'after_create', after_import_shipment_item_insert)

# 선적 품목 업데이트
after_import_shipment_item_update = DDL('''
DROP TRIGGER IF EXISTS after_shipment_release_request_update;
CREATE TRIGGER after_shipment_release_request_update
AFTER UPDATE ON import_shipment_item
FOR EACH ROW
BEGIN
    IF NEW.qty != OLD.qty THEN
        # 발주 품목 미선적 수량 업데이트
        CALL proc_update_import_purchase_order_item_not_shipment(NEW.fk_import_purchase_order_item_id);
    END IF;
END;''')
event.listen(ImportShipmentItem.__table__, 'after_create', after_import_shipment_item_update)

# 선적 품목 삭제
after_import_shipment_item_delete = DDL('''
DROP TRIGGER IF EXISTS after_import_shipment_item_delete;
CREATE TRIGGER after_import_shipment_item_delete
AFTER DELETE ON import_shipment_item
FOR EACH ROW
BEGIN
    # 발주 품목 미선적 수량 업데이트
    CALL proc_update_import_purchase_order_item_not_shipment(OLD.fk_import_purchase_order_item_id);
END;''')
event.listen(ImportShipmentItem.__table__, 'after_create', after_import_shipment_item_delete)

# 통관 삭제
before_import_clearance_delete = DDL('''
DROP TRIGGER IF EXISTS before_import_clearance_delete;
CREATE TRIGGER before_import_clearance_delete
BEFORE DELETE ON import_clearance
FOR EACH ROW
BEGIN
    # 통관관리 품목 삭제
    DELETE FROM import_clearance_item WHERE fk_import_clearance_id = OLD.id;
END;''')
event.listen(ImportClearance.__table__, 'after_create', before_import_clearance_delete)

# 통관 품목 추가
after_import_clearance_item_insert = DDL('''
DROP TRIGGER IF EXISTS after_import_clearance_item_insert;
CREATE TRIGGER after_import_clearance_item_insert
AFTER INSERT ON import_clearance_item
FOR EACH ROW
BEGIN
    # 선적 품목 미통관 수량 업데이트
    CALL proc_update_import_shipment_item_not_clearance(NEW.fk_import_shipment_item_id);
    
    # company id 가져오기
    CALL proc_get_import_clearance_company_id(NEW.fk_import_clearance_id, @companyId);

    # 기초재고가 없으면 추가
    CALL proc_insert_setup_basic_stock(NEW.item_code, NEW.warehouse_code, @companyId);
    
    # 기초재고 업데이트
    UPDATE setup_basic_stock
    SET current_stock = current_stock + NEW.qty, available_stock = available_stock + NEW.qty
    WHERE item_code = NEW.item_code AND wh_code = NEW.warehouse_code;
END;''')
event.listen(ImportClearanceItem.__table__, 'after_create', after_import_clearance_item_insert)

# 통관 품목 업데이트
after_import_clearance_item_update = DDL('''
DROP TRIGGER IF EXISTS after_import_clearance_item_update;
CREATE TRIGGER after_import_clearance_item_update
AFTER UPDATE ON import_clearance_item
FOR EACH ROW
BEGIN
    IF NEW.qty != OLD.qty THEN
        # 선적 품목 미통관 수량 업데이트
        CALL proc_update_import_shipment_item_not_clearance(NEW.fk_import_shipment_item_id);
        
        # company id 가져오기
        CALL proc_get_import_clearance_company_id(NEW.fk_import_clearance_id, @companyId);
        
        # 기초재고가 없으면 추가
        CALL proc_insert_setup_basic_stock(NEW.item_code, NEW.warehouse_code, @company_id);
        
        # 기초재고 업데이트
        UPDATE setup_basic_stock
        SET current_stock = current_stock - OLD.qty + NEW.qty, available_stock = available_stock - OLD.qty + NEW.qty
        WHERE item_code = NEW.item_code AND wh_code = NEW.warehouse_code;
    END IF;
END;''')
event.listen(ImportClearanceItem.__table__, 'after_create', after_import_clearance_item_update)

# 통관 품목 삭제
after_import_clearance_item_delete = DDL('''
DROP TRIGGER IF EXISTS after_import_clearance_item_delete;
CREATE TRIGGER after_import_clearance_item_delete
AFTER DELETE ON import_clearance_item
FOR EACH ROW
BEGIN
    DECLARE company_id INT;

    # 선적 품목 미통관 수량 업데이트
    CALL proc_update_import_shipment_item_not_clearance(OLD.fk_import_shipment_item_id);
    
    # company id 가져오기
    CALL proc_get_import_clearance_company_id(OLD.fk_import_clearance_id, @companyId);
    
    # 기초재고가 없으면 추가
    CALL proc_insert_setup_basic_stock(OLD.item_code, OLD.warehouse_code, @company_id);

    # 기초재고 업데이트
    UPDATE setup_basic_stock
    SET current_stock = current_stock - OLD.qty, available_stock = available_stock - OLD.qty
    WHERE item_code = OLD.item_code AND wh_code = OLD.warehouse_code;
END;''')
event.listen(ImportClearanceItem.__table__, 'after_create', after_import_clearance_item_delete)

# 입고계산서 삭제
before_import_credit_delete = DDL('''
DROP TRIGGER IF EXISTS before_import_credit_delete;
CREATE TRIGGER before_import_credit_delete
BEFORE DELETE ON import_credit
FOR EACH ROW
BEGIN
    # 입고계산서 품목 삭제
    DELETE FROM import_credit_item WHERE fk_import_credit_id = OLD.id;
END;''')
event.listen(ImportCredit.__table__, 'after_create', before_import_credit_delete)

# 결재등록 삭제
before_import_approval_delete = DDL('''
DROP TRIGGER IF EXISTS before_import_approval_delete;
CREATE TRIGGER before_import_approval_delete
BEFORE DELETE ON import_approval
FOR EACH ROW
BEGIN
    # 결재등록 품목 삭제
    DELETE FROM import_approval_item WHERE fk_import_credit_id = OLD.id;
END;''')
event.listen(ImportApproval.__table__, 'after_create', before_import_approval_delete)

# 결재비용 삭제
before_import_approval_cost_delete = DDL('''
DROP TRIGGER IF EXISTS before_import_approval_cost_delete;
CREATE TRIGGER before_import_approval_cost_delete
BEFORE DELETE ON import_approval_cost
FOR EACH ROW
BEGIN
    # 결재비용 품목 삭제
    DELETE FROM import_approval_cost_item WHERE fk_import_approval_cost_id = OLD.id;
END;''')
event.listen(ImportApprovalCost.__table__, 'after_create', before_import_approval_cost_delete)

# 통관비용 삭제
before_import_clearance_cost_delete = DDL('''
DROP TRIGGER IF EXISTS before_import_clearance_cost_delete;
CREATE TRIGGER before_import_clearance_cost_delete
BEFORE DELETE ON import_clearance_cost
FOR EACH ROW
BEGIN
    # 통관비용 품목 삭제
    DELETE FROM import_clearance_cost_item WHERE fk_import_clearance_cost_id = OLD.id;
END;''')
event.listen(ImportClearanceCost.__table__, 'after_create', before_import_clearance_cost_delete)
