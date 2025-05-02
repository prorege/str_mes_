# -*- coding: utf-8 -*-

print("module [backend_model.table_base.py] loaded")
from datetime import datetime
from sqlalchemy import DDL, event
from backend_model.database import DBManager
from backend_model.table_common import Companies
from sqlalchemy.dialects.mysql import MEDIUMTEXT

db = DBManager.db


class BaseCode(db.Model):  # 기준정보 - 기준코드(최상위 코드들은 이미 정해져 있고, 그 밑에 트리구조로 등록/수정할 수 있도록)
    __tablename__ = "base_code"
    __table_args__ = {"comment": "기준정보(기준코드)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    code_name = db.Column("code_name", db.String(48), comment="코드명")
    code_class_detail = db.Column("code_class_detail", db.String(256), comment="설명")
    code_order = db.Column("code_order", db.Integer, comment="순서")
    code_depth = db.Column("code_depth", db.Integer, comment="코드 Depth")
    max_depth = db.Column("max_depth", db.Integer, default=2, comment="코드 Depth 최대치")
    parent_code_id = db.Column("parent_code_id", db.Integer, db.ForeignKey("base_code.id"), comment="상위 기준코드 FK")
    fk_company_id = db.Column("fk_company_id", db.Integer, db.ForeignKey(Companies.id), comment="회사테이블 FK")
    items = db.relationship("BaseCode", order_by="asc(BaseCode.code_order)")


class BaseWarehouse(db.Model):  # 기준정보 - 창고관리
    __tablename__ = "base_warehouse"
    __table_args__ = {"comment": "기준정보(창고관리)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    wh_code = db.Column("wh_code", db.String(48), unique=True, comment="창고코드")
    wh_name = db.Column("wh_name", db.String(48), comment="창고명")
    wh_detail = db.Column("wh_detail", db.String(256), comment="설명")
    wh_order = db.Column("wh_order", db.Integer, comment="표시순서")
    use_cost_closing = db.Column("use_cost_closing", db.Boolean, server_default="0", comment="원가마감적용")
    fk_company_id = db.Column("fk_company_id", db.Integer, db.ForeignKey(Companies.id), comment="회사테이블 FK")


class BaseDepartment(db.Model):  # 기준정보 - 부서
    __tablename__ = "base_department"
    __table_args__ = {"comment": "기준정보(부서)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    department_name = db.Column("department_name", db.String(48), comment="부서명")
    wh_code = db.Column("wh_code", db.String(48), db.ForeignKey(BaseWarehouse.wh_code), comment="창고코드")
    depart_head_name = db.Column("depart_head_name", db.String(48), comment="부서장")
    fk_company_id = db.Column("fk_company_id", db.Integer, db.ForeignKey(Companies.id), comment="회사테이블 FK")
    warehouse = db.relationship("BaseWarehouse", foreign_keys=[wh_code])

    def serialize(self):
        json = {
            # property (a)
            "id": self.id,
            "department_name": self.department_name,
            "wh_code": self.wh_code,
            "depart_head_name": self.depart_head_name,
        }
        return json


class BaseEmployee(db.Model):  # 기준정보 - 사원
    __tablename__ = "base_employee"
    __table_args__ = {"comment": "기준정보(사원)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    emp_code = db.Column("emp_code", db.String(48), comment="사원코드")
    emp_name = db.Column("emp_name", db.String(48), comment="사원명")
    emp_order = db.Column("emp_order", db.Integer, comment="표시순서")
    emp_picture_path = db.Column("emp_picture_path", MEDIUMTEXT, comment="사원사진파일데이터")
    emp_sign_path = db.Column("emp_sign_path", MEDIUMTEXT, comment="사원사진파일데이터")
    emp_addr = db.Column("emp_addr", db.String(256), comment="자택주소")
    emp_addr_detail = db.Column("emp_addr_detail", db.String(256), comment="자택상세주소")
    emp_addr_zipcode = db.Column("emp_addr_zipcode", db.String(6), comment="자택우편번호")
    emp_direct_phone = db.Column("emp_direct_phone", db.String(20), comment="직통전화번호")
    emp_ext_phone = db.Column("emp_ext_phone", db.String(20), comment="내선번호")
    emp_mobile = db.Column("emp_mobile", db.String(64), comment="핸드폰번호")
    emp_position = db.Column("emp_position", db.String(20), comment="직급")
    emp_email = db.Column("emp_email", db.String(48), comment="이메일주소")
    emp_joindate = db.Column("emp_joindate", db.DateTime, comment="입사일")
    memo = db.Column("memo", db.String(2048), comment="메모")
    emp_name_en = db.Column("emp_name_en", db.String(48), comment="사원명(영문)")
    emp_gender = db.Column("emp_gender", db.String(10), comment="성별")
    emp_country = db.Column("emp_country", db.String(20), comment="국적")
    resignation_yn = db.Column("resignation_yn", db.Boolean, comment="퇴사가부")
    resignation_date = db.Column("resignation_date", db.DateTime, comment="퇴사일")
    resignation_type = db.Column("resignation_type", db.String(20), comment="퇴사사유")  # (base_code)
    fk_setup_group_auth = db.Column("fk_setup_group_auth", db.Integer, comment="권한그룹 ID FK")  # (setup_group_auth)
    fk_department_id = db.Column("fk_department_id", db.Integer, db.ForeignKey(BaseDepartment.id), comment="내가 소속되어 있는 부서 FK")  # (base_department)
    fk_company_id = db.Column("fk_company_id", db.Integer, db.ForeignKey(Companies.id), comment="회사테이블 FK")

    def excel_import_columns(self):
        return dict(
            output=[
                self.emp_code,
                self.emp_name,
                (self.fk_department_id, BaseDepartment, "department_name", "id"),
                self.emp_addr,
                self.emp_addr_detail,
                self.emp_addr_zipcode,
                self.emp_direct_phone,
                self.emp_ext_phone,
                self.emp_mobile,
                self.emp_position,
                self.emp_email,
                self.emp_joindate,
                self.memo,
                self.emp_name_en,
                self.emp_gender,
                self.emp_country,
                self.resignation_yn,
                self.resignation_date,
                self.resignation_type,
            ],
            key=[self.emp_code, self.fk_company_id],
        )


class BaseClient(db.Model):  # 기준정보 - 거래처관리
    __tablename__ = "base_client"
    __table_args__ = {"comment": "기준정보(거래처관리)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    alias = db.Column("alias", db.String(48), comment="업체약칭")
    name = db.Column("name", db.String(48), comment="업체명")
    address = db.Column("address", db.String(256), comment="주소")
    address_detail = db.Column("address_detail", db.String(256), comment="상세주소")
    zip_code = db.Column("zip_code", db.String(10), comment="우편번호")
    phone = db.Column("phone", db.String(30), comment="대표전화번호")
    fax = db.Column("fax", db.String(30), comment="팩스번호")
    email = db.Column("email", db.String(48), comment="대표 이메일")
    homepage = db.Column("homepage", db.String(128), comment="홈페이지")
    bill_manager = db.Column("bill_manager", db.String(48), comment="계산서 담당자")
    bill_email = db.Column("bill_email", db.String(48), comment="계산서 이메일")
    client_type = db.Column("client_type", db.String(20), comment="업체분류")  # (base_code)
    district_type = db.Column("district_type", db.String(20), comment="지역구분")  # (base_code)
    manager = db.Column("manager", db.String(20), comment="당사담당자")  # (base_employee)
    trade_yn = db.Column("trade_yn", db.Boolean, default=False, comment="거래중지여부")  # 0:정상, 1:중지
    zero_tax_rate_yn = db.Column("zero_tax_rate_yn", db.Boolean, default=0, comment="영세율여부")  # 0:n, 1:y
    before_alias = db.Column("before_alias", db.String(48), comment="변경전 업체약칭")
    after_alias = db.Column("after_alias", db.String(48), comment="변경후 업체약칭")
    corp_number = db.Column("corp_number", db.String(24), comment="법인번호")
    business_number = db.Column("business_number", db.String(24), comment="사업자번호")
    business_name = db.Column("business_name", db.String(48), comment="사업자상호")
    ceo_name = db.Column("ceo_name", db.String(48), comment="대표자명")
    business_status = db.Column("business_status", db.String(48), comment="업태")
    business_sector = db.Column("business_sector", db.String(48), comment="종목")
    name_en = db.Column("name_en", db.String(48), comment="업체명(영문)")
    ceo_name_en = db.Column("ceo_name_en", db.String(48), comment="대표자명(영문)")
    phone_en = db.Column("phone_en", db.String(30), comment="전화번호(국제)")
    fax_en = db.Column("fax_en", db.String(30), comment="팩스번호(국제)")
    address_en = db.Column("address_en", db.String(256), comment="주소(영문)")
    etc = db.Column("etc", db.Text, comment="비고")
    register_id = db.Column("register_id", db.String(48), comment="최초등록자")
    modify_id = db.Column("modify_id", db.String(48), comment="최종수정자")
    last_updated_date = db.Column("last_updated_date", db.DateTime, comment="최종수정일자")
    fk_company_id = db.Column("fk_company_id", db.Integer, db.ForeignKey(Companies.id), comment="회사테이블 FK")

    def excel_import_columns(self):
        return dict(
            output=[
                self.alias,
                self.name,
                self.address,
                self.address_detail,
                self.zip_code,
                self.phone,
                self.fax,
                self.email,
                self.homepage,
                self.bill_manager,
                self.bill_email,
                self.client_type,
                self.district_type,
                self.manager,
                self.trade_yn,
                self.before_alias,
                self.after_alias,
                self.corp_number,
                self.business_number,
                self.business_name,
                self.ceo_name,
                self.business_status,
                self.business_sector,
                self.name_en,
                self.ceo_name_en,
                self.phone_en,
                self.fax_en,
                self.address_en,
                self.etc
            ],
            key=[self.name, self.fk_company_id],
        )


class BaseClientManager(db.Model):  # 기준정보 - 거래처관리 - 거래처담당자
    __tablename__ = "base_client_manager"
    __table_args__ = {"comment": "거래처관리(거래처담당자)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    name = db.Column("name", db.String(48), comment="거래처담당자")
    department = db.Column("department", db.String(48), comment="부서")
    position = db.Column("position", db.String(48), comment="직급")
    mobile = db.Column("mobile", db.String(20), comment="휴대폰번호")
    email = db.Column("email", db.String(48), comment="이메일주소")
    direct_phone = db.Column("name_en", db.String(20), comment="직통전화번호")
    ext_phone = db.Column("ext_phone", db.String(20), comment="내선번호")
    etc = db.Column("etc", db.Text, comment="비고")
    fk_client_id = db.Column("fk_client_id", db.Integer, db.ForeignKey(BaseClient.id), comment="거래처 ID FK")  
    client = db.relationship("BaseClient", foreign_keys=[fk_client_id])# (base_client)


class BaseItem(db.Model):  # 기준정보 - 품목관리
    __tablename__ = "base_item"
    __table_args__ = {"comment": "기준정보(품목관리)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    item_code = db.Column("item_code", db.String(48), unique=True, comment="품목코드")
    item_name = db.Column("item_name", db.String(128), comment="품명")
    item_standard = db.Column("item_standard", db.String(128), comment="규격")
    asset_type = db.Column("asset_type", db.String(48), comment="자산구분")
    item_group = db.Column("item_group", db.String(128), comment="품목 그룹")
    main_category = db.Column("main_category", db.String(48), comment="품목관리 대분류")
    middle_category = db.Column("middle_category", db.String(48), comment="품목관리 중분류")
    sub_category = db.Column("sub_category", db.String(48), comment="품목관리 소분류")
    delivery_date = db.Column("delivery_date", db.String(48), comment="표준 납기일")
    item_detail = db.Column("item_detail", db.String(48), comment="품목설명")
    color_type = db.Column('color_type', db.String(48), comment="지원색상")
    dot_number = db.Column('dot_number', db.String(48), comment="Dot 구성")
    dot_pitch = db.Column('dot_pitch', db.String(48), comment="Dot Pitch")
    module_size = db.Column('module_size', db.String(48), comment="모듈크기")
    dot_size = db.Column('dot_size', db.String(48), comment="필셀크기")
    drive_mode = db.Column('drive_mode', db.String(48), comment="고동 모드")
    in_out_point = db.Column('in_out_point', db.String(48), comment="적용장소")
    brightness = db.Column('brightness', db.String(48), comment="밝기(cd/m2)")
    watt = db.Column('watt', db.String(48), comment="소비전력(w)")
    etc = db.Column("etc", db.Text, comment="비고")
    safety_stock = db.Column("safety_stock", db.Integer, server_default="0", comment="안전재고")
    unit = db.Column("unit", db.String(10), comment="단위")
    sales_price = db.Column("sales_price", db.BigInteger, server_default="0", comment="매출단가")
    purchase_price = db.Column("purchase_price", db.Numeric(12, 2), server_default="0", comment="매입단가")
    cost_price = db.Column("cost_price", db.Numeric(10, 2), server_default="0.00", comment="마감원가")
    note1 = db.Column("note1", db.String(256), comment="참고1")
    note2 = db.Column("note2", db.String(256), comment="참고2")
    item_img = db.Column("item_img", MEDIUMTEXT, comment="품목이미지")
    moq = db.Column("moq", db.Integer, server_default="0", comment="MOQ")
    packing_quantity = db.Column("packing_quantity", db.Integer, comment="포장단위수량")
    transfer_quantity = db.Column("transfer_quantity", db.Integer, comment="이송단위수량")
    import_check = db.Column("import_check", db.Boolean, server_default="0", comment="수입검사")
    shipment_check = db.Column("shipment_check", db.Boolean, server_default="0", comment="출하검사")
    lot_check = db.Column("lot_check", db.Boolean, server_default="0", comment="LOT관리")
    before_item_code = db.Column("before_item_code", db.String(48), comment="변경전품목코드")
    after_item_code = db.Column("after_item_code", db.String(48), comment="변경후품목코드")
    end_of_use = db.Column("end_of_use", db.Boolean, server_default="0", comment="사용종료")
    end_date = db.Column("end_date", db.DateTime, comment="종료일자")
    hs_code = db.Column("hs_code", db.String(128), comment="HSCode")
    register_id = db.Column("register_id", db.String(48), comment="최초등록자")
    modify_id = db.Column("modify_id", db.String(48), comment="최종수정자")
    modify_date = db.Column("modify_date", db.DateTime, comment="최종수정일자")
    bom_yn = db.Column("bom_yn", db.Boolean, server_default="0", comment="BOM 여부")
    fk_manufacturer_client_id = db.Column('fk_manufacturer_client_id', db.Integer, db.ForeignKey(BaseClient.id), comment="제조업체 FK")
    fk_company_id = db.Column("fk_company_id", db.Integer, db.ForeignKey(Companies.id), comment="회사테이블 FK")
    client = db.relationship('BaseClient', foreign_keys=[fk_manufacturer_client_id])
    client_item = db.relationship("BaseClientItem")
    basic_stock = db.relationship("SetupBasicStock")

    def excel_import_columns(self):
        return dict(
            output=[
                self.item_code,
                self.item_name,
                self.item_standard,
                self.end_date,
                self.asset_type,
                self.item_group,
                self.main_category,
                self.middle_category,
                self.sub_category,
                self.delivery_date,
                self.item_detail,
                self.color_type,
                self.dot_number,
                self.dot_pitch,
                self.module_size,
                self.dot_size,
                self.drive_mode,
                self.in_out_point,
                self.brightness,
                self.watt,
                self.etc,
                self.safety_stock,
                self.unit,
                self.sales_price,
                self.purchase_price,
                self.note1,
                self.note2,
                self.item_img,
                self.moq,
                self.packing_quantity,
                self.transfer_quantity,
                self.import_check,
                self.shipment_check,
                self.lot_check,
                self.before_item_code,
                self.after_item_code,
                self.end_of_use,
                self.end_date,
            ],
            key=[self.item_code, self.fk_company_id],
        )


class BaseClientItem(db.Model):
    __tablename__ = "base_client_item"
    __table_args__ = {"comment": "기준정보(품목관리-거래처품목코드)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    client_item_code = db.Column("client_item_code", db.String(48), comment="거래처품번")
    unit_price_type = db.Column("unit_price_type", db.String(48), comment="단가구분")
    unit_price = db.Column("unit_price", db.Numeric(12, 2), comment="단가")
    main_supplier = db.Column("main_supplier", db.Boolean, default=False, comment="주공급업체")
    note = db.Column("note", db.String(256), comment="참고")
    etc = db.Column("etc", db.Text, comment="비고")
    item_code = db.Column("item_code", db.String(48), db.ForeignKey(BaseItem.item_code, onupdate="CASCADE", ondelete="CASCADE"), comment="품목코드")  # (base_item)
    client_id = db.Column("client_id", db.Integer, db.ForeignKey(BaseClient.id), comment="고객 ID")  # (base_client)
    fk_company_id = db.Column("fk_company_id", db.Integer, db.ForeignKey(Companies.id), comment="회사테이블 FK")
    client = db.relationship("BaseClient", foreign_keys=[client_id])
    item = db.relationship("BaseItem", foreign_keys=[item_code])


class BaseDesign(db.Model):
    __tablename__ = "base_design"
    __table_args__ = {"comment": "기준정보(품목관리-도면관리)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    design_number = db.Column("design_number", db.String(48), comment="도면번호")
    registration_date = db.Column("registration_date", db.DateTime, comment="등록일자")
    design_type = db.Column("design_type", db.String(48), comment="설변구분")
    note = db.Column("note", db.String(256), comment="설변사항")
    design_file_name = db.Column("design_file_name", db.String(256), comment="도면파일첨부이름")
    design_file_path = db.Column("design_file_path", db.String(256), comment="도면파일첨부경로")
    design_file = db.Column("design_file", MEDIUMTEXT, comment="파일데이터")
    item_code = db.Column("item_code", db.String(48), db.ForeignKey(BaseItem.item_code, onupdate="CASCADE", ondelete="CASCADE"), comment="품목코드")  # (base_item)
    item = db.relationship("BaseItem", foreign_keys=[item_code])


class BaseProcess(db.Model):  # 기준정보 - 공정관리
    __tablename__ = "base_process"
    __table_args__ = {"comment": "기준정보(공정관리)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    process_code = db.Column("process_code", db.String(48), comment="공정코드")
    process_name = db.Column("process_name", db.String(48), comment="공정명")
    ct = db.Column("ct", db.Integer, comment="C/T")
    unit = db.Column("unit", db.String(10), comment="단위")
    unit_price = db.Column("unit_price", db.Integer, comment="단가")
    etc = db.Column("etc", db.Text, comment="비고")
    fk_company_id = db.Column("fk_company_id", db.Integer, db.ForeignKey(Companies.id), comment="회사테이블 FK")


class BaseBOM(db.Model):  # 기준정보 - BOM관리
    __tablename__ = "base_bom"
    __table_args__ = {"comment": "기준정보(BOM)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    item_id = db.Column("item_id", db.Integer, db.ForeignKey("base_item.id", onupdate='CASCADE', ondelete='CASCADE'), comment="품목코드 ID")  # (base_item)
    bom_depth = db.Column("bom_depth", db.Integer, comment="BOM Depth")
    fk_company_id = db.Column("fk_company_id", db.Integer, db.ForeignKey(Companies.id), comment="회사테이블 FK")
    item = db.relationship("BaseItem", uselist=False)


class BaseBOMLink(db.Model):
    __tablename__ = "base_bom_link"
    __table_args__ = {"comment": "BOM(Link)"}
    link_id = db.Column("link_id", db.Integer, primary_key=True, comment="UID")
    parent_id = db.Column("parent_id", db.Integer, db.ForeignKey("base_bom.id", onupdate='CASCADE', ondelete='CASCADE'), comment="부모 BOM ID FK")
    child_id = db.Column("child_id", db.Integer, db.ForeignKey("base_bom.id", onupdate='CASCADE', ondelete='CASCADE'), comment="자식 BOM ID FK")
    lrate = db.Column("lrate", db.Float, default=0, comment="L/Rate")
    requirement = db.Column("requirement", db.Float, default=0, comment="소요량")
    root_id = db.Column("root_id", db.Integer, comment="최상위 BOM FK")
    consume_yn = db.Column("consume_yn", db.Boolean, default=False, comment="자재소모 여부")
    client_company = db.Column("client_company", db.String(256), comment="주공급업체")
    parent_bom = db.relationship("BaseBOM", foreign_keys=[parent_id])
    child_bom = db.relationship("BaseBOM", foreign_keys=[child_id])


class BaseBOMProcess(db.Model):  # 기준정보 - BOM관리 - 공정관리
    __tablename__ = "base_bom_process"
    __table_args__ = {"comment": "BOM(공정관리)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    process_id = db.Column("process_id", db.Integer, db.ForeignKey("base_process.id"), comment="공정관리 ID FK")  # (base_process)
    bom_id = db.Column("bom_id", db.Integer, db.ForeignKey("base_bom.id", onupdate='CASCADE', ondelete='CASCADE'), comment="BOM ID")  # (base_process)
    check_yn = db.Column("check_yn", db.Boolean, comment="검사여부")
    outsource_yn = db.Column("outsource_yn", db.Boolean, comment="외주발주여부")
    order = db.Column("order", db.Integer, comment="공정순서")
    ct = db.Column("ct", db.Float, comment="C/T")
    price = db.Column("price", db.Integer, comment="단가")

    process = db.relationship("BaseProcess", uselist=False)


class BaseBOMHistory(db.Model):  # 기준정보 - BOM관리 - BOM변경내역관리
    __tablename__ = "base_bom_history"
    __table_args__ = {"comment": "BOM(변경내역관리)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    bom_id = db.Column("bom_id", db.Integer, db.ForeignKey("base_bom.id", onupdate='CASCADE', ondelete='CASCADE'), comment="BOM ID FK")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    manager = db.Column("manager", db.String(48), comment="입력사원")
    detail = db.Column("detail", db.Text, comment="사유(내용)")
    important_yn = db.Column("important_yn", db.Boolean, comment="중요")


class BaseBank(db.Model):  # 기준정보 - 은행관리
    __tablename__ = "base_bank"
    __table_args__ = {"comment": "기준정보(은행관리)"}
    id = db.Column("id", db.Integer, primary_key=True, comment="UID")
    created = db.Column("created", db.DateTime, default=datetime.now, comment="생성시간")
    bank_code = db.Column("bank_code", db.String(48), unique=True, comment="은행코드")
    bank_name = db.Column("bank_name", db.String(128), comment="은행이름")
    bank_address = db.Column("bank_address", db.String(128), comment="은행주소")
    account_number = db.Column("account_number", db.String(128), comment="계좌번호")
    iban_code = db.Column("iban_code", db.String(48), comment="IBAN Code")
    blz_no = db.Column("blz_no", db.String(48), comment="BLZ No")
    swift_code = db.Column("swift_code", db.String(48), comment="SWIFT Code")
    note = db.Column("note", db.String(512), comment="비고")
    fk_company_id = db.Column("fk_company_id", db.Integer, db.ForeignKey(Companies.id), comment="회사테이블 FK")


# ----------------------------------------------------------------------------------------------------------------------
# CREATE TRIGGER

# BOM 추가 시 품목의 BOM 여부 업데이트
after_base_bom_insert = DDL(
    """
DROP TRIGGER IF EXISTS after_base_bom_insert;
CREATE TRIGGER after_base_bom_insert 
AFTER INSERT ON base_bom
FOR EACH ROW
BEGIN
    UPDATE base_item
    SET bom_yn = 1
    WHERE id = NEW.item_id;
END;"""
)
event.listen(BaseBOM.__table__, "after_create", after_base_bom_insert)

# BOM 삭제 시 품목의 BOM 여부 업데이트
after_base_bom_delete = DDL(
    """
DROP TRIGGER IF EXISTS after_base_bom_delete;
CREATE TRIGGER after_base_bom_delete 
AFTER DELETE ON base_bom
FOR EACH ROW
BEGIN
    UPDATE base_item
    SET bom_yn = 0
    WHERE id = OLD.item_id;
END;"""
)
event.listen(BaseBOM.__table__, "after_create", after_base_bom_delete)

# Client 추가
after_base_client_insert = DDL(
    """
DROP TRIGGER IF EXISTS after_base_client_insert;
CREATE TRIGGER after_base_client_insert 
AFTER INSERT ON base_client
FOR EACH ROW
BEGIN
    INSERT INTO setup_basic_balance(created, sales_balance, purchase_balance, fk_company_id, fk_base_client_id) 
    VALUES(now(), 0, 0, NEW.fk_company_id, NEW.id);
END;"""
)
event.listen(BaseClient.__table__, "after_create", after_base_client_insert)

after_base_item_insert = DDL(
"""
DROP TRIGGER IF EXISTS after_base_item_insert;
CREATE TRIGGER after_base_item_insert
AFTER INSERT ON base_item
FOR EACH ROW
BEGIN
    INSERT INTO setup_basic_stock (
        created,
        wh_code,
        item_code,
        basic_stock,
        current_stock,
        available_stock,
        fk_company_id
    )
    SELECT 
        NOW(),
        base_warehouse.wh_code,
        NEW.item_code,
        0,
        0,
        0,
        NEW.fk_company_id
    FROM base_warehouse;
END;
"""
)
event.listen(BaseItem.__table__, "after_create", after_base_item_insert)

after_base_item_delete = DDL(
"""
DROP TRIGGER IF EXISTS after_base_item_delete;
CREATE TRIGGER after_base_item_delete
AFTER DELETE ON base_item
FOR EACH ROW
BEGIN
    DELETE FROM setup_basic_stock WHERE item_code = OLD.item_code;
END;
"""
)
event.listen(BaseItem.__table__, "after_create", after_base_item_delete)

after_base_warehouse_insert = DDL(
"""
DROP TRIGGER IF EXISTS after_base_warehouse_insert;
CREATE TRIGGER after_base_warehouse_insert
AFTER INSERT ON base_warehouse
FOR EACH ROW
BEGIN
    INSERT INTO setup_basic_stock (
        created,
        wh_code,
        item_code,
        basic_stock,
        current_stock,
        available_stock,
        fk_company_id
    )
    SELECT 
        NOW(),
        NEW.wh_code,
        base_item.item_code,
        0,
        0,
        0,
        NEW.fk_company_id
    FROM base_item;
END;
"""
)
event.listen(BaseWarehouse.__table__, "after_create", after_base_warehouse_insert)

after_base_warehouse_delete = DDL(
"""
DROP TRIGGER IF EXISTS after_base_warehouse_delete;
CREATE TRIGGER after_base_warehouse_delete
AFTER DELETE ON base_warehouse
FOR EACH ROW
BEGIN
    DELETE FROM setup_basic_stock WHERE wh_code = OLD.wh_code;
END;
"""
)
event.listen(BaseWarehouse.__table__, "after_create", after_base_warehouse_delete)
