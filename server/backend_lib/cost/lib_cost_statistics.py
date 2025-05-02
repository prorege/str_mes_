# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional, Dict, Union, Tuple

from backend_model.database import DBManager
from backend_model.table_setup import SetupBasicStock

db = DBManager.db


class LibCostStatistics(object):

    @staticmethod
    def get_cost_statistics(basic_stock: SetupBasicStock, start_date: str, end_date: str) -> list:
        _res_id = 0
        response = []

        # 이월재고
        _res_id, _past_stock_n_price = LibCostStatistics.__get_past_stock_n_price(
            res_id=_res_id,
            basic_stock=basic_stock,
            start_date=start_date,
            end_date=end_date
        )
        response.append(_past_stock_n_price)

        # 구매관리 - 입고
        _res_id, _purchase_receiving_item_list = LibCostStatistics.__get_purchase_receiving_item_list(
            res_id=_res_id,
            basic_stock=basic_stock,
            start_date=start_date,
            end_date=end_date
        )
        response.extend(_purchase_receiving_item_list)

        # 재고관리 - 기타입고
        _res_id, _stock_etc_receiving_item_list = LibCostStatistics.__get_stock_etc_receiving_item_list(
            res_id=_res_id,
            basic_stock=basic_stock,
            start_date=start_date,
            end_date=end_date
        )
        response.extend(_stock_etc_receiving_item_list)

        # 재고관리 - 재고이동입고
        _res_id, _stock_move_receiving_item_list = LibCostStatistics.__get_stock_move_receiving_item_list(
            res_id=_res_id,
            basic_stock=basic_stock,
            start_date=start_date,
            end_date=end_date
        )
        response.extend(_stock_move_receiving_item_list)

        # 생산관리 - 생산입고
        _res_id, _produce_receiving_item_list = LibCostStatistics.__get_produce_receiving_item_list(
            res_id=_res_id,
            basic_stock=basic_stock,
            start_date=start_date,
            end_date=end_date
        )
        response.extend(_produce_receiving_item_list)

        # 출하관리 - 출고반품
        _res_id, _shipment_release_return_item_list = LibCostStatistics.__get_shipment_release_return_item_list(
            res_id=_res_id,
            basic_stock=basic_stock,
            start_date=start_date,
            end_date=end_date
        )
        response.extend(_shipment_release_return_item_list)

        # 수입관리 - 통관
        _res_id, _import_clearance_item_list = LibCostStatistics.__get_import_clearance_item_list(
            res_id=_res_id,
            basic_stock=basic_stock,
            start_date=start_date,
            end_date=end_date
        )
        response.extend(_import_clearance_item_list)

        # 출하관리 - 출고
        _res_id, _shipment_release_item_list = LibCostStatistics.__get_shipment_release_item_list(
            res_id=_res_id,
            basic_stock=basic_stock,
            start_date=start_date,
            end_date=end_date
        )
        response.extend(_shipment_release_item_list)

        # 재고관리 - 기타출고
        _res_id, _stock_etc_release_item_list = LibCostStatistics.__get_stock_etc_release_item_list(
            res_id=_res_id,
            basic_stock=basic_stock,
            start_date=start_date,
            end_date=end_date
        )
        response.extend(_stock_etc_release_item_list)

        # 재고관리 - 재고이동출고
        _res_id, _stock_move_release_item_list = LibCostStatistics.__get_stock_move_release_item_list(
            res_id=_res_id,
            basic_stock=basic_stock,
            start_date=start_date,
            end_date=end_date
        )
        response.extend(_stock_move_release_item_list)

        # 생산관리 - 자재소모
        _res_id, _produce_release_item_list = LibCostStatistics.__get_produce_release_item_list(
            res_id=_res_id,
            basic_stock=basic_stock,
            start_date=start_date,
            end_date=end_date
        )
        response.extend(_produce_release_item_list)

        # 구매관리 - 입고반품
        _res_id, _purchase_receiving_return_item_list = LibCostStatistics.__get_purchase_receiving_return_item_list(
            res_id=_res_id,
            basic_stock=basic_stock,
            start_date=start_date,
            end_date=end_date
        )
        response.extend(_purchase_receiving_return_item_list)

        # 수출관리 - 선적
        _res_id, _export_comm_invoice_item_list = LibCostStatistics.__get_export_comm_invoice_item_list(
            res_id=_res_id,
            basic_stock=basic_stock,
            start_date=start_date,
            end_date=end_date
        )
        response.extend(_export_comm_invoice_item_list)

        return response

    @staticmethod
    def __get_basic_stock_quantity(basic_stock: SetupBasicStock, end_date: str) -> int:
        from backend_model.table_common import Companies
        company = db.session.query(
            Companies
        ).filter(
            Companies.basic_stock_date < end_date
        ).first()
        basic_stock_quantity = 0
        if company:
            basic_stock_quantity = basic_stock.basic_stock
        return basic_stock_quantity

    @staticmethod
    def __get_past_stock_n_price(
            res_id: int, basic_stock: SetupBasicStock, start_date: str, end_date: str
    ) -> Tuple[int, dict]:
        basic_stock_quantity = LibCostStatistics.__get_basic_stock_quantity(basic_stock=basic_stock, end_date=end_date)

        from backend_lib.lib_setup import LibSetupBasicStock
        past_release_quantity = LibSetupBasicStock.get_total_release_quantity(
            item_code=basic_stock.item_code,
            warehouse_code=basic_stock.wh_code,
            end_date=start_date
        )
        past_receiving_quantity = LibSetupBasicStock.get_total_receiving_quantity(
            item_code=basic_stock.item_code,
            warehouse_code=basic_stock.wh_code,
            end_date=start_date
        )
        past_release_price = LibSetupBasicStock.get_total_release_price(
            item_code=basic_stock.item_code,
            warehouse_code=basic_stock.wh_code,
            end_date=start_date
        )
        past_receiving_price = LibSetupBasicStock.get_total_receiving_price(
            item_code=basic_stock.item_code,
            warehouse_code=basic_stock.wh_code,
            end_date=start_date
        )
        past_stock = basic_stock_quantity + \
                     past_receiving_quantity['total_receiving_quantity'] - \
                     past_release_quantity['total_release_quantity']
        past_price = basic_stock.item_price + \
                     past_receiving_price['total_receiving_price'] - \
                     past_release_price['total_release_price']

        from datetime import timedelta
        date_one_day_ago = datetime.strptime(start_date, '%Y%m%d').date() - timedelta(days=1)
        start_date_one_day_ago = datetime(date_one_day_ago.year, date_one_day_ago.month,
                                          date_one_day_ago.day)  # date to datetime
        res = LibCostStatistics.__make_statistics_response(
            response_id=res_id,
            action_date=start_date_one_day_ago,
            inout_type='이월재고',
            past_stock=past_stock,
            past_price=past_price
        )
        return res_id, res

    @staticmethod
    def __get_purchase_receiving_item_list(
            res_id: int, basic_stock: SetupBasicStock, start_date: str, end_date: str
    ) -> Tuple[int, list]:
        result_list = []

        from backend_lib.lib_purchase import LibPurchaseReceivingItem
        receiving_list = LibPurchaseReceivingItem.get_all_receiving_item_for_statistics(
            item_code=basic_stock.item_code,
            warehouse_code=basic_stock.wh_code,
            start_date=start_date,
            end_date=end_date
        )
        for _item in receiving_list:
            res_id += 1
            res = LibCostStatistics.__make_statistics_response(
                response_id=res_id,
                number=_item.receiving_number,
                action_date=_item.receiving_date,
                inout_type=_item.receiving_type,
                company=_item.client_company,
                unit_price=_item.unit_price,
                receiving_stock=_item.receiving_quantity,
                receiving_price=_item.unit_price * _item.receiving_quantity,
                fk_project_management_id=_item.fk_project_management_id
            )
            result_list.append(res)
        return res_id, result_list

    @staticmethod
    def __get_stock_etc_receiving_item_list(
            res_id: int, basic_stock: SetupBasicStock, start_date: str, end_date: str
    ) -> Tuple[int, list]:
        result_list = []

        from backend_lib.lib_stock import LibStockEtcItem
        stock_etc_receiving_list = LibStockEtcItem.get_all_receiving_item_for_statistics(
            item_code=basic_stock.item_code,
            warehouse_code=basic_stock.wh_code,
            start_date=start_date,
            end_date=end_date
        )
        for _item in stock_etc_receiving_list:
            res_id += 1
            res = LibCostStatistics.__make_statistics_response(
                response_id=res_id,
                number=_item.number,
                action_date=_item.target_date,
                inout_type=_item.inout_type,
                unit_price=_item.unit_price,
                receiving_stock=_item.quantity,
                receiving_price=_item.unit_price * _item.quantity,
                fk_project_management_id=_item.fk_project_management_id
            )
            result_list.append(res)
        return res_id, result_list

    @staticmethod
    def __get_stock_move_receiving_item_list(
            res_id: int, basic_stock: SetupBasicStock, start_date: str, end_date: str
    ) -> Tuple[int, list]:
        result_list = []

        from backend_lib.lib_stock import LibStockMoveReleaseItem
        stock_move_receiving_list = LibStockMoveReleaseItem.get_all_receiving_item_for_statistics(
            item_code=basic_stock.item_code,
            warehouse_code=basic_stock.wh_code,
            start_date=start_date,
            end_date=end_date
        )
        for item in stock_move_receiving_list:
            res_id += 1
            res = LibCostStatistics.__make_statistics_response(
                response_id=res_id,
                number=item.number,
                action_date=item.target_date,
                inout_type='재고이동입고',
                company=item.out_warehouse,
                unit_price=item.unit_price,
                receiving_stock=item.release_quantity,
                receiving_price=item.unit_price * item.release_quantity,
                fk_project_management_id=item.fk_project_management_id
            )
            result_list.append(res)
        return res_id, result_list

    @staticmethod
    def __get_produce_receiving_item_list(
            res_id: int, basic_stock: SetupBasicStock, start_date: str, end_date: str
    ) -> Tuple[int, list]:
        result_list = []

        from backend_lib.lib_production import LibPerformanceRegistrationItem1
        produce_receiving_list = LibPerformanceRegistrationItem1.get_all_receiving_item_for_statistics(
            item_code=basic_stock.item_code,
            warehouse_code=basic_stock.wh_code,
            start_date=start_date,
            end_date=end_date
        )
        for item in produce_receiving_list:
            res_id += 1

            # 수주 업체 표시
            company = LibPerformanceRegistrationItem1.get_shipment_order_company(item.fk_work_order_item)

            res = LibCostStatistics.__make_statistics_response(
                response_id=res_id,
                number=item.number,
                action_date=item.target_date,
                inout_type='생산입고',
                company=company,
                unit_price=item.unit_price,
                receiving_stock=item.good_quantity,
                receiving_price=item.unit_price * item.good_quantity,
                fk_project_management_id=item.fk_project_management_id
            )
            result_list.append(res)
        return res_id, result_list

    @staticmethod
    def __get_shipment_release_return_item_list(
            res_id: int, basic_stock: SetupBasicStock, start_date: str, end_date: str
    ) -> Tuple[int, list]:
        result_list = []

        from backend_lib.lib_shipment import LibShipmentReleaseReturnItem
        release_return_list = LibShipmentReleaseReturnItem.get_all_receiving_item_for_statistics(
            item_code=basic_stock.item_code,
            warehouse_code=basic_stock.wh_code,
            start_date=start_date,
            end_date=end_date
        )
        for item in release_return_list:
            res_id += 1
            res = LibCostStatistics.__make_statistics_response(
                response_id=res_id,
                number=item.return_number,
                action_date=item.return_date,
                inout_type=item.return_type,
                company=item.client_company,
                unit_price=item.cost_price,
                receiving_stock=item.return_quantity,
                receiving_price=item.cost_price * item.return_quantity
            )
            result_list.append(res)
        return res_id, result_list

    @staticmethod
    def __get_import_clearance_item_list(
            res_id: int, basic_stock: SetupBasicStock, start_date: str, end_date: str
    ) -> Tuple[int, list]:
        result_list = []

        from backend_lib.lib_import import LibImportClearanceItem
        import_list = LibImportClearanceItem.get_all_receiving_item_for_statistics(
            item_code=basic_stock.item_code,
            warehouse_code=basic_stock.wh_code,
            start_date=start_date,
            end_date=end_date
        )
        for item in import_list:
            res_id += 1
            res = LibCostStatistics.__make_statistics_response(
                response_id=res_id,
                number=item.clearance_number,
                action_date=item.clearance_date,
                inout_type='통관',
                company=item.supplier,
                unit_price=item.cost_price,
                receiving_stock=item.qty,
                receiving_price=item.cost_price * item.qty)
            result_list.append(res)
        return res_id, result_list

    @staticmethod
    def __get_shipment_release_item_list(
            res_id: int, basic_stock: SetupBasicStock, start_date: str, end_date: str
    ) -> Tuple[int, list]:
        result_list = []

        from backend_lib.lib_shipment import LibShipmentReleaseItem
        release_list = LibShipmentReleaseItem.get_all_release_item_for_statistics(
            item_code=basic_stock.item_code,
            warehouse_code=basic_stock.wh_code,
            start_date=start_date,
            end_date=end_date
        )
        for item in release_list:
            res_id += 1
            res = LibCostStatistics.__make_statistics_response(
                response_id=res_id,
                number=item.release_number,
                action_date=item.release_date,
                inout_type=item.release_type,
                company=item.client_company,
                unit_price=item.cost_price,
                release_stock=item.release_quantity,
                release_price=item.total_cost_price,
                fk_project_management_id=item.fk_project_management_id
            )
            result_list.append(res)
        return res_id, result_list

    @staticmethod
    def __get_stock_etc_release_item_list(
            res_id: int, basic_stock: SetupBasicStock, start_date: str, end_date: str
    ) -> Tuple[int, list]:
        result_list = []

        from backend_lib.lib_stock import LibStockEtcItem
        stock_etc_release_list = LibStockEtcItem.get_all_release_item_for_statistics(
            item_code=basic_stock.item_code,
            warehouse_code=basic_stock.wh_code,
            start_date=start_date,
            end_date=end_date
        )
        for item in stock_etc_release_list:
            res_id += 1
            res = LibCostStatistics.__make_statistics_response(
                response_id=res_id,
                number=item.number,
                action_date=item.target_date,
                inout_type=item.inout_type,
                unit_price=item.cost_price,
                release_stock=item.quantity,
                release_price=item.total_cost_price,
                fk_project_management_id=item.fk_project_management_id
            )
            result_list.append(res)
        return res_id, result_list

    @staticmethod
    def __get_stock_move_release_item_list(
            res_id: int, basic_stock: SetupBasicStock, start_date: str, end_date: str
    ) -> Tuple[int, list]:
        result_list = []

        from backend_lib.lib_stock import LibStockMoveReleaseItem
        stock_move_release_list = LibStockMoveReleaseItem.get_all_release_item_for_statistics(
            item_code=basic_stock.item_code,
            warehouse_code=basic_stock.wh_code,
            start_date=start_date,
            end_date=end_date
        )
        for item in stock_move_release_list:
            res_id += 1
            res = LibCostStatistics.__make_statistics_response(
                response_id=res_id,
                number=item.number,
                action_date=item.target_date,
                inout_type='재고이동출고',
                company=item.in_warehouse,
                unit_price=item.cost_price,
                release_stock=item.release_quantity,
                release_price=item.total_cost_price,
                fk_project_management_id=item.fk_project_management_id
            )
            result_list.append(res)
        return res_id, result_list

    @staticmethod
    def __get_produce_release_item_list(
            res_id: int, basic_stock: SetupBasicStock, start_date: str, end_date: str
    ) -> Tuple[int, list]:
        result_list = []

        from backend_lib.lib_production import LibPerformanceRegistrationItem2
        produce_release_list = LibPerformanceRegistrationItem2.get_all_release_item_for_statistics(
            item_code=basic_stock.item_code,
            warehouse_code=basic_stock.wh_code,
            start_date=start_date,
            end_date=end_date
        )
        for item in produce_release_list:
            res_id += 1
            res = LibCostStatistics.__make_statistics_response(
                response_id=res_id,
                number=item.number,
                action_date=item.target_date,
                inout_type='자재소모',
                unit_price=item.cost_price,
                release_stock=item.material_quantity,
                release_price=item.total_cost_price
            )
            result_list.append(res)
        return res_id, result_list

    @staticmethod
    def __get_purchase_receiving_return_item_list(
            res_id: int, basic_stock: SetupBasicStock, start_date: str, end_date: str
    ) -> Tuple[int, list]:
        result_list = []

        from backend_lib.lib_purchase import LibPurchaseReceivingReturnItem
        purchase_return_list = LibPurchaseReceivingReturnItem.get_all_release_item_for_statistics(
            item_code=basic_stock.item_code,
            warehouse_code=basic_stock.wh_code,
            start_date=start_date,
            end_date=end_date
        )
        for item in purchase_return_list:
            res_id += 1
            res = LibCostStatistics.__make_statistics_response(
                response_id=res_id,
                number=item.return_number,
                action_date=item.return_date,
                inout_type=item.return_type,
                company=item.client_company,
                unit_price=item.cost_price,
                release_stock=item.return_quantity,
                release_price=item.total_cost_price
            )
            result_list.append(res)
        return res_id, result_list

    @staticmethod
    def __get_export_comm_invoice_item_list(
            res_id: int, basic_stock: SetupBasicStock, start_date: str, end_date: str
    ) -> Tuple[int, list]:
        result_list = []

        from backend_lib.lib_export import LibExportCommInvoiceItem
        export_list = LibExportCommInvoiceItem.get_all_release_item_for_statistics(
            item_code=basic_stock.item_code,
            warehouse_code=basic_stock.wh_code,
            start_date=start_date,
            end_date=end_date
        )
        for item in export_list:
            res_id += 1
            res = LibCostStatistics.__make_statistics_response(
                response_id=res_id,
                number=item.invoice_number,
                action_date=item.invoice_date,
                inout_type='선적',
                company=item.client_company,
                unit_price=item.cost_price,
                release_stock=item.invoice_quantity,
                release_price=item.total_cost_price
            )
            result_list.append(res)
        return res_id, result_list

    @staticmethod
    def __make_statistics_response(
            response_id, action_date, inout_type, company='', unit_price=0, past_stock=0, past_price=0,
            receiving_stock=0, receiving_price=0, release_stock=0, release_price=0,fk_project_management_id=None, number=''
    ) -> dict:
        res = {
            'id': response_id,
            'number': number,
            'action_date': action_date.strftime('%Y-%m-%dT00:00:00'),
            'inout_type': inout_type,
            'company': company,
            'unit_price': unit_price,
            'past_stock': past_stock,
            'past_price': past_price,
            'receiving_stock': receiving_stock,
            'receiving_price': receiving_price,
            'release_stock': release_stock,
            'release_price': release_price,
            'fk_project_management_id': fk_project_management_id,
            'group_id': action_date.strftime('%Y-%m')
        }
        return res
