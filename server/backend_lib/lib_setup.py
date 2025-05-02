# -*- coding: utf-8 -*-

from decimal import Decimal
from backend_model.table_setup import *
from backend_model.table_base import *
from backend_model.table_shipment import *

db = DBManager.db


class LibSetupGroup(object):
    @staticmethod
    def post_postprocessor(result=None, **kw):
        if result is None:
            return
        try:
            group_id = result['id']
        except:
            return

        # setupGroup(권한그룹)이 추가되면 setupGroupAuth(메뉴권한)을 추가
        setup_menus = db.session.query(SetupMenu).all()
        for menu in setup_menus:
            setup_group_auth = SetupGroupAuth()
            setup_group_auth.menu_auth = 31
            setup_group_auth.fk_group_id = group_id
            setup_group_auth.fk_menu_id = menu.id
            db.session.add(setup_group_auth)
        db.session.commit()

    @staticmethod
    def delete_single_preprocessor(instance_id=None, **kw):
        if instance_id is None:
            return

        # setupGroup(권한그룹)이 삭제되면 setupGroupAuth(메뉴권한)을 삭제
        db.session.query(SetupGroupAuth).filter(SetupGroupAuth.fk_group_id == instance_id).delete()
        db.session.commit()


class LibSetupGroupAuth(object):
    @staticmethod
    def get_many_preprocessor(search_params=None, **kw):
        filt = dict(name='menu', op='has', val=dict(name='menu_enable', op='eq', val=True))
        search_params['filters'].append(filt)


