# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional, Dict

from backend_model.database import DBManager

db = DBManager.db


class LibCostClosingPerformanceRegistration(object):

    @staticmethod
    def get_produce_receiving_item_list(
            end_date: datetime, item_code: Optional[str] = None, warehouse_code: Optional[str] = None
    ) -> list:
        receiving_items = []

        from backend_model.table_production import PerformanceRegistration, PerformanceRegistrationItem1
        query = db.session.query(
            PerformanceRegistrationItem1
        ).join(
            PerformanceRegistration, PerformanceRegistrationItem1.performance_registration
        ).filter(
            PerformanceRegistration.target_date <= end_date
        )
        if item_code:
            query = query.filter(
                PerformanceRegistrationItem1.item_code == item_code
            )
        if warehouse_code:
            query = query.filter(
                PerformanceRegistrationItem1.warehouse_code == warehouse_code
            )
        query = query.order_by(
            PerformanceRegistration.target_date.asc()
        )
        produce_receiving_items = query.all()

        for item in produce_receiving_items:
            receiving_items.append({
                'id': item.id,
                'type': 'PerformanceRegistrationItem1',
                'receiving_date': item.performance_registration.target_date,
                'quantity': item.production_receiving_quantity,
                'item_code': item.item_code,
                'unit_price': item.unit_price
            })
        return receiving_items

    @staticmethod
    def get_material_consume_item_list(
            end_date: datetime, item_code: Optional[str] = None, warehouse_code: Optional[str] = None
    ) -> list:
        release_items = []

        from backend_model.table_production import PerformanceRegistration, PerformanceRegistrationItem2
        query = db.session.query(
            PerformanceRegistrationItem2
        ).join(
            PerformanceRegistration, PerformanceRegistrationItem2.performance_registration
        ).filter(
            PerformanceRegistration.target_date <= end_date
        )
        if item_code:
            query = query.filter(
                PerformanceRegistrationItem2.item_code == item_code
            )
        if warehouse_code:
            query = query.filter(
                PerformanceRegistrationItem2.warehouse_code == warehouse_code
            )
        query = query.order_by(
            PerformanceRegistration.target_date.asc()
        )
        material_consume_items = query.all()

        for item in material_consume_items:
            release_items.append({
                'id': item.id,
                'type': 'PerformanceRegistrationItem2',
                'release_date': item.performance_registration.target_date,
                'quantity': item.material_quantity,
                'item_code': item.item_code
            })
        return release_items

    @staticmethod
    def clear_cost_price(start_date, end_date, warehouse_code, item_code):
        from backend_model.table_production import PerformanceRegistration, PerformanceRegistrationItem2
        query = db.session.query(
            PerformanceRegistrationItem2
        ).join(
            PerformanceRegistration,
            PerformanceRegistration.id == PerformanceRegistrationItem2.fk_performance_registration_id
        ).filter(
            PerformanceRegistration.target_date >= start_date
        ).filter(
            PerformanceRegistration.target_date <= end_date
        )
        if item_code:
            query = query.filter(
                PerformanceRegistrationItem2.item_code == item_code
            )
        if warehouse_code:
            query = query.filter(
                PerformanceRegistrationItem2.warehouse_code == warehouse_code
            )
        performance_registration_items = query.all()
        for item in performance_registration_items:
            item.cost_price = None
            item.total_cost_price = None
        db.session.commit()
