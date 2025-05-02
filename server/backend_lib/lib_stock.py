# -*- coding: utf-8 -*-

from decimal import Decimal
from backend_model.table_stock import *
from backend_lib.lib_common import LibCommon

db = DBManager.db


class LibStockEtc(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        LibCommon.get_item_number(data, 'number', StockEtc, StockEtc.number, '/stock/etc')


class LibStockEtcItem(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_setup import LibSetupBasicStock

        if data and 'warehouse_code' in data and 'item_code' in data and 'quantity' in data:
            basic_stock = LibSetupBasicStock.get_basic_stock(data['item_code'], data['warehouse_code'])

            modified_value = data['quantity'] if data['type'] == '입고' else data['quantity'] * -1
            modified_current_value = basic_stock.current_stock + modified_value
            modified_available_value = basic_stock.available_stock + modified_value

            basic_stock.current_stock = modified_current_value
            basic_stock.available_stock = modified_available_value

            # 마이너스 수불 처리 가능 여부 확인
            from backend_lib.lib_setup import LibSetupControl
            LibSetupControl.check_minus_stock(basic_stock.fk_company_id, modified_current_value)
            db.session.commit()

    @staticmethod
    def patch_single_preprocessor(instance_id=None, data=None, **kw):
        from backend_lib.lib_setup import LibSetupBasicStock

        if instance_id and data is not None and 'quantity' in data:
            stock_etc_item = db.session.query(StockEtcItem).filter(StockEtcItem.id == instance_id).first()
            if stock_etc_item:
                modified_value = data['quantity'] - stock_etc_item.quantity

                basic_stock = LibSetupBasicStock.get_basic_stock(stock_etc_item.item_code, stock_etc_item.warehouse_code)

                modified_value = modified_value if stock_etc_item.type == '입고' else modified_value * -1
                modified_current_value = basic_stock.current_stock + modified_value
                modified_available_value = basic_stock.available_stock + modified_value

                basic_stock.current_stock = modified_current_value
                basic_stock.available_stock = modified_available_value

                # 마이너스 수불 처리 가능 여부 확인
                from backend_lib.lib_setup import LibSetupControl
                LibSetupControl.check_minus_stock(basic_stock.fk_company_id, modified_current_value)
                db.session.commit()

    @staticmethod
    def get_total_release_quantity_by_item_code_query(use_count, item_code, warehouse_code, start_date=None, end_date=None):
        if use_count:
            query = db.session.query(
                db.func.sum(StockEtcItem.quantity)
            )
        else:
            query = db.session.query(
                StockEtc.number,
                StockEtc.target_date,
                StockEtcItem.unit_price,
                StockEtcItem.quantity,
                StockEtcItem.fk_project_management_id,
                StockEtcItem.inout_type,
                StockEtcItem.cost_price,
                db.func.ifnull(StockEtcItem.total_cost_price, 0).label('total_cost_price')
            )
        query = query.join(
            StockEtc, StockEtcItem.fk_stock_etc_id == StockEtc.id
        ).filter(
            StockEtcItem.type == '출고'
        ).filter(
            StockEtcItem.item_code == item_code
        ).filter(
            StockEtcItem.warehouse_code == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                StockEtc.target_date >= start_date
            ).filter(
                StockEtc.target_date <= end_date
            )
        elif end_date:
            query = query.filter(
                StockEtc.target_date < end_date
            )
        return query

    @staticmethod
    def get_total_release_quantity_by_item_code(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibStockEtcItem.get_total_release_quantity_by_item_code_query(use_count=True,
                                                                              item_code=item_code,
                                                                              warehouse_code=warehouse_code,
                                                                              start_date=start_date,
                                                                              end_date=end_date)
        release_quantity = query.first()[0]
        release_quantity = 0 if not release_quantity else release_quantity
        return release_quantity

    @staticmethod
    def get_all_release_item_for_statistics(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibStockEtcItem.get_total_release_quantity_by_item_code_query(use_count=False,
                                                                              item_code=item_code,
                                                                              warehouse_code=warehouse_code,
                                                                              start_date=start_date,
                                                                              end_date=end_date)
        release_items = query.all()
        return release_items

    @staticmethod
    def get_total_release_price_by_item_code(item_code: str, warehouse_code: str, start_date=None, end_date=None) -> int:
        query = db.session.query(
            db.func.sum(db.func.ifnull(StockEtcItem.total_cost_price, 0))
        ).join(
            StockEtc, StockEtcItem.fk_stock_etc_id == StockEtc.id
        ).filter(
            StockEtcItem.type == '출고'
        ).filter(
            StockEtcItem.item_code == item_code
        ).filter(
            StockEtcItem.warehouse_code == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                StockEtc.target_date >= start_date
            ).filter(
                StockEtc.target_date <= end_date
            )
        elif end_date:
            query = query.filter(
                StockEtc.target_date < end_date
            )
        release_price = query.first()[0]
        release_price = 0 if not release_price else release_price
        return release_price

    @staticmethod
    def get_total_receiving_quantity_by_item_code_query(use_count, item_code, warehouse_code, start_date=None, end_date=None):
        if use_count:
            query = db.session.query(
                db.func.sum(StockEtcItem.quantity)
            )
        else:
            query = db.session.query(
                StockEtc.number,
                StockEtc.target_date,
                StockEtcItem.unit_price,
                StockEtcItem.quantity,
                StockEtcItem.fk_project_management_id,
                StockEtcItem.inout_type
            )
        query = query.join(
            StockEtc, StockEtcItem.fk_stock_etc_id == StockEtc.id
        ).filter(
            StockEtcItem.type == "입고"
        ).filter(
            StockEtcItem.item_code == item_code
        ).filter(
            StockEtcItem.warehouse_code == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                StockEtc.target_date >= start_date
            ).filter(
                StockEtc.target_date <= end_date
            )
        elif end_date:
            query = query.filter(
                StockEtc.target_date < end_date
            )
        return query

    @staticmethod
    def get_total_receiving_quantity_by_item_code(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibStockEtcItem.get_total_receiving_quantity_by_item_code_query(use_count=True,
                                                                                item_code=item_code,
                                                                                warehouse_code=warehouse_code,
                                                                                start_date=start_date,
                                                                                end_date=end_date)
        receiving_quantity = query.first()[0]
        receiving_quantity = 0 if not receiving_quantity else receiving_quantity
        return receiving_quantity

    @staticmethod
    def get_all_receiving_item_for_statistics(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibStockEtcItem.get_total_receiving_quantity_by_item_code_query(use_count=False,
                                                                                item_code=item_code,
                                                                                warehouse_code=warehouse_code,
                                                                                start_date=start_date,
                                                                                end_date=end_date)
        release_items = query.all()
        return release_items

    @staticmethod
    def get_total_receiving_price_by_item_code(item_code: str, warehouse_code: str, start_date=None, end_date=None) -> int:
        query = db.session.query(
            db.func.sum(StockEtcItem.quantity * StockEtcItem.unit_price)
        ).join(
            StockEtc, StockEtcItem.fk_stock_etc_id == StockEtc.id
        ).filter(
            StockEtcItem.type == "입고"
        ).filter(
            StockEtcItem.item_code == item_code
        ).filter(
            StockEtcItem.warehouse_code == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                StockEtc.target_date >= start_date
            ).filter(
                StockEtc.target_date <= end_date
            )
        elif end_date:
            query = query.filter(
                StockEtc.target_date < end_date
            )
        receiving_price = query.first()[0]
        receiving_price = 0 if not receiving_price else receiving_price
        return receiving_price


class LibStockMoveRequest(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        LibCommon.get_item_number(data, 'number', StockMoveRequest, StockMoveRequest.number, '/stock/move-request')

class LibStockMoveRequestItem(object):
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

class LibStockMoveRelease(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        LibCommon.get_item_number(data, 'number', StockMoveRelease, StockMoveRelease.number, '/stock/move-release')


class LibStockMoveReleaseItem(object):
    @staticmethod
    def post_postprocessor(result=None, **kw):
        LibStockMoveReleaseItem.update_release_item_not_shipped(result['fk_stock_move_request_item_id'])

    @staticmethod
    def patch_single_postprocessor(result=None, **kw):
        LibStockMoveReleaseItem.update_release_item_not_shipped(result['fk_stock_move_request_item_id'])

    @staticmethod
    def update_release_item_not_shipped(request_item_id):
        # 재고요청 품목을 가져온다
        request_item = db.session.query(
            StockMoveRequestItem
        ).filter(
            StockMoveRequestItem.id == request_item_id
        ).first()
        # 해당 재고요청 품목의 전체 출고 수량을 찾는다
        release_quantity = db.session.query(
            db.func.sum(StockMoveReleaseItem.release_quantity)
        ).filter(
            StockMoveReleaseItem.fk_stock_move_request_item_id == request_item_id
        ).first()[0]
        # 재고요청 품목의 미출고 수량을 업데이트 (요청 수량 - 전체 출고 수량)
        import math
        request_item.not_shipped = math.ceil(request_item.quantity) - release_quantity
        db.session.commit()

        if request_item.fk_work_order_item_id:
            from backend_lib.lib_production import LibWorkOrderItem2
            LibWorkOrderItem2.update_uninput_quantity(1, request_item.not_shipped)

    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_setup import LibSetupBasicStock

        if data and 'out_warehouse' in data and 'in_warehouse' in data:
            # 입고 창고에 수량 증가
            basic_in_row = LibSetupBasicStock.get_basic_stock(data['item_code'], data['in_warehouse'])
            basic_in_row.current_stock = basic_in_row.current_stock + data['release_quantity']
            basic_in_row.available_stock = basic_in_row.available_stock + data['release_quantity']

            # 출고 창고에 수량 차감
            basic_out_row = LibSetupBasicStock.get_basic_stock(data['item_code'], data['out_warehouse'])
            basic_out_row.current_stock = basic_out_row.current_stock - data['release_quantity']
            basic_out_row.available_stock = basic_out_row.available_stock - data['release_quantity']

            # 마이너스 수불 처리 가능 여부 확인
            from backend_lib.lib_setup import LibSetupControl
            LibSetupControl.check_minus_stock(basic_out_row.fk_company_id, basic_out_row.current_stock)
            db.session.commit()

    @staticmethod
    def patch_single_preprocessor(instance_id=None, data=None, **kw):
        from backend_lib.lib_setup import LibSetupBasicStock
        stock = StockMoveReleaseItem.query.filter(StockMoveReleaseItem.id == instance_id).first()

        if 'out_warehouse' in data:  # 출고 창고가 변경된 경우
            # 기존 출고 창고에서 재고 증가
            basic_out_asis = LibSetupBasicStock.get_basic_stock(stock.item_code, stock.out_warehouse)
            basic_out_asis.current_stock += stock.release_quantity
            basic_out_asis.available_stock += stock.release_quantity

            # 새로운 출고 창고에서 재고 차감
            basic_out_tobe = LibSetupBasicStock.get_basic_stock(stock.item_code, data['out_warehouse'])
            basic_out_tobe.current_stock -= stock.release_quantity
            basic_out_tobe.available_stock -= stock.release_quantity
            db.session.commit()

        if 'in_warehouse' in data:  # 입고 창고가 변경된 경우
            # 기존 입고 창고에서 재고 차감
            basic_in_asis = LibSetupBasicStock.get_basic_stock(stock.item_code, stock.in_warehouse)
            basic_in_asis.current_stock -= stock.release_quantity
            basic_in_asis.available_stock -= stock.release_quantity

            # 새로운 입고 창고에서 재고 증가
            basic_in_tobe = LibSetupBasicStock.get_basic_stock(stock.item_code, data['in_warehouse'])
            basic_in_tobe.current_stock += stock.release_quantity
            basic_in_tobe.available_stock += stock.release_quantity
            db.session.commit()

        if 'release_quantity' in data:  # 수량이 변경된 경우
            modified_value = data['release_quantity'] - stock.release_quantity

            basic_in_tobe = LibSetupBasicStock.get_basic_stock(stock.item_code, stock.in_warehouse)
            basic_in_tobe.current_stock += modified_value
            basic_in_tobe.available_stock += modified_value

            basic_out_tobe = LibSetupBasicStock.get_basic_stock(stock.item_code, stock.out_warehouse)
            basic_out_tobe.current_stock -= modified_value
            basic_out_tobe.available_stock -= modified_value

            # 마이너스 수불 처리 가능 여부 확인
            from backend_lib.lib_setup import LibSetupControl
            LibSetupControl.check_minus_stock(basic_out_tobe.fk_company_id, basic_out_tobe.current_stock)
            db.session.commit()

    @staticmethod
    def get_total_release_quantity_by_item_code_query(use_count, item_code, warehouse_code, start_date=None, end_date=None):
        if use_count:
            query = db.session.query(
                db.func.sum(StockMoveReleaseItem.release_quantity)
            )
        else:
            query = db.session.query(
                StockMoveRelease.number,
                StockMoveRelease.target_date,
                StockMoveReleaseItem.cost_price,
                db.func.ifnull(StockMoveReleaseItem.total_cost_price, 0).label('total_cost_price'),
                StockMoveReleaseItem.unit_price,
                StockMoveReleaseItem.release_quantity,
                StockMoveReleaseItem.fk_project_management_id,
                StockMoveReleaseItem.in_warehouse
            )
        query = query.join(
            StockMoveRelease, StockMoveReleaseItem.fk_stock_move_release_id == StockMoveRelease.id
        ).filter(
            StockMoveReleaseItem.item_code == item_code
        ).filter(
            StockMoveReleaseItem.out_warehouse == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                StockMoveRelease.target_date >= start_date
            ).filter(
                StockMoveRelease.target_date <= end_date
            )
        elif end_date:
            query = query.filter(
                StockMoveRelease.target_date < end_date
            )
        return query

    @staticmethod
    def get_total_release_quantity_by_item_code(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibStockMoveReleaseItem.get_total_release_quantity_by_item_code_query(use_count=True,
                                                                                      item_code=item_code,
                                                                                      warehouse_code=warehouse_code,
                                                                                      start_date=start_date,
                                                                                      end_date=end_date)
        release_quantity = query.first()[0]
        release_quantity = 0 if not release_quantity else release_quantity
        return release_quantity

    @staticmethod
    def get_all_release_item_for_statistics(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibStockMoveReleaseItem.get_total_release_quantity_by_item_code_query(use_count=False,
                                                                                      item_code=item_code,
                                                                                      warehouse_code=warehouse_code,
                                                                                      start_date=start_date,
                                                                                      end_date=end_date)
        release_items = query.all()
        return release_items

    @staticmethod
    def get_total_release_price_by_item_code(item_code: str, warehouse_code: str, start_date=None, end_date=None) -> Decimal:
        query = db.session.query(
            db.func.sum(db.func.ifnull(StockMoveReleaseItem.total_cost_price, 0))
        ).join(
            StockMoveRelease, StockMoveReleaseItem.fk_stock_move_release_id == StockMoveRelease.id
        ).filter(
            StockMoveReleaseItem.item_code == item_code
        ).filter(
            StockMoveReleaseItem.out_warehouse == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                StockMoveRelease.target_date >= start_date
            ).filter(
                StockMoveRelease.target_date <= end_date
            )
        elif end_date:
            query = query.filter(
                StockMoveRelease.target_date < end_date
            )
        release_price = query.first()[0]
        release_price = Decimal('0') if not release_price else release_price
        return release_price

    @staticmethod
    def get_total_receiving_quantity_by_item_code_query(use_count, item_code, warehouse_code, start_date=None, end_date=None):
        if use_count:
            query = db.session.query(
                db.func.sum(StockMoveReleaseItem.release_quantity)
            )
        else:
            query = db.session.query(
                StockMoveRelease.number,
                StockMoveRelease.target_date,
                StockMoveReleaseItem.unit_price,
                StockMoveReleaseItem.release_quantity,
                StockMoveReleaseItem.fk_project_management_id,
                StockMoveReleaseItem.out_warehouse
            )
        query = query.join(
            StockMoveRelease, StockMoveReleaseItem.fk_stock_move_release_id == StockMoveRelease.id
        ).filter(
            StockMoveReleaseItem.item_code == item_code
        ).filter(
            StockMoveReleaseItem.in_warehouse == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                StockMoveRelease.target_date >= start_date
            ).filter(
                StockMoveRelease.target_date <= end_date
            )
        elif end_date:
            query = query.filter(
                StockMoveRelease.target_date < end_date
            )
        return query

    @staticmethod
    def get_total_receiving_quantity_by_item_code(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibStockMoveReleaseItem.get_total_receiving_quantity_by_item_code_query(use_count=True,
                                                                                        item_code=item_code,
                                                                                        warehouse_code=warehouse_code,
                                                                                        start_date=start_date,
                                                                                        end_date=end_date)
        receiving_quantity = query.first()[0]
        receiving_quantity = 0 if not receiving_quantity else receiving_quantity
        return receiving_quantity

    @staticmethod
    def get_all_receiving_item_for_statistics(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibStockMoveReleaseItem.get_total_receiving_quantity_by_item_code_query(use_count=False,
                                                                                        item_code=item_code,
                                                                                        warehouse_code=warehouse_code,
                                                                                        start_date=start_date,
                                                                                        end_date=end_date)
        release_items = query.all()
        return release_items

    @staticmethod
    def get_total_receiving_price_by_item_code(item_code, warehouse_code, start_date=None, end_date=None):
        query = db.session.query(
            db.func.sum(StockMoveReleaseItem.release_quantity * StockMoveReleaseItem.unit_price)
        ).join(
            StockMoveRelease, StockMoveReleaseItem.fk_stock_move_release_id == StockMoveRelease.id
        ).filter(
            StockMoveReleaseItem.item_code == item_code
        ).filter(
            StockMoveReleaseItem.in_warehouse == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                StockMoveRelease.target_date >= start_date
            ).filter(
                StockMoveRelease.target_date <= end_date
            )
        elif end_date:
            query = query.filter(
                StockMoveRelease.target_date < end_date
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
                    if item['client_company']:
                        client = db.session.query(
                            BaseClient.alias
                        ).filter(
                            BaseClient.name == item['client_company']
                        ).first()
                        item['client_alias'] = client.alias
                except:
                    pass

class LibStockCorrection(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        LibCommon.get_item_number(data, 'number', StockCorrection, StockCorrection.number, '/stock/stock-correction')