class LibSetupBasicStock(object):
    @staticmethod
    def get_many_postprocessor(result=None, search_params=None, **kw):
        item_list = result['objects']
        for bs in item_list:
            # 할당수량의 합을 구한다 (품목코드, 창고코드)
            from backend_lib.lib_shipment import LibShipmentOrderItem
            assign_quantity = LibShipmentOrderItem.get_total_assign_quantity_by_item_code(bs['item_code'], bs['wh_code'])
            bs['assign_stock'] = int(assign_quantity)

    @staticmethod
    def update_available_stock(item_code, warehouse_code):
        # 기초재고를 찾는다 (품목코드, 창고코드)
        basic_stock = LibSetupBasicStock.get_basic_stock(item_code, warehouse_code)
        if basic_stock:
            basic_stock.available_stock = LibSetupBasicStock.calculate_available_stock(item_code, warehouse_code, basic_stock.current_stock)
            db.session.commit()
            return basic_stock
        else:
            return None

    @staticmethod
    def update_current_stock(item_code, warehouse_code, new_current_stock):
        basic_stock = LibSetupBasicStock.get_basic_stock(item_code, warehouse_code)
        if basic_stock:
            basic_stock.current_stock = new_current_stock
            db.session.commit()

    @staticmethod
    def get_basic_stock(item_code, warehouse_code):
        return LibSetupBasicStock.check_basic_stock(item_code, warehouse_code)

    @staticmethod
    def check_basic_stock(item_code, warehouse_code):
        """
        기초재고가 없으면 추가해준다

        :param item_code: 품목코드
        :param warehouse_code: 창고코드
        :return:
        """
        item = db.session.query(BaseItem).filter(BaseItem.item_code == item_code).first()
        if item:
            basic_stock = db.session.query(
                SetupBasicStock
            ).filter(
                SetupBasicStock.item_code == item_code
            ).filter(
                SetupBasicStock.wh_code == warehouse_code
            ).first()
            if not basic_stock:
                basic_stock = LibSetupBasicStock.insert_basic_stock(item_code, warehouse_code, item.fk_company_id)
            return basic_stock

    @staticmethod
    def insert_basic_stock(item_code, warehouse_code, company_id):
        basic_stock = SetupBasicStock()
        basic_stock.wh_code = warehouse_code
        basic_stock.item_code = item_code
        basic_stock.basic_stock = 0
        basic_stock.current_stock = 0
        basic_stock.available_stock = 0
        basic_stock.item_unit_price = 0
        basic_stock.item_price = 0
        basic_stock.fk_company_id = company_id
        db.session.add(basic_stock)
        db.session.commit()
        return basic_stock

    @staticmethod
    def update_stock_by_item_code(item_code, warehouse_code):
        basic_stock = LibSetupBasicStock.get_basic_stock(item_code, warehouse_code)
        if basic_stock:
            basic_stock.current_stock = LibSetupBasicStock.calculate_current_stock(item_code, warehouse_code, basic_stock.basic_stock)
            basic_stock.available_stock = LibSetupBasicStock.calculate_available_stock(item_code, warehouse_code, basic_stock.current_stock)
            db.session.commit()

    @staticmethod
    def get_total_release_quantity(item_code, warehouse_code, start_date=None, end_date=None):
        # 출하관리 - 출고
        from backend_lib.lib_shipment import LibShipmentReleaseItem
        shipment_release_quantity = LibShipmentReleaseItem.get_total_release_quantity_by_item_code(item_code, warehouse_code, start_date, end_date)
        # 재고관리 - 기타출고
        from backend_lib.lib_stock import LibStockEtcItem
        stock_etc_release_quantity = LibStockEtcItem.get_total_release_quantity_by_item_code(item_code, warehouse_code, start_date, end_date)
        # 재고관리 - 재고이동출고
        from backend_lib.lib_stock import LibStockMoveReleaseItem
        stock_move_release_quantity = LibStockMoveReleaseItem.get_total_release_quantity_by_item_code(item_code, warehouse_code, start_date, end_date)
        # 생산관리 - 자재소모
        from backend_lib.lib_production import LibPerformanceRegistrationItem2
        produce_release_quantity = LibPerformanceRegistrationItem2.get_total_release_quantity_by_item_code(item_code, warehouse_code, start_date, end_date)
        # 구매관리 - 입고반품
        from backend_lib.lib_purchase import LibPurchaseReceivingReturnItem
        purchase_return_quantity = LibPurchaseReceivingReturnItem.get_total_release_quantity_by_item_code(item_code, warehouse_code, start_date, end_date)
        # 수출관리 - 선적
        from backend_lib.lib_export import LibExportCommInvoiceItem
        export_comm_invoice_quantity = LibExportCommInvoiceItem.get_total_release_quantity_by_item_code(item_code, warehouse_code, start_date, end_date)

        total_release_quantity = shipment_release_quantity + stock_etc_release_quantity + stock_move_release_quantity + produce_release_quantity + purchase_return_quantity + export_comm_invoice_quantity
        return {
            'shipment_release_quantity': shipment_release_quantity,
            'stock_etc_release_quantity': stock_etc_release_quantity,
            'stock_move_release_quantity': stock_move_release_quantity,
            'produce_release_quantity': produce_release_quantity,
            'purchase_return_quantity': purchase_return_quantity,
            'export_comm_invoice_quantity': export_comm_invoice_quantity,
            'total_release_quantity': total_release_quantity
        }

    @staticmethod
    def get_total_receiving_quantity(item_code, warehouse_code, start_date=None, end_date=None):
        # 구매관리 - 입고
        from backend_lib.lib_purchase import LibPurchaseReceivingItem
        purchase_receiving_quantity = LibPurchaseReceivingItem.get_total_receiving_quantity_by_item_code(item_code, warehouse_code, start_date, end_date)
        # 재고관리 - 기타입고
        from backend_lib.lib_stock import LibStockEtcItem
        stock_etc_receiving_quantity = LibStockEtcItem.get_total_receiving_quantity_by_item_code(item_code, warehouse_code, start_date, end_date)
        # 재고관리 - 재고이동입고
        from backend_lib.lib_stock import LibStockMoveReleaseItem
        stock_move_receiving_quantity = LibStockMoveReleaseItem.get_total_receiving_quantity_by_item_code(item_code, warehouse_code, start_date, end_date)
        # 생산관리 - 생산입고
        from backend_lib.lib_production import LibPerformanceRegistrationItem1
        produce_receiving_quantity = LibPerformanceRegistrationItem1.get_total_receiving_quantity_by_item_code(item_code, warehouse_code, start_date, end_date)
        # 출하관리 - 출고반품
        from backend_lib.lib_shipment import LibShipmentReleaseReturnItem
        release_return_quantity = LibShipmentReleaseReturnItem.get_total_receiving_quantity_by_item_code(item_code, warehouse_code, start_date, end_date)
        # 수입관리 - 통관
        from backend_lib.lib_import import LibImportClearanceItem
        import_clearance_quantity = LibImportClearanceItem.get_total_receiving_quantity_by_item_code(item_code, warehouse_code, start_date, end_date)

        total_receiving_quantity = purchase_receiving_quantity + stock_etc_receiving_quantity + stock_move_receiving_quantity + produce_receiving_quantity + release_return_quantity + import_clearance_quantity
        return {
            'purchase_receiving_quantity': purchase_receiving_quantity,
            'stock_etc_receiving_quantity': stock_etc_receiving_quantity,
            'stock_move_receiving_quantity': stock_move_receiving_quantity,
            'produce_receiving_quantity': produce_receiving_quantity,
            'release_return_quantity': release_return_quantity,
            'import_clearance_quantity': import_clearance_quantity,
            'total_receiving_quantity': total_receiving_quantity
        }

    @staticmethod
    def get_total_release_price(item_code: str, warehouse_code: str, start_date=None, end_date=None):
        # 출하관리 - 출고
        from backend_lib.lib_shipment import LibShipmentReleaseItem
        shipment_release_price = LibShipmentReleaseItem.get_total_release_price_by_item_code(
            item_code, warehouse_code, start_date, end_date)
        # 재고관리 - 기타출고
        from backend_lib.lib_stock import LibStockEtcItem
        stock_etc_release_price = LibStockEtcItem.get_total_release_price_by_item_code(
            item_code, warehouse_code, start_date, end_date)
        # 재고관리 - 재고이동출고
        from backend_lib.lib_stock import LibStockMoveReleaseItem
        stock_move_release_price = LibStockMoveReleaseItem.get_total_release_price_by_item_code(
            item_code, warehouse_code, start_date, end_date)
        # 생산관리 - 자재소모
        from backend_lib.lib_production import LibPerformanceRegistrationItem2
        produce_release_price = LibPerformanceRegistrationItem2.get_total_release_price_by_item_code(
            item_code, warehouse_code, start_date, end_date)
        # 구매관리 - 입고반품
        from backend_lib.lib_purchase import LibPurchaseReceivingReturnItem
        purchase_return_price = LibPurchaseReceivingReturnItem.get_total_release_price_by_item_code(
            item_code, warehouse_code, start_date, end_date)
        # 수출관리 - 선적
        from backend_lib.lib_export import LibExportCommInvoiceItem
        export_comm_invoice_price = LibExportCommInvoiceItem.get_total_release_price_by_item_code(
            item_code, warehouse_code, start_date, end_date)

        total_release_price = shipment_release_price + stock_etc_release_price + stock_move_release_price + produce_release_price + purchase_return_price + export_comm_invoice_price
        return {
            'shipment_release_price': Decimal(shipment_release_price),
            'stock_etc_release_price': Decimal(stock_etc_release_price),
            'stock_move_release_price': Decimal(stock_move_release_price),
            'produce_release_price': Decimal(produce_release_price),
            'purchase_return_price': Decimal(purchase_return_price),
            'export_comm_invoice_price': Decimal(export_comm_invoice_price),
            'total_release_price': Decimal(total_release_price)
        }

    @staticmethod
    def get_total_receiving_price(item_code: str, warehouse_code: str, start_date=None, end_date=None):
        # 구매관리 - 입고
        from backend_lib.lib_purchase import LibPurchaseReceivingItem
        purchase_receiving_price = LibPurchaseReceivingItem.get_total_receiving_price_by_item_code(
            item_code, warehouse_code, start_date, end_date)
        # 재고관리 - 기타입고
        from backend_lib.lib_stock import LibStockEtcItem
        stock_etc_receiving_price = LibStockEtcItem.get_total_receiving_price_by_item_code(
            item_code, warehouse_code, start_date, end_date)
        # 재고관리 - 재고이동입고
        from backend_lib.lib_stock import LibStockMoveReleaseItem
        stock_move_receiving_price = LibStockMoveReleaseItem.get_total_receiving_price_by_item_code(
            item_code, warehouse_code, start_date, end_date)
        # 생산관리 - 생산입고
        from backend_lib.lib_production import LibPerformanceRegistrationItem1
        produce_receiving_price = LibPerformanceRegistrationItem1.get_total_receiving_price_by_item_code(
            item_code, warehouse_code, start_date, end_date)
        # 출하관리 - 출고반품
        from backend_lib.lib_shipment import LibShipmentReleaseReturnItem
        release_return_price = LibShipmentReleaseReturnItem.get_total_receiving_price_by_item_code(
            item_code, warehouse_code, start_date, end_date)
        # 수입관리 - 통관
        from backend_lib.lib_import import LibImportClearanceItem
        import_clearance_price = LibImportClearanceItem.get_total_receiving_price_by_item_code(
            item_code, warehouse_code, start_date, end_date)

        total_receiving_price = purchase_receiving_price + stock_etc_receiving_price + stock_move_receiving_price + produce_receiving_price + release_return_price + import_clearance_price
        return {
            'purchase_receiving_price': int(purchase_receiving_price),
            'stock_etc_receiving_price': int(stock_etc_receiving_price),
            'stock_move_receiving_price': int(stock_move_receiving_price),
            'produce_receiving_price': int(produce_receiving_price),
            'release_return_price': int(release_return_price),
            'import_clearance_price': int(import_clearance_price),
            'total_receiving_price': int(total_receiving_price)
        }

    @staticmethod
    def calculate_current_stock(item_code, warehouse_code, basic_stock):
        release_result = LibSetupBasicStock.get_total_release_quantity(item_code=item_code, warehouse_code=warehouse_code)
        receiving_result = LibSetupBasicStock.get_total_receiving_quantity(item_code=item_code, warehouse_code=warehouse_code)
        closing_stock = basic_stock + receiving_result['total_receiving_quantity'] - release_result['total_release_quantity']
        return closing_stock

    @staticmethod
    def calculate_available_stock(item_code, warehouse_code, current_stock):
        from backend_lib.lib_shipment import LibShipmentOrderItem
        total_assign_quantity = LibShipmentOrderItem.get_total_assign_quantity_by_item_code(item_code, warehouse_code)
        available_stock = current_stock - total_assign_quantity
        available_stock = 0 if available_stock < 0 else available_stock
        return available_stock


class LibSetupControl(object):
    @staticmethod
    def get_control(company_id):
        control = db.session.query(
            SetupControl
        ).filter(
            SetupControl.fk_company_id == company_id
        ).first()
        return control

    @staticmethod
    def get_not_use_minus_stock(company_id):
        control = db.session.query(
            SetupControl
        ).filter(
            SetupControl.fk_company_id == company_id
        ).first()
        if control:
            return control.not_use_minus_stock
        return False

    @staticmethod
    def check_minus_stock(company_id, new_current_stock):
        not_use_minus_stock = LibSetupControl.get_not_use_minus_stock(company_id)
        if not_use_minus_stock:
            if new_current_stock < 0:
                from backend_lib.lib_exception import MesException
                MesException.raise_overflow_current_stock()
