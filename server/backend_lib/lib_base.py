# -*- coding: utf-8 -*-

import os
from backend import app
from backend_model.table_base import *

db = DBManager.db


class LibBaseItem(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_util import LibUtil
        if data is not None and 'item_img' in data and data['item_img'] is not None:
            BASE_DIR = app.config['UPLOAD_BASE_DIR']
            abs_path = os.path.join(BASE_DIR, "item-images")
            data['item_img'] = LibUtil.base64_to_file(data['item_img'], abs_path)

    @staticmethod
    def patch_preprocessor(instance_id=id, data=None, **kw):
        from backend_lib.lib_util import LibUtil
        if data is not None and 'item_img' in data and data['item_img'] is not None and data['item_img'].startswith('data:'):
            BASE_DIR = app.config['UPLOAD_BASE_DIR']
            abs_path = os.path.join(BASE_DIR, "item-images")
            data['item_img'] = LibUtil.base64_to_file(data['item_img'], abs_path)

    @staticmethod
    def delete_single_preprocessor(instance_id=None, **kw):
        from backend_lib.lib_util import LibUtil
        from backend_model.table_shipment import (ShipmentQuoteItem, ShipmentOrderItem, ShipmentReleaseItem, ShipmentReleaseReturnItem, ShipmentSalesStatementItem)
        from backend_model.table_purchase import (PurchaseOrderPlanItem, PurchaseOrderItem, PurchasePreReceivingItem, PurchaseReceivingItem, PurchaseReceivingReturnItem)
        from backend_model.table_production import (ProductionPlanItem1, WorkOrderItem1, WorkOrderItem2, MeasureRequirementItem1, MeasureRequirementItem2, PerformanceRegistrationItem1, PerformanceRegistrationItem2, ProcessPerformanceRegistration, ProcessMaterialConsumption)
        from backend_model.table_stock import (StockEtcItem, StockMoveRequestItem, StockMoveReleaseItem, StockCorrectionItem)
        from backend_model.table_export import (ExportSalesOrderItem, ExportCommInvoiceItem)
        from backend_model.table_import import (ImportPurchaseOrderItem, ImportShipmentItem, ImportClearanceItem, ImportClearanceCostItem)
        from backend_model.table_project import (ProjectItem, ProjectExcutionPlanItem)
        from backend_model.table_qr import (QRManagement, LOTManagement)
        from backend_model.table_quality import (QualityManagement)
        
        tables = [
            ShipmentQuoteItem, ShipmentOrderItem, ShipmentReleaseItem, ShipmentReleaseReturnItem, ShipmentSalesStatementItem,
            PurchaseOrderPlanItem, PurchaseOrderItem, PurchasePreReceivingItem, PurchaseReceivingItem, PurchaseReceivingReturnItem,
            ProductionPlanItem1, WorkOrderItem1, WorkOrderItem2, MeasureRequirementItem1, MeasureRequirementItem2, PerformanceRegistrationItem1, PerformanceRegistrationItem2, ProcessPerformanceRegistration, ProcessMaterialConsumption,
            StockEtcItem, StockMoveRequestItem, StockMoveReleaseItem, StockCorrectionItem,
            ExportSalesOrderItem, ExportCommInvoiceItem,
            ImportPurchaseOrderItem, ImportShipmentItem, ImportClearanceItem, ImportClearanceCostItem,
            ProjectItem, ProjectExcutionPlanItem,
            QRManagement, LOTManagement,
            QualityManagement
            ]
   
        exist = []
        for table in tables:
            if LibUtil.check_item_code_exist_connected_data(table, instance_id):
                exist.append(table.__table__.comment)
        if exist:
            from flask_restless import ProcessingException
            result_string = "<br/>".join(exist)
            raise ProcessingException(description=result_string, code=605)
    
    @staticmethod
    def get_many_postprocessor(result=None, search_params=None, **kw):
        if result:
            item_list = result['objects']
            for item in item_list:
                try:
                    client = LibBaseClient.get_main_client_company_by_item(item['item_code'])
                    if client:
                        item['client_company'] = client.name
                except:
                    pass

    @staticmethod
    def post_postprocessor(result=None, **kw):
        from backend_model.table_base import BaseBOM
        add_item = BaseBOM()
        add_item.id = result['id']
        add_item.item_id = result['id']
        add_item.bom_depth = 0
        add_item.fk_company_id = result['fk_company_id']
        db.session.add(add_item)
        db.session.commit()
        
class LibBaseBom(object):
    @staticmethod
    def get_single_postprocessor(result=None, search_params=None, **kw):
        if result:
            try:
                client_item = db.session.query(
                    BaseClientItem
                ).filter(
                    BaseClientItem.item_code == result['item']['item_code']
                ).first()
                if client_item:
                    result['item']['client_company'] = client_item.client.name
            except:
                pass

    @staticmethod
    def get_many_postprocessor(result=None, search_params=None, **kw):
        if result:
            bom_list = result['objects']
            for bom in bom_list:
                try:
                    client_item = db.session.query(
                        BaseClientItem
                    ).filter(
                        BaseClientItem.item_code == bom['item']['item_code']
                    ).first()
                    if client_item:
                        bom['item']['client_company'] = client_item.client.name
                except:
                    pass

    @staticmethod
    def find_bom(find_items):
        leaf = {}
        for item in find_items:
            bom = db.session.query(BaseBOM).filter(BaseBOM.item_id == item['id']).first()
            if bom:
                LibBaseBom.find_leaf_bom(bom.id, item['count'], leaf)
                if bom.id in leaf:
                    del leaf[bom.id]
        return leaf

    @staticmethod
    def find_leaf_bom(parent_id, multiplicand, leaf):
        linked_bom = db.session.query(BaseBOMLink).filter(BaseBOMLink.parent_id == parent_id).all()
        if len(linked_bom) == 0:
            if parent_id in leaf:
                leaf[parent_id] += multiplicand
            else:
                leaf[parent_id] = multiplicand
            return
        for bom in linked_bom:
            if bom.parent_bom.bom_depth == 1:  # 반제품 사용
                if bom.child_id in leaf:
                    leaf[bom.child_id] += (multiplicand * bom.requirement)
                else:
                    leaf[bom.child_id] = (multiplicand * bom.requirement)
            else:
                LibBaseBom.find_leaf_bom(bom.child_id, multiplicand * bom.requirement, leaf)


class LibBaseBomLink(object):
    @staticmethod
    def get_client_company(bom_id):
        try:
            result = db.session.query(BaseClient)\
                .join(BaseClientItem, BaseClientItem.client_id == BaseClient.id)\
                .join(BaseItem, BaseItem.item_code == BaseClientItem.item_code)\
                .join(BaseBOM, BaseBOM.item_id == BaseItem.id)\
                .filter(BaseBOM.id == bom_id)\
                .filter(BaseClientItem.main_supplier == True)\
                .first()

            return result.name if result else ''
        except:
            return None

    @staticmethod
    def get_single_postprocessor(result=None, search_params=None, **kw):
        if result:
            result['client_company'] = LibBaseBomLink.get_client_company(result['child_id'])

    @staticmethod
    def get_many_postprocessor(result=None, search_params=None, **kw):
        if result:
            for item in result['objects']:
                item['client_company'] = LibBaseBomLink.get_client_company(item['child_id'])


class LibBaseCode(object):
    @staticmethod
    def get_first_code_name(code_name):
        parent_base_code = db.session.query(
            BaseCode
        ).filter(
            BaseCode.code_name == code_name
        ).first()
        if parent_base_code:
            child_base_code = db.session.query(
                BaseCode
            ).filter(
                BaseCode.parent_code_id == parent_base_code.id
            ).first()
            if child_base_code:
                return child_base_code.code_name
        return ''

    @staticmethod
    def get_all_code_name(code_name):
        response = []
        parent_base_code = db.session.query(
            BaseCode
        ).filter(
            BaseCode.code_name == code_name
        ).first()
        if parent_base_code:
            child_base_codes = db.session.query(
                BaseCode
            ).filter(
                BaseCode.parent_code_id == parent_base_code.id
            ).all()
            for child_base_code in child_base_codes:
                response.append(child_base_code.code_name)
        return response


class LibBaseDepartment(object):
    @staticmethod
    def delete_single_preprocessor(instance_id=None, **kw):
        from backend_lib.lib_util import LibUtil
        LibUtil.check_exist_connected_data(BaseEmployee, BaseEmployee.fk_department_id, instance_id)


class LibBaseClient(object):
    @staticmethod
    def get_first_client_company_by_item(item_code: str):
        client = None
        client_item = db.session.query(
            BaseClientItem
        ).filter(
            BaseClientItem.item_code == item_code
        ).first()
        if client_item:
            client = client_item.client
        return client

    @staticmethod
    def get_main_client_company_by_item(item_code: str) -> BaseClient:
        client = None
        client_item = db.session.query(
            BaseClientItem
        ).filter(
            BaseClientItem.item_code == item_code
        ).filter(
            BaseClientItem.main_supplier == True
        ).first()
        if client_item:
            client = client_item.client
        return client
    
    @staticmethod
    def patch_single_preprocessor(instance_id=None, data=None, **kw):
        if 'name' in data:
            client = BaseClient.query.filter_by(id=instance_id).first()
            if client and client.name != data['name']:
                db.session.execute(f'''CALL proc_update_global_client_company('{client.name}', '{data['name']}')''')


class LibBaseWarehouse(object):
    @staticmethod
    def get_warehouse_by_name(warehouse_name: str):
        warehouse = db.session.query(
            BaseWarehouse
        ).filter(
            BaseWarehouse.wh_name == warehouse_name
        ).first()
        return warehouse


