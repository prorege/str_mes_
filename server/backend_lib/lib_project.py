# -*- coding: utf-8 -*-

import os
from math import floor
from functools import reduce
from backend import app
from backend_model.table_project import *

db = DBManager.db


class LibProjectManagement(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'project_number', ProjectManagement, ProjectManagement.project_number, '/project/registration')
    @staticmethod
    def patch_single_preprocessor(instance_id=None, data=None, **kw):
        if 'business' in data and data['business'] is not None:
            db.session.query(
                ProjectBusiness
            ).filter(
                ProjectBusiness.fk_project_management_id == instance_id
            ).update({'fk_project_management_id' : None})
            data['business']['fk_project_management_id'] = instance_id
            db.session.commit()
        
    @staticmethod
    def delete_single_preprocessor(instance_id=None, **kw):
        projectDocument = db.session.query(ProjectDocument).filter(
            ProjectDocument.fk_project_management_id == instance_id)
        for item in projectDocument.all():
            file_path = os.path.join(app.config['UPLOAD_BASE_DIR'], item.file_path)
            try:
                os.remove(file_path)
            except IsADirectoryError:
                pass
        db.session.query(
            ProjectBusiness
        ).filter(
            ProjectBusiness.fk_project_management_id == instance_id
        ).update({'fk_project_management_id' : None})
        projectDocument.delete()
        db.session.commit()

    @staticmethod
    def post_postprocessors(result=None, **kw):
        if result['fk_business_id'] is not None:
            fk_business_id = result['fk_business_id']
            project_id = result['id']
            db.session.query(
                ProjectBusiness
            ).filter(
                ProjectBusiness.id == fk_business_id
            ).update({'fk_project_management_id' : project_id})
            db.session.commit()

    @staticmethod
    def update_non_invoice(project_management_id):
        project_management = db.session.query(
            ProjectManagement
        ).filter(
            ProjectManagement.id == project_management_id
        ).first()
        if project_management:
            from backend_model.table_shipment import ShipmentSalesStatementItem
            invoice_price = db.session.query(
                db.func.sum(ShipmentSalesStatementItem.supply_price)
            ).filter(
                ShipmentSalesStatementItem.fk_project_management_id == project_management_id
            ).first()[0]
            if invoice_price is None:
                invoice_price = 0
            project_management.non_invoice = project_management.company_amount - invoice_price
            db.session.commit()

class LibProjectSchedule(object):
    @staticmethod
    def update_project_progress(instance_id=None, data=None, **kw):
        if instance_id is None:
            project_id = data['fk_project_management_id']
            project_schedule = ProjectSchedule.query.filter(
                ProjectSchedule.fk_project_management_id == project_id).all()
            sum_value = reduce(lambda acc, cur: acc + cur.progress_percent, project_schedule, 0)
            avg = floor(sum_value / (len(project_schedule) + 1))

            project = db.session.query(ProjectManagement).filter(ProjectManagement.id == project_id).first()
            project.total_progress = avg
            db.session.commit()

        else:
            schedule = ProjectSchedule.query.filter(ProjectSchedule.id == instance_id).first()
            project_id = schedule.fk_project_management_id

            mod_value = 0
            mod_count = 0
            if data is None:
                mod_value = schedule.progress_percent * -1
                mod_count = -1
            elif 'progress_percent' in data:
                mod_value = data['progress_percent'] - schedule.progress_percent

            project_schedule = ProjectSchedule.query.filter(ProjectSchedule.fk_project_management_id == project_id).all()
            sum_value = reduce(lambda acc, cur: acc + cur.progress_percent, project_schedule, 0)
            sum_value += mod_value
            avg = floor(sum_value / (len(project_schedule) + mod_count))

            project = db.session.query(ProjectManagement).filter(ProjectManagement.id == project_id).first()
            project.total_progress = avg
            db.session.commit()


