# -*- coding: utf-8 -*-

from decimal import Decimal
from backend_model.database import DBManager
from backend_model.table_shipment import *
from backend_lib.lib_common import LibCommon
from backend_lib.lib_setup import LibSetupBasicStock

db = DBManager.db


class LibShipmentQuote(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        LibCommon.get_item_number(data, 'quote_number', ShipmentQuote, ShipmentQuote.quote_number, '/shipment/quote')

    @staticmethod
    def is_exist_item_number(table, column_number, new_number, company_id):
        exist = db.session.query(
            table
        ).filter(
            column_number == new_number
        ).filter(
            table.fk_company_id == company_id
        ).first()
        return False if exist is None else True

    @staticmethod
    def post_postprocessor(result=None, **kw):
        fk_previous_quote_id = result['fk_previous_quote_id']
        if fk_previous_quote_id is not None and fk_previous_quote_id != '':
            quote = db.session.query(
                ShipmentQuote
            ).filter(
                ShipmentQuote.id == fk_previous_quote_id
            ).first()
            quote_items = db.session.query(
                ShipmentQuoteItem
            ).filter(
                ShipmentQuoteItem.fk_quote_id == quote.id
            ).filter(
                ShipmentQuoteItem.fk_parent_id == None
            ).all()
     
            for quote_item in quote_items:
                add_item = ShipmentQuoteItem()
                add_item.item_code = quote_item.item_code
                add_item.quote_quantity = quote_item.quote_quantity
                add_item.unit_price = quote_item.unit_price
                add_item.sales_unit_price = quote_item.sales_unit_price
                add_item.purchase_unit_price = quote_item.purchase_unit_price
                add_item.supply_price = quote_item.supply_price
                add_item.sales_supply_price = quote_item.sales_supply_price
                add_item.dc_rate = quote_item.dc_rate
                add_item.request_delivery_date = quote_item.request_delivery_date
                add_item.client_item_number = quote_item.client_item_number
                add_item.note = quote_item.note
                add_item.item_order = quote_item.item_order
                add_item.not_ordered = quote_item.quote_quantity
                add_item.warehouse_code = quote_item.warehouse_code
                add_item.fk_quote_id = result['id']
                db.session.add(add_item)
                db.session.commit()
                LibShipmentQuote.create_child_quote_item(parent=add_item, quote_item=quote_item.serialize())
            
            if result['quote_type'] == '신규견적':
                db.session.query(
                    ShipmentQuote
                ).filter(
                    ShipmentQuote.id == result['id']
                ).update({'fk_previous_quote_id' : None})

            # quote_items2 = db.session.query(
            #     ShipmentQuoteItem2
            # ).filter(
            #     ShipmentQuoteItem2.fk_quote_id == quote.id
            # ).all()
            # for quote_item in quote_items2:
            #     add_item = ShipmentQuoteItem2()
            #     add_item.item_code = quote_item.item_code
            #     add_item.item_name = quote_item.item_name
            #     add_item.item_standard = quote_item.item_standard
            #     add_item.item_detail = quote_item.item_detail
            #     add_item.unit = quote_item.unit
            #     add_item.quote_quantity = quote_item.quote_quantity
            #     add_item.unit_price = quote_item.unit_price
            #     add_item.supply_price = quote_item.supply_price
            #     add_item.request_delivery_date = quote_item.request_delivery_date
            #     add_item.client_item_number = quote_item.client_item_number
            #     add_item.note = quote_item.note
            #     add_item.warehouse_code = quote_item.warehouse_code
            #     add_item.fk_quote_id = result['id']
            #     db.session.add(add_item)
            db.session.commit()

    @staticmethod
    def create_child_quote_item(parent, quote_item):
        if 'children' in quote_item:
            for child in quote_item['children']:
                add_item = ShipmentQuoteItem()
                add_item.item_code = child['item_code']
                add_item.quote_quantity = child['quote_quantity']
                add_item.unit_price = child['unit_price']
                add_item.sales_unit_price = child['sales_unit_price']
                add_item.purchase_unit_price = child['purchase_unit_price']
                add_item.supply_price = child['supply_price']
                add_item.sales_supply_price = child['sales_supply_price']
                add_item.dc_rate = child['dc_rate']
                add_item.request_delivery_date = child['request_delivery_date']
                add_item.client_item_number = child['client_item_number']
                add_item.note = child['note']
                add_item.item_order = child['item_order']
                add_item.not_ordered = child['quote_quantity']
                add_item.warehouse_code = child['warehouse_code']
                add_item.fk_parent_id = parent.id
                add_item.fk_quote_id = parent.fk_quote_id
                db.session.add(add_item)
                db.session.commit()
                LibShipmentQuote.create_child_quote_item(parent=add_item, quote_item=child)

class LibShipmentQuoteManual(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        LibCommon.get_item_number(data, 'quote_number', ShipmentQuoteManual, ShipmentQuoteManual.quote_number, '/shipment/quote-manual')

    @staticmethod
    def is_exist_item_number(table, column_number, new_number, company_id):
        exist = db.session.query(
            table
        ).filter(
            column_number == new_number
        ).filter(
            table.fk_company_id == company_id
        ).first()
        return False if exist is None else True

    @staticmethod
    def post_postprocessor(result=None, **kw):
        previous_quote_number = result['previous_quote_number']
        if previous_quote_number is not None and previous_quote_number != '':
            quote = db.session.query(
                ShipmentQuoteManual
            ).filter(
                ShipmentQuoteManual.quote_number == previous_quote_number
            ).first()
            quote_items = db.session.query(
                ShipmentQuoteManualItem
            ).filter(
                ShipmentQuoteManualItem.fk_quote_id == quote.id
            ).all()
            for quote_item in quote_items:
                add_item = ShipmentQuoteItem()
                add_item.item_code = quote_item.item_code
                add_item.quote_quantity = quote_item.quote_quantity
                add_item.unit_price = quote_item.unit_price
                add_item.supply_price = quote_item.supply_price
                add_item.request_delivery_date = quote_item.request_delivery_date
                add_item.client_item_number = quote_item.client_item_number
                add_item.note = quote_item.note
                add_item.project_number = quote_item.project_number
                add_item.warehouse_code = quote_item.warehouse_code
                add_item.fk_quote_id = result['id']
                db.session.add(add_item)
            db.session.commit()


class LibShipmentQuoteItem(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        if 'item_code' in data and 'warehouse_code' in data:
            LibSetupBasicStock.check_basic_stock(data['item_code'], data['warehouse_code'])

    @staticmethod
    def get_many_postprocessor(result=None, **kw):
        quote_item_list = result['objects']
        for quote_item in quote_item_list:
            order_quantity = db.session.query(
                db.func.sum(ShipmentOrderItem.order_quantity)
            ).filter(
                ShipmentOrderItem.fk_quote_item_id == quote_item['id']
            ).first()[0]
            not_ordered = quote_item['quote_quantity']
            if order_quantity:
                not_ordered = quote_item['quote_quantity'] - order_quantity
            if not_ordered is None or not_ordered < 0:
                not_ordered = 0
            quote_item['not_ordered'] = not_ordered

    @staticmethod
    def delete_single_preprocessor(instance_id=None, **kw):
        from backend_lib.lib_util import LibUtil
        LibUtil.check_exist_connected_data(ShipmentOrderItem, ShipmentOrderItem.fk_quote_item_id, instance_id)

        db.session.query(
            ShipmentQuoteItem
        ).filter(
            ShipmentQuoteItem.fk_parent_id == instance_id
        ).delete()

    @staticmethod
    def update_not_ordered(quote_item_id):
        order_quantity = db.session.query(
            db.func.sum(ShipmentOrderItem.order_quantity)
        ).filter(
            ShipmentOrderItem.fk_quote_item_id == quote_item_id
        ).first()[0]
        quote_item = db.session.query(
            ShipmentQuoteItem
        ).filter(
            ShipmentQuoteItem.id == quote_item_id
        ).first()
        not_ordered = quote_item.quote_quantity - order_quantity
        quote_item.not_ordered = not_ordered
        db.session.commit()

class LibShipmentOrder(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        LibCommon.get_item_number(data, 'order_number', ShipmentOrder, ShipmentOrder.order_number, '/shipment/order')

    @staticmethod
    def is_not_assign_quantity(order_id):
        order = db.session.query(ShipmentOrder).filter(ShipmentOrder.id == order_id).first()
        if not order:
            return False
        if order.order_type == 'STOCK':
            return True
        if order.order_type.find('반품') >= 0:
            return True
        return False

class LibShipmentOrderItem(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        basic_stock = LibSetupBasicStock.get_basic_stock(data['item_code'], data['warehouse_code'])
        if basic_stock is None:
            # 기초 재고가 없으면 에러
            from backend_lib.lib_exception import MesException
            MesException.raise_not_exist_basic_stock()
        if 'assign_quantity' not in data:
            return
        if basic_stock.available_stock < data['assign_quantity']:
            data['assign_quantity'] = basic_stock.available_stock

    @staticmethod
    def patch_single_preprocessor(instance_id=None, data=None, **kw):
        # 수주 항목이 종결되었으면 할당재고를 0으로 변경한다
        if 'closing_yn' in data:
            if data['closing_yn'] is True:
                data['assign_quantity'] = 0

        if 'warehouse_code' in data:
            order_item = db.session.query(ShipmentOrderItem).filter(ShipmentOrderItem.id == instance_id).first()
            if order_item:
                order_item.assign_quantity = 0
                db.session.commit()
                LibSetupBasicStock.update_available_stock(item_code=order_item.item_code,
                                                          warehouse_code=order_item.warehouse_code)

    @staticmethod
    def post_postprocessor(result=None, **kw):
        updated_stock = LibShipmentOrderItem.update_assign_quantity(result['id'], result['item_code'],
                                                                    result['warehouse_code'])
        # 기초재고의 가용재고를 업데이트
        # 업데이트된 가용재고를 결과에 담는다
        basic_stock = result['basic_stock']
        if basic_stock and updated_stock:
            basic_stock['available_stock'] = updated_stock.available_stock

        # 연결된 프로젝트 아이템이 있으면 미수주수량 업데이트
        if result['fk_project_item_id']:
            from backend_lib.lib_project import LibProjectItem
            LibProjectItem.update_not_ordered(result['fk_project_item_id'])

        # 연결된 견적 아이템이 있으면 미수주수량 업데이트
        if result['fk_quote_item_id']:
            LibShipmentQuoteItem.update_not_ordered(result['fk_quote_item_id'])

    @staticmethod
    def patch_single_postprocessor(result=None, **kw):
        LibSetupBasicStock.update_available_stock(result['item_code'], result['warehouse_code'])
        # 연결된 프로젝트 아이템이 있으면 미수주수량 업데이트
        if result['fk_project_item_id']:
            from backend_lib.lib_project import LibProjectItem
            LibProjectItem.update_not_ordered(result['fk_project_item_id'])

    @staticmethod
    def update_assign_quantity(order_item_id, item_code, warehouse):
        basic_stock = LibSetupBasicStock.update_available_stock(item_code, warehouse)

        order_item = db.session.query(ShipmentOrderItem).filter(ShipmentOrderItem.id == order_item_id).first()
        if order_item:
            if not order_item.assign_quantity:
                order_item.assign_quantity = 0
            if order_item.closing_yn != 0 or LibShipmentOrder.is_not_assign_quantity(order_item.fk_order_id):
                order_item.assign_quantity = 0
            else:
                if basic_stock.available_stock > 0 and order_item.not_shipped > 0:
                    if order_item.not_shipped - order_item.assign_quantity < basic_stock.available_stock:
                        order_item.assign_quantity = order_item.not_shipped
                    else:
                        order_item.assign_quantity += basic_stock.available_stock
                else:
                    order_item.assign_quantity = 0
        db.session.commit()
        updated_stock = LibSetupBasicStock.update_available_stock(item_code, warehouse)
        return updated_stock

    @staticmethod
    def get_total_assign_quantity_by_item_code(item_code, warehouse_code):
        assign_quantity = db.session.query(
            db.func.sum(ShipmentOrderItem.assign_quantity)
        ).filter(
            ShipmentOrderItem.item_code == item_code
        ).filter(
            ShipmentOrderItem.warehouse_code == warehouse_code
        ).first()[0]
        assign_quantity = 0 if not assign_quantity else assign_quantity
        return assign_quantity

    @staticmethod
    def get_many_postprocessor(result=None, **kw):
        if result:
            from backend_model.table_base import BaseClient
            item_list = result['objects']
            for item in item_list:
                try:
                    if item['order']['client_company']:
                        client = db.session.query(
                            BaseClient.alias
                        ).filter(
                            BaseClient.name == item['order']['client_company']
                        ).first()
                        item['order']['client_alias'] = client.alias
                except:
                    pass

class LibShipmentRelease(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        LibCommon.get_item_number(data, 'release_number', ShipmentRelease, ShipmentRelease.release_number,
                                  '/shipment/release')


class LibShipmentReleaseItem(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        # 현재고를 가져온다
        basic_stock = LibSetupBasicStock.get_basic_stock(data['item_code'], data['warehouse_code'])
        if basic_stock is None:
            from backend_lib.lib_exception import MesException
            MesException.raise_not_exist_basic_stock()
        # 마이너스 수불 처리 가능 여부 확인
        from backend_lib.lib_setup import LibSetupControl
        not_use_minus_stock = LibSetupControl.get_not_use_minus_stock(basic_stock.fk_company_id)
        # 현재고 계산
        new_current_stock = basic_stock.current_stock - data['release_quantity']
        # 마이너스 수불 처리 불가인 경우
        if not_use_minus_stock:
            if new_current_stock < 0:  # 출고수량이 현재고보다 크면 에러를 리턴한다
                from backend_lib.lib_exception import MesException
                MesException.raise_overflow_current_stock()
        # 현재고가 출고수량보다 크면 현재고를 업데이트한다
        LibSetupBasicStock.update_current_stock(data['item_code'], data['warehouse_code'], new_current_stock)

    @staticmethod
    def patch_single_preprocessor(instance_id=None, data=None, **kw):
        if 'release_quantity' in data:  # 출고수량이 있는지 확인
            # 기존의 출고품목 데이터를 가져온다
            release_item = db.session.query(
                ShipmentReleaseItem
            ).filter(
                ShipmentReleaseItem.id == instance_id
            ).first()
            if release_item:
                # 현재고를 가져온다
                basic_stock = LibSetupBasicStock.get_basic_stock(release_item.item_code, release_item.warehouse_code)
                # 기초 재고가 없으면 에러
                if basic_stock is None:
                    from backend_lib.lib_exception import MesException
                    MesException.raise_not_exist_basic_stock()
                # 마이너스 수불 처리 가능 여부 확인
                from backend_lib.lib_setup import LibSetupControl
                not_use_minus_stock = LibSetupControl.get_not_use_minus_stock(basic_stock.fk_company_id)
                # 새로운 현재고를 계산한다 (기존 현재고 + 기존 출고 수량 - 새로운 출고 수량)
                new_current_stock = basic_stock.current_stock + release_item.release_quantity - data['release_quantity']
                # 마이너스 수불 처리 불가인 경우
                if not_use_minus_stock:
                    if new_current_stock < 0:  # 새로운 현재고가 0보다 작으면 에러
                        from backend_lib.lib_exception import MesException
                        MesException.raise_overflow_current_stock()
                # 현재고를 업데이트한다
                LibSetupBasicStock.update_current_stock(release_item.item_code,
                                                        release_item.warehouse_code,
                                                        new_current_stock)
                # 가용재고를 업데이트한다
                LibSetupBasicStock.update_available_stock(release_item.item_code, release_item.warehouse_code)

    @staticmethod
    def post_postprocessor(result=None, **kw):
        LibShipmentReleaseItem.update_order_item_not_shipped(result['fk_order_item_id'])
        LibShipmentReleaseItem.update_order_item_assign_quantity(result['id'])

        # LOT 번호를 업데이트한다 (2023-12-5 주석처리 조상래, 사유: https://trello.com/c/EZMgI1IA)
        # LibShipmentReleaseItem.set_lot_number(result['fk_release_id'])

    @staticmethod
    def patch_single_postprocessor(result=None, **kw):
        LibShipmentReleaseItem.update_order_item_not_shipped(result['fk_order_item_id'])
        LibShipmentReleaseItem.update_order_item_assign_quantity(result['id'])

        # LOT 번호를 업데이트한다 (2023-12-5 주석처리 조상래, 사유: https://trello.com/c/EZMgI1IA) 
        # LibShipmentReleaseItem.set_lot_number(result['fk_release_id'])

    @staticmethod
    def update_order_item_not_shipped(order_item_id):
        """
        수주품목의 미출고 수량을 업데이트한다
        :param order_item_id: 수주품목 아이디
        :return:
        """
        # 수주 품목을 가져온다
        order_item = db.session.query(
            ShipmentOrderItem
        ).filter(
            ShipmentOrderItem.id == order_item_id
        ).first()
        if order_item:
            # 해당 수주 품목의 전체 출고 수량을 찾는다
            release_quantity = db.session.query(
                db.func.sum(ShipmentReleaseItem.release_quantity)
            ).filter(
                ShipmentReleaseItem.fk_order_item_id == order_item_id
            ).first()[0]
            if not release_quantity:
                release_quantity = 0
            # 수주 품목의 미출고 수량을 업데이트 (수주 수량 - 전체 출고 수량)
            order_item.not_shipped = order_item.order_quantity - release_quantity
            db.session.commit()

    @staticmethod
    def update_non_invoice(release_item_id):
        release_item = db.session.query(
            ShipmentReleaseItem
        ).filter(
            ShipmentReleaseItem.id == release_item_id
        ).first()
        if release_item:
            invoice_quantity = db.session.query(
                db.func.sum(ShipmentSalesStatementItem.quantity)
            ).filter(
                ShipmentSalesStatementItem.fk_release_item_id == release_item_id
            ).first()[0]
            if not invoice_quantity:
                invoice_quantity = 0
            release_item.non_invoice = release_item.release_quantity - invoice_quantity
            db.session.commit()

    @staticmethod
    def update_order_item_assign_quantity(release_item_id):
        """
        출고품목의 아이디로 수주품목을 찾아서 할당수량을 업데이트한다
        :param release_item_id: 출고품목 아이디
        :return:
        """
        release = db.session.query(
            ShipmentReleaseItem
        ).filter(
            ShipmentReleaseItem.id == release_item_id
        ).first()
        if release and release.order_item:
            LibShipmentOrderItem.update_assign_quantity(release.order_item.id,
                                                        release.order_item.item_code,
                                                        release.order_item.warehouse_code)
            LibSetupBasicStock.update_available_stock(release.order_item.item_code, release.order_item.warehouse_code)

    @staticmethod
    def get_total_release_quantity_by_item_code_query(use_count, item_code, warehouse_code, start_date=None, end_date=None):
        if use_count:
            query = db.session.query(
                db.func.sum(ShipmentReleaseItem.release_quantity)
            )
        else:
            query = db.session.query(
                ShipmentRelease.release_number,
                ShipmentRelease.release_date,
                ShipmentRelease.client_company,
                ShipmentRelease.release_type,
                ShipmentReleaseItem.cost_price,
                db.func.ifnull(ShipmentReleaseItem.total_cost_price, 0).label('total_cost_price'),
                ShipmentReleaseItem.unit_price,
                ShipmentReleaseItem.release_quantity,
                ShipmentReleaseItem.fk_project_management_id
            )
        query = query.join(
            ShipmentRelease, ShipmentReleaseItem.fk_release_id == ShipmentRelease.id
        ).filter(
            ShipmentReleaseItem.item_code == item_code
        ).filter(
            ShipmentReleaseItem.warehouse_code == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                ShipmentRelease.release_date >= start_date
            ).filter(
                ShipmentRelease.release_date <= end_date
            )
        elif end_date:
            query = query.filter(
                ShipmentRelease.release_date < end_date
            )
        return query

    @staticmethod
    def get_total_release_quantity_by_item_code(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibShipmentReleaseItem.get_total_release_quantity_by_item_code_query(use_count=True,
                                                                                     item_code=item_code,
                                                                                     warehouse_code=warehouse_code,
                                                                                     start_date=start_date,
                                                                                     end_date=end_date)
        release_quantity = query.first()[0]
        release_quantity = 0 if not release_quantity else release_quantity
        return release_quantity

    @staticmethod
    def get_all_release_item_for_statistics(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibShipmentReleaseItem.get_total_release_quantity_by_item_code_query(use_count=False,
                                                                                     item_code=item_code,
                                                                                     warehouse_code=warehouse_code,
                                                                                     start_date=start_date,
                                                                                     end_date=end_date)
        release_items = query.all()
        return release_items

    @staticmethod
    def get_total_release_price_by_item_code(item_code: str, warehouse_code: str, start_date=None, end_date=None) -> Decimal:
        query = db.session.query(
            db.func.sum(db.func.ifnull(ShipmentReleaseItem.total_cost_price, 0))
        ).join(
            ShipmentRelease, ShipmentReleaseItem.fk_release_id == ShipmentRelease.id
        ).filter(
            ShipmentReleaseItem.item_code == item_code
        ).filter(
            ShipmentReleaseItem.warehouse_code == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                ShipmentRelease.release_date >= start_date
            ).filter(
                ShipmentRelease.release_date <= end_date
            )
        elif end_date:
            query = query.filter(
                ShipmentRelease.release_date < end_date
            )
        release_price = query.first()[0]
        release_price = Decimal('0') if not release_price else release_price
        return release_price

    @staticmethod
    def set_lot_number(release_id):
        release_items = db.session.query(
            ShipmentReleaseItem
        ).filter(
            ShipmentReleaseItem.fk_release_id == release_id
        ).all()
        seq = 1
        for release_item in release_items:
            release_item.lot_number = f'LOT-S-{release_item.release.release_number}-{seq}'
            seq += 1
        db.session.commit()
    @staticmethod
    def get_many_postprocessor(result=None, **kw):
        if result:
            from backend_model.table_base import BaseClient
            item_list = result['objects']
            for item in item_list:
                try:
                    if item['release']['client_company']:
                        client = db.session.query(
                            BaseClient.alias
                        ).filter(
                            BaseClient.name == item['release']['client_company']
                        ).first()
                        item['release']['client_alias'] = client.alias
                except:
                    pass

class LisShipmentReleaseItemWithClient(object):
    @staticmethod
    def get_many_postprocessor(result=None, search_params=None, **kw):
        if result:
            from backend_model.table_base import BaseClient, BaseEmployee, BaseDepartment

            item_list = result['objects']
            for item in item_list:
                try:
                    if item['release']['client_company']:
                        client = db.session.query(
                            BaseClient.id,
                            BaseClient.client_type,
                            BaseClient.alias,
                            BaseEmployee.emp_name,
                            BaseDepartment.department_name
                        ).filter(
                            BaseClient.name == item['release']['client_company']
                        ).join(
                            BaseEmployee, BaseEmployee.emp_name == BaseClient.manager
                        ).join(
                            BaseDepartment, BaseDepartment.id == BaseEmployee.fk_department_id
                        ).first()
                        item['release']['department'] = client.department_name
                        item['release']['manager'] = client.emp_name
                        item['release']['client_type'] = client.client_type
                        item['release']['client_alias'] = client.alias
                except:
                    pass

class LibShipmentReleaseReturn(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        LibCommon.get_item_number(data, 'return_number', ShipmentReleaseReturn, ShipmentReleaseReturn.return_number,
                                  '/shipment/release-return')


class LibShipmentReleaseReturnItem(object):
    @staticmethod
    def post_postprocessor(result=None, **kw):
        from backend_lib.lib_setup import LibSetupBasicStock
        LibSetupBasicStock.update_stock_by_item_code(result['item_code'], result['warehouse_code'])

    @staticmethod
    def patch_single_postprocessor(result=None, **kw):
        from backend_lib.lib_setup import LibSetupBasicStock
        LibSetupBasicStock.update_stock_by_item_code(result['item_code'], result['warehouse_code'])

    @staticmethod
    def update_non_invoice(return_item_id):
        return_item = db.session.query(
            ShipmentReleaseReturnItem
        ).filter(
            ShipmentReleaseReturnItem.id == return_item_id
        ).first()
        if return_item:
            invoice_quantity = db.session.query(
                db.func.sum(ShipmentSalesStatementItem.quantity)
            ).filter(
                ShipmentSalesStatementItem.fk_release_return_item_id == return_item_id
            ).first()[0]
            if not invoice_quantity:
                invoice_quantity = 0
            return_item.non_invoice = return_item.return_quantity - invoice_quantity
            db.session.commit()

    @staticmethod
    def get_total_receiving_quantity_by_item_code_query(use_count, item_code, warehouse_code, start_date=None, end_date=None):
        if use_count:
            query = db.session.query(
                db.func.sum(ShipmentReleaseReturnItem.return_quantity)
            )
        else:
            query = db.session.query(
                ShipmentReleaseReturn.return_number,
                ShipmentReleaseReturn.return_date,
                ShipmentReleaseReturn.client_company,
                ShipmentReleaseReturn.return_type,
                ShipmentReleaseReturnItem.return_quantity,
                ShipmentReleaseReturnItem.unit_price,
                db.func.ifnull(ShipmentReleaseReturnItem.cost_price, 0).label('cost_price')
            )
        query = query.join(
            ShipmentReleaseReturn, ShipmentReleaseReturnItem.fk_release_return_id == ShipmentReleaseReturn.id
        ).filter(
            ShipmentReleaseReturnItem.item_code == item_code
        ).filter(
            ShipmentReleaseReturnItem.warehouse_code == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                ShipmentReleaseReturn.return_date >= start_date
            ).filter(
                ShipmentReleaseReturn.return_date <= end_date
            )
        elif end_date:
            query = query.filter(
                ShipmentReleaseReturn.return_date < end_date
            )
        return query

    @staticmethod
    def get_total_receiving_quantity_by_item_code(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibShipmentReleaseReturnItem.get_total_receiving_quantity_by_item_code_query(use_count=True,
                                                                                             item_code=item_code,
                                                                                             warehouse_code=warehouse_code,
                                                                                             start_date=start_date,
                                                                                             end_date=end_date)
        receiving_quantity = query.first()[0]
        receiving_quantity = 0 if not receiving_quantity else receiving_quantity
        return receiving_quantity

    @staticmethod
    def get_all_receiving_item_for_statistics(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibShipmentReleaseReturnItem.get_total_receiving_quantity_by_item_code_query(use_count=False,
                                                                                             item_code=item_code,
                                                                                             warehouse_code=warehouse_code,
                                                                                             start_date=start_date,
                                                                                             end_date=end_date)
        release_items = query.all()
        return release_items

    @staticmethod
    def get_total_receiving_price_by_item_code(item_code: str, warehouse_code: str, start_date=None, end_date=None) -> int:
        query = db.session.query(
            db.func.sum(ShipmentReleaseReturnItem.return_quantity * db.func.ifnull(ShipmentReleaseItem.cost_price, 0))
        ).join(
            ShipmentReleaseReturn, ShipmentReleaseReturnItem.fk_release_return_id == ShipmentReleaseReturn.id
        ).filter(
            ShipmentReleaseReturnItem.item_code == item_code
        ).filter(
            ShipmentReleaseReturnItem.warehouse_code == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                ShipmentReleaseReturn.return_date >= start_date
            ).filter(
                ShipmentReleaseReturn.return_date <= end_date
            )
        elif end_date:
            query = query.filter(
                ShipmentReleaseReturn.return_date < end_date
            )
        receiving_price = query.first()[0]
        receiving_price = 0 if not receiving_price else receiving_price
        return receiving_price
    
    @staticmethod
    def get_many_postprocessor(result=None, **kw):
        if result:
            from backend_model.table_base import BaseClient
            item_list = result['objects']
            for item in item_list:
                try:
                    if item['release_return']['client_company']:
                        client = db.session.query(
                            BaseClient.alias
                        ).filter(
                            BaseClient.name == item['release_return']['client_company']
                        ).first()
                        item['release_return']['client_alias'] = client.alias
                except:
                    pass

class LibShipmentSalesStatement(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        LibCommon.get_item_number(data, 'sales_number', ShipmentSalesStatement, ShipmentSalesStatement.sales_number,
                                  '/shipment/sales-statement')

    @staticmethod
    def update_not_deposit(sales_id):
        """
        매출계산서의 미입금 금액을 업데이트한다
        :param sales_id: 매출계산서 아이디
        :return:
        """
        deposit_price = db.session.query(
            db.func.sum(ShipmentDepositItem.price)
        ).filter(
            ShipmentDepositItem.fk_sales_id == sales_id
        ).first()[0]
        if not deposit_price:
            deposit_price = 0
        # total_price = db.session.query(
        #     db.func.sum(ShipmentSalesStatementItem.total_price)
        # ).filter(
        #     ShipmentSalesStatementItem.fk_sales_id == sales_id
        # ).first()[0]
            
        total_price = db.session.query(ShipmentSalesStatement.total_price).filter(ShipmentSalesStatement.id == sales_id).first()[0]
        if not total_price:
            total_price = 0

        not_deposit = total_price - deposit_price
        # if not_deposit < 0:
        #     not_deposit = 0

        sales = db.session.query(
            ShipmentSalesStatement
        ).filter(
            ShipmentSalesStatement.id == sales_id
        ).first()
        if sales:
            sales.not_deposit = not_deposit
            db.session.commit()

    @staticmethod
    def get_many_postprocessor(result=None, **kw):
        if result:
            from backend_model.table_base import BaseClient
            item_list = result['objects']
            for item in item_list:
                try:
                    if item['client_company']:
                        client = db.session.query(
                            BaseClient.alias
                        ).filter(
                            BaseClient.name == item['client_company']
                        ).first()
                        item['client_alias'] = client.alias
                except:
                    pass

class LibShipmentSalesStatementItem(object):
    @staticmethod
    def post_postprocessor(result=None, **kw):
        LibShipmentSalesStatement.update_not_deposit(result['fk_sales_id'])
        try:
            if result['fk_project_management_id']:
                from backend_lib.lib_project import LibProjectManagement
                LibProjectManagement.update_non_invoice(result['fk_project_management_id'])
            if result['fk_release_item_id']:
                LibShipmentReleaseItem.update_non_invoice(result['fk_release_item_id'])
            if result['fk_release_return_item_id']:
                LibShipmentReleaseReturnItem.update_non_invoice(result['fk_release_return_item_id'])
        except:
            pass

    @staticmethod
    def patch_single_postprocessor(result=None, **kw):
        LibShipmentSalesStatement.update_not_deposit(result['fk_sales_id'])
        try:
            if result['fk_project_management_id']:
                from backend_lib.lib_project import LibProjectManagement
                LibProjectManagement.update_non_invoice(result['fk_project_management_id'])
            if result['fk_release_item_id']:
                LibShipmentReleaseItem.update_non_invoice(result['fk_release_item_id'])
            if result['fk_release_return_item_id']:
                LibShipmentReleaseReturnItem.update_non_invoice(result['fk_release_return_item_id'])
        except:
            pass

    @staticmethod
    def get_many_postprocessor(result=None, **kw):
        if result:
            from backend_model.table_base import BaseClient
            item_list = result['objects']
            for item in item_list:
                try:
                    if item['sales']['client_company']:
                        client = db.session.query(
                            BaseClient.alias
                        ).filter(
                            BaseClient.name == item['sales']['client_company']
                        ).first()
                        item['sales']['client_alias'] = client.alias
                except:
                    pass

class LibShipmentDeposit(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        LibCommon.get_item_number(data, 'deposit_number', ShipmentDeposit, ShipmentDeposit.deposit_number,
                                  '/shipment/deposit')


class LibShipmentDepositItem(object):
    @staticmethod
    def post_postprocessor(result=None, **kw):
        LibShipmentSalesStatement.update_not_deposit(result['fk_sales_id'])

    @staticmethod
    def patch_single_postprocessor(result=None, **kw):
        LibShipmentSalesStatement.update_not_deposit(result['fk_sales_id'])

    @staticmethod
    def get_many_postprocessor(result=None, **kw):
        if result:
            from backend_model.table_base import BaseClient
            item_list = result['objects']
            for item in item_list:
                try:
                    if item['deposit']['client_company']:
                        client = db.session.query(
                            BaseClient.alias
                        ).filter(
                            BaseClient.name == item['deposit']['client_company']
                        ).first()
                        item['deposit']['client_alias'] = client.alias
                except:
                    pass

class LibShipmentLend(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        LibCommon.get_item_number(data, 'lend_number', ShipmentLend, ShipmentLend.lend_number,
                                  '/shipment/lend')

    @staticmethod
    def update_not_retrieved_quantity(lend_id):
        lend = db.session.query(
            ShipmentLend
        ).filter(
            ShipmentLend.id == lend_id
        ).first()
        if lend:
            retrieved_quantity = db.session.query(
                db.func.sum(ShipmentRetrieve.quantity)
            ).filter(
                ShipmentRetrieve.fk_lend_id == lend_id
            ).first()[0]
            if not retrieved_quantity:
                retrieved_quantity = 0

            lend.not_retrieved_quantity = lend.quantity - retrieved_quantity
            db.session.commit()


class LibShipmentRetrieve(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        LibCommon.get_item_number(data, 'retrieve_number', ShipmentRetrieve, ShipmentRetrieve.retrieve_number,
                                  '/shipment/retrieve')

    @staticmethod
    def post_postprocessor(result=None, **kw):
        LibShipmentLend.update_not_retrieved_quantity(result['fk_lend_id'])

    @staticmethod
    def patch_single_postprocessor(result=None, **kw):
        LibShipmentLend.update_not_retrieved_quantity(result['fk_lend_id'])
