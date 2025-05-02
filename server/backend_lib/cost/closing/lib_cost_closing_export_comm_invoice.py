# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional, Dict

from backend_model.database import DBManager

db = DBManager.db


class LibCostClosingExportCommInvoice(object):

    @staticmethod
    def get_export_comm_invoice_item_list(
            end_date: datetime, item_code: Optional[str] = None, warehouse_code: Optional[str] = None
    ) -> list:
        release_items = []

        from backend_model.table_export import ExportCommInvoice, ExportCommInvoiceItem
        query = db.session.query(
            ExportCommInvoiceItem
        ).join(
            ExportCommInvoice, ExportCommInvoiceItem.export_comm_invoice
        ).filter(
            ExportCommInvoice.invoice_date <= end_date
        )
        if item_code:
            query = query.filter(
                ExportCommInvoiceItem.item_code == item_code
            )
        if warehouse_code:
            query = query.filter(
                ExportCommInvoiceItem.warehouse_code == warehouse_code
            )
        query = query.order_by(
            ExportCommInvoice.invoice_date.asc()
        )
        invoice_items = query.all()

        for item in invoice_items:
            release_items.append({
                'id': item.id,
                'type': 'ExportCommInvoiceItem',
                'release_date': item.export_comm_invoice.invoice_date,
                'quantity': item.invoice_quantity,
                'item_code': item.item_code
            })
        return release_items

    @staticmethod
    def clear_cost_price(start_date, end_date, warehouse_code, item_code):
        from backend_model.table_export import ExportCommInvoice, ExportCommInvoiceItem
        query = db.session.query(
            ExportCommInvoiceItem
        ).join(
            ExportCommInvoice, ExportCommInvoice.id == ExportCommInvoiceItem.fk_export_comm_invoice_id
        ).filter(
            ExportCommInvoice.invoice_date >= start_date
        ).filter(
            ExportCommInvoice.invoice_date <= end_date
        )
        if item_code:
            query = query.filter(
                ExportCommInvoiceItem.item_code == item_code
            )
        if warehouse_code:
            query = query.filter(
                ExportCommInvoiceItem.warehouse_code == warehouse_code
            )
        export_comm_invoice_items = query.all()
        for item in export_comm_invoice_items:
            item.cost_price = None
            item.total_cost_price = None
        db.session.commit()