class LibProjectItem(object):
    @staticmethod
    def update_not_ordered(project_item_id):
        from backend_model.table_shipment import ShipmentOrderItem
        order_quantity = db.session.query(
            db.func.sum(ShipmentOrderItem.order_quantity)
        ).filter(
            ShipmentOrderItem.fk_project_item_id == project_item_id
        ).first()[0]
        project_item = db.session.query(
            ProjectItem
        ).filter(
            ProjectItem.id == project_item_id
        ).first()
        not_ordered = project_item.quantity - order_quantity
        project_item.not_ordered = not_ordered
        db.session.commit()

class LibProjectBusiness(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'business_number', ProjectBusiness, ProjectBusiness.business_number, '/project/business')

    @staticmethod
    def patch_single_preprocessor(instance_id=None, data=None, **kw):
        if 'project' in data and data['project'] is not None:
            db.session.query(
                ProjectManagement
            ).filter(
                ProjectManagement.fk_business_id == instance_id
            ).update({'fk_business_id' : None})
            data['project']['fk_business_id'] = instance_id
            db.session.commit()

    @staticmethod
    def delete_single_preprocessors(instance_id=None, **kw):
        db.session.query(
            ProjectManagement
        ).filter(
            ProjectManagement.fk_business_id == instance_id
        ).update({'fk_business_id' : None})
        db.session.commit()

    @staticmethod
    def post_postprocessors(result=None, **kw):
        if result['fk_project_management_id'] is not None:
            fk_project_management_id = result['fk_project_management_id']
            business_id = result['id']
            db.session.query(
                ProjectManagement
            ).filter(
                ProjectManagement.id == fk_project_management_id
            ).update({'fk_business_id' : business_id})
            db.session.commit()
      
class LibProjectExcutionPlan(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'excution_plan_number', ProjectExcutionPlan, ProjectExcutionPlan.excution_plan_number, '/project/excution-plan')

    @staticmethod
    def patch_single_preprocessor(instance_id=None, data=None, **kw):
        if 'project_management' in data and data['project_management'] is not None:
            db.session.query(
                ProjectManagement
            ).filter(
                ProjectManagement.fk_excution_plan_id == instance_id
            ).update({'fk_excution_plan_id' : None})
            data['project_management']['fk_excution_plan_id'] = instance_id
            db.session.commit()
            
    @staticmethod
    def delete_single_preprocessor(instance_id=None, **kw):
        db.session.query(
            ProjectManagement
        ).filter(
            ProjectManagement.fk_excution_plan_id == instance_id
        ).update({'fk_excution_plan_id' : None})
        
        db.session.commit()

    @staticmethod
    def post_postprocessors(result=None, **kw):
        if result['fk_project_management_id'] is not None:
            fk_project_management_id = result['fk_project_management_id']
            excution_plan_id = result['id']
            db.session.query(
                ProjectManagement
            ).filter(
                ProjectManagement.id == fk_project_management_id
            ).update({'fk_excution_plan_id' : excution_plan_id})
            db.session.commit()

class LibProjectExcutionPlanItem(object):
    @staticmethod
    def update_not_excution_plan_quantity_quantity(excution_plan_item_id):
        from backend_model.table_purchase import PurchaseOrderItem
        try:
            excution_plan_item = db.session.query(
                ProjectExcutionPlanItem
            ).filter(
                ProjectExcutionPlanItem.id == excution_plan_item_id
            ).first()
            if excution_plan_item is None:
                return
            
            total_order_quantity = db.session.query(
                db.func.sum(PurchaseOrderItem.order_quantity)
            ).filter(
                PurchaseOrderItem.fk_excution_plan_item_id == excution_plan_item_id
            ).first()[0]
            if total_order_quantity is None:
                total_order_quantity = 0
            
            not_excution_plan_quantity = excution_plan_item.excution_plan_quantity - total_order_quantity
            if not_excution_plan_quantity > 0 :
                excution_plan_item.not_excution_plan_quantity = not_excution_plan_quantity
            else:
                excution_plan_item.not_excution_plan_quantity = 0
                excution_plan_item.closing_yn = True
            db.session.commit()
        except:
            pass
        
