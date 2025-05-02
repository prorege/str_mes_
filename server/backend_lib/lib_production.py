# -*- coding: utf-8 -*-

from decimal import Decimal
from dateutil.relativedelta import relativedelta
from backend_model.table_production import *

db = DBManager.db


class LibProductionPlan(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'number', ProductionPlan, ProductionPlan.number, '/produce/plan')


class LibProductionPlanItem1(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_setup import LibSetupBasicStock
        if 'item_code' in data and 'warehouse_code' in data:
            LibSetupBasicStock.check_basic_stock(data['item_code'], data['warehouse_code'])

    @staticmethod
    def delete_single_preprocessor(instance_id=None, **kw):
        from backend_lib.lib_util import LibUtil
        LibUtil.check_exist_connected_data(MeasureRequirementItem1, MeasureRequirementItem1.fk_plan_item_id, instance_id)
        LibUtil.check_exist_connected_data(WorkOrderItem1, WorkOrderItem1.fk_plan_item_id, instance_id)

    @staticmethod
    def update_unordered_quantity(plan_item_id):
        """
        생산계획품목의 미작지수량을 업데이트한다

        :param plan_item_id: 생산계획품목 아이디
        :return:
        """
        ordered_quantity = db.session.query(
            db.func.sum(WorkOrderItem1.required_quantity)
        ).filter(
            WorkOrderItem1.fk_plan_item_id == plan_item_id
        ).first()[0]
        if ordered_quantity is None:
            ordered_quantity = 0

        plan_item = db.session.query(
            ProductionPlanItem1
        ).filter(
            ProductionPlanItem1.id == plan_item_id
        ).first()
        if plan_item:
            unordered_quantity = plan_item.production_plan_quantity - ordered_quantity
            if unordered_quantity < 0:
                unordered_quantity = 0
            plan_item.unordered_quantity = unordered_quantity
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

class LibMeasureRequirement(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'number', MeasureRequirement, MeasureRequirement.number,
                                  '/produce/measure-requirement')


class LibMeasureRequirementItem1(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_setup import LibSetupBasicStock
        if 'item_code' in data and 'warehouse_code' in data:
            LibSetupBasicStock.check_basic_stock(data['item_code'], data['warehouse_code'])


class LibMeasureRequirementItem2(object):
    @staticmethod
    def update_unordered_plan_quantity(req_item_id, plan_quantity):
        req_item = db.session.query(
            MeasureRequirementItem2
        ).filter(
            MeasureRequirementItem2.id == req_item_id
        ).first()
        if req_item:
            req_item.unordered_plan_quantity = req_item.order_plan_quantity - plan_quantity
            if req_item.unordered_plan_quantity < 0:
                req_item.unordered_plan_quantity = 0
            db.session.commit()


class LibWorkOrder(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'number', WorkOrder, WorkOrder.number, '/produce/work-order')


class LibWorkOrderItem1(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_setup import LibSetupBasicStock
        if 'item_code' in data and 'warehouse_code' in data:
            LibSetupBasicStock.check_basic_stock(data['item_code'], data['warehouse_code'])

    @staticmethod
    def post_postprocessor(result=None, **kw):
        # 생산계획품목의 미작지수량 업데이트
        if result['fk_plan_item_id']:
            LibProductionPlanItem1.update_unordered_quantity(result['fk_plan_item_id'])

    @staticmethod
    def delete_single_preprocessor(instance_id=None, **kw):
        from backend_lib.lib_util import LibUtil
        LibUtil.check_exist_connected_data(PerformanceRegistrationItem1,
                                           PerformanceRegistrationItem1.fk_work_order_item, instance_id)

    @staticmethod
    def update_unproduced_quantity(work_order_item_id):
        """
        작업지시품목의 미생산수량을 업데이트한다

        :param work_order_item_id: 작업지시품목 아이디
        :return:
        """
        produce_quantity = db.session.query(
            db.func.sum(PerformanceRegistrationItem1.production_receiving_quantity)
        ).filter(
            PerformanceRegistrationItem1.fk_work_order_item == work_order_item_id
        ).first()[0]
        if produce_quantity is None:
            produce_quantity = 0

        work_order_item = db.session.query(
            WorkOrderItem1
        ).filter(
            WorkOrderItem1.id == work_order_item_id
        ).first()
        if work_order_item:
            unproduced_quantity = work_order_item.required_quantity - produce_quantity
            if unproduced_quantity < 0:
                unproduced_quantity = 0
            work_order_item.unproduced_quantity = unproduced_quantity
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

class LibWorkOrderItem2(object):
    @staticmethod
    def update_uninput_quantity(work_order_item_id, quantity):
        work_order_item = db.session.query(
            WorkOrderItem2
        ).filter(
            WorkOrderItem2.id == work_order_item_id
        ).first()
        if work_order_item:
            work_order_item.uninput_quantity = quantity
            db.session.commit()


class LibPerformanceRegistration(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'number', PerformanceRegistration, PerformanceRegistration.number,
                                  '/produce/performance-registration')


class LibPerformanceRegistrationItem1(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_setup import LibSetupBasicStock
        if 'item_code' in data and 'warehouse_code' in data:
            LibSetupBasicStock.check_basic_stock(data['item_code'], data['warehouse_code'])

    @staticmethod
    def delete_single_preprocessor(instance_id=None, **kw):
        from backend_lib.lib_util import LibUtil
        from backend_model.table_quality import QualityManagement
        LibUtil.check_exist_connected_data(QualityManagement,
                                           QualityManagement.fk_performance_registration_item, instance_id)

        item = db.session.query(
            PerformanceRegistrationItem1
        ).filter(
            PerformanceRegistrationItem1.id == instance_id
        ).first()
        # 자재소모 완료 여부 업데이트
        if item:
            performance = db.session.query(
                PerformanceRegistration
            ).filter(
                PerformanceRegistration.id == item.fk_performance_registration_id
            ).first()
            if performance:
                performance.closing_yn = False
                db.session.commit()

    @staticmethod
    def post_postprocessor(result=None, **kw):
        if result['fk_work_order_item']:
            LibWorkOrderItem1.update_unproduced_quantity(result['fk_work_order_item'])
        # 재고를 업데이트한다
        from backend_lib.lib_setup import LibSetupBasicStock
        LibSetupBasicStock.update_stock_by_item_code(result['item_code'], result['warehouse_code'])
        # 자재소모 완료 여부 업데이트
        if result['fk_performance_registration_id']:
            performance = db.session.query(
                PerformanceRegistration
            ).filter(
                PerformanceRegistration.id == result['fk_performance_registration_id']
            ).first()
            if performance:
                performance.closing_yn = False
                db.session.commit()

    @staticmethod
    def patch_single_postprocessor(result=None, **kw):
        if result['fk_work_order_item']:
            LibWorkOrderItem1.update_unproduced_quantity(result['fk_work_order_item'])
        # 자재소모 완료 여부 업데이트
        if result['fk_performance_registration_id']:
            performance = db.session.query(
                PerformanceRegistration
            ).filter(
                PerformanceRegistration.id == result['fk_performance_registration_id']
            ).first()
            if performance:
                performance.closing_yn = False
                db.session.commit()

    @staticmethod
    def update_check_quantity(reg_item_id: int, check_quantity: int, bad_quantity: int, good_quantity: int,
                              check: int):
        """
        생산입고품목의 검수수량, 불량수량, 양품수량, 검수완료를 업데이트한다

        :param reg_item_id: 생산입고품목 아이디
        :param check_quantity: 검수수량
        :param bad_quantity: 불량수량
        :param good_quantity: 양품수량
        :param check: 검수완료
        :return:
        """
        reg_item = db.session.query(
            PerformanceRegistrationItem1
        ).filter(
            PerformanceRegistrationItem1.id == reg_item_id
        ).first()
        if reg_item:
            reg_item.check_quantity = check_quantity
            reg_item.bad_quantity = bad_quantity
            reg_item.good_quantity = good_quantity
            reg_item.check_yn = check
            db.session.commit()

            from backend_lib.lib_setup import LibSetupBasicStock
            LibSetupBasicStock.update_stock_by_item_code(reg_item.item_code, reg_item.warehouse_code)

    @staticmethod
    def get_total_receiving_quantity_by_item_code_query(use_count, item_code, warehouse_code, start_date=None, end_date=None):
        if use_count:
            query = db.session.query(
                db.func.sum(PerformanceRegistrationItem1.good_quantity)
            )
        else:
            query = db.session.query(
                PerformanceRegistration.number,
                PerformanceRegistration.target_date,
                PerformanceRegistrationItem1.unit_price,
                PerformanceRegistrationItem1.good_quantity,
                PerformanceRegistrationItem1.fk_project_management_id,
                PerformanceRegistrationItem1.fk_work_order_item
            )
        query = query.join(
            PerformanceRegistration,
            PerformanceRegistrationItem1.fk_performance_registration_id == PerformanceRegistration.id
        ).filter(
            PerformanceRegistrationItem1.item_code == item_code
        ).filter(
            PerformanceRegistrationItem1.warehouse_code == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                PerformanceRegistration.target_date >= start_date
            ).filter(
                PerformanceRegistration.target_date <= end_date
            )
        elif end_date:
            query = query.filter(
                PerformanceRegistration.target_date < end_date
            )
        return query

    @staticmethod
    def get_total_receiving_quantity_by_item_code(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibPerformanceRegistrationItem1.get_total_receiving_quantity_by_item_code_query(use_count=True,
                                                                                                item_code=item_code,
                                                                                                warehouse_code=warehouse_code,
                                                                                                start_date=start_date,
                                                                                                end_date=end_date)
        receiving_quantity = query.first()[0]
        receiving_quantity = 0 if not receiving_quantity else receiving_quantity
        return receiving_quantity

    @staticmethod
    def get_all_receiving_item_for_statistics(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibPerformanceRegistrationItem1.get_total_receiving_quantity_by_item_code_query(use_count=False,
                                                                                                item_code=item_code,
                                                                                                warehouse_code=warehouse_code,
                                                                                                start_date=start_date,
                                                                                                end_date=end_date)
        release_items = query.all()
        return release_items

    @staticmethod
    def get_total_receiving_price_by_item_code(item_code: str, warehouse_code: str, start_date=None, end_date=None) -> int:
        query = db.session.query(
            db.func.sum(PerformanceRegistrationItem1.good_quantity * PerformanceRegistrationItem1.unit_price)
        ).join(
            PerformanceRegistration,
            PerformanceRegistrationItem1.fk_performance_registration_id == PerformanceRegistration.id
        ).filter(
            PerformanceRegistrationItem1.item_code == item_code
        ).filter(
            PerformanceRegistrationItem1.warehouse_code == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                PerformanceRegistration.target_date >= start_date
            ).filter(
                PerformanceRegistration.target_date <= end_date
            )
        elif end_date:
            query = query.filter(
                PerformanceRegistration.target_date < end_date
            )
        receiving_price = query.first()[0]
        receiving_price = 0 if not receiving_price else receiving_price
        return receiving_price

    @staticmethod
    def get_shipment_order_company(work_order_item_id):
        from backend_model.table_production import WorkOrderItem1
        work_order_item = db.session.query(
            WorkOrderItem1
        ).filter(
            WorkOrderItem1.id == work_order_item_id
        ).first()
        if not work_order_item:
            return ''

        from backend_model.table_production import ProductionPlanItem1
        produce_plan_item = db.session.query(
            ProductionPlanItem1
        ).filter(
            ProductionPlanItem1.id == work_order_item.fk_plan_item_id
        ).first()
        if not produce_plan_item:
            return ''

        from backend_model.table_shipment import ShipmentOrderItem
        shipment_order_item = db.session.query(
            ShipmentOrderItem
        ).filter(
            ShipmentOrderItem.id == produce_plan_item.fk_order_item_id
        ).first()
        if not shipment_order_item:
            return ''

        return shipment_order_item.order.client_company

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

class LibPerformanceRegistrationItem2(object):
    @staticmethod
    def patch_single_preprocessor(instance_id=None, data=None, **kw):
        reg_item = db.session.query(
            PerformanceRegistrationItem2
        ).filter(
            PerformanceRegistrationItem2.id == instance_id
        ).first()
        if reg_item and reg_item.basic_stock:
            from backend_model.table_setup import SetupBasicStock
            basic_stock = db.session.query(
                SetupBasicStock
            ).filter(
                SetupBasicStock.id == reg_item.basic_stock.id
            ).first()
            if basic_stock:
                basic_stock.available_stock += reg_item.material_quantity
                basic_stock.current_stock += reg_item.material_quantity

            new_basic_stock = db.session.query(
                SetupBasicStock
            ).filter(
                SetupBasicStock.item_code == data.item_code
            ).filter(
                SetupBasicStock.wh_code == data.warehouse_code
            ).first()
            if new_basic_stock:
                basic_stock.available_stock -= data.material_quantity
                basic_stock.current_stock -= data.material_quantity
        db.session.commit()

    @staticmethod
    def get_total_release_quantity_by_item_code_query(use_count, item_code, warehouse_code, start_date=None, end_date=None):
        if use_count:
            query = db.session.query(
                db.func.sum(PerformanceRegistrationItem2.material_quantity)
            )
        else:
            query = db.session.query(
                PerformanceRegistration.number,
                PerformanceRegistration.target_date,
                PerformanceRegistrationItem2.material_quantity,
                PerformanceRegistrationItem2.cost_price,
                db.func.ifnull(PerformanceRegistrationItem2.total_cost_price, 0).label('total_cost_price')
            )
        query = query.join(
            PerformanceRegistration,
            PerformanceRegistrationItem2.fk_performance_registration_id == PerformanceRegistration.id
        ).filter(
            PerformanceRegistrationItem2.item_code == item_code
        ).filter(
            PerformanceRegistrationItem2.warehouse_code == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                PerformanceRegistration.target_date >= start_date
            ).filter(
                PerformanceRegistration.target_date <= end_date
            )
        elif end_date:
            query = query.filter(
                PerformanceRegistration.target_date < end_date
            )
        return query

    @staticmethod
    def get_total_release_quantity_by_item_code(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibPerformanceRegistrationItem2.get_total_release_quantity_by_item_code_query(use_count=True,
                                                                                              item_code=item_code,
                                                                                              warehouse_code=warehouse_code,
                                                                                              start_date=start_date,
                                                                                              end_date=end_date)
        release_quantity = query.first()[0]
        release_quantity = 0 if not release_quantity else release_quantity
        return release_quantity

    @staticmethod
    def get_all_release_item_for_statistics(item_code, warehouse_code, start_date=None, end_date=None):
        query = LibPerformanceRegistrationItem2.get_total_release_quantity_by_item_code_query(use_count=False,
                                                                                              item_code=item_code,
                                                                                              warehouse_code=warehouse_code,
                                                                                              start_date=start_date,
                                                                                              end_date=end_date)
        release_items = query.all()
        return release_items

    @staticmethod
    def get_total_release_price_by_item_code(item_code: str, warehouse_code: str, start_date=None, end_date=None) -> Decimal:
        query = db.session.query(
            db.func.sum(db.func.ifnull(PerformanceRegistrationItem2.total_cost_price, 0))
        ).join(
            PerformanceRegistration,
            PerformanceRegistrationItem2.fk_performance_registration_id == PerformanceRegistration.id
        ).filter(
            PerformanceRegistrationItem2.item_code == item_code
        ).filter(
            PerformanceRegistrationItem2.warehouse_code == warehouse_code
        )
        if start_date and end_date:
            query = query.filter(
                PerformanceRegistration.target_date >= start_date
            ).filter(
                PerformanceRegistration.target_date <= end_date
            )
        elif end_date:
            query = query.filter(
                PerformanceRegistration.target_date < end_date
            )
        release_price = query.first()[0]
        release_price = Decimal('0') if not release_price else release_price
        return release_price


class LibProcessPerformanceRegistration(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + relativedelta(days=1)

        new_index = 1
        last_item = db.session.query(ProcessPerformanceRegistration.number)\
            .filter(ProcessPerformanceRegistration.created >= start)\
            .filter(ProcessPerformanceRegistration.created < end)\
            .order_by(ProcessPerformanceRegistration.created.desc())\
            .order_by(ProcessPerformanceRegistration.number.desc())\
            .first()

        if last_item:
            new_index = int(last_item.number[-3:]) + 1

        now = datetime.now()
        datestr = now.strftime('%Y%m%d')
        number = 'PRCPE-{datestr}-{count:03d}'.format(datestr=datestr, count=new_index)
        data['number'] = number

    @staticmethod
    def get_many_postprocessor(result=None, **kw):
        if result:
            from backend_model.table_base import BaseClient
            item_list = result['objects']
            for item in item_list:
                try:
                    if item['work_order_item']['client_company']:
                        client = db.session.query(
                            BaseClient.alias
                        ).filter(
                            BaseClient.name == item['work_order_item']['client_company']
                        ).first()
                        item['work_order_item']['client_alias'] = client.alias
                except:
                    pass