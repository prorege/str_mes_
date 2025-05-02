# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional, Dict

from backend_model.database import DBManager

db = DBManager.db


class LibCostClosing(object):

    @staticmethod
    def get_receiving_item_list(
            end_date: datetime, item_code: Optional[str] = None, warehouse_code: Optional[str] = None
    ) -> list:
        receiving_items = []

        # 기초 재고
        from backend_lib.cost.closing.lib_cost_closing_setup_basic_stock import LibCostClosingSetupBasicStock
        basic_stock_item_list = LibCostClosingSetupBasicStock.get_basic_stock_item_list(
            item_code=item_code,
            warehouse_code=warehouse_code
        )
        receiving_items.extend(basic_stock_item_list)

        # 구매 입고
        from backend_lib.cost.closing.lib_cost_closing_purchase_receiving import LibCostClosingPurchaseReceiving
        purchase_receiving_items = LibCostClosingPurchaseReceiving.get_purchase_receiving_item_list(
            end_date=end_date,
            item_code=item_code,
            warehouse_code=warehouse_code
        )
        receiving_items.extend(purchase_receiving_items)

        # 기타 입고
        from backend_lib.cost.closing.lib_cost_closing_stock_etc import LibCostClosingStockEtc
        stock_etc_receiving_items = LibCostClosingStockEtc.get_stock_etc_receiving_item_list(
            end_date=end_date,
            item_code=item_code,
            warehouse_code=warehouse_code
        )
        receiving_items.extend(stock_etc_receiving_items)

        # 재고 이동 입고
        from backend_lib.cost.closing.lib_cost_closing_stock_move import LibCostClosingStockMove
        stock_move_receiving_items = LibCostClosingStockMove.get_stock_move_receiving_item_list(
            end_date=end_date,
            item_code=item_code,
            warehouse_code=warehouse_code
        )
        receiving_items.extend(stock_move_receiving_items)

        # 생산 입고
        from backend_lib.cost.closing.lib_cost_closing_performance_registration import LibCostClosingPerformanceRegistration
        produce_receiving_items = LibCostClosingPerformanceRegistration.get_produce_receiving_item_list(
            end_date=end_date,
            item_code=item_code,
            warehouse_code=warehouse_code
        )
        receiving_items.extend(produce_receiving_items)

        # 출고반품
        from backend_lib.cost.closing.lib_cost_closing_shipement_release_return import LibCostClosingShipmentReleaseReturn
        release_return_items = LibCostClosingShipmentReleaseReturn.get_release_return_item_list(
            end_date=end_date,
            item_code=item_code,
            warehouse_code=warehouse_code
        )
        receiving_items.extend(release_return_items)

        # 통관
        from backend_lib.cost.closing.lib_cost_closing_import_clearance import LibCostClosingImportClearance
        import_clearance_items = LibCostClosingImportClearance.get_import_clearance_item_list(
            end_date=end_date,
            item_code=item_code,
            warehouse_code=warehouse_code
        )
        receiving_items.extend(import_clearance_items)

        return receiving_items

    @staticmethod
    def get_release_item_list(
            end_date: datetime, item_code: Optional[str] = None, warehouse_code: Optional[str] = None
    ) -> list:
        release_items = []

        # 출고
        from backend_lib.cost.closing.lib_cost_closing_shipment_release import LibCostClosingShipmentRelease
        shipment_release_items = LibCostClosingShipmentRelease.get_shipment_release_item_list(
            end_date=end_date,
            item_code=item_code,
            warehouse_code=warehouse_code
        )
        release_items.extend(shipment_release_items)

        # 기타 출고
        from backend_lib.cost.closing.lib_cost_closing_stock_etc import LibCostClosingStockEtc
        stock_etc_release_items = LibCostClosingStockEtc.get_stock_etc_release_item_list(
            end_date=end_date,
            item_code=item_code,
            warehouse_code=warehouse_code
        )
        release_items.extend(stock_etc_release_items)

        # 재고 이동 출고
        from backend_lib.cost.closing.lib_cost_closing_stock_move import LibCostClosingStockMove
        stock_move_release_items = LibCostClosingStockMove.get_stock_move_release_item_list(
            end_date=end_date,
            item_code=item_code,
            warehouse_code=warehouse_code
        )
        release_items.extend(stock_move_release_items)

        # 자재 소모
        from backend_lib.cost.closing.lib_cost_closing_performance_registration import LibCostClosingPerformanceRegistration
        material_consume_items = LibCostClosingPerformanceRegistration.get_material_consume_item_list(
            end_date=end_date,
            item_code=item_code,
            warehouse_code=warehouse_code
        )
        release_items.extend(material_consume_items)

        # 입고반품
        from backend_lib.cost.closing.lib_cost_closing_purchase_receiving_return import LibCostClosingPurchaseReceivingReturn
        purchase_receiving_items = LibCostClosingPurchaseReceivingReturn.get_purchase_receiving_return_item_list(
            end_date=end_date,
            item_code=item_code,
            warehouse_code=warehouse_code
        )
        release_items.extend(purchase_receiving_items)

        # 선적
        from backend_lib.cost.closing.lib_cost_closing_export_comm_invoice import LibCostClosingExportCommInvoice
        export_comm_invoice_items = LibCostClosingExportCommInvoice.get_export_comm_invoice_item_list(
            end_date=end_date,
            item_code=item_code,
            warehouse_code=warehouse_code
        )
        release_items.extend(export_comm_invoice_items)

        return release_items

    @staticmethod
    def update_cost_price(release_type, item_id, cost_price, total_cost_price):
        if release_type == 'ShipmentReleaseItem':
            LibCostClosing.__update_shipment_release_item_cost_price(item_id, cost_price, total_cost_price)
        elif release_type == 'StockEtcItem':
            LibCostClosing.__update_stock_etc_item_cost_price(item_id, cost_price, total_cost_price)
        elif release_type == 'StockMoveReleaseItem':
            LibCostClosing.__update_stock_move_release_item_cost_price(item_id, cost_price, total_cost_price)
        elif release_type == 'PerformanceRegistrationItem2':
            LibCostClosing.__update_produce_material_consume_item_cost_price(item_id, cost_price, total_cost_price)
        elif release_type == 'PurchaseReceivingReturnItem':
            LibCostClosing.__update_purchase_receiving_return_item_cost_price(item_id, cost_price, total_cost_price)
        elif release_type == 'ExportCommInvoiceItem':
            LibCostClosing.__update_export_comm_invoice_item_cost_price(item_id, cost_price, total_cost_price)

    @staticmethod
    def clear_cost_price(start_date, end_date, warehouse_code, item_code):
        from backend_lib.cost.closing.lib_cost_closing_shipment_release import LibCostClosingShipmentRelease
        LibCostClosingShipmentRelease.clear_cost_price(start_date, end_date, warehouse_code, item_code)

        from backend_lib.cost.closing.lib_cost_closing_stock_etc import LibCostClosingStockEtc
        LibCostClosingStockEtc.clear_cost_price(start_date, end_date, warehouse_code, item_code)

        from backend_lib.cost.closing.lib_cost_closing_stock_move import LibCostClosingStockMove
        LibCostClosingStockMove.clear_cost_price(start_date, end_date, warehouse_code, item_code)

        from backend_lib.cost.closing.lib_cost_closing_performance_registration import LibCostClosingPerformanceRegistration
        LibCostClosingPerformanceRegistration.clear_cost_price(start_date, end_date, warehouse_code, item_code)

        from backend_lib.cost.closing.lib_cost_closing_purchase_receiving_return import LibCostClosingPurchaseReceivingReturn
        LibCostClosingPurchaseReceivingReturn.clear_cost_price(start_date, end_date, warehouse_code, item_code)

        from backend_lib.cost.closing.lib_cost_closing_export_comm_invoice import LibCostClosingExportCommInvoice
        LibCostClosingExportCommInvoice.clear_cost_price(start_date, end_date, warehouse_code, item_code)

    @staticmethod
    def __update_shipment_release_item_cost_price(item_id, cost_price, total_cost_price):
        from backend_model.table_shipment import ShipmentReleaseItem
        LibCostClosing.__update_cost_price_in_table(ShipmentReleaseItem, item_id, cost_price, total_cost_price)

    @staticmethod
    def __update_stock_etc_item_cost_price(item_id, cost_price, total_cost_price):
        from backend_model.table_stock import StockEtcItem
        LibCostClosing.__update_cost_price_in_table(StockEtcItem, item_id, cost_price, total_cost_price)

    @staticmethod
    def __update_stock_move_release_item_cost_price(item_id, cost_price, total_cost_price):
        from backend_model.table_stock import StockMoveReleaseItem
        LibCostClosing.__update_cost_price_in_table(StockMoveReleaseItem, item_id, cost_price, total_cost_price)

    @staticmethod
    def __update_produce_material_consume_item_cost_price(item_id, cost_price, total_cost_price):
        from backend_model.table_production import PerformanceRegistrationItem2
        LibCostClosing.__update_cost_price_in_table(PerformanceRegistrationItem2, item_id, cost_price, total_cost_price)

    @staticmethod
    def __update_purchase_receiving_return_item_cost_price(item_id, cost_price, total_cost_price):
        from backend_model.table_purchase import PurchaseReceivingReturnItem
        LibCostClosing.__update_cost_price_in_table(PurchaseReceivingReturnItem, item_id, cost_price, total_cost_price)

    @staticmethod
    def __update_export_comm_invoice_item_cost_price(item_id, cost_price, total_cost_price):
        from backend_model.table_export import ExportCommInvoiceItem
        LibCostClosing.__update_cost_price_in_table(ExportCommInvoiceItem, item_id, cost_price, total_cost_price)

    @staticmethod
    def __update_cost_price_in_table(table, item_id, cost_price, total_cost_price):
        db.session.query(
            table
        ).filter(
            table.id == item_id
        ).update({
            'cost_price': cost_price,
            'total_cost_price': total_cost_price
        })
        db.session.commit()

    @staticmethod
    def sort_item_dict_in_list(item_list: list, sort_key: str):
        return sorted(item_list, key=lambda d: d[sort_key])

    @staticmethod
    def classify_by_item_code(sorted_items):
        dict_items = {}
        for item in sorted_items:
            item_code = item['item_code']
            if item_code not in dict_items:
                dict_items[item_code] = []
            dict_items[item_code].append(item)
        return dict_items

    @staticmethod
    def calculate_cost_price(release_quantity, receiving_list: list):
        import math
        from decimal import Decimal
        saved_release_quantity = release_quantity
        total_receiving_price = Decimal(0)
        for receiving_item in receiving_list[:]:
            receiving_quantity = receiving_item['quantity']
            if receiving_item['type'] == 'ShipmentReleaseReturnItem':
                if receiving_item['release_item_id']:
                    from backend_model.table_shipment import ShipmentReleaseItem
                    release_item = db.session.query(ShipmentReleaseItem).filter(ShipmentReleaseItem.id == receiving_item['release_item_id']).first()
                    if release_item:
                        if release_item.cost_price:
                            receiving_item['unit_price'] = release_item.cost_price
                        else:
                            receiving_item['unit_price'] = 0

            receiving_price = Decimal(str(receiving_item['unit_price']))
            if receiving_quantity < release_quantity:
                release_quantity -= receiving_quantity
                total_receiving_price += (Decimal(receiving_quantity) * receiving_price)
                receiving_list.pop(0)
                continue
            elif receiving_quantity == release_quantity:
                total_receiving_price += (Decimal(receiving_quantity) * receiving_price)
                receiving_list.pop(0)
                release_quantity = 0
                break
            else:
                receiving_item['quantity'] -= release_quantity
                total_receiving_price += (Decimal(release_quantity) * receiving_price)
                release_quantity = 0
                break
        if release_quantity > 0:
            return None, None
        cost_price = Decimal(math.trunc((total_receiving_price / saved_release_quantity) * 100)) / Decimal(100)
        return cost_price, total_receiving_price

    @staticmethod
    def insert_cost_closing_history(start_date, end_date, manager, company_id: int, warehouse_code: str):
        from backend_model.table_cost import CostClosingHistory
        cost_closing_history = CostClosingHistory()
        cost_closing_history.start_date = start_date
        cost_closing_history.end_date = end_date
        cost_closing_history.manager = manager
        cost_closing_history.fk_company_id = company_id
        cost_closing_history.warehouse_code = warehouse_code

        db.session.add(cost_closing_history)
        db.session.commit()

        return cost_closing_history

    @staticmethod
    def set_cost_closing_history_applied(history_id: str):
        from backend_model.table_cost import CostClosingHistory
        cost_closing_history = db.session.query(
            CostClosingHistory
        ).filter(
            CostClosingHistory.id == history_id
        ).first()
        cost_closing_history.applied = 1
        db.session.commit()

    @staticmethod
    def get_cost_release_quantity_n_price_list(
            item_code_list: list, warehouse_code: str, start_date = None, end_date = None
    ):
        from sqlalchemy.sql.expression import literal_column
        from backend_model.table_shipment import ShipmentRelease, ShipmentReleaseItem

        query1 = db.session.query(
            ShipmentRelease.release_date.label('release_date'),
            ShipmentReleaseItem.item_code,
            ShipmentReleaseItem.cost_price.label('cost_price'),
            db.func.sum(ShipmentReleaseItem.release_quantity).label('shipment_release_quantity'),
            db.func.sum(db.func.ifnull(ShipmentReleaseItem.total_cost_price, 0)).label('shipment_release_price'),
            literal_column('0').label('stock_etc_release_quantity'),
            literal_column('0').label('stock_etc_release_price'),
            literal_column('0').label('stock_move_release_quantity'),
            literal_column('0').label('stock_move_release_price'),
            literal_column('0').label('produce_release_quantity'),
            literal_column('0').label('produce_release_price'),
            literal_column('0').label('purchase_return_quantity'),
            literal_column('0').label('purchase_return_price'),
            literal_column('0').label('export_comm_invoice_quantity'),
            literal_column('0').label('export_comm_invoice_price'),
        ).join(
            ShipmentRelease, ShipmentReleaseItem.fk_release_id == ShipmentRelease.id
        ).filter(
            ShipmentReleaseItem.item_code.in_(item_code_list)
        ).filter(
            ShipmentReleaseItem.warehouse_code == warehouse_code
        )
        if start_date is None:
            query1 = query1.filter(
                ShipmentRelease.release_date < end_date
            )
        else:
            query1 = query1.filter(
                ShipmentRelease.release_date >= start_date
            ).filter(
                ShipmentRelease.release_date <= end_date
            )
        query1 = query1.group_by(
            ShipmentReleaseItem.item_code
        )

        from backend_model.table_stock import StockEtc, StockEtcItem
        query2 = db.session.query(
            StockEtc.target_date.label('release_date'),
            StockEtcItem.item_code,
            StockEtcItem.cost_price.label('cost_price'),
            literal_column('0').label('shipment_release_quantity'),
            literal_column('0').label('shipment_release_price'),
            db.func.sum(StockEtcItem.quantity).label('stock_etc_release_quantity'),
            db.func.sum(db.func.ifnull(StockEtcItem.total_cost_price, 0)).label('stock_etc_release_price'),
            literal_column('0').label('stock_move_release_quantity'),
            literal_column('0').label('stock_move_release_price'),
            literal_column('0').label('produce_release_quantity'),
            literal_column('0').label('produce_release_price'),
            literal_column('0').label('purchase_return_quantity'),
            literal_column('0').label('purchase_return_price'),
            literal_column('0').label('export_comm_invoice_quantity'),
            literal_column('0').label('export_comm_invoice_price'),
        ).join(
            StockEtc, StockEtcItem.fk_stock_etc_id == StockEtc.id
        ).filter(
            StockEtcItem.type == '출고'
        ).filter(
            StockEtcItem.item_code.in_(item_code_list)
        ).filter(
            StockEtcItem.warehouse_code == warehouse_code
        )
        if start_date is None:
            query2 = query2.filter(
                StockEtc.target_date < end_date
            )
        else:
            query2 = query2.filter(
                StockEtc.target_date >= start_date
            ).filter(
                StockEtc.target_date <= end_date
            )
        query2 = query2.group_by(
            StockEtcItem.item_code
        )

        from backend_model.table_stock import StockMoveRelease, StockMoveReleaseItem
        query3 = db.session.query(
            StockMoveRelease.target_date.label('release_date'),
            StockMoveReleaseItem.item_code,
            StockMoveReleaseItem.cost_price.label('cost_price'),
            literal_column('0').label('shipment_release_quantity'),
            literal_column('0').label('shipment_release_price'),
            literal_column('0').label('stock_etc_release_quantity'),
            literal_column('0').label('stock_etc_release_price'),
            db.func.sum(StockMoveReleaseItem.release_quantity).label('stock_move_release_quantity'),
            db.func.sum(db.func.ifnull(StockMoveReleaseItem.total_cost_price, 0)).label('stock_move_release_price'),
            literal_column('0').label('produce_release_quantity'),
            literal_column('0').label('produce_release_price'),
            literal_column('0').label('purchase_return_quantity'),
            literal_column('0').label('purchase_return_price'),
            literal_column('0').label('export_comm_invoice_quantity'),
            literal_column('0').label('export_comm_invoice_price'),
        ).join(
            StockMoveRelease, StockMoveReleaseItem.fk_stock_move_release_id == StockMoveRelease.id
        ).filter(
            StockMoveReleaseItem.item_code.in_(item_code_list)
        ).filter(
            StockMoveReleaseItem.out_warehouse == warehouse_code
        )
        if start_date is None:
            query3 = query3.filter(
                StockMoveRelease.target_date < end_date
            )
        else:
            query3 = query3.filter(
                StockMoveRelease.target_date >= start_date
            ).filter(
                StockMoveRelease.target_date <= end_date
            )
        query3 = query3.group_by(
            StockMoveReleaseItem.item_code
        )

        from backend_model.table_production import PerformanceRegistration, PerformanceRegistrationItem2
        query4 = db.session.query(
            PerformanceRegistration.target_date.label('release_date'),
            PerformanceRegistrationItem2.item_code,
            PerformanceRegistrationItem2.cost_price.label('cost_price'),
            literal_column('0').label('shipment_release_quantity'),
            literal_column('0').label('shipment_release_price'),
            literal_column('0').label('stock_etc_release_quantity'),
            literal_column('0').label('stock_etc_release_price'),
            literal_column('0').label('stock_move_release_quantity'),
            literal_column('0').label('stock_move_release_price'),
            db.func.sum(PerformanceRegistrationItem2.material_quantity).label('produce_release_quantity'),
            db.func.sum(db.func.ifnull(PerformanceRegistrationItem2.total_cost_price, 0)).label('produce_release_price'),
            literal_column('0').label('purchase_return_quantity'),
            literal_column('0').label('purchase_return_price'),
            literal_column('0').label('export_comm_invoice_quantity'),
            literal_column('0').label('export_comm_invoice_price'),
        ).join(
            PerformanceRegistration,
            PerformanceRegistrationItem2.fk_performance_registration_id == PerformanceRegistration.id
        ).filter(
            PerformanceRegistrationItem2.item_code.in_(item_code_list)
        ).filter(
            PerformanceRegistrationItem2.warehouse_code == warehouse_code
        )
        if start_date is None:
            query4 = query4.filter(
                PerformanceRegistration.target_date < end_date
            )
        else:
            query4 = query4.filter(
                PerformanceRegistration.target_date >= start_date
            ).filter(
                PerformanceRegistration.target_date <= end_date
            )
        query4 = query4.group_by(
            PerformanceRegistrationItem2.item_code
        )

        from backend_model.table_purchase import PurchaseReceivingReturn, PurchaseReceivingReturnItem
        query5 = db.session.query(
            PurchaseReceivingReturn.return_date.label('release_date'),
            PurchaseReceivingReturnItem.item_code,
            PurchaseReceivingReturnItem.cost_price.label('cost_price'),
            literal_column('0').label('shipment_release_quantity'),
            literal_column('0').label('shipment_release_price'),
            literal_column('0').label('stock_etc_release_quantity'),
            literal_column('0').label('stock_etc_release_price'),
            literal_column('0').label('stock_move_release_quantity'),
            literal_column('0').label('stock_move_release_price'),
            literal_column('0').label('produce_release_quantity'),
            literal_column('0').label('produce_release_price'),
            db.func.sum(PurchaseReceivingReturnItem.return_quantity).label('purchase_return_quantity'),
            db.func.sum(db.func.ifnull(PurchaseReceivingReturnItem.total_cost_price, 0)).label('purchase_return_price'),
            literal_column('0').label('export_comm_invoice_quantity'),
            literal_column('0').label('export_comm_invoice_price'),
        ).join(
            PurchaseReceivingReturn, PurchaseReceivingReturnItem.fk_receiving_return_id == PurchaseReceivingReturn.id
        ).filter(
            PurchaseReceivingReturnItem.item_code.in_(item_code_list)
        ).filter(
            PurchaseReceivingReturnItem.warehouse_code == warehouse_code
        )
        if start_date is None:
            query5 = query5.filter(
                PurchaseReceivingReturn.return_date < end_date
            )
        else:
            query5 = query5.filter(
                PurchaseReceivingReturn.return_date >= start_date
            ).filter(
                PurchaseReceivingReturn.return_date <= end_date
            )
        query5 = query5.group_by(
            PurchaseReceivingReturnItem.item_code
        )

        from backend_model.table_export import ExportCommInvoice, ExportCommInvoiceItem
        query6 = db.session.query(
            ExportCommInvoice.invoice_date.label('release_date'),
            ExportCommInvoiceItem.item_code,
            ExportCommInvoiceItem.cost_price.label('cost_price'),
            literal_column('0').label('shipment_release_quantity'),
            literal_column('0').label('shipment_release_price'),
            literal_column('0').label('stock_etc_release_quantity'),
            literal_column('0').label('stock_etc_release_price'),
            literal_column('0').label('stock_move_release_quantity'),
            literal_column('0').label('stock_move_release_price'),
            literal_column('0').label('produce_release_quantity'),
            literal_column('0').label('produce_release_price'),
            literal_column('0').label('purchase_return_quantity'),
            literal_column('0').label('purchase_return_price'),
            db.func.sum(ExportCommInvoiceItem.invoice_quantity).label('export_comm_invoice_quantity'),
            db.func.sum(db.func.ifnull(ExportCommInvoiceItem.total_cost_price, 0)).label('export_comm_invoice_price'),
        ).join(
            ExportCommInvoice, ExportCommInvoiceItem.fk_export_comm_invoice_id == ExportCommInvoice.id
        ).filter(
            ExportCommInvoiceItem.item_code.in_(item_code_list)
        ).filter(
            ExportCommInvoiceItem.warehouse_code == warehouse_code
        )
        if start_date is None:
            query6 = query6.filter(
                ExportCommInvoice.invoice_date < end_date
            )
        else:
            query6 = query6.filter(
                ExportCommInvoice.invoice_date >= start_date
            ).filter(
                ExportCommInvoice.invoice_date <= end_date
            )
        query6 = query6.group_by(
            ExportCommInvoiceItem.item_code
        )

        release_datas = query1.union(query2).union(query3).union(query4).union(query5).union(query6).all()
        return release_datas

    @staticmethod
    def get_cost_receiving_quantity_n_price_list(
            item_code_list: list, warehouse_code: str, start_date = None, end_date = None
    ):
        from sqlalchemy.sql.expression import literal_column
        from backend_model.table_purchase import PurchaseReceiving, PurchaseReceivingItem
        query7 = db.session.query(
            PurchaseReceivingItem.item_code,
            db.func.sum(PurchaseReceivingItem.receiving_quantity).label('purchase_receiving_quantity'),
            db.func.sum(PurchaseReceivingItem.receiving_quantity * PurchaseReceivingItem.unit_price).label('purchase_receiving_price'),
            literal_column('0').label('stock_etc_receiving_quantity'),
            literal_column('0').label('stock_etc_receiving_price'),
            literal_column('0').label('stock_move_receiving_quantity'),
            literal_column('0').label('stock_move_receiving_price'),
            literal_column('0').label('produce_receiving_quantity'),
            literal_column('0').label('produce_receiving_price'),
            literal_column('0').label('release_return_quantity'),
            literal_column('0').label('release_return_price'),
            literal_column('0').label('import_clearance_quantity'),
            literal_column('0').label('import_clearance_price'),
        ).join(
            PurchaseReceiving, PurchaseReceivingItem.fk_receiving_id == PurchaseReceiving.id
        ).filter(
            PurchaseReceivingItem.item_code.in_(item_code_list)
        ).filter(
            PurchaseReceivingItem.warehouse_code == warehouse_code
        )
        if start_date is None:
            query7 = query7.filter(
                PurchaseReceiving.receiving_date2 < end_date
            )
        else:
            query7 = query7.filter(
                PurchaseReceiving.receiving_date2 >= start_date
            ).filter(
                PurchaseReceiving.receiving_date2 <= end_date
            )
        query7 = query7.group_by(
            PurchaseReceivingItem.item_code
        )

        from backend_model.table_stock import StockEtc, StockEtcItem
        query8 = db.session.query(
            StockEtcItem.item_code,
            literal_column('0').label('purchase_receiving_quantity'),
            literal_column('0').label('purchase_receiving_price'),
            db.func.sum(StockEtcItem.quantity).label('stock_etc_receiving_quantity'),
            db.func.sum(StockEtcItem.quantity * StockEtcItem.unit_price).label('stock_etc_receiving_price'),
            literal_column('0').label('stock_move_receiving_quantity'),
            literal_column('0').label('stock_move_receiving_price'),
            literal_column('0').label('produce_receiving_quantity'),
            literal_column('0').label('produce_receiving_price'),
            literal_column('0').label('release_return_quantity'),
            literal_column('0').label('release_return_price'),
            literal_column('0').label('import_clearance_quantity'),
            literal_column('0').label('import_clearance_price'),
        ).join(
            StockEtc, StockEtcItem.fk_stock_etc_id == StockEtc.id
        ).filter(
            StockEtcItem.type == "입고"
        ).filter(
            StockEtcItem.item_code.in_(item_code_list)
        ).filter(
            StockEtcItem.warehouse_code == warehouse_code
        )
        if start_date is None:
            query8 = query8.filter(
                StockEtc.target_date < end_date
            )
        else:
            query8 = query8.filter(
                StockEtc.target_date >= start_date
            ).filter(
                StockEtc.target_date <= end_date
            )
        query8 = query8.group_by(
            StockEtcItem.item_code
        )

        from backend_model.table_stock import StockMoveRelease, StockMoveReleaseItem
        query9 = db.session.query(
            StockMoveReleaseItem.item_code,
            literal_column('0').label('purchase_receiving_quantity'),
            literal_column('0').label('purchase_receiving_price'),
            literal_column('0').label('stock_etc_receiving_quantity'),
            literal_column('0').label('stock_etc_receiving_price'),
            db.func.sum(StockMoveReleaseItem.release_quantity).label('stock_move_receiving_quantity'),
            db.func.sum(StockMoveReleaseItem.release_quantity * StockMoveReleaseItem.unit_price).label('stock_move_receiving_price'),
            literal_column('0').label('produce_receiving_quantity'),
            literal_column('0').label('produce_receiving_price'),
            literal_column('0').label('release_return_quantity'),
            literal_column('0').label('release_return_price'),
            literal_column('0').label('import_clearance_quantity'),
            literal_column('0').label('import_clearance_price'),
        ).join(
            StockMoveRelease, StockMoveReleaseItem.fk_stock_move_release_id == StockMoveRelease.id
        ).filter(
            StockMoveReleaseItem.item_code.in_(item_code_list)
        ).filter(
            StockMoveReleaseItem.in_warehouse == warehouse_code
        )
        if start_date is None:
            query9 = query9.filter(
                StockMoveRelease.target_date < end_date
            )
        else:
            query9 = query9.filter(
                StockMoveRelease.target_date >= start_date
            ).filter(
                StockMoveRelease.target_date <= end_date
            )
        query9 = query9.group_by(
            StockMoveReleaseItem.item_code
        )

        from backend_model.table_production import PerformanceRegistration, PerformanceRegistrationItem1
        query10 = db.session.query(
            PerformanceRegistrationItem1.item_code,
            literal_column('0').label('purchase_receiving_quantity'),
            literal_column('0').label('purchase_receiving_price'),
            literal_column('0').label('stock_etc_receiving_quantity'),
            literal_column('0').label('stock_etc_receiving_price'),
            literal_column('0').label('stock_move_receiving_quantity'),
            literal_column('0').label('stock_move_receiving_price'),
            db.func.sum(PerformanceRegistrationItem1.good_quantity).label('produce_receiving_quantity'),
            db.func.sum(PerformanceRegistrationItem1.good_quantity * PerformanceRegistrationItem1.unit_price).label('produce_receiving_price'),
            literal_column('0').label('release_return_quantity'),
            literal_column('0').label('release_return_price'),
            literal_column('0').label('import_clearance_quantity'),
            literal_column('0').label('import_clearance_price'),
        ).join(
            PerformanceRegistration,
            PerformanceRegistrationItem1.fk_performance_registration_id == PerformanceRegistration.id
        ).filter(
            PerformanceRegistrationItem1.item_code.in_(item_code_list)
        ).filter(
            PerformanceRegistrationItem1.warehouse_code == warehouse_code
        )
        if start_date is None:
            query10 = query10.filter(
                PerformanceRegistration.target_date < end_date
            )
        else:
            query10 = query10.filter(
                PerformanceRegistration.target_date >= start_date
            ).filter(
                PerformanceRegistration.target_date <= end_date
            )
        query10 = query10.group_by(
            PerformanceRegistrationItem1.item_code
        )

        from backend_model.table_shipment import ShipmentReleaseReturn, ShipmentReleaseReturnItem
        query11 = db.session.query(
            ShipmentReleaseReturnItem.item_code,
            literal_column('0').label('purchase_receiving_quantity'),
            literal_column('0').label('purchase_receiving_price'),
            literal_column('0').label('stock_etc_receiving_quantity'),
            literal_column('0').label('stock_etc_receiving_price'),
            literal_column('0').label('stock_move_receiving_quantity'),
            literal_column('0').label('stock_move_receiving_price'),
            literal_column('0').label('produce_receiving_quantity'),
            literal_column('0').label('produce_receiving_price'),
            db.func.sum(ShipmentReleaseReturnItem.return_quantity).label('release_return_quantity'),
            db.func.sum(ShipmentReleaseReturnItem.return_quantity * db.func.ifnull(ShipmentReleaseReturnItem.cost_price, 0)).label('release_return_price'),
            literal_column('0').label('import_clearance_quantity'),
            literal_column('0').label('import_clearance_price'),
        ).join(
            ShipmentReleaseReturn, ShipmentReleaseReturnItem.fk_release_return_id == ShipmentReleaseReturn.id
        ).filter(
            ShipmentReleaseReturnItem.item_code.in_(item_code_list)
        ).filter(
            ShipmentReleaseReturnItem.warehouse_code == warehouse_code
        )
        if start_date is None:
            query11 = query11.filter(
                ShipmentReleaseReturn.return_date < end_date
            )
        else:
            query11 = query11.filter(
                ShipmentReleaseReturn.return_date >= start_date
            ).filter(
                ShipmentReleaseReturn.return_date <= end_date
            )
        query11 = query11.group_by(
            ShipmentReleaseReturnItem.item_code
        )

        from backend_model.table_import import ImportClearance, ImportClearanceItem
        query12 = db.session.query(
            ImportClearanceItem.item_code,
            literal_column('0').label('purchase_receiving_quantity'),
            literal_column('0').label('purchase_receiving_price'),
            literal_column('0').label('stock_etc_receiving_quantity'),
            literal_column('0').label('stock_etc_receiving_price'),
            literal_column('0').label('stock_move_receiving_quantity'),
            literal_column('0').label('stock_move_receiving_price'),
            literal_column('0').label('produce_receiving_quantity'),
            literal_column('0').label('produce_receiving_price'),
            literal_column('0').label('release_return_quantity'),
            literal_column('0').label('release_return_price'),
            db.func.sum(ImportClearanceItem.qty).label('import_clearance_quantity'),
            db.func.sum(ImportClearanceItem.qty * ImportClearanceItem.cost_price).label('import_clearance_price'),
        ).join(
            ImportClearance, ImportClearanceItem.fk_import_clearance_id == ImportClearance.id
        ).filter(
            ImportClearanceItem.item_code.in_(item_code_list)
        ).filter(
            ImportClearanceItem.warehouse_code == warehouse_code
        )
        if start_date is None:
            query12 = query12.filter(
                ImportClearance.clearance_date < end_date
            )
        else:
            query12 = query12.filter(
                ImportClearance.clearance_date >= start_date
            ).filter(
                ImportClearance.clearance_date <= end_date
            )
        query12 = query12.group_by(
            ImportClearanceItem.item_code
        )

        receiving_datas = query7.union(query8).union(query9).union(query10).union(query11).union(query12).all()
        return receiving_datas