# 견적서 코드
class LibProjectEstimateDocument(object):
    @staticmethod
    def delete_single_preprocessor(instance_id=None, **kw):
        estimate_item = db.session.query(
            ProjectEstimateDocument
        ).filter(
            ProjectEstimateDocument.id == instance_id
        ).first()
        if estimate_item is None:
            return
        if estimate_item.file_path:
            file_path = os.path.join(app.config['UPLOAD_BASE_DIR'], estimate_item.file_path)
            try:
                os.remove(file_path)
            except IsADirectoryError:
                pass
class LibProjectExcutionPlanSubcontract(object):
    @staticmethod
    def update_closing(excution_plan_subcontract_id):
        from backend_model.table_purchase import PurchaseOrderItem
        try:
            excution_plan_subcontract = db.session.query(
                ProjectExcutionPlanSubcontract
            ).filter(
                ProjectExcutionPlanSubcontract.id == excution_plan_subcontract_id
            ).first()
            if excution_plan_subcontract is None:
                return
            purchase_order_item = db.session.query(
                PurchaseOrderItem
            ).filter(
                PurchaseOrderItem.fk_excution_plan_subcontract_id == excution_plan_subcontract_id
            ).first()
            if purchase_order_item is None:
                return
            excution_plan_subcontract.closing_yn = True
            db.session.commit()
        except:
            pass


    @staticmethod
    def patch_single_preprocessor(instance_id=None, data=None, **kw):
        if not data:
            pass

        item = db.session.query(ProjectExcutionPlanSubcontract).filter(
            ProjectExcutionPlanSubcontract.id == instance_id).first()
        
        if item is None:
            pass

        # 견적서 수정 시 기존 파일 삭제
        if 'estimate_document' in data and data['estimate_document'] != item.estimate_document:
            if item.estimate_document_path:
                file_path = os.path.join(app.config['UPLOAD_BASE_DIR'], item.estimate_document_path)
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"[견적서 삭제 실패] {file_path}: {e}")

        # 계약서 수정 시 기존 파일 삭제
        if 'contract_document' in data and data['contract_document'] != item.contract_document:
            if item.contract_document_path:
                file_path = os.path.join(app.config['UPLOAD_BASE_DIR'], item.contract_document_path)
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"[계약서 삭제 실패] {file_path}: {e}")
                



    @staticmethod
    def delete_single_preprocessor(instance_id=None, **kw):
        item = db.session.query(ProjectExcutionPlanSubcontract).filter(
            ProjectExcutionPlanSubcontract.id == instance_id).first()
        if item is None:
            return

        # 견적서 파일 삭제
        if item.estimate_document_path:
            file_path = os.path.join(app.config['UPLOAD_BASE_DIR'], item.estimate_document_path)
            try:
                os.remove(file_path)
            except Exception:
                pass
        if item.contract_document_path:
            file_path = os.path.join(app.config['UPLOAD_BASE_DIR'], item.contract_document_path)
            try:
                os.remove(file_path)
            except Exception:
                pass
#여기까지

class LibProjectBusinessQuote(object):
    @staticmethod
    def delete_single_preprocessor(instance_id=None, **kw):
        quote_item = db.session.query(
            ProjectBusinessQuote
        ).filter(
            ProjectBusinessQuote.id == instance_id
        ).first()
        if quote_item is None:
            return
        if quote_item.file_path:
            file_path = os.path.join(app.config['UPLOAD_BASE_DIR'], quote_item.file_path)
            try:
                os.remove(file_path)
            except IsADirectoryError:
                pass

class LibProjectBusinessBasic(object):
    @staticmethod
    def delete_single_preprocessor(instance_id=None, **kw):
        basic_item = db.session.query(
            ProjectBusinessBasic
        ).filter(
            ProjectBusinessBasic.id == instance_id
        ).first()
        if basic_item is None:
            return
        if basic_item.file_path:
            file_path = os.path.join(app.config['UPLOAD_BASE_DIR'], basic_item.file_path)
            try:
                os.remove(file_path)
            except IsADirectoryError:
                pass