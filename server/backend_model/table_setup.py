# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import DDL, event
from dateutil.relativedelta import relativedelta
from backend_model.database import DBManager
from backend_model.table_common import Companies
from backend_model.table_base import BaseItem, BaseWarehouse

print("module [backend_model.table_setup.py] loaded")

db = DBManager.db


class SetupBasicStock(db.Model):  # 셋업관리 - 기초재고관리
    __tablename__ = "setup_basic_stock"
    __table_args__ = {"comment": "셋업관리(기초재고관리)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    wh_code = db.Column("wh_code", db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment="창고코드")
    item_code = db.Column("item_code", db.String(48), db.ForeignKey(BaseItem.item_code, onupdate="CASCADE", ondelete="CASCADE"), comment="품목코드")
    basic_stock = db.Column("basic_stock", db.Integer, comment="기초재고")
    current_stock = db.Column("current_stock", db.Integer, comment="현재고")
    available_stock = db.Column("available_stock", db.Integer, comment="가용재고")
    item_unit_price = db.Column("item_unit_price", db.Float, server_default="0", comment="단가")
    item_price = db.Column("item_price", db.Numeric(12, 2), server_default="0", comment="금액")
    etc = db.Column("etc", db.Text, comment="비고")
    fk_company_id = db.Column("fk_company_id", db.Integer, db.ForeignKey(Companies.id), comment="회사 FK")
    warehouse = db.relationship("BaseWarehouse", foreign_keys=[wh_code])
    item = db.relationship("BaseItem", foreign_keys=[item_code])

    def excel_import_columns(self):
        return dict(
            output=[
                self.wh_code,
                self.item_code,
                self.basic_stock,
                self.current_stock,
                self.available_stock,
                self.item_unit_price,
                self.item_price,
                self.etc,
            ],
            key=[self.wh_code, self.item_code, self.fk_company_id],
        )

class SetupBasicStockHistory(db.Model): # 셋업관리 - 기초재고히스토리
    __tablename__ = "setup_basic_stock_history"
    __table_args__ = {"comment": "셋업관리(기초재고히스토리)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    item_code = db.Column("item_code", db.String(48), db.ForeignKey(BaseItem.item_code, onupdate="CASCADE",ondelete="CASCADE"), comment="품목코드")
    wh_code = db.Column("wh_code", db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment="창고코드")
    current_stock = db.Column("current_stock", db.Integer, comment="현재고")


class SetupMenu(db.Model):  # 셋업관리 - 메뉴관리,자동체번관리
    __tablename__ = "setup_menu"
    __table_args__ = {"comment": "셋업관리(메뉴관리,자동체번관리)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    parent_id = db.Column("parent_id", db.Integer, comment="상위 메뉴 아이디")  #  (최상위 메뉴는 -1)
    menu_name = db.Column("menu_name", db.String(48), comment="메뉴명")
    menu_depth = db.Column("menu_depth", db.Integer, comment="메뉴레벨")  # (1:Main, 2:Sub)
    menu_order = db.Column("menu_order", db.Integer, comment="표시순서")
    menu_enable = db.Column("menu_enable", db.Boolean, default=True, comment="사용여부")
    menu_initial = db.Column("menu_initial", db.String(10), comment="자동채번이니셜")
    menu_initial_enable = db.Column(
        "menu_initial_enable", db.Boolean, default=False, comment="자동채번이니셜사용여부"
    )
    menu_format = db.Column(
        "menu_format", db.Integer, default=1, comment="연월일표기유형"
    )  # (1:YYYYMMDD, 2:YYYYMM, 3:YYYY)
    menu_middle_letter = db.Column(
        "menu_middle_letter", db.String(5), default="-", comment="중간자"
    )
    menu_last_digit = db.Column(
        "menu_last_digit", db.Integer, default=3, comment="뒷자리수"
    )
    menu_function = db.Column(
        "menu_function", db.Integer, default=31, comment="메뉴별기능목록"
    )  # (1:신규,2:수정,4:삭제,8:인쇄,16:엑셀)
    path = db.Column("path", db.String(256), comment="View Path")
    etc = db.Column("etc", db.Text, comment="비고")
    fk_company_id = db.Column(
        "fk_company_id", db.Integer, db.ForeignKey(Companies.id), comment="회사 FK"
    )

    def date_format(self):
        if self.menu_format == 2:
            return "%Y%m"
        elif self.menu_format == 3:
            return "%Y"
        else:
            return "%Y%m%d"

    def get_range(self):
        if self.menu_format == 2:
            start = datetime.now().replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            )
            end = start + relativedelta(months=1)
        elif self.menu_format == 3:
            start = datetime.now().replace(
                month=1, day=1, hour=0, minute=0, second=0, microsecond=0
            )
            end = start + relativedelta(years=1)
        else:
            start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + relativedelta(days=1)
        return start, end

    def menu_number_format(self, count):
        if self.menu_initial is not None and self.menu_initial != "":
            output = "{initial}{menu_middle_letter}{datestr}{menu_middle_letter}"
            initial = self.menu_initial
        else:
            output = "{datestr}{menu_middle_letter}"
            initial = ''
        date_format = self.date_format()

        menu_middle_letter = self.menu_middle_letter
        output += "{count:0" + str(self.menu_last_digit) + "d}"
        now = datetime.now()
        datestr = now.strftime(date_format)
        return output.format(
            initial=initial,
            menu_middle_letter=menu_middle_letter,
            datestr=datestr,
            count=count + 1,
        )


class SetupGroup(db.Model):  # 셋업관리 - 권한그룹관리
    __tablename__ = "setup_group"
    __table_args__ = {"comment": "셋업관리(그룹관리)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    group_name = db.Column("group_name", db.String(48), comment="그룹명")
    group_detail = db.Column("group_detail", db.String(256), comment="그룹상세")
    fk_company_id = db.Column(
        "fk_company_id", db.Integer, db.ForeignKey(Companies.id), comment="회사 FK"
    )


class SetupGroupAuth(db.Model):  # 셋업관리 - 권한그룹관리
    __tablename__ = "setup_group_auth"
    __table_args__ = {"comment": "셋업관리(권한그룹관리)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    fk_group_id = db.Column(
        "fk_group_id", db.Integer, db.ForeignKey(SetupGroup.id), comment="그룹 ID"
    )
    fk_menu_id = db.Column(
        "fk_menu_id", db.Integer, db.ForeignKey(SetupMenu.id), comment="메뉴 ID"
    )
    menu_yn = db.Column("menu_yn", db.Boolean, default=True, comment="메뉴 SHOW/HIDE")
    menu_auth = db.Column(
        "menu_auth", db.Integer, default=31, comment="메뉴 권한"
    )  # (1:신규,2:수정,4:삭제,8:인쇄,16:엑셀)
    group = db.relationship("SetupGroup", foreign_keys=[fk_group_id])
    menu = db.relationship("SetupMenu", foreign_keys=[fk_menu_id])


class SetupCodeChangeHistory(db.Model):  # 셋업관리 - 코드변경이력
    __tablename__ = "setup_code_change_history"
    __table_args__ = {"comment": "셋업관리(코드변경이력)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    change_type = db.Column("change_type", db.Integer, comment="코드변경타입")  # 1:품목, 2:업체코드
    previous_code = db.Column("previous_code", db.String(48), comment="변경전 코드")
    after_code = db.Column("after_code", db.String(48), comment="변경후 코드")
    name = db.Column("name", db.String(48), comment="품명/업체명")
    change_reason = db.Column("change_reason", db.String(256), comment="변경사유")
    manager = db.Column("manager", db.String(48), comment="변경담당자")
    fk_company_id = db.Column(
        "fk_company_id", db.Integer, db.ForeignKey(Companies.id), comment="회사 FK"
    )


class SetupControl(db.Model):  # 셋업관리 - 통제관리
    __tablename__ = "setup_control"
    __table_args__ = {"comment": "셋업관리(통제관리)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    not_use_minus_stock = db.Column(
        "not_use_minus_stock", db.Boolean, default=False, comment="- 수불 처리 불가"
    )
    not_use_prereceiving = db.Column(
        "not_use_prereceiving", db.Boolean, default=False, comment="가입고 사용 안함"
    )
    not_use_lot = db.Column(
        "not_use_lot", db.Boolean, default=False, comment="LOT 사용 안함"
    )
    monitoring_zoom = db.Column(
        "monitoring_zoom", db.String(48), default="1.8", comment="모니터링 화면 줌"
    )
    monitoring_page = db.Column(
        "monitoring_page", db.Integer, default=10, comment="모니터링 화면 페이지"
    )
    fk_company_id = db.Column(
        "fk_company_id", db.Integer, db.ForeignKey(Companies.id), comment="회사 FK"
    )


class SetupProduceCost(db.Model):  # 셋업관리 - 년도별 원가구성 요율관리
    __tablename__ = "setup_produce_cost"
    __table_args__ = {"comment": "셋업관리(년도별 원가구성 요율관리)"}
    year = db.Column("year", db.String(48), primary_key=True, comment="적용연도")
    subfix = db.Column("subfix", db.String(48), primary_key=True, comment="구분")
    name = db.Column("name", db.String(48), comment="제조구분")
    labor_cost = db.Column("labor_cost", db.Integer, comment="노무비단가(원)")
    produce_cost_rate = db.Column("produce_cost_rate", db.Integer, comment="제조경비(%)")
    operating_cost_rate = db.Column("operating_cost_rate", db.Integer, comment="판관비(%)")
    fk_company_id = db.Column(
        "fk_company_id",
        db.Integer,
        db.ForeignKey(Companies.id),
        primary_key=True,
        comment="회사 FK",
    )


class SetupBasicBalance(db.Model):  # 셋업관리 - 기초잔액관리
    from backend_model.table_base import BaseClient

    __tablename__ = "setup_basic_balance"
    __table_args__ = {"comment": "셋업관리(기초잔액관리)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    sales_balance = db.Column(
        "sales_balance", db.BigInteger, server_default="0", comment="매출잔액"
    )
    purchase_balance = db.Column(
        "purchase_balance", db.BigInteger, server_default="0", comment="매입잔액"
    )
    fk_company_id = db.Column(
        "fk_company_id", db.Integer, db.ForeignKey(Companies.id), comment="회사 FK"
    )
    fk_base_client_id = db.Column(
        "fk_base_client_id",
        db.Integer,
        db.ForeignKey(BaseClient.id, onupdate="CASCADE", ondelete="CASCADE"),
        comment="거래처 FK",
    )
    base_client = db.relationship("BaseClient", foreign_keys=[fk_base_client_id])

class SetupSgaExpense(db.Model):
    __tablename__ = 'setup_sga_expense'
    __table_args__ = {
        'comment': 'SGA 비용 설정'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    name = db.Column('name', db.String(48), comment='비용명')
    rate = db.Column('rate', db.Integer, comment='비율')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사테이블 FK')
    
class SetupMD(db.Model):
    __tablename__ = 'setup_md'
    __table_args__ = {
        'comment': 'M/D'
    }
    id = db.Column('id', db.Integer, primary_key=True, comment='UID')
    created = db.Column('created', db.DateTime, default=datetime.now, comment='생성시간')
    name = db.Column('name', db.String(48), comment='비용명')
    md = db.Column('md', db.Integer, comment='M/D')
    fk_company_id = db.Column('fk_company_id', db.Integer, db.ForeignKey(Companies.id), comment='회사테이블 FK')
        
    

# ----------------------------------------------------------------------------------------------------------------------
# CREATE STORED PROCEDURE

# 기초 재고가 없으면 추가한다
proc_insert_setup_basic_stock = DDL(
    """
DROP PROCEDURE IF EXISTS proc_insert_setup_basic_stock;
CREATE PROCEDURE `proc_insert_setup_basic_stock`(
    IN `itemCode` VARCHAR(48),
    IN `warehouseCode` VARCHAR(48),
    IN `companyId` INT
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '기초 재고가 없으면 추가한다'
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM setup_basic_stock WHERE item_code = itemCode AND wh_code = warehouseCode
    ) THEN
        INSERT INTO setup_basic_stock (created, item_code, wh_code, basic_stock, current_stock, available_stock, item_unit_price, item_price, fk_company_id)
        VALUES (now(), itemCode, warehouseCode, 0, 0, 0, 0, 0, companyId);
    END IF;
END
"""
)
event.listen(SetupBasicStock.__table__, "after_create", proc_insert_setup_basic_stock)


# 가용재고 계산 및 업데이트
proc_update_available_stock = DDL(
    """
DROP PROCEDURE IF EXISTS proc_update_available_stock;
CREATE PROCEDURE `proc_update_available_stock`(
    IN `itemCode` VARCHAR(48),
    IN `warehouseCode` VARCHAR(48)
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '가용재고 계산 및 업데이트'
BEGIN
    DECLARE currentStock INT;
    DECLARE assignQuantity INT;

    SELECT current_stock INTO currentStock FROM setup_basic_stock WHERE item_code = itemCode AND wh_code = warehouseCode;

    # 전체 할당 수량
    SET assignQuantity = (SELECT SUM(assign_quantity)
                          FROM shipment_order_item
                          WHERE item_code = itemCode AND warehouse_code = warehouseCode
                          GROUP BY item_code, warehouse_code);
    IF assignQuantity IS NULL THEN
        SET assignQuantity = 0;
    ENd IF;
    
    UPDATE setup_basic_stock SET available_stock = currentStock - assignQuantity where item_code = itemCode AND wh_code = warehouseCode;
END
"""
)
event.listen(SetupBasicStock.__table__, "after_create", proc_update_available_stock)


# 현재고 계산 및 업데이트
proc_update_current_stock = DDL(
    """
DROP PROCEDURE IF EXISTS proc_update_current_stock;
CREATE PROCEDURE `proc_update_current_stock`(
    IN `itemCode` VARCHAR(48),
    IN `warehouseCode` VARCHAR(48)
)
LANGUAGE SQL NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER
COMMENT '현재고 계산 및 업데이트'
BEGIN
    DECLARE closingStock INT;
    DECLARE stock INT;
    DECLARE shipmentReleaseQuantity INT;
    DECLARE stockEtcReleaseQuantity INT;
    DECLARE stockMoveReleaseQuantity INT;
    DECLARE produceReleaseQuantity INT;
    DECLARE purchaseReturnQuantity INT;
    DECLARE exportCommInvoiceQuantity INT;
    DECLARE purchaseReceivingQuantity INT;
    DECLARE stockEtcReceivingQuantity INT;
    DECLARE stockMoveReceivingQuantity INT;
    DECLARE produceReceivingQuantity INT;
    DECLARE releaseReturnQuantity INT;
    DECLARE importClearanceQuantity INT;

    SELECT basic_stock INTO stock FROM setup_basic_stock WHERE item_code = itemCode AND wh_code = warehouseCode;
    
    # 출하관리 - 출고 수량
    SET shipmentReleaseQuantity = (SELECT SUM(release_quantity)
                                   FROM shipment_release_item
                                   WHERE item_code = itemCode AND warehouse_code = warehouseCode
                                   GROUP BY item_code, warehouse_code);
    IF shipmentReleaseQuantity IS NULL THEN
        SET shipmentReleaseQuantity = 0;
    ENd IF;
    
    # 재고관리 - 기타출고
    SET stockEtcReleaseQuantity = (SELECT SUM(quantity)
                                   FROM stock_etc_item
                                   WHERE item_code = itemCode AND warehouse_code = warehouseCode AND type = '출고'
                                   GROUP BY item_code, warehouse_code);
    IF stockEtcReleaseQuantity IS NULL THEN
        SET stockEtcReleaseQuantity = 0;
    ENd IF;
    
    # 재고관리 - 재고이동출고
    SET stockMoveReleaseQuantity = (SELECT SUM(release_quantity)
                                    FROM stock_move_release_item
                                    WHERE item_code = itemCode AND out_warehouse = warehouseCode
                                    GROUP BY item_code, out_warehouse);
    IF stockMoveReleaseQuantity IS NULL THEN
        SET stockMoveReleaseQuantity = 0;
    ENd IF;
    
    # 생산관리 - 자재소모
    SET produceReleaseQuantity = (SELECT SUM(material_quantity)
                                    FROM performance_registration_item2
                                    WHERE item_code = itemCode AND warehouse_code = warehouseCode
                                    GROUP BY item_code, warehouse_code);
    IF produceReleaseQuantity IS NULL THEN
        SET produceReleaseQuantity = 0;
    ENd IF;
    
    # 구매관리 - 입고반품
    SET purchaseReturnQuantity = (SELECT SUM(return_quantity)
                                  FROM purchase_receiving_return_item
                                  WHERE item_code = itemCode AND warehouse_code = warehouseCode
                                  GROUP BY item_code, warehouse_code);
    IF purchaseReturnQuantity IS NULL THEN
        SET purchaseReturnQuantity = 0;
    ENd IF;
    
    # 수출관리 - 선적
    SET exportCommInvoiceQuantity = (SELECT SUM(invoice_quantity)
                                     FROM export_comm_invoice_item
                                     WHERE item_code = itemCode AND warehouse_code = warehouseCode
                                     GROUP BY item_code, warehouse_code);
    IF exportCommInvoiceQuantity IS NULL THEN
        SET exportCommInvoiceQuantity = 0;
    ENd IF;
    
    # 구매관리 - 입고
    SET purchaseReceivingQuantity = (SELECT SUM(receiving_quantity)
                                     FROM purchase_receiving_item
                                     WHERE item_code = itemCode AND warehouse_code = warehouseCode
                                     GROUP BY item_code, warehouse_code);
    IF purchaseReceivingQuantity IS NULL THEN
        SET purchaseReceivingQuantity = 0;
    ENd IF;
    
    # 재고관리 - 기타입고
    SET stockEtcReceivingQuantity = (SELECT SUM(quantity)
                                     FROM stock_etc_item
                                     WHERE item_code = itemCode AND warehouse_code = warehouseCode AND type = '입고'
                                     GROUP BY item_code, warehouse_code);
    IF stockEtcReceivingQuantity IS NULL THEN
        SET stockEtcReceivingQuantity = 0;
    ENd IF;
    
    # 재고관리 - 재고이동입고
    SET stockMoveReceivingQuantity = (SELECT SUM(release_quantity)
                                      FROM stock_move_release_item
                                      WHERE item_code = itemCode AND in_warehouse = warehouseCode
                                      GROUP BY item_code, in_warehouse);
    IF stockMoveReceivingQuantity IS NULL THEN
        SET stockMoveReceivingQuantity = 0;
    ENd IF;
    
    # 생산관리 - 생산입고
    SET produceReceivingQuantity = (SELECT SUM(good_quantity)
                                   FROM performance_registration_item1
                                   WHERE item_code = itemCode AND warehouse_code = warehouseCode
                                   GROUP BY item_code, warehouse_code);
    IF produceReceivingQuantity IS NULL THEN
        SET produceReceivingQuantity = 0;
    ENd IF;
    
    # 출하관리 - 출고반품
    SET releaseReturnQuantity = (SELECT SUM(return_quantity)
                                 FROM shipment_release_return_item
                                 WHERE item_code = itemCode AND warehouse_code = warehouseCode
                                 GROUP BY item_code, warehouse_code);
    IF releaseReturnQuantity IS NULL THEN
        SET releaseReturnQuantity = 0;
    ENd IF;
    
    # 수입관리 - 통관
    SET importClearanceQuantity = (SELECT SUM(qty)
                                   FROM import_clearance_item
                                   WHERE item_code = itemCode AND warehouse_code = warehouseCode
                                   GROUP BY item_code, warehouse_code);
    IF importClearanceQuantity IS NULL THEN
        SET importClearanceQuantity = 0;
    ENd IF;

    SET closingStock = stock - 
                       shipmentReleaseQuantity - stockEtcReleaseQuantity - 
                       stockMoveReleaseQuantity - produceReleaseQuantity - 
                       purchaseReturnQuantity - exportCommInvoiceQuantity + 
                       purchaseReceivingQuantity + stockEtcReceivingQuantity +
                       stockMoveReceivingQuantity + produceReceivingQuantity +
                       releaseReturnQuantity + importClearanceQuantity;
    
    UPDATE setup_basic_stock SET current_stock = closingStock where item_code = itemCode AND wh_code = warehouseCode;
END
"""
)
event.listen(SetupBasicStock.__table__, "after_create", proc_update_current_stock)


# ----------------------------------------------------------------------------------------------------------------------
# CREATE TRIGGER

# 기초재고 추가
before_setup_basic_stock_insert = DDL(
    """
DROP TRIGGER IF EXISTS before_setup_basic_stock_insert;
CREATE TRIGGER before_setup_basic_stock_insert 
BEFORE INSERT ON setup_basic_stock
FOR EACH ROW
BEGIN
    DECLARE count_stock INT;
    
    SELECT COUNT(*) INTO count_stock
    FROM setup_basic_stock
    WHERE item_code = NEW.item_code AND wh_code = NEW.wh_code;
    
    IF count_stock > 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = "basic stock already exist";
    END IF;
END;"""
)
event.listen(SetupBasicStock.__table__, "after_create", before_setup_basic_stock_insert)
