# -*- coding: utf-8 -*-

from decimal import Decimal
from backend_model.table_purchase import *

db = DBManager.db


class LibPurchaseOrderPlan(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'order_plan_number', PurchaseOrderPlan, PurchaseOrderPlan.order_plan_number,
                                  '/purchase/order-plan')


class LibPurchaseOrderPlanItem(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_setup import LibSetupBasicStock

        if 'item_code' in data and 'warehouse_code' in data:
            LibSetupBasicStock.check_basic_stock(data['item_code'], data['warehouse_code'])

    @staticmethod
    def delete_single_preprocessor(instance_id=None, **kw):
        from backend_lib.lib_util import LibUtil
        LibUtil.check_exist_connected_data(PurchaseOrderItem, PurchaseOrderItem.fk_order_plan_item_id, instance_id)

    @staticmethod
    def post_postprocessor(result=None, **kw):
        if result['order_plan_quantity'] and result['fk_measure_requirement_item2_id']:
            from backend_lib.lib_production import LibMeasureRequirementItem2
            LibMeasureRequirementItem2.update_unordered_plan_quantity(result['fk_measure_requirement_item2_id'],
                                                                      result['order_plan_quantity'])

    @staticmethod
    def patch_single_postprocessor(result=None, **kw):
        if result['order_plan_quantity'] and result['fk_measure_requirement_item2_id']:
            from backend_lib.lib_production import LibMeasureRequirementItem2
            LibMeasureRequirementItem2.update_unordered_plan_quantity(result['fk_measure_requirement_item2_id'],
                                                                      result['order_plan_quantity'])

    @staticmethod
    def update_unordered_quantity(order_plan_item_id):
        try:
            # 발주계획 품목을 가져온다
            order_plan_item = db.session.query(
                PurchaseOrderPlanItem
            ).filter(
                PurchaseOrderPlanItem.id == order_plan_item_id
            ).first()
            if order_plan_item is None:
                return

            # 해당 발주 품목의 전체 발주 수량을 찾는다
            total_order_quantity = db.session.query(
                db.func.sum(PurchaseOrderItem.order_quantity)
            ).filter(
                PurchaseOrderItem.fk_order_plan_item_id == order_plan_item_id
            ).first()[0]
            if total_order_quantity is None:
                total_order_quantity = 0

            # 발주계획 품목의 미발주 수량을 업데이트 (발주계획 수량 - 전체 발주 수량)
            unordered_quantity = order_plan_item.order_plan_quantity - total_order_quantity
            if unordered_quantity > 0:
                order_plan_item.unordered_quantity = unordered_quantity
            else:
                order_plan_item.unordered_quantity = 0
            db.session.commit()
        except:
            pass
        
    @staticmethod
    def get_many_postprocessor(result=None, **kw):
        if result:
            from backend_model.table_base import BaseClient
            item_list = result['objects']
            for item in item_list:
                try:
                    if item['main_supplier']:
                        client = db.session.query(
                            BaseClient.alias
                        ).filter(
                            BaseClient.name == item['main_supplier']
                        ).first()
                        item['main_supplier_alias'] = client.alias
                except:
                    pass

class LibPurchaseOrder(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'order_number', PurchaseOrder, PurchaseOrder.order_number,
                                  '/purchase/order-plan')


class LibPurchaseOrderItem(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_setup import LibSetupBasicStock

        if 'item_code' in data and 'warehouse_code' in data:
            LibSetupBasicStock.check_basic_stock(data['item_code'], data['warehouse_code'])

    @staticmethod
    def post_postprocessor(result=None, **kw):
        LibPurchaseOrderPlanItem.update_unordered_quantity(result['fk_order_plan_item_id'])

    @staticmethod
    def patch_single_postprocessor(result=None, **kw):
        LibPurchaseOrderPlanItem.update_unordered_quantity(result['fk_order_plan_item_id'])

    @staticmethod
    def get_many_postprocessor(result=None, search_params=None, **kw):
        item_list = result['objects']
        from backend_model.table_base import BaseClient
        for item in item_list:
            try:
                # 발주 품목에 대한 검수수량 구한다 (가입고의 검수수량)
                total_quantity = db.session.query(
                    db.func.sum(PurchasePreReceivingItem.check_quantity),
                    db.func.sum(PurchasePreReceivingItem.bad_quantity),
                    db.func.sum(PurchasePreReceivingItem.good_quantity)
                ).filter(
                    PurchasePreReceivingItem.fk_order_item_id == item['id']
                ).first()
                # 검수수량을 추가한다
                if total_quantity:
                    if total_quantity[0]:
                        item['check_quantity'] = total_quantity[0]
                    else:
                        item['check_quantity'] = 0
                    if total_quantity[1]:
                        item['bad_quantity'] = total_quantity[1]
                    else:
                        item['bad_quantity'] = 0
                    if total_quantity[2]:
                        item['good_quantity'] = total_quantity[2]
                    else:
                        item['good_quantity'] = 0
                else:
                    item['check_quantity'] = 0
                    item['bad_quantity'] = 0
                    item['good_quantity'] = 0
            except:
                pass

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
    @staticmethod
    def delete_single_preprocessor(instance_id=None, **kw):
        from backend_lib.lib_util import LibUtil
        LibUtil.check_exist_connected_data(PurchasePreReceivingItem, PurchasePreReceivingItem.fk_order_item_id,
                                           instance_id)

    @staticmethod
    def update_not_shipped(order_item_id):
        try:
            # 총 입고 수량을 구한다
            total_receiving_quantity = LibPurchaseReceivingItem.get_total_receiving_quantity_by_order_item(order_item_id)
            # 발주품목을 구한다
            order_item = db.session.query(
                PurchaseOrderItem
            ).filter(
                PurchaseOrderItem.id == order_item_id
            ).first()
            # 미입고 수량을 업데이트한다
            order_item.not_shipped = order_item.order_quantity - total_receiving_quantity
            db.session.commit()
        except:
            pass


class LibPurchaseOrderReceivingStatus(object):
    @staticmethod
    def get_many_postprocessor(result=None, search_params=None, **kw):
        item_list = result['objects']
        from backend_model.table_base import BaseClient
        for item in item_list:
            try:
                receiving_quantity = db.session.query(
                    db.func.sum(PurchaseReceivingItem.receiving_quantity)
                ).filter(
                    PurchaseReceivingItem.fk_order_item_id == item['id']
                ).first()[0]
                if not receiving_quantity:
                    receiving_quantity = 0
                item['receiving_quantity'] = receiving_quantity

            except:
                item['receiving_quantity'] = 0

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
            
class LibPurchasePreReceiving(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'prereceiving_number', PurchasePreReceiving,
                                  PurchasePreReceiving.prereceiving_number, '/purchase/pre-receiving')


class LibPurchasePreReceivingItem(object):
    @staticmethod
    def update_check_quantity(pre_receiving_id: int, check_quantity: int, bad_quantity: int, good_quantity: int,
                              check: int):
        """
        가입고품목의 검수수량, 불량수량, 양품수량, 검수완료를 업데이트한다

        :param pre_receiving_id: 가입고품목 아이디
        :param check_quantity: 검수수량
        :param bad_quantity: 불량수량
        :param good_quantity: 양품수량
        :param check: 검수완료
        :return:
        """
        pre_receiving_item = db.session.query(
            PurchasePreReceivingItem
        ).filter(
            PurchasePreReceivingItem.id == pre_receiving_id
        ).first()
        if pre_receiving_item:
            receiving_quantity = db.session.query(
                db.func.sum(PurchaseReceivingItem.receiving_quantity)
            ).filter(
                PurchaseReceivingItem.fk_prereceiving_item_id == pre_receiving_item.id
            ).first()[0]
            if not receiving_quantity:
                receiving_quantity = 0

            pre_receiving_item.check_quantity = check_quantity
            pre_receiving_item.bad_quantity = bad_quantity
            pre_receiving_item.good_quantity = good_quantity
            pre_receiving_item.check_yn = check
            pre_receiving_item.not_shipped = pre_receiving_item.good_quantity - receiving_quantity

            order_item = db.session.query(
                PurchaseOrderItem
            ).filter(
                PurchaseOrderItem.id == pre_receiving_item.fk_order_item_id
            ).first()
            if order_item:
                order_item.check_yn = check
            db.session.commit()

    @staticmethod
    def delete_single_preprocessor(instance_id=None, **kw):
        from backend_lib.lib_util import LibUtil
        from backend_model.table_quality import QualityManagement
        LibUtil.check_exist_connected_data(QualityManagement, QualityManagement.fk_prereceiving_item, instance_id)

    @staticmethod
    def get_many_postprocessor(result=None, **kw):
        if result:
            from backend_model.table_base import BaseClient
            item_list = result['objects']
            for item in item_list:
                try:
                    if item['prereceiving']['client_company']:
                        client = db.session.query(
                            BaseClient.alias
                        ).filter(
                            BaseClient.name == item['prereceiving']['client_company']
                        ).first()
                        item['prereceiving']['client_alias'] = client.alias
                except:
                    pass

class LibPurchaseReceiving(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'receiving_number', PurchaseReceiving, PurchaseReceiving.receiving_number,
                                  '/purchase/receiving')


class LibPurchaseReceivingItem(object):
    @staticmethod
    def post_postprocessor(result=None, **kw):
        try:
            # LOT 번호를 업데이트한다
            LibPurchaseReceivingItem.set_lot_number(result['fk_receiving_id'])

            from backend_lib.lib_setup import LibSetupBasicStock
            # 현재고를 업데이트한다
            LibSetupBasicStock.update_stock_by_item_code(result['item_code'], result['warehouse_code'])
        except:
            pass

    @staticmethod
    def patch_single_postprocessor(result=None, **kw):
        from backend_lib.lib_util import LibUtil
        try:
            # LOT 번호를 업데이트한다
            LibPurchaseReceivingItem.set_lot_number(result['fk_receiving_id'])

            from backend_lib.lib_setup import LibSetupBasicStock
            # 현재고를 업데이트한다
            #------------------------------------------
            # 입고창고 수정 시 창고별 재고 수정 임시 코드
            base_warehouse = db.session.query(
                BaseWarehouse.wh_code
            ).all()
            if base_warehouse:
                for warehouse_code in base_warehouse:
                    LibSetupBasicStock.update_stock_by_item_code(result['item_code'], warehouse_code)
            #------------------------------------------
            # 가입고 품목의 단가, 공급가 업데이트
            if result['fk_prereceiving_item_id']:
                prereceiving_item = db.session.query(
                    PurchasePreReceivingItem
                ).filter(
                    PurchasePreReceivingItem.id == result['fk_prereceiving_item_id']
                ).first()
                if prereceiving_item:
                    prereceiving_item.unit_price = result['unit_price']
                    prereceiving_item.supply_price = prereceiving_item.prereceiving_quantity * prereceiving_item.unit_price
                    db.session.commit()

                    # 발주 품목의 단가, 공급가 업데이트
                    if prereceiving_item.fk_order_item_id:
                        order_item = db.session.query(
                            PurchaseOrderItem
                        ).filter(
                            PurchaseOrderItem.id == prereceiving_item.fk_order_item_id
                        ).first()
                        if order_item:
                            order_item.unit_price = result['unit_price']
                            order_item.supply_price = order_item.order_quantity * order_item.unit_price
                            db.session.commit()

                        # 발주의 공급가, 부가세, 합계금액 업데이트
                        order = db.session.query(
                            PurchaseOrder
                        ).filter(
                            PurchaseOrder.id == order_item.fk_purchase_order_id
                        ).first()
                        if order:
                            order_items = db.session.query(
                                PurchaseOrderItem
                            ).filter(
                                PurchaseOrderItem.fk_purchase_order_id == order.id
                            ).all()
                            total_supply_price = 0
                            total_vat = 0
                            total_price = 0
                            for item in order_items:
                                price = LibUtil.calculate_price(order.vat_type, item.order_quantity,
                                                                item.unit_price)
                                total_supply_price += price['supply_price']
                                total_vat += price['vat']
                                total_price += price['total_price']
                            order.supply_price = total_supply_price
                            order.vat = total_vat
                            order.total_price = total_price
                            db.session.commit()

            # 가입고의 공급가, 부가세, 합계금액 업데이트
            if result['fk_prereceiving_id']:
                prereceiving = db.session.query(
                    PurchasePreReceiving
                ).filter(
                    PurchasePreReceiving.id == result['fk_prereceiving_id']
                ).first()
                if prereceiving:
                    prereceiving_items = db.session.query(
                        PurchasePreReceivingItem
                    ).filter(
                        PurchasePreReceivingItem.fk_prereceiving_id == prereceiving.id
                    ).all()
                    total_supply_price = 0
                    total_vat = 0
                    total_price = 0
                    for item in prereceiving_items:
                        price = LibUtil.calculate_price(prereceiving.vat_type, item.prereceiving_quantity, item.unit_price)
                        total_supply_price += price['supply_price']
                        total_vat += price['vat']
                        total_price += price['total_price']
                    prereceiving.supply_price = total_supply_price
                    prereceiving.vat = total_vat
                    prereceiving.total_price = total_price
                    db.session.commit()
        except:
            pass

    @staticmethod
    def get_total_receiving_quantity_by_order_item(order_item_id):
        total_receiving_quantity = db.session.query(
            db.func.sum(PurchaseReceivingItem.receiving_quantity)
        ).filter(
            PurchaseReceivingItem.fk_order_item_id == order_item_id
        ).first()[0]
        if total_receiving_quantity:
            return total_receiving_quantity
        else:
            return 0

    @staticmethod
    def set_lot_number(receiving_id):
        receiving_items = db.session.query(
            PurchaseReceivingItem
        ).filter(
            PurchaseReceivingItem.fk_receiving_id == receiving_id
        ).all()
        seq = 1
        for receiving_item in receiving_items:
            receiving_item.lot_number = f'LOT-{receiving_item.receiving.receiving_number}-{seq}'
            seq += 1
        db.session.commit()

    @staticmethod
    def get_total_receiving_quantity_by_item_code_query(use_count, item_code, warehouse_code, start_date=None, end_date=None):
        if use_count:
            query = db.session.query(
                db.func.sum(PurchaseReceivingItem.receiving_quantity)
            )
        else:
            query = db.session.query(
                PurchaseReceiving.receiving_number,
                PurchaseReceiving.receiving_date,
                PurchaseReceiving.client_company,
                PurchaseReceiving.receiving_type,
                PurchaseReceivingItem.receiving_quantity,
                PurchaseReceivingItem.unit_price,
                PurchaseReceivingItem.fk_project_management_id
            )
        query = query.join(
            PurchaseReceiving, PurchaseReceivingItem.fk_receiving_id == PurchaseReceiving.id
        ).filter(
            PurchaseReceivingItem.item_code == item_code
        ).filter(
            PurchaseReceivingItem.warehouse_code == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                PurchaseReceiving.receiving_date2 >= start_date
            ).filter(
                PurchaseReceiving.receiving_date2 <= end_date
            )
        elif end_date:
            query = query.filter(
                PurchaseReceiving.receiving_date2 < end_date
            )
        return query

    @staticmethod
    def get_total_receiving_quantity_by_item_code(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibPurchaseReceivingItem.get_total_receiving_quantity_by_item_code_query(use_count=True,
                                                                                         item_code=item_code,
                                                                                         warehouse_code=warehouse_code,
                                                                                         start_date=start_date,
                                                                                         end_date=end_date)
        receiving_quantity = query.first()[0]
        receiving_quantity = 0 if not receiving_quantity else receiving_quantity
        return receiving_quantity

    @staticmethod
    def get_all_receiving_item_for_statistics(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibPurchaseReceivingItem.get_total_receiving_quantity_by_item_code_query(use_count=False,
                                                                                         item_code=item_code,
                                                                                         warehouse_code=warehouse_code,
                                                                                         start_date=start_date,
                                                                                         end_date=end_date)
        release_items = query.all()
        return release_items

    @staticmethod
    def get_total_receiving_price_by_item_code(item_code: str, warehouse_code: str, start_date=None, end_date=None) -> int:
        query = db.session.query(
            db.func.sum(PurchaseReceivingItem.receiving_quantity * PurchaseReceivingItem.unit_price)
        ).join(
            PurchaseReceiving, PurchaseReceivingItem.fk_receiving_id == PurchaseReceiving.id
        ).filter(
            PurchaseReceivingItem.item_code == item_code
        ).filter(
            PurchaseReceivingItem.warehouse_code == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                PurchaseReceiving.receiving_date2 >= start_date
            ).filter(
                PurchaseReceiving.receiving_date2 <= end_date
            )
        elif end_date:
            query = query.filter(
                PurchaseReceiving.receiving_date2 < end_date
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
                    if item['receiving']['client_company']:
                        client = db.session.query(
                            BaseClient.alias
                        ).filter(
                            BaseClient.name == item['receiving']['client_company']
                        ).first()
                        item['receiving']['client_alias'] = client.alias
                except:
                    pass

class LibPurchaseReceivingReturn(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'return_number', PurchaseReceivingReturn, PurchaseReceivingReturn.return_number,
                                  '/purchase/receiving-return')


class LibPurchaseReceivingReturnItem(object):
    @staticmethod
    def post_postprocessor(result=None, **kw):
        from backend_lib.lib_setup import LibSetupBasicStock
        LibSetupBasicStock.update_stock_by_item_code(result['item_code'], result['warehouse_code'])

    @staticmethod
    def patch_single_postprocessor(result=None, **kw):
        from backend_lib.lib_setup import LibSetupBasicStock
        LibSetupBasicStock.update_stock_by_item_code(result['item_code'], result['warehouse_code'])

    @staticmethod
    def get_total_release_quantity_by_item_code_query(use_count, item_code, warehouse_code, start_date=None, end_date=None):
        if use_count:
            query = db.session.query(
                db.func.sum(PurchaseReceivingReturnItem.return_quantity),
            )
        else:
            query = db.session.query(
                PurchaseReceivingReturn.return_number,
                PurchaseReceivingReturn.return_date,
                PurchaseReceivingReturn.client_company,
                PurchaseReceivingReturn.return_type,
                PurchaseReceivingReturnItem.return_quantity,
                PurchaseReceivingReturnItem.cost_price,
                db.func.ifnull(PurchaseReceivingReturnItem.total_cost_price, 0).label('total_cost_price'),
                PurchaseReceivingItem.unit_price,
            ).join(
                PurchaseReceivingItem, PurchaseReceivingReturnItem.fk_receiving_item_id == PurchaseReceivingItem.id
            )
        query = query.join(
            PurchaseReceivingReturn, PurchaseReceivingReturnItem.fk_receiving_return_id == PurchaseReceivingReturn.id
        ).filter(
            PurchaseReceivingReturnItem.item_code == item_code
        ).filter(
            PurchaseReceivingReturnItem.warehouse_code == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                PurchaseReceivingReturn.return_date >= start_date
            ).filter(
                PurchaseReceivingReturn.return_date <= end_date
            )
        elif end_date:
            query = query.filter(
                PurchaseReceivingReturn.return_date < end_date
            )
        return query

    @staticmethod
    def get_total_release_quantity_by_item_code(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibPurchaseReceivingReturnItem.get_total_release_quantity_by_item_code_query(use_count=True,
                                                                                             item_code=item_code,
                                                                                             warehouse_code=warehouse_code,
                                                                                             start_date=start_date,
                                                                                             end_date=end_date)
        release_quantity = query.first()[0]
        release_quantity = 0 if not release_quantity else release_quantity
        return release_quantity

    @staticmethod
    def get_all_release_item_for_statistics(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibPurchaseReceivingReturnItem.get_total_release_quantity_by_item_code_query(use_count=False,
                                                                                             item_code=item_code,
                                                                                             warehouse_code=warehouse_code,
                                                                                             start_date=start_date,
                                                                                             end_date=end_date)
        release_items = query.all()
        return release_items

    @staticmethod
    def get_total_release_price_by_item_code(item_code: str, warehouse_code: str, start_date=None, end_date=None) -> Decimal:
        query = db.session.query(
            db.func.sum(db.func.ifnull(PurchaseReceivingReturnItem.total_cost_price, 0)),
        ).join(
            PurchaseReceivingReturn, PurchaseReceivingReturnItem.fk_receiving_return_id == PurchaseReceivingReturn.id
        ).filter(
            PurchaseReceivingReturnItem.item_code == item_code
        ).filter(
            PurchaseReceivingReturnItem.warehouse_code == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                PurchaseReceivingReturn.return_date >= start_date
            ).filter(
                PurchaseReceivingReturn.return_date <= end_date
            )
        elif end_date:
            query = query.filter(
                PurchaseReceivingReturn.return_date < end_date
            )
        release_price = query.first()[0]
        release_price = Decimal('0') if not release_price else release_price
        return release_price

    @staticmethod
    def get_many_postprocessor(result=None, **kw):
        if result:
            from backend_model.table_base import BaseClient
            item_list = result['objects']
            for item in item_list:
                try:
                    if item['receiving_return']['client_company']:
                        client = db.session.query(
                            BaseClient.alias
                        ).filter(
                            BaseClient.name == item['receiving_return']['client_company']
                        ).first()
                        item['receiving_return']['client_alias'] = client.alias
                except:
                    pass

class LibPurchaseStatement(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'statement_number', PurchaseStatement, PurchaseStatement.statement_number, '/purchase/statement')

class LibPurchasePayment(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'payment_number', PurchasePayment, PurchasePayment.payment_number, '/purchase/payment')