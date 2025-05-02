#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import hashlib
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

print("module [backend_model.database] loaded")


class DBManager:
    db = None

    @staticmethod
    def init(app):
        DBManager.db = SQLAlchemy(app)

    @staticmethod
    def init_db():
        print("-- DBManager init_db()")

        DBManager.db.drop_all()
        DBManager.db.create_all()
        DBManager.insert_init_data()
        # DBManager.insert_dummy_data()

    @staticmethod
    def clear_db():
        print("-- DBManager clear_db()")
        # DBManager.db.drop_all()
        
    @staticmethod
    def insert_init_data():
        print('insert_init_data')
      



        
        '''
        DBManager.insert_dummy_data_common()
        DBManager.insert_dummy_data_code()
        DBManager.insert_dummy_data_menu()
        DBManager.insert_dummy_data_warehouse()
        DBManager.insert_dummy_data_employee()
        DBManager.insert_dummy_data_client()
        DBManager.insert_dummy_data_basic_stock()

        DBManager.insert_dummy_data_item()
        DBManager.insert_dummy_data_project()
        DBManager.insert_dummy_data_group_auth()
        DBManager.insert_dummy_data_process()
        DBManager.insert_dummy_data_shipment_quote()
        DBManager.insert_dummy_data_shipment_order()
        DBManager.insert_dummy_data_shipment_release()
        DBManager.insert_dummy_data_purchase_order_plan()
        DBManager.insert_dummy_data_purchase_order()
        DBManager.insert_dummy_data_pre_purchase_receiving()
        DBManager.insert_dummy_data_purchase_receiving()
        DBManager.insert_dummy_data_stock_etc()
        DBManager.insert_dummy_data_stock_move_request()
        DBManager.insert_dummy_data_stock_move_release()
        '''

    @staticmethod
    def insert_dummy_data():
        print('insert_dummy_data')
        DBManager.insert_dummy_data_code()
        DBManager.insert_dummy_data_menu()

    @staticmethod
    def password_encoder(password):
        pass1 = hashlib.sha1(password).digest()
        pass2 = hashlib.sha1(pass1).hexdigest()
        hashed_pw = "*" + pass2.upper()
        return hashed_pw

    @staticmethod
    def get_random_date():
        end = datetime.utcnow()
        start = end + timedelta(days=-60)

        random_date = start + timedelta(
            # Get a random amount of seconds between `start` and `end`
            seconds=random.randint(0, int((end - start).total_seconds())),
        )

        return random_date

    @staticmethod
    def password_encoder_512(password):
        h = hashlib.sha512()
        h.update(password.encode('utf-8'))
        return h.hexdigest()

    # 셋업관리
    @staticmethod
    def insert_dummy_data_common():
        from backend_model.table_common import Companies, Users

        comp = Companies()
        comp.name = "에스텍아이앤씨(주)"
        comp.address = "경기도 용인시 처인구 모현읍 곡현로717번길 23-8"
        comp.zip_code = ""
        comp.phone = "031-338-1285"
        comp.fax = "031)338-0118"
        comp.email = "onetech114@naver.com"
        comp.homepage = "http://www.onetechnology.co.kr/"
        comp.bill_manager = "홍길동"
        comp.bill_email = ""
        comp.system_start_date = DBManager.get_random_date()
        comp.basic_stock_date = DBManager.get_random_date()
        comp.basic_balance_date = DBManager.get_random_date()
        comp.corp_number = ""
        comp.business_number = "142-81-00754"
        comp.ceo_name = "김종달"
        comp.business_status = "제조업"
        comp.business_sector = "옥외,전시광고"
        comp.name_en = "One Technology"
        comp.ceo_name_en = "Kim, Jongdal"
        comp.phone_en = "+82-031-338-1285"
        comp.fax_en = "+82-031-338-0118"
        comp.address_en = ""
        comp.register_id = "stechadmin"
        comp.modify_id = ""
        comp.last_updated_date = DBManager.get_random_date()
        DBManager.db.session.add(comp)
        DBManager.db.session.commit()

        user = Users()
        user.user_id = "stechadmin"
        user.user_pw = DBManager.password_encoder_512('1234')
        user.user_name = "관리자"
        user.user_type = 1
        user.phone = "010-1234-5678"
        user.email = "admin@signtelecom.com"
        user.fk_company_id = 1
        DBManager.db.session.add(user)
        '''
        user = Users()
        user.user_id = "emp001"
        user.user_pw = DBManager.password_encoder_512('1234')
        user.user_name = "사원명001"
        user.user_type = 2
        user.phone = "010-1234-5678"
        user.email = "signuser1@signtelecom.com"
        user.fk_company_id = 1
        DBManager.db.session.add(user)

        user = Users()
        user.user_id = "emp002"
        user.user_pw = DBManager.password_encoder_512('1234')
        user.user_name = "사원명002"
        user.user_type = 2
        user.phone = "010-1234-5678"
        user.email = "signuser2@signtelecom.com"
        user.fk_company_id = 1
        DBManager.db.session.add(user)
        '''
        DBManager.db.session.commit()

    @staticmethod
    def add_root_menu(name, path, enabled, initial_enabled=False):
        from backend_model.table_setup import SetupMenu
        menu_count = DBManager.db.session.query(
            SetupMenu
        ).filter(
            SetupMenu.menu_depth == 1
        ).count()

        menu = SetupMenu()
        menu.menu_name = name
        menu.fk_company_id = 1
        menu.parent_id = -1
        menu.menu_depth = 1
        menu.menu_order = menu_count + 1
        menu.menu_enable = enabled
        menu.path = path
        menu.menu_initial_enable = initial_enabled
        DBManager.db.session.add(menu)
        DBManager.db.session.commit()
        return menu.id

    @staticmethod
    def add_child_menu(name, parent_id, path, initial, enabled, initial_enabled=False):
        from backend_model.table_setup import SetupMenu
        menu_count = DBManager.db.session.query(
            SetupMenu
        ).filter(
            SetupMenu.menu_depth == 2
        ).filter(
            SetupMenu.parent_id == parent_id
        ).count()

        menu = SetupMenu()
        menu.menu_name = name
        menu.fk_company_id = 1
        menu.menu_initial = initial
        menu.parent_id = parent_id
        menu.menu_depth = 2
        menu.menu_order = menu_count + 1
        menu.path = path
        menu.menu_enable = enabled
        menu.menu_initial_enable = initial_enabled
        DBManager.db.session.add(menu)
        DBManager.db.session.commit()

    # 메뉴관리
    @staticmethod
    def insert_dummy_data_menu():
         # 모니터링(1)
        parent_id = DBManager.add_root_menu('모니터링', '/monitoring', False)
        DBManager.add_child_menu('생산진행상황', parent_id, '/monitoring/produce-progress', '', False)
        DBManager.add_child_menu('재고현황', parent_id, '/monitoring/store-status', '', False)
        DBManager.add_child_menu('프로젝트현황', parent_id, '/monitoring/project', '', False)
        DBManager.add_child_menu('품질현황', parent_id, '/monitoring/quality', '', False)
        DBManager.add_child_menu('외근-출장현황', parent_id, '/monitoring/trip-log-status', '', False)
        
        parent_id = DBManager.add_root_menu('QR관리', '/qr', True)
        DBManager.add_child_menu('QR관리', parent_id, '/qr/qr', '', True)
        DBManager.add_child_menu('LOT관리', parent_id, '/qr/lot', '', True)

        parent_id = DBManager.add_root_menu('출하관리', '/shipment', True, True)
        DBManager.add_child_menu('견적', parent_id, '/shipment/quote', 'QUOTE', True, True)
        DBManager.add_child_menu('견적(수기)', parent_id, '/shipment/quote-manual', 'QUOMA', True, True)
        DBManager.add_child_menu('수주', parent_id, '/shipment/order', 'ORDER', True, True)
        DBManager.add_child_menu('출고', parent_id, '/shipment/release', 'RELSE', True, True)
        DBManager.add_child_menu('출고반품', parent_id, '/shipment/release-return', 'RELRT', True, True)
        DBManager.add_child_menu('매출계산서', parent_id, '/shipment/sales-statement', 'SLSTT', True, True)
        DBManager.add_child_menu('입금', parent_id, '/shipment/deposit', 'DEPST', True, True)
        DBManager.add_child_menu('가출고', parent_id, '/shipment/lend', 'LEND', True, True)
        DBManager.add_child_menu('가출고회수', parent_id, '/shipment/retrieve', 'RETRI', True, True)
        DBManager.add_child_menu('출하(현장)', parent_id, '/shipment/on-site', '', False)
        DBManager.add_child_menu('견적현황', parent_id, '/shipment/quote/status', '', True)
        DBManager.add_child_menu('수주현황', parent_id, '/shipment/order/status', '', True)
        DBManager.add_child_menu('수주현황(관리자)', parent_id, '/shipment/order-admin/status', '', True)
        DBManager.add_child_menu('출고현황', parent_id, '/shipment/release/status', '', True)
        DBManager.add_child_menu('출고요청현황', parent_id, '/shipment/release-request/status', '', True)
        DBManager.add_child_menu('매출계산서현황', parent_id, '/shipment/sales-statement/status', '', True)
        DBManager.add_child_menu('입금현황', parent_id, '/shipment/deposit/status', '', True)
        DBManager.add_child_menu('견적-수주현황', parent_id, '/shipment/quote-to-order/status', '', True)
        DBManager.add_child_menu('수주-출고현황', parent_id, '/shipment/order-to-release/status', '', True)
        DBManager.add_child_menu('출고-계산서현황', parent_id, '/shipment/release-to-sales/status', '', True)
        DBManager.add_child_menu('계산서-입금현황', parent_id, '/shipment/sales-to-deposit/status', '', True)
        DBManager.add_child_menu('출고반품현황', parent_id, '/shipment/release-return/status', '', True)
        DBManager.add_child_menu('매출원장', parent_id, '/shipment/sales-balance-item/status', '', True)
        DBManager.add_child_menu('매출잔액장', parent_id, '/shipment/sales-balance/status', '', True)

        parent_id = DBManager.add_root_menu('구매관리', '/purchase', True, True)
        DBManager.add_child_menu('발주계획', parent_id, '/purchase/order-plan', 'ORDPL', True, True)
        DBManager.add_child_menu('발주', parent_id, '/purchase/order', 'ORDER', True, True)
        DBManager.add_child_menu('가입고', parent_id, '/purchase/pre-receiving', 'PRERE', True, True)
        DBManager.add_child_menu('입고', parent_id, '/purchase/receiving', 'RECIV', True, True)
        DBManager.add_child_menu('입고반품', parent_id, '/purchase/receiving-return', 'RECRT', True, True)
        DBManager.add_child_menu('발주계획현황', parent_id, '/purchase/order-plan-status', '', True)
        DBManager.add_child_menu('발주현황', parent_id, '/purchase/order-status', '', True)
        DBManager.add_child_menu('가입고현황', parent_id, '/purchase/pre-receiving-status', '', True)
        DBManager.add_child_menu('입고현황', parent_id, '/purchase/receiving-status', '', True)
        DBManager.add_child_menu('발주-가입고현황', parent_id, '/purchase/order-to-prereceiving-status', '', True)
        DBManager.add_child_menu('발주-입고현황', parent_id, '/purchase/order-receiving-status', '', True)
        DBManager.add_child_menu('가입고-입고현황', parent_id, '/purchase/prereceiving-to-receiving-status', '', True)
        DBManager.add_child_menu('입고반품현황', parent_id, '/purchase/receiving-return-status', '', True)
        DBManager.add_child_menu('발주계획-발주현황', parent_id, '/purchase/order-receiving-status_', '', True) # 감리를 위한 임시 화면
        DBManager.add_child_menu('매입계산서', parent_id, '/purchase/statement', 'PURST', True, True)
        DBManager.add_child_menu('결재', parent_id, '/purchase/payment', 'PURPT', True, True)
        DBManager.add_child_menu('매입원장', parent_id, '/purchase/balance-item-status', '', True)
        DBManager.add_child_menu('매입잔액장', parent_id, '/purchase/balance-status', '', True)

        parent_id = DBManager.add_root_menu('재고관리', '/stock', True, True)
        DBManager.add_child_menu('기초재고관리', parent_id, '/stock/basic', 'STOCK', False, True)
        DBManager.add_child_menu('기타입출고', parent_id, '/stock/etc', 'ETCRR', True, True)
        DBManager.add_child_menu('재고이동요청', parent_id, '/stock/move-request', 'STKMV', True, True)
        DBManager.add_child_menu('재고이동출고', parent_id, '/stock/move-release', 'STRELE', True, True)
        DBManager.add_child_menu('기타입출고현황', parent_id, '/stock/etc-status', '', True)
        DBManager.add_child_menu('재고이동요청현황', parent_id, '/stock/move-request-status', '', True)
        DBManager.add_child_menu('재고이동출고현황', parent_id, '/stock/move-release-status', '', True)
        DBManager.add_child_menu('재고조회', parent_id, '/stock/stock-status', '', True)
        DBManager.add_child_menu('재고금액', parent_id, '/stock/stock-price', '', True)
        DBManager.add_child_menu('수불집계', parent_id, '/stock/receive-payment-status', '', True)
        DBManager.add_child_menu('사급자재입고', parent_id, '/stock/stock-correction', '', True)
        DBManager.add_child_menu('사급자재입고현황', parent_id, '/stock/stock-correction-status', '', True)
        DBManager.add_child_menu('상품수불장', parent_id, '/stock/stock-item-status', '', True)
        DBManager.add_child_menu('재고보정', parent_id, '/stock/etc_', '', True) # 감리를 위한 임시 화면
        DBManager.add_child_menu('재고보정현황', parent_id, '/stock/etc_-status', '', True) # 감리를 위한 임시 화면

        parent_id = DBManager.add_root_menu('품질관리', '/quality', True)
        DBManager.add_child_menu('검사등록관리', parent_id, '/quality/test-registration', 'QULTY', True)
        DBManager.add_child_menu('검사등록현황', parent_id, '/quality/test-registration-status', '', True)
        DBManager.add_child_menu('부적합조치등록', parent_id, '/quality/nonconformance-action', 'NOCOF', True)
        DBManager.add_child_menu('부적합조치현황', parent_id, '/quality/nonconformance-action-status', '', True)
        DBManager.add_child_menu('측정장비등록', parent_id, '/quality/measuring-equipment', 'EQMNT', True)
        DBManager.add_child_menu('검사기준등록', parent_id, '/quality/qa-standard', 'QASTD', True)
        DBManager.add_child_menu('품질관리현황', parent_id, '/quality/test-registration-status_', '', True)

        parent_id = DBManager.add_root_menu('생산관리', '/produce', True, True)
        DBManager.add_child_menu('생산계획', parent_id, '/produce/plan', 'PPLAN', True, True)
        DBManager.add_child_menu('소요량계산', parent_id, '/produce/measure-requirement', '', True)
        DBManager.add_child_menu('작업지시', parent_id, '/produce/work-order', 'WKODR', True, True)
        DBManager.add_child_menu('생산입고', parent_id, '/produce/performance-registration', 'PERPM', True, True)
        DBManager.add_child_menu('생산계획현황', parent_id, '/produce/plan-status', '', True)
        DBManager.add_child_menu('작업지시현황', parent_id, '/produce/work-order-status', '', True)
        DBManager.add_child_menu('생산입고현황', parent_id, '/produce/performance-registration-status', '', True)
        DBManager.add_child_menu('작지-입고현황', parent_id, '/produce/work-order-receiving-status', '', True)
        DBManager.add_child_menu('공정실적등록현황', parent_id, '/produce/process-performance-status', '', True)

        parent_id = DBManager.add_root_menu('프로젝트관리', '/project', True, True)
        DBManager.add_child_menu('영업건등록', parent_id, '/project/business', '', True)
        DBManager.add_child_menu('프로젝트등록', parent_id, '/project/registration', 'PROJT', True, True)
        DBManager.add_child_menu('실행계획등록', parent_id, '/project/excution-plan', 'EXCPL', True, True)
        DBManager.add_child_menu('영업건현황', parent_id, '/project/business-status', '', True)
        DBManager.add_child_menu('프로젝트현황', parent_id, '/project/status', '', True)
        DBManager.add_child_menu('실행계획현황', parent_id, '/project/excution-plan-status', '', True)
        DBManager.add_child_menu('공지사항', parent_id, '/project/notice', '', True)
        DBManager.add_child_menu('일정관리', parent_id, '/project/schedule', '', True)
        DBManager.add_child_menu('자료등록', parent_id, '/project/resource', '', True)
        DBManager.add_child_menu('자료등록', parent_id, '/project/resource', '', True)
        DBManager.add_child_menu('외근-출장관리', parent_id, '/project/business-trip-log', '', True)
        DBManager.add_child_menu('외근-출장관리현황', parent_id, '/project/business-trip-log-status', '', True)
        DBManager.add_child_menu('해피콜관리', parent_id, '/project/happy-call', '', True)
        DBManager.add_child_menu('해피콜현황', parent_id, '/project/happy-call-status', '', True)
        DBManager.add_child_menu('실행계획발주보내기', parent_id, '/project/excution-plan-order', '', True)

        parent_id = DBManager.add_root_menu('EIS(경영자정보)', '/eis', False)
        DBManager.add_child_menu('매출실적', parent_id, '/eis/sales', '', False)
        DBManager.add_child_menu('구매실적', parent_id, '/eis/purchase', '', False)
        DBManager.add_child_menu('생산실적', parent_id, '/eis/production', '', False)
        DBManager.add_child_menu('프로젝트실적', parent_id, '/eis/project', '', False)

        parent_id = DBManager.add_root_menu('기준정보', '/base', True)
        DBManager.add_child_menu('기준코드', parent_id, '/base/code', '', True)
        DBManager.add_child_menu('부서/사원', parent_id, '/base/employee', '', True)
        DBManager.add_child_menu('창고관리', parent_id, '/base/warehouse', 'WAHUS', True)
        DBManager.add_child_menu('거래처관리', parent_id, '/base/client', 'CLINT', True)
        DBManager.add_child_menu('품목관리', parent_id, '/base/item', 'ITEM', True, True)
        DBManager.add_child_menu('공정관리', parent_id, '/base/process', 'PROCS', True)
        DBManager.add_child_menu('BOM관리', parent_id, '/base/bom', 'BOM', True)
        DBManager.add_child_menu('은행관리', parent_id, '/base/bank', 'BK', True)

        parent_id = DBManager.add_root_menu('공통관리', '/common', True)
        DBManager.add_child_menu('셋업관리', parent_id, '/common/setup', '', True)
        DBManager.add_child_menu('메뉴관리', parent_id, '/common/menu', '', True)
        DBManager.add_child_menu('권한그룹관리', parent_id, '/common/group/auth', '', True)
        DBManager.add_child_menu('코드변경관리', parent_id, '/common/code', '', False)
        DBManager.add_child_menu('통제관리', parent_id, '/common/control', '', False)

        parent_id = DBManager.add_root_menu('KPI지표', '/kpi', True)
        DBManager.add_child_menu('제조리드타임', parent_id, '/kpi/produce-leadtime', '', True)
        DBManager.add_child_menu('제품원가', parent_id, '/kpi/product-cost', '', True)
        DBManager.add_child_menu('수주-출하리드타임', parent_id, '/kpi/order-to-release-leadtime', '', True)
        DBManager.add_child_menu('불량률현황', parent_id, '/kpi/defective-rate-status', '', True)
        DBManager.add_child_menu('Claim 건 수', parent_id, '/kpi/claim', '', True) # 감리를 위한 임시 화면
        DBManager.add_child_menu('수주-출하리드타임', parent_id, '/kpi/order-to-release-leadtime-chart', '', True) # 감리를 위한 임시 화면

        parent_id = DBManager.add_root_menu('원가관리', '/cost', True)
        DBManager.add_child_menu('원가마감관리', parent_id, '/cost/closing', '', True)
        DBManager.add_child_menu('품목별매출이익현황', parent_id, '/cost/profit-stock-status', '', True)
        DBManager.add_child_menu('생산매출원가분석현황', parent_id, '/cost/produce-sales-cost-status', '', True)
        DBManager.add_child_menu('매출이익현황', parent_id, '/cost/profit-status', '', True)
        DBManager.add_child_menu('원가마감 재고수불집계', parent_id, '/cost/closing-receive-payment-status', '', True)
        DBManager.add_child_menu('원가 재고수불장', parent_id, '/cost/stock-item-status', '', True)
        DBManager.add_child_menu('품목별 마감재고', parent_id, '/cost/closing-stock-status', '', True)
        DBManager.add_child_menu('품목그룹별 마감재고', parent_id, '/cost/closing-stock-group-status', '', True)
        DBManager.add_child_menu('출고원가보정', parent_id, '/cost/correction', '', True)

        parent_id = DBManager.add_root_menu('수입관리', '/import', True)
        DBManager.add_child_menu('Purchase-Order', parent_id, '/import/purchase-order', '', True)
        DBManager.add_child_menu('Shipment', parent_id, '/import/shipment', '', True)
        DBManager.add_child_menu('Clearance', parent_id, '/import/clearance', '', True)
        DBManager.add_child_menu('Credit', parent_id, '/import/credit', '', True)
        DBManager.add_child_menu('결재등록', parent_id, '/import/approval', '', True)
        DBManager.add_child_menu('수입결재비용', parent_id, '/import/approval-cost', '', True)
        DBManager.add_child_menu('수입통관비용', parent_id, '/import/clearance-cost', '', True)

        parent_id = DBManager.add_root_menu('수출관리', '/export', True)
        DBManager.add_child_menu('Sales-Order', parent_id, '/export/sales-order', 'ESORDER', True)
        DBManager.add_child_menu('Comm-Invoice', parent_id, '/export/comm-invoice', 'CINVOICE', True)
        DBManager.add_child_menu('Sales-Order-Status', parent_id, '/export/sales-order/status', '', True)
        DBManager.add_child_menu('Comm-Invoice-Status', parent_id, '/export/comm-invoice/status', '', True)

        parent_id = DBManager.add_root_menu('전자결재', '/approval', True)
        DBManager.add_child_menu('전자결재관리', parent_id, '/approval/management', '', True)
    # 권한그룹관리
    @staticmethod
    def insert_dummy_data_group_auth():
        from backend_model.table_setup import SetupGroup, SetupGroupAuth

        group = SetupGroup()
        group.fk_company_id = 1
        group.group_name = "전체권한그룹"
        group.group_detail = "전체권한부여"
        DBManager.db.session.add(group)

        group = SetupGroup()
        group.fk_company_id = 1
        group.group_name = "읽기권한그룹"
        group.group_detail = "읽기권한부여"
        DBManager.db.session.add(group)

        DBManager.db.session.commit()

        for i in range(1, 69):
            ga = SetupGroupAuth()
            ga.fk_group_id = 1
            ga.fk_menu_id = i
            ga.menu_auth = 63
            DBManager.db.session.add(ga)

            ga = SetupGroupAuth()
            ga.fk_group_id = 2
            ga.fk_menu_id = i
            ga.menu_auth = 48
            DBManager.db.session.add(ga)

        DBManager.db.session.commit()

    @staticmethod
    def add_basic_stock(item_code, warehouse_code):
        stock = int(random.randrange(10, 1000))
        unit_price = int(random.randrange(10000, 100000))

        from backend_model.table_setup import SetupBasicStock
        basic_stock = SetupBasicStock()
        basic_stock.wh_code = warehouse_code
        basic_stock.item_code = item_code
        basic_stock.basic_stock = stock
        basic_stock.current_stock = stock
        basic_stock.available_stock = stock
        basic_stock.item_unit_price = unit_price
        basic_stock.item_price = stock * unit_price
        basic_stock.etc = '비고'
        basic_stock.fk_company_id = 1
        DBManager.db.session.add(basic_stock)
        DBManager.db.session.commit()

    # 기초재고관리
    @staticmethod
    def insert_dummy_data_basic_stock():
        DBManager.add_basic_stock('ITEM-001', 'WH01')
        DBManager.add_basic_stock('ITEM-002', 'WH01')
        DBManager.add_basic_stock('ITEM-001', 'WH02')

    # 기준코드
    @staticmethod
    def insert_dummy_data_code():
        from backend_model.table_base import BaseCode

        items_list = [
            ["품목분류", "대분류", "중분류", "소분류"],
            ["자산구분", "제품", "반제품", "원자재", "부자재"],
            ["직급", "대표", "전무", "상무", "이사", "본부장", "부장", "차장", "과장", "대리", "주임", "반장", "사원"],
            ["성별", "남", "여"],
            ["국적", "대한민국", "미국", "베트남"],
            ["퇴사사유", "일신상", "이직"],
            ["업체분류", "공급업체", "고객업체", "협력업체", "대리점", "매출처", "매입처", "매입/매출"],
            ["지역구분", "경기도", "서울", "충청", "경상", "전라", "강원", "제주도"],
            ["단위", "EA", "SET", "PC", "PCS", "일", "시간", "분"],
            ["단가구분", "매입단가", "매출단가", "일반단가", "프로모션단가"],
            ["공정코드", "조립", "절단"],
            ["견적구분", "일반견적", "재견적"],
            ["부가세구분", "포함", "별도", "영세"],
            ["결재조건", "납품후현금결재", "납품후월말결재"],
            ["납품기한", "발주후일주일", "ASAP"],
            ["납품장소", "당사지정장소", "당사창고"],
            ["수주구분", "일반수주", "프로젝트수주"],
            ["출고구분", "일반출고", "프로젝트출고"],
            ["발주구분", "일반발주", "프로젝트발주", "재발주"],
            ["입고구분", "일반입고", "프로젝트입고", "재입고"],
            ["보증종류", "계약보증", "선금보증", "하자보증", "기타보증"],
            ["보험종류", "고용산재", "건강보험", "국민연금"],
            ["수금구분", "계약금액", "중도금", "잔금"],
            ["계약종류", "1차계약", "2차계약", "3차계약"],
            ["발행상태", "발행", "미발행"],
            ["개시요청", "O", "X"],
            ["입출고유형", "입고", "출고"],
            ["불량유형", "납땜불량", "하네스불량", "성능불량_ON", "성능불량_OFF"],
            ["조치내용", "재작업", "폐기처리"],
            ["현장공정담당자", "사원명1"],
            ["검사구분", "외관", "치수"],
            ["검사항목", "전장", "무게"],
            ["측정단위", "mm", "kg"],
            ["검사방법", "캘리퍼스", "전자저울"],
            ["입력구분", "텍스트", "숫자"],
            ["발행구분", "선발행", "역발행", "역발행+선발행", "정발행", "정발행+선발행"],
            ["계산서유형", "과세매출", "비과세", "영세"],
            ["결재유형", "청구", "영수"],
            ["본지점구분", "본점발행", "지점발행"],
            ["입금형태", "은행입금", "어음", "전자어음", "전자예금"],
            ["설변구분", "신규", "설변", "개선", "중단"],
            ["Destination", "INCHEON AIRPORT", "INCHEON PORT", "PUSAN PORT", "SHANHAI PORT", "MAKER'S TO BE FINAL"],
            ["ValidPeriod", "ONE MONTH", "TWO MONTH"],
            ["Insurance", "내자", "외자", "무한", "유한"],
            ["Delivery", "PAYMENT NET IN ADVANCE", "PREVIOUS SHIPMENT TO THE PAYMENT", "RIGHT AFTER RECEIPT OF THE L/C", "RIGHT AFTER RECEIPT OF THE PAYMENT", "WITHIN 30 DAYS AFTER RECEIPT OF YOUR ORDER", "WITHIN 4 WEEKS AFTER RECEIPT OF THE PAYMENT", "WITHIN 8 WEEKS AFTER RECEIPT OF THE L/C"],
            ["Origin", "CHINA", "ENGLAND", "F.O.B. CHINA PORT", "FRANCE", "GERMANY", "HONG KONG", "ITALY", "JAPAN", "JAPNA OR CHINA", "KOREA", "MEXICO", "SINGAPORE", "SWITZERLAND", "U.S.A", "U.S.A/MEXICO"],
            ["Packing", "EXPORT STANDARD PACKING", "STANDARD PACKING"],
            ["Pay Terms", "BY 60 DAYS NET AFTER YOUR SHIPMENT", "BY 90 DAYS NET AFTER YOUR SHIPMENT", "BY AN IRREVOCABLE AT SIGHT L/C", "BY BANK TRANSFER (T/T)", "BY BILLS DRAWN AT USANCE L/C", "BY CHECK BEFORE RECEIVING", "WITHIN 180 DAYS NET AFTER RECEIPT OF THE INVOICE", "WITHIN 90 DAYS NET AFTER RECEIPT OF THE INVOICE", "WITHIN 60 DAYS NET AFTER RECEIPT OF THE INVOICE"],
            ["Pay Period", "COD 60 day"],
            ["Price Terms", "C & F KIMPO AIRPORT", "C&F INCHEON AIRPORT", "C&F PUSAN PORT", "C.I.F. CHINA PORT", "C.I.F. INCHEON AIRPORT", "C.I.F. PUSAN PORT", "EX-WORKS FACTORY", "EX-WORKS LOEHNE", "F.O.B, JAPAN PORT", "F.O.B. CHINA PORT", "F.O.B. ENGLAND AIRPORT", "F.O.B. FRENCH AIRPORT", "F.O.B. GERMAN AIRPORT", "F.O.B. GERMAN PORT", "F.O.B. HONGKONG AIRPORT", "F.O.B. ITALIAN AIRPORT", "F.O.B. JAPANESE AIRPORT", "F.O.B. JAPANESE OR HONGKONG AIRPORT", "F.O.B. SINGAPORE AIRPORT", "F.O.B. SINGAPORE PORT", "F.O.B. U.S.A. AIRPORT", "F.O.B. U.S.A. AIRPORT/FACTORY", "F.O.B. U.S.A. FACTORY", "F.O.B. ZURICH AIRPORT"],
            ["AdvBank", "AdvBank"],
            ["Ship Port", "CHINA AIRPORT", "CHINA PORT", "ENGLAND AIRPORT", "FRENCH AIRPORT", "FRENCH PORT", "GERMAN AIRPORT", "GERMAN PORT", "HONG KONG AIRPORT", "ITALIAN AIRPORT", "JAPAN OR HONGKONG AIRPORT", "JAPAN PORT", "JAPANESE AIRPORT", "SINGAPORE AIRPORT", "SINGAPORE PORT", "SWEDEN PORT", "SWITZERLAND AIRPORT", "U.S.A. AIRPORT", "ZURICH AIRPORT"],
            ["Currency", "CHF", "CNY", "EUR", "GBP", "JPY", "KRW", "SGD", "USD", "WON"],
            ["CurrencyType", "CHF", "DM", "EUR", "HKD", "JPY", "KRW", "SGD", "USD"],
            ["Inspection", "MAKER'S TO BE FINAL"],
            ["Payment", "Payment"],
            ["계정과목", "계정과목1", "계정과목2", "계정과목3"],
            ["지불방법", "지불방법1", "지불방법2", "지불방법3"],
            ["적요", "적요1", "적요2", "적요3"],
            ["비용구분", "수입B/L비용", "수입통관비용"],
            ["현재단계", "신규", "제안", "견적", "보류"],
            ["진행현황", "계약", "진행", "완료"],
            ["진행단계", "영업", "계약", "취소"],
            ["중요", "일반", "중요"],
            ["진행방법", "전화", "방문", "이메일"],
            ["업체구분", "감리", "감독", "파트너"],
            ["품목그룹", "LED 모듈", "전원 모듈", "콘트롤러", "카메라", "제어함체", "경광등", "DID모니터", "컴퓨터", "광 장비", "써지보호기", "차단기", "Relay", "일반모니터", "UPS", "이더넷 스위치", "영상장비", "접지부품", "랙 자재", "VMS 제어기", "제어기(접점,전원)", "구조물", "S/W 구독/구매", "잡자재", "통신장비", "기타부품"],
            ["결재상태", "승인", "진행", "반려"],
            ["경비내역"],
            ["유효기간"],
            ["보증기간"],
            ["인도조건"],
            ["품명"],
        ]

        i = 1
        parent_id = 1
        for items in items_list:
            bc = BaseCode()
            bc.code_name = bc.code_class_detail = items[0]
            bc.code_order = i
            bc.code_depth = 1
            bc.max_depth = 4 if i == 1 else 2
            bc.parent_code_id = None
            bc.fk_company_id = 1
            DBManager.db.session.add(bc)
            j = 1
            for item in items[1:]:
                bc = BaseCode()
                bc.code_name = bc.code_class_detail = item
                bc.code_order = j
                bc.code_depth = 2
                bc.max_depth = 4 if i == 1 else 2
                bc.parent_code_id = parent_id
                bc.fk_company_id = 1
                DBManager.db.session.add(bc)
                j += 1
            parent_id += j
            i += 1

        # bc = BaseCode()
        # bc.code_name = bc.code_class_detail = "품목중1"
        # bc.code_order = 1
        # bc.code_depth = 3
        # bc.max_depth = 3
        # bc.parent_code_id = 2
        # bc.fk_company_id = 1
        # DBManager.db.session.add(bc)

        # bc = BaseCode()
        # bc.code_name = bc.code_class_detail = "품목중2"
        # bc.code_order = 1
        # bc.code_depth = 3
        # bc.max_depth = 3
        # bc.parent_code_id = 3
        # bc.fk_company_id = 1
        # DBManager.db.session.add(bc)

        # bc = BaseCode()
        # bc.code_name = bc.code_class_detail = "품목중3"
        # bc.code_order = 1
        # bc.code_depth = 3
        # bc.max_depth = 3
        # bc.parent_code_id = 4
        # bc.fk_company_id = 1
        # DBManager.db.session.add(bc)

        # bc = BaseCode()
        # bc.code_name = bc.code_class_detail = "품목소1"
        # bc.code_order = 1
        # bc.code_depth = 4
        # bc.max_depth = 3
        # bc.parent_code_id = parent_id
        # bc.fk_company_id = 1
        # DBManager.db.session.add(bc)

        # bc = BaseCode()
        # bc.code_name = bc.code_class_detail = "품목소2"
        # bc.code_order = 1
        # bc.code_depth = 4
        # bc.max_depth = 3
        # bc.parent_code_id = parent_id + 1
        # bc.fk_company_id = 1
        # DBManager.db.session.add(bc)

        # bc = BaseCode()
        # bc.code_name = bc.code_class_detail = "품목소3"
        # bc.code_order = 1
        # bc.code_depth = 4
        # bc.max_depth = 3
        # bc.parent_code_id = parent_id + 2
        # bc.fk_company_id = 1
        # DBManager.db.session.add(bc)

        DBManager.db.session.commit()

    @staticmethod
    def add_warehouse(warehouse_code, warehouse_name):
        from backend_model.table_base import BaseWarehouse
        row_count = DBManager.db.session.query(
            BaseWarehouse
        ).count()

        warehouse = BaseWarehouse()
        warehouse.wh_code = warehouse_code
        warehouse.wh_name = warehouse_name
        warehouse.wh_order = row_count + 1
        warehouse.fk_company_id = 1
        DBManager.db.session.add(warehouse)
        DBManager.db.session.commit()

    # 창고관리
    @staticmethod
    def insert_dummy_data_warehouse():
        DBManager.add_warehouse('WH01', '자재창고')
        DBManager.add_warehouse('WH02', '제품창고')
        DBManager.add_warehouse('WH03', '현장창고')
        DBManager.add_warehouse('WH04', '불량창고')

    # 품목관리
    @staticmethod
    def insert_dummy_data_item():
        from backend_model.table_base import BaseItem

        for i in range(1, 100):
            idx_str = str(i).zfill(3)
            item = BaseItem()
            item.fk_company_id = 1
            item.item_code = "ITEM-" + idx_str
            item.item_name = "아이템-" + idx_str
            item.item_standard = "규격"
            item.asset_type = "제품"
            item.main_category = "품목대1"
            item.middle_category = "품목중1"
            item.sub_category = "품목소1"
            item.delivery_date = DBManager.get_random_date()
            item.item_detail = "품목설명"
            item.safety_stock = int(random.randrange(10, 1000))
            item.unit = "EA"
            item.sales_price = int(random.randrange(10000, 1000000))
            item.purchase_price = int(random.randrange(10000, 1000000))
            item.note1 = "참고1"
            item.note2 = "참고2"
            item.item_img_path = ""
            item.moq = int(random.randrange(10, 100))
            item.packing_quantity = int(random.randrange(10, 1000))
            item.transfer_quantity = int(random.randrange(10, 1000))
            item.import_check = int(random.randrange(10, 100)) % 2
            item.shipment_check = int(random.randrange(10, 100)) % 2
            item.before_item_code = "ITEM-" + idx_str
            item.after_item_code = "ITEM-" + idx_str
            item.end_of_use = int(random.randrange(10, 100)) % 2
            item.end_date = DBManager.get_random_date()
            item.register_id = "stechadmin"
            item.modify_id = "stechadmin"
            item.modify_date = DBManager.get_random_date()

            DBManager.db.session.add(item)
        DBManager.db.session.commit()

    @staticmethod
    def add_department(department_name, warehouse_code, head_name):
        from backend_model.table_base import BaseDepartment
        department = BaseDepartment()
        department.department_name = department_name
        department.wh_code = warehouse_code
        department.depart_head_name = head_name
        department.fk_company_id = 1
        DBManager.db.session.add(department)
        DBManager.db.session.commit()

    # 부서/사원
    @staticmethod
    def insert_dummy_data_employee():
        from backend_model.table_base import BaseEmployee
        DBManager.add_department('자재부서', 'WH01', '사원명001')
        DBManager.add_department('제품부서', 'WH02', '사원명002')
        DBManager.add_department('현장부서', 'WH03', '사원명003')
        DBManager.add_department('불량부서', 'WH04', '사원명004')

        for i in range(1, 100):
            idx_str = str(i).zfill(3)
            emp = BaseEmployee()
            emp.fk_company_id = 1
            emp.emp_code = "emp" + idx_str
            emp.emp_name = "사원명" + idx_str
            emp.emp_order = i
            # emp.emp_picture_path = "/dat/img/" + idx_str + ".jpg"
            # emp.emp_sign_path = "/dat/sign/" + idx_str + ".jpg"
            emp.emp_addr = "자택주소" + idx_str
            emp.emp_addr_detail = "자택상세주소" + idx_str
            emp.emp_addr_zipcode = "12312"
            emp.emp_direct_phone = "231"
            emp.emp_ext_phone = "02-123-1234"
            emp.emp_mobile = "010-1234-7869"
            emp.emp_position = "사원"
            emp.emp_email = "emp@email.com"
            emp.emp_joindate = DBManager.get_random_date()
            emp.memo = "메모" + idx_str
            emp.emp_name_en = "Joe"
            emp.emp_gender = "남" if int(random.randrange(1, 3)) == 1 else "여"
            emp.emp_country = "대한민국"
            emp.resignation_yn = True
            emp.resignation_date = DBManager.get_random_date()
            emp.resignation_type = "일신상"
            emp.fk_setup_group_auth = int(random.randrange(1, 3))
            emp.fk_department_id = int(random.randrange(1, 5))
            DBManager.db.session.add(emp)

        DBManager.db.session.commit()

    # 거래처관리
    @staticmethod
    def insert_dummy_data_client():
        from backend_model.table_base import BaseClient, BaseClientManager

        for i in range(1, 10000):
            idx_str = str(i).zfill(3)
            cli = BaseClient()
            cli.fk_company_id = 1
            cli.alias = "업체약칭" + idx_str
            cli.name = "거래처" + idx_str
            cli.address = "주소" + idx_str
            cli.address_detail = "상세주소" + idx_str
            cli.zip_code = "12345"
            cli.phone = "02-123-1234"
            cli.fax = "02-123-4332"
            cli.email = "test@email.com"
            cli.homepage = "rainmaker.co.kr"
            cli.bill_manager = "홍길동"
            cli.bill_email = "hong@email.com"
            cli.client_type = "공급업체"
            cli.district_type = "경기도"
            cli.manager = "김영희"
            cli.trade_yn = int(random.randrange(0, 2))
            cli.before_alias = "변경전업체약칭" + idx_str
            cli.after_alias = "변경후업체약칭" + idx_str
            cli.corp_number = "4736392837264"
            cli.business_number = "3148133490"
            cli.ceo_name = "씨이오"
            cli.business_status = "서비스업"
            cli.business_sector = "소프트웨어개발"
            cli.name_en = "Johnny"
            cli.ceo_name_en = "Daniel"
            cli.phone_en = "+82-2-291-23123"
            cli.fax_en = "+82-2-123-1234"
            cli.address_en = "Seoul"
            cli.register_id = "stechadmin"
            cli.modify_id = "stechadmin"
            cli.last_updated_date = DBManager.get_random_date()

            DBManager.db.session.add(cli)
            DBManager.db.session.commit()

            for j in range(1, 5):
                bc = BaseClientManager()
                idx_str = str(j).zfill(2)
                bc.name = "이름" + idx_str
                bc.department = "부서" + idx_str
                bc.postion = "사원"
                bc.mobile = "010-2344-0293"
                bc.email = "manager@email.com"
                bc.direct_phone = "1231"
                bc.ext_phone = "5543"
                bc.etc = "비고" + idx_str
                bc.fk_client_id = i

                DBManager.db.session.add(bc)
            DBManager.db.session.commit()

    # 공정관리
    @staticmethod
    def insert_dummy_data_process():
        from backend_model.table_base import BaseProcess

        for i in range(1, 100):
            idx_str = str(i).zfill(3)
            proc = BaseProcess()
            proc.fk_company_id = 1
            proc.process_code = "PROC" + idx_str
            proc.process_name = "공정" + idx_str
            proc.ct = int(random.randrange(1, 1000))
            proc.unit = "EA"
            proc.unit_price = int(random.randrange(10000, 1000000))
            proc.etc = "비고" + idx_str

            DBManager.db.session.add(proc)
        DBManager.db.session.commit()

    # 출하관리
    @staticmethod
    def insert_dummy_data_shipment_quote():
        from backend_model.table_shipment import ShipmentQuote, ShipmentQuoteItem

        for i in range(1, 100):
            idx_str = str(i).zfill(3)
            sq = ShipmentQuote()
            sq.quote_number = "QUOTE-" + idx_str
            sq.quote_date = DBManager.get_random_date()
            sq.client_company = "네이버"
            sq.client_manager = "홍길동"
            sq.quote_department = "견적부서"
            sq.quote_manager = "김철수"
            sq.quote_type = "A타입"
            sq.vat_type = "별도"
            sq.payment_terms = "현금"
            sq.delivery_date = DBManager.get_random_date()
            sq.delivery_place = ""
            sq.previous_quote_number = "QUOTE-" + idx_str
            sq.project_number = "PRJ-" + idx_str
            sq.end_user = "네이버"
            sq.note = "참고사항"
            sq.etc = "비고"
            sq.supply_price = int(random.randrange(10, 1000)) * 1000
            sq.vat = sq.supply_price * 0.1
            sq.total_price = sq.supply_price + sq.vat
            sq.fk_company_id = 1

            DBManager.db.session.add(sq)
            DBManager.db.session.commit()

            for j in range(1, 10):
                idx_str = str(int(random.randrange(1, 100))).zfill(3)
                sqi = ShipmentQuoteItem()
                sqi.type = int(random.randrange(1, 3))
                if sqi.type == 1:
                    sqi.item_code = "ITEM-" + idx_str
                    sqi.item_name = "품목-" + idx_str
                    sqi.item_detail = "품목상세-" + idx_str
                    sqi.note = "견적1"
                else:
                    sqi.item_code = "CUSTOM-" + idx_str
                    sqi.item_name = "입력품목-" + idx_str
                    sqi.item_detail = "입력품목상세-" + idx_str
                    sqi.note = "견적2"

                sqi.standard = "정품"
                sqi.quote_quantity = int(random.randrange(1, 1000))
                sqi.unit_price = int(random.randrange(10, 1000)) * 1000
                sqi.unit = int(random.randrange(1, 100))
                sqi.supply_price = sqi.unit_price * sqi.unit
                sqi.request_delivery_date = DBManager.get_random_date()
                sqi.available_stock = int(random.randrange(1, 100))
                sqi.current_stock = int(random.randrange(1, 100))
                sqi.client_item_number = "고객사품번-" + idx_str
                sqi.project_number = "PROJ-001"
                sqi.fk_quote_id = i

                DBManager.db.session.add(sqi)
            DBManager.db.session.commit()

    @staticmethod
    def insert_dummy_data_shipment_order():
        from backend_model.table_shipment import ShipmentOrder, ShipmentOrderItem

        for i in range(1, 100):
            idx_str = str(i).zfill(3)
            sq = ShipmentOrder()
            sq.order_number = "ORDER-" + idx_str
            sq.order_date = DBManager.get_random_date()
            sq.client_company = "카카오"
            sq.client_manager = "김영희"
            sq.order_department = "수주부서"
            sq.order_manager = "김대중"
            sq.order_type = "A타입"
            sq.vat_type = "별도"
            sq.payment_terms = "현금"
            sq.delivery_date = DBManager.get_random_date()
            sq.delivery_place = ""
            sq.client_order_number = "ORDER-" + idx_str
            sq.project_number = "PRJ-" + idx_str
            sq.end_user = "카카오"
            sq.note = "참고사항"
            sq.etc = "비고"
            sq.supply_price = int(random.randrange(10, 1000)) * 1000
            sq.vat = sq.supply_price * 0.1
            sq.total_price = sq.supply_price + sq.vat
            sq.confirmed = int(random.randrange(0, 2))
            sq.fk_company_id = 1

            DBManager.db.session.add(sq)
            DBManager.db.session.commit()

            for j in range(1, 10):
                idx_str = str(int(random.randrange(1, 100))).zfill(3)
                sqi = ShipmentOrderItem()
                sqi.item_code = "ITEM-" + idx_str
                sqi.item_name = "품목-" + idx_str
                sqi.item_detail = "품목상세-" + idx_str
                sqi.note = "수주"
                sqi.standard = "정품"
                sqi.order_quantity = int(random.randrange(1, 1000))
                sqi.assign_quantity = int(random.randrange(1, 1000))
                sqi.unit_price = int(random.randrange(10, 1000)) * 1000
                sqi.unit = int(random.randrange(1, 100))
                sqi.supply_price = sqi.unit_price * sqi.unit
                sqi.request_delivery_date = DBManager.get_random_date()
                sqi.release_warehouse = "자재창고"
                sqi.not_shipped = int(random.randrange(1, 1000))
                sqi.available_stock = int(random.randrange(1, 100))
                sqi.current_stock = int(random.randrange(1, 100))
                sqi.quote_number = "ORDER-" + idx_str
                sqi.client_item_number = "고객사품번-" + idx_str
                sqi.closing_yn = int(random.randrange(0, 2))
                sqi.project_number = "PROJ-001"
                sqi.fk_order_id = i

                DBManager.db.session.add(sqi)
            DBManager.db.session.commit()

    @staticmethod
    def insert_dummy_data_shipment_release():
        from backend_model.table_shipment import ShipmentRelease, ShipmentReleaseItem

        for i in range(1, 100):
            idx_str = str(i).zfill(3)
            sq = ShipmentRelease()
            sq.release_number = "RELEASE-" + idx_str
            sq.release_date = DBManager.get_random_date()
            sq.client_company = "디트리플"
            sq.client_manager = "신현식"
            sq.release_department = "출고부서"
            sq.release_manager = "노무현"
            sq.release_type = "A타입"
            sq.vat_type = "별도"
            sq.payment_terms = "현금"
            sq.delivery_date = DBManager.get_random_date()
            sq.delivery_place = ""
            sq.client_order_number = "ORDER-" + idx_str
            sq.project_number = "PRJ-" + idx_str
            sq.end_user = "디트리플"
            sq.note = "참고사항"
            sq.etc = "비고"
            sq.supply_price = int(random.randrange(10, 1000)) * 1000
            sq.vat = sq.supply_price * 0.1
            sq.total_price = sq.supply_price + sq.vat
            sq.confirmed = int(random.randrange(0, 2))
            sq.fk_company_id = 1

            DBManager.db.session.add(sq)
            DBManager.db.session.commit()

            for j in range(1, 10):
                idx_str = str(int(random.randrange(1, 100))).zfill(3)
                sqi = ShipmentReleaseItem()
                sqi.item_code = "ITEM-" + idx_str
                sqi.item_name = "품목-" + idx_str
                sqi.item_detail = "품목상세-" + idx_str
                sqi.note = "출고"
                sqi.standard = "정품"
                sqi.order_quantity = int(random.randrange(1, 1000))
                sqi.release_quantity = int(random.randrange(1, 1000))
                sqi.unit_price = int(random.randrange(10, 1000)) * 1000
                sqi.unit = int(random.randrange(1, 100))
                sqi.supply_price = sqi.unit_price * sqi.unit
                sqi.request_delivery_date = DBManager.get_random_date()
                sqi.non_invoice = int(random.randrange(1, 1000))
                sqi.release_warehouse = "출고창고"
                sqi.current_stock = int(random.randrange(1, 100))
                sqi.order_number = "ORDER-" + idx_str
                sqi.client_item_number = "고객사품번-" + idx_str
                sqi.closing_yn = int(random.randrange(0, 2))
                sqi.project_number = "PROJ-001"
                sqi.fk_release_id = i
                sqi.fk_order_item_id = i

                DBManager.db.session.add(sqi)
            DBManager.db.session.commit()

    # 구매관리 - 발주계획
    @staticmethod
    def insert_dummy_data_purchase_order_plan():
        from backend_model.table_purchase import PurchaseOrderPlan, PurchaseOrderPlanItem

        for i in range(1, 100):
            idx_str = str(i).zfill(3)
            p = PurchaseOrderPlan()
            p.order_plan_number = "PA-" + idx_str
            p.order_plan_date = DBManager.get_random_date()
            p.order_plan_department = "발주계획부서"
            p.order_plan_manager = "신현식"
            p.note = "참고사항"
            p.etc = "비고"
            p.supply_price = int(random.randrange(10, 1000)) * 1000
            p.vat = p.supply_price * 0.1
            p.total_price = p.supply_price + p.vat
            p.fk_company_id = 1

            DBManager.db.session.add(p)
            DBManager.db.session.commit()

            for j in range(1, 10):
                idx_str = str(int(random.randrange(1, 100))).zfill(3)
                sqi = PurchaseOrderPlanItem()
                sqi.item_code = "ITEM-" + idx_str
                sqi.item_name = "품목-" + idx_str
                sqi.standard = "정품"
                sqi.order_plan_quantity = int(random.randrange(1, 1000))
                sqi.unit_price = int(random.randrange(10, 1000)) * 1000
                sqi.unit = int(random.randrange(1, 100))
                sqi.price = sqi.unit_price * sqi.unit
                sqi.unordered_quantity = int(random.randrange(1, 1000))
                sqi.available_stock = int(random.randrange(1, 100))
                sqi.current_stock = int(random.randrange(1, 100))
                sqi.order_number = "ORDER-" + idx_str
                sqi.main_supplier = "씨젠"
                sqi.order_date = DBManager.get_random_date()
                sqi.client_item_number = "고객사품번-" + idx_str
                sqi.end_user = "JYP"
                sqi.delivery_date = DBManager.get_random_date()
                sqi.project_number = "PROJ-001"
                sqi.fk_purchase_order_plan_id = i

                DBManager.db.session.add(sqi)
            DBManager.db.session.commit()

    # 구매관리 - 발주
    @staticmethod
    def insert_dummy_data_purchase_order():
        from backend_model.table_purchase import PurchaseOrder, PurchaseOrderItem

        for i in range(1, 100):
            idx_str = str(i).zfill(3)
            p = PurchaseOrder()
            p.order_number = "PO-" + idx_str
            p.order_date = DBManager.get_random_date()
            p.client_company = "삼성전자"
            p.client_manager = "김삼성"
            p.order_department = "발주부서"
            p.order_manager = "신현식"
            p.order_type = "A타입"
            p.vat_type = "별도"
            p.payment_terms = "현금"
            p.delivery_date = DBManager.get_random_date()
            p.delivery_place = ""
            p.ref_number = "REF" + str(i)
            p.project_number = "PROJ" + str(i)
            p.end_user = "삼성" + str(i)
            p.note = "참고사항"
            p.etc = "비고"
            p.supply_price = int(random.randrange(10, 1000)) * 1000
            p.vat = p.supply_price * 0.1
            p.total_price = p.supply_price + p.vat
            p.confirmed = int(random.randrange(0, 2))
            p.fk_company_id = 1

            DBManager.db.session.add(p)
            DBManager.db.session.commit()

            for j in range(1, 10):
                idx_str = str(int(random.randrange(1, 100))).zfill(3)
                poi = PurchaseOrderItem()
                poi.item_code = "ITEM-" + idx_str
                poi.item_name = "품목-" + idx_str
                poi.standard = "정품"
                poi.order_quantity = int(random.randrange(1, 1000))
                poi.unit_price = int(random.randrange(10, 1000)) * 1000
                poi.unit = int(random.randrange(1, 100))
                poi.supply_price = poi.unit_price * poi.unit
                poi.request_delivery_date = DBManager.get_random_date()
                poi.not_shipped = int(random.randrange(1, 1000))
                poi.available_stock = int(random.randrange(1, 100))
                poi.current_stock = int(random.randrange(1, 100))
                poi.order_plan_number = "ORDERPLAN-" + idx_str
                poi.client_item_number = "고객사품번-" + idx_str
                poi.item_detail = ""
                poi.note = ""
                poi.closing_yn = int(random.randrange(0, 2))
                poi.project_number = "PROJ-001"
                poi.fk_purchase_order_id = i

                DBManager.db.session.add(poi)
            DBManager.db.session.commit()

    # 구매관리 - 가입고
    @staticmethod
    def insert_dummy_data_pre_purchase_receiving():
        from backend_model.table_purchase import PurchasePreReceiving, PurchasePreReceivingItem

        for i in range(1, 100):
            idx_str = str(i).zfill(3)
            p = PurchasePreReceiving()
            p.prereceiving_number = "PRN-" + idx_str
            p.prereceiving_date = DBManager.get_random_date()
            p.client_company = "LG전자"
            p.client_manager = "김엘지"
            p.receiving_department = "가입고부서"
            p.receiving_manager = "주강대"
            p.receiving_type = "B타입"
            p.vat_type = "별도"
            p.payment_terms = "현금"
            p.delivery_date = DBManager.get_random_date()
            p.delivery_place = ""
            p.ref_number = "REF" + str(i)
            p.project_number = "PROJ" + str(i)
            p.end_user = "셀트리온" + str(i)
            p.note = "참고사항"
            p.etc = "비고"
            p.supply_price = int(random.randrange(10, 1000)) * 1000
            p.vat = p.supply_price * 0.1
            p.total_price = p.supply_price + p.vat
            p.confirmed = int(random.randrange(0, 2))
            p.fk_company_id = 1

            DBManager.db.session.add(p)
            DBManager.db.session.commit()

            for j in range(1, 10):
                idx_str = str(int(random.randrange(1, 100))).zfill(3)
                pri = PurchasePreReceivingItem()
                pri.item_code = "ITEM-" + idx_str
                pri.item_name = "품목-" + idx_str
                pri.standard = "정품"
                pri.order_quantity = int(random.randrange(1, 1000))
                pri.prereceiving_quantity = int(random.randrange(1, 1000))
                pri.unit_price = int(random.randrange(10, 1000)) * 1000
                pri.unit = int(random.randrange(1, 100))
                pri.supply_price = pri.unit_price * pri.unit
                pri.request_delivery_date = DBManager.get_random_date()
                pri.receiving_warehouse = "입고창고" + str(j)
                pri.current_stock = int(random.randrange(1, 100))
                pri.order_number = "ORDER-" + idx_str
                pri.client_item_number = "고객사품번-" + idx_str
                pri.item_detail = ""
                pri.note = ""
                pri.closing_yn = int(random.randrange(0, 2))
                pri.project_number = "PROJ-001"
                pri.fk_order_item_id = i
                pri.fk_prereceiving_id = i

                DBManager.db.session.add(pri)
            DBManager.db.session.commit()

    # 구매관리 - 입고
    @staticmethod
    def insert_dummy_data_purchase_receiving():
        from backend_model.table_purchase import PurchaseReceiving, PurchaseReceivingItem

        for i in range(1, 100):
            idx_str = str(i).zfill(3)
            p = PurchaseReceiving()
            p.receiving_number = "RN-" + idx_str
            p.receiving_date = DBManager.get_random_date()
            p.client_company = "LG전자"
            p.client_manager = "김엘지"
            p.receiving_department = "입고부서"
            p.receiving_manager = "박홍범"
            p.receiving_type = "A타입"
            p.vat_type = "별도"
            p.payment_terms = "현금"
            p.delivery_date = DBManager.get_random_date()
            p.delivery_place = ""
            p.ref_number = "REF" + str(i)
            p.project_number = "PROJ" + str(i)
            p.end_user = "엘지" + str(i)
            p.note = "참고사항"
            p.etc = "비고"
            p.supply_price = int(random.randrange(10, 1000)) * 1000
            p.vat = p.supply_price * 0.1
            p.total_price = p.supply_price + p.vat
            p.confirmed = int(random.randrange(0, 2))
            p.fk_company_id = 1

            DBManager.db.session.add(p)
            DBManager.db.session.commit()

            for j in range(1, 10):
                idx_str = str(int(random.randrange(1, 100))).zfill(3)
                pri = PurchaseReceivingItem()
                pri.item_code = "ITEM-" + idx_str
                pri.item_name = "품목-" + idx_str
                pri.standard = "정품"
                pri.order_quantity = int(random.randrange(1, 1000))
                pri.receiving_quantity = int(random.randrange(1, 1000))
                pri.unit_price = int(random.randrange(10, 1000)) * 1000
                pri.unit = int(random.randrange(1, 100))
                pri.supply_price = pri.unit_price * pri.unit
                pri.request_delivery_date = DBManager.get_random_date()
                pri.receiving_warehouse = "입고창고" + str(j)
                pri.current_stock = int(random.randrange(1, 100))
                pri.order_number = "ORDER-" + idx_str
                pri.client_item_number = "고객사품번-" + idx_str
                pri.item_detail = ""
                pri.note = ""
                pri.closing_yn = int(random.randrange(0, 2))
                pri.project_number = "PROJ-001"
                pri.fk_order_item_id = i
                pri.fk_receiving_id = i

                DBManager.db.session.add(pri)
            DBManager.db.session.commit()

    # 프로젝트
    @staticmethod
    def insert_dummy_data_project():
        from backend_model.table_project import ProjectManagement, ProjectSchedule, ProjectNotice

        step_sample = ['영업', '제안', '계약', '설계', '제작', '납품', '설치', '완료']

        for i in range(1, 100):
            idx_str = str(i).zfill(3)
            start_date = DBManager.get_random_date()
            end_date = start_date + timedelta(days=30)
            p = ProjectManagement()
            p.project_number = 'PROJ-' + idx_str
            p.project_name = '계약건명-' + idx_str
            p.order_company = '발주기관' + idx_str
            p.contract_date = start_date
            p.contract_begin_date = start_date
            p.contract_end_date = end_date
            p.contract_amount = int(random.randrange(10000, 999999))
            p.register_department = '등록부서'
            p.register_manager = '등록담당자'
            p.register_date = start_date
            p.sales_department = '영업부서'
            p.sales_manager = '오시운B'
            p.contract_type = '우수조달'
            p.contract_item = '계약품목' + idx_str
            p.business_department = '사업부서'
            p.business_manager = '오시운G'
            p.site_address = '현장주소' + idx_str
            p.note = '참고사항' + idx_str
            p.allocation_amount = int(random.randrange(10000, 999999))
            p.use_price = int(random.randrange(10000, 999999))
            p.use_department = '시스템사업부'
            p.use_date = start_date
            p.total_progress = int(random.randrange(0, 100))
            p.step = random.choice(step_sample)
            p.fk_company_id = 1
            DBManager.db.session.add(p)
            DBManager.db.session.flush()

            s = ProjectSchedule()
            s.start_date = start_date
            s.end_date = end_date
            s.title = '스케쥴 ' + idx_str
            s.fk_project_management_id = p.id
            s.progress_percent = int(random.randrange(0, 100))
            DBManager.db.session.add(s)

        DBManager.db.session.commit()

        for i in range(1, 10):
            start_date = DBManager.get_random_date()

            idx_str = str(i).zfill(3)
            pn = ProjectNotice()
            pn.title = "공지제목" + idx_str
            pn.start_date = DBManager.get_random_date()
            pn.end_date = start_date + timedelta(days=30)
            pn.important = int(random.randrange(1, 10)) % 2
            pn.content_html = "<html><body><h3>공지사항테스트</h3></body></html>"
            pn.register_id = "stechadmin"
            pn.fk_company_id = 1
            DBManager.db.session.add(pn)

        DBManager.db.session.commit()

    # 재고관리 - 기타입출고
    @staticmethod
    def insert_dummy_data_stock_etc():
        from backend_model.table_stock import StockEtc, StockEtcItem

        for i in range(1, 100):
            idx_str = str(i).zfill(3)
            p = StockEtc()
            p.number = "SE-" + idx_str
            p.target_date = DBManager.get_random_date()
            p.department = "구매부"
            p.manager = "안근진"
            p.note = "참고사항" + idx_str
            p.etc = "비고" + idx_str
            p.fk_company_id = 1

            DBManager.db.session.add(p)
            DBManager.db.session.commit()

            for j in range(1, 10):
                idx_str = str(int(random.randrange(1, 100))).zfill(3)
                pri = StockEtcItem()
                pri.item_type = "기타입고"
                pri.item_code = "ITEM-" + idx_str
                pri.quantity = int(random.randrange(1, 1000))
                pri.unit_price = int(random.randrange(10, 1000)) * 1000
                pri.unit = "EA"
                pri.supply_price = pri.unit_price * pri.quantity
                pri.inout_warehouse = "재고창고"
                pri.type = "입고"
                pri.available_stock = int(random.randrange(1, 100))
                pri.current_stock = int(random.randrange(1, 100))
                pri.project_number = "PROJ-001"
                pri.note = "비고" + idx_str
                pri.asset_type = "원자재"
                pri.fk_stock_etc_id = i

                DBManager.db.session.add(pri)
            DBManager.db.session.commit()

    # 재고관리 - 재고이동요청
    @staticmethod
    def insert_dummy_data_stock_move_request():
        from backend_model.table_stock import StockMoveRequest, StockMoveRequestItem

        for i in range(1, 100):
            idx_str = str(i).zfill(3)
            p = StockMoveRequest()
            p.number = "SMR-" + idx_str
            p.target_date = DBManager.get_random_date()
            p.department = "구매부"
            p.manager = "담당자"
            p.note = "참고사항" + idx_str
            p.etc = "비고" + idx_str
            p.fk_company_id = 1

            DBManager.db.session.add(p)
            DBManager.db.session.commit()

            for j in range(1, 10):
                idx_str = str(int(random.randrange(1, 100))).zfill(3)
                pri = StockMoveRequestItem()
                pri.item_code = "ITEM-" + idx_str
                pri.quantity = int(random.randrange(1, 1000))
                pri.unit_price = int(random.randrange(10, 1000)) * 1000
                pri.unit = "EA"
                pri.supply_price = pri.unit_price * pri.quantity
                pri.out_warehouse = "출고창고"
                pri.in_warehouse = "입고창고"
                pri.note = "비고" + idx_str
                pri.asset_type = "원자재"
                pri.project_number = "PROJ-001"
                pri.fk_stock_move_request_id = i

                DBManager.db.session.add(pri)
            DBManager.db.session.commit()

    # 재고관리 - 재고이동출고
    @staticmethod
    def insert_dummy_data_stock_move_release():
        from backend_model.table_stock import StockMoveRelease, StockMoveReleaseItem

        for i in range(1, 100):
            idx_str = str(i).zfill(3)
            p = StockMoveRelease()
            p.number = "SE-" + idx_str
            p.target_date = DBManager.get_random_date()
            p.department = "출고부"
            p.manager = "박준현"
            p.note = "참고사항" + idx_str
            p.etc = "비고" + idx_str
            p.fk_company_id = 1

            DBManager.db.session.add(p)
            DBManager.db.session.commit()

            for j in range(1, 10):
                idx_str = str(int(random.randrange(1, 100))).zfill(3)
                pri = StockMoveReleaseItem()
                pri.item_code = "ITEM-" + idx_str
                pri.quantity = int(random.randrange(1, 1000))
                pri.unit_price = int(random.randrange(10, 1000)) * 1000
                pri.unit = "EA"
                pri.supply_price = pri.unit_price * pri.quantity
                pri.inout_warehouse = "재고창고"
                pri.type = "입고"
                pri.available_stock = int(random.randrange(1, 100))
                pri.current_stock = int(random.randrange(1, 100))
                pri.project_number = "PROJ-001"
                pri.note = "비고" + idx_str
                pri.asset_type = "원자재"
                pri.project_number = "PROJ-001"
                pri.fk_stock_move_release_id = i

                DBManager.db.session.add(pri)
            DBManager.db.session.commit()
