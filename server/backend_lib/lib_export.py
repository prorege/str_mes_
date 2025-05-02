# -*- coding: utf-8 -*-

from decimal import Decimal
from backend_model.table_export import *

db = DBManager.db


class LibExportSalesOrder(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'order_number', ExportSalesOrder, ExportSalesOrder.order_number, '/export/sales-order')


class LibExportSalesOrderItem(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_setup import LibSetupBasicStock

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
    def sales_order_update_assign_quantity(sales_order_item_id, item_code, warehouse):
        basic_stock = LibExportSalesOrderItem.saels_order_update_available_stock(item_code, warehouse)
        sales_order_item = db.session.query(ExportSalesOrderItem).filter(ExportSalesOrderItem.id == sales_order_item_id).first()
        if sales_order_item:
            if not sales_order_item.assign_quantity:
                sales_order_item.assign_quantity = 0
            if basic_stock.available_stock > 0 and sales_order_item.not_shipped > 0:
                if sales_order_item.not_shipped - sales_order_item.assign_quantity < basic_stock.available_stock:
                    sales_order_item.assign_quantity = sales_order_item.not_shipped
                else:
                    sales_order_item.assign_quantity += basic_stock.available_stock
        db.session.commit()
        updated_stock = LibExportSalesOrderItem.saels_order_update_available_stock(item_code, warehouse)
        return updated_stock

    @staticmethod
    def saels_order_update_available_stock(item_code, warehouse_code):
        from backend_lib.lib_setup import LibSetupBasicStock

        # 기초재고를 찾는다 (품목코드, 창고코드)
        basic_stock = LibSetupBasicStock.get_basic_stock(item_code, warehouse_code)
        if basic_stock:
            basic_stock.available_stock = LibExportSalesOrderItem.sales_order_calculate_available_stock(item_code, warehouse_code, basic_stock.current_stock)
            db.session.commit()
            return basic_stock
        else:
            return None
        
    @staticmethod
    def sales_order_calculate_available_stock(item_code, warehouse_code, current_stock):
        total_assign_quantity = LibExportSalesOrderItem.sales_order_item_get_total_assign_quantity_by_item_code(item_code, warehouse_code)
        available_stock = current_stock - total_assign_quantity
        available_stock = 0 if available_stock < 0 else available_stock
        return available_stock

    @staticmethod
    def sales_order_item_get_total_assign_quantity_by_item_code(item_code, warehouse_code):
        assign_quantity = db.session.query(
            db.func.sum(ExportSalesOrderItem.assign_quantity)
        ).filter(
            ExportSalesOrderItem.item_code == item_code
        ).filter(
            ExportSalesOrderItem.warehouse_code == warehouse_code
        ).first()[0]
        assign_quantity = 0 if not assign_quantity else assign_quantity
        return assign_quantity

    @staticmethod
    def post_postprocessor(result=None, **kw):
        updated_stock = LibExportSalesOrderItem.sales_order_update_assign_quantity(result['id'], result['item_code'], result['warehouse_code'])

        # 기초재고의 가용재고를 업데이트
        # 업데이트된 가용재고를 결과에 담는다
        basic_stock = result['basic_stock']
        if basic_stock and updated_stock:
            basic_stock['available_stock'] = updated_stock.available_stock


class LibExportCommInvoice(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'invoice_number', ExportCommInvoice, ExportCommInvoice.invoice_number, '/export/comm-invoice')


class LibExportCommInvoiceItem(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_setup import LibSetupBasicStock

        # 현재고를 가져온다
        basic_stock = LibSetupBasicStock.get_basic_stock(data['item_code'], data['warehouse_code'])
        if basic_stock is None:
            from backend_lib.lib_exception import MesException
            MesException.raise_not_exist_basic_stock()
        # 마이너스 수불 처리 가능 여부 확인
        from backend_lib.lib_setup import LibSetupControl
        not_use_minus_stock = LibSetupControl.get_not_use_minus_stock(basic_stock.fk_company_id)
        # 현재고 계산
        new_current_stock = basic_stock.current_stock - data['invoice_quantity']
        # 마이너스 수불 처리 불가인 경우
        if not_use_minus_stock:
            if new_current_stock < 0:  # 출고수량이 현재고보다 크면 에러를 리턴한다
                from backend_lib.lib_exception import MesException
                MesException.raise_overflow_current_stock()
        # 현재고가 출고수량보다 크면 현재고를 업데이트한다
        LibSetupBasicStock.update_current_stock(data['item_code'], data['warehouse_code'], new_current_stock)

    @staticmethod
    def patch_single_preprocessor(instance_id=None, data=None, **kw):
        from backend_lib.lib_setup import LibSetupBasicStock

        if 'invoice_quantity' in data:  # 출고수량이 있는지 확인
            # 기존의 출고품목 데이터를 가져온다
            invoice_item = db.session.query(
                ExportCommInvoiceItem
            ).filter(
                ExportCommInvoiceItem.id == instance_id
            ).first()
            if invoice_item:
                # 현재고를 가져온다
                basic_stock = LibSetupBasicStock.get_basic_stock(invoice_item.item_code, invoice_item.warehouse_code)
                # 기초 재고가 없으면 에러
                if basic_stock is None:
                    from backend_lib.lib_exception import MesException
                    MesException.raise_not_exist_basic_stock()
                # 마이너스 수불 처리 가능 여부 확인
                from backend_lib.lib_setup import LibSetupControl
                not_use_minus_stock = LibSetupControl.get_not_use_minus_stock(basic_stock.fk_company_id)
                # 새로운 현재고를 계산한다 (기존 현재고 + 기존 출고 수량 - 새로운 출고 수량)
                new_current_stock = basic_stock.current_stock + invoice_item.invoice_quantity - data['invoice_quantity']
                # 마이너스 수불 처리 불가인 경우
                if not_use_minus_stock:
                    if new_current_stock < 0:  # 새로운 현재고가 0보다 작으면 에러
                        from backend_lib.lib_exception import MesException
                        MesException.raise_overflow_current_stock()
                # 현재고를 업데이트한다
                LibSetupBasicStock.update_current_stock(invoice_item.item_code,
                                                        invoice_item.warehouse_code,
                                                        new_current_stock)
                # 가용재고를 업데이트한다
                LibSetupBasicStock.update_available_stock(invoice_item.item_code, invoice_item.warehouse_code)

    @staticmethod
    def post_postprocessor(result=None, **kw):
        LibExportCommInvoiceItem.update_order_item_assign_quantity(result['id'])
        LibExportCommInvoiceItem.update_order_item_not_shipped(result['fk_export_sales_order_item_id'])

    @staticmethod
    def patch_single_postprocessor(result=None, **kw):
        LibExportCommInvoiceItem.update_order_item_assign_quantity(result['id'])
        LibExportCommInvoiceItem.update_order_item_not_shipped(result['fk_export_sales_order_item_id'])

    @staticmethod
    def update_order_item_assign_quantity(invoice_item_id):
        """
        출고품목의 아이디로 수주품목을 찾아서 할당수량을 업데이트한다
        :param invoice_item_id: 출고품목 아이디
        :return:
        """
        from backend_lib.lib_setup import LibSetupBasicStock

        invoice = db.session.query(
            ExportCommInvoiceItem
        ).filter(
            ExportCommInvoiceItem.id == invoice_item_id
        ).first()

        invoice_quantity = invoice.invoice_quantity
        assign_quantity = invoice.export_sales_order_item.assign_quantity
        invoice.export_sales_order_item.assign_quantity = assign_quantity - invoice_quantity
        if invoice.export_sales_order_item.assign_quantity < 0:
            invoice.export_sales_order_item.assign_quantity = 0
        db.session.commit()

        LibSetupBasicStock.update_available_stock(invoice.export_sales_order_item.item_code, invoice.export_sales_order_item.warehouse_code)

    @staticmethod
    def update_order_item_not_shipped(order_item_id):
        """
        수주품목의 미출고 수량을 업데이트한다
        :param order_item_id: 수주품목 아이디
        :return:
        """
        # 수주 품목을 가져온다
        order_item = db.session.query(
            ExportSalesOrderItem
        ).filter(
            ExportSalesOrderItem.id == order_item_id
        ).first()
        # 해당 수주 품목의 전체 출고 수량을 찾는다
        invoice_quantity = db.session.query(
            db.func.sum(ExportCommInvoiceItem.invoice_quantity)
        ).filter(
            ExportCommInvoiceItem.fk_export_sales_order_item_id == order_item_id
        ).first()[0]
        # 수주 품목의 미출고 수량을 업데이트 (수주 수량 - 전체 출고 수량)
        order_item.not_shipped = order_item.order_quantity - invoice_quantity
        db.session.commit()

    @staticmethod
    def get_total_release_quantity_by_item_code_query(use_count, item_code, warehouse_code, start_date=None, end_date=None):
        if use_count:
            query = db.session.query(
                db.func.sum(ExportCommInvoiceItem.invoice_quantity)
            )
        else:
            query = db.session.query(
                ExportCommInvoice.invoice_number,
                ExportCommInvoice.invoice_date,
                ExportCommInvoice.client_company,
                ExportCommInvoiceItem.invoice_quantity,
                ExportCommInvoiceItem.unit_price,
                ExportCommInvoiceItem.cost_price,
                db.func.ifnull(ExportCommInvoiceItem.total_cost_price, 0).label('total_cost_price')
            )
        query = query.join(
            ExportCommInvoice, ExportCommInvoiceItem.fk_export_comm_invoice_id == ExportCommInvoice.id
        ).filter(
            ExportCommInvoiceItem.item_code == item_code
        ).filter(
            ExportCommInvoiceItem.warehouse_code == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                ExportCommInvoice.invoice_date >= start_date
            ).filter(
                ExportCommInvoice.invoice_date <= end_date
            )
        elif end_date:
            query = query.filter(
                ExportCommInvoice.invoice_date < end_date
            )
        return query

    @staticmethod
    def get_total_release_quantity_by_item_code(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibExportCommInvoiceItem.get_total_release_quantity_by_item_code_query(use_count=True,
                                                                                       item_code=item_code,
                                                                                       warehouse_code=warehouse_code,
                                                                                       start_date=start_date,
                                                                                       end_date=end_date)
        release_quantity = query.first()[0]
        release_quantity = 0 if not release_quantity else release_quantity
        return release_quantity

    @staticmethod
    def get_all_release_item_for_statistics(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibExportCommInvoiceItem.get_total_release_quantity_by_item_code_query(use_count=False,
                                                                                       item_code=item_code,
                                                                                       warehouse_code=warehouse_code,
                                                                                       start_date=start_date,
                                                                                       end_date=end_date)
        release_items = query.all()
        return release_items

    @staticmethod
    def get_total_release_price_by_item_code(item_code: str, warehouse_code: str, start_date=None, end_date=None) -> Decimal:
        query = db.session.query(
            db.func.sum(db.func.ifnull(ExportCommInvoiceItem.total_cost_price, 0))
        ).join(
            ExportCommInvoice, ExportCommInvoiceItem.fk_export_comm_invoice_id == ExportCommInvoice.id
        ).filter(
            ExportCommInvoiceItem.item_code == item_code
        ).filter(
            ExportCommInvoiceItem.warehouse_code == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                ExportCommInvoice.invoice_date >= start_date
            ).filter(
                ExportCommInvoice.invoice_date <= end_date
            )
        elif end_date:
            query = query.filter(
                ExportCommInvoice.invoice_date < end_date
            )
        release_price = query.first()[0]
        release_price = Decimal('0') if not release_price else release_price
        return release_price
