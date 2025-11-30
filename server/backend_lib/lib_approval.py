# -*- coding: utf-8 -*-

from decimal import Decimal
from backend import app
from backend_model.database import DBManager
from backend_model.table_approval import *
from backend_lib.lib_common import LibCommon
from backend_lib.lib_setup import LibSetupBasicStock
import os
from flask import make_response, jsonify
from sqlalchemy import func
from datetime import datetime

db = DBManager.db

class LibApproval(object):
    @staticmethod
    def approval_preprocessor(data=None, **kw):
        LibCommon.get_item_number(data, 'approval_number', Approval, Approval.approval_number, '/approval/request')


    @staticmethod
    def get_many_postprocessor(result=None, **kw):
        approval_list = result['objects']
        approval_emp_ids = set()
        request_emp_ids = set()
        for approval in approval_list:
            if approval.get('approval_line_result'):
                for item in approval['approval_line_result']:
                    if item.get('fk_approval_emp_id'):
                        approval_emp_ids.add(item['fk_approval_emp_id'])
                    if item.get('fk_request_emp_id'):
                        request_emp_ids.add(item['fk_request_emp_id'])
        if approval_emp_ids:
            approval_employees = {emp.id: { 'id' : emp.id, 'emp_name' : emp.emp_name, 'emp_sign_path' : emp.emp_sign_path } for emp in 
                        db.session.query(BaseEmployee).filter(BaseEmployee.id.in_(approval_emp_ids)).all()}
        if request_emp_ids:
            request_employees = {emp.id: { 'id' : emp.id, 'emp_name' : emp.emp_name, 'emp_sign_path' : emp.emp_sign_path } for emp in 
                        db.session.query(BaseEmployee).filter(BaseEmployee.id.in_(request_emp_ids)).all()}
      
            for approval in approval_list:
                if approval.get('approval_line_result'):
                    for item in approval['approval_line_result']:
                        ap_emp_id = item.get('fk_approval_emp_id')
                        if ap_emp_id and ap_emp_id in approval_employees:
                            item['approval_employee'] = approval_employees[ap_emp_id]
                        req_emp_id = item.get('fk_request_emp_id')
                        if req_emp_id and req_emp_id in request_employees:
                            item['request_employee'] = request_employees[req_emp_id]

class LibApprovalDocument(object):
    @staticmethod
    def get_many_preprocessor(manager_value=None):
        if manager_value:
            document_list = db.session.query(ApprovalDocument.id, ApprovalDocument.max_line).all()
            for document_id, max_line in document_list:
                existing_orders_set = {
                    order.line_order for order in db.session.query(ApprovalLine.line_order).filter(
                        ApprovalLine.fk_document_id == document_id,
                        ApprovalLine.manager == manager_value
                    )
                }

                for line_order in range(1, max_line + 1):
                    if line_order not in existing_orders_set:
                        new_line = ApprovalLine(
                            fk_document_id=document_id,
                            manager=manager_value,
                            line_order=line_order
                        )
                        db.session.add(new_line)

            db.session.commit()

        

class LibApprovalAttachment(object):
    @staticmethod
    def delete_single_preprocessor(instance_id=None, **kw):
        if instance_id:
            attachment = db.session.query(ApprovalAttachment).filter(ApprovalAttachment.id == instance_id).first()
            if attachment:
                file_path = attachment.file_path
                if not file_path:
                    return
                try:
                    base_url = '/api/mes/v1/approval/approval-attachment/'
                    if file_path.startswith(base_url):
                        filename = file_path.replace(base_url, '', 1)
                    else:
                        filename = os.path.basename(file_path)

                    base_path = os.path.join(app.config['UPLOAD_BASE_DIR'], "approval-attachment")
                    abs_path = os.path.join(base_path, filename)

                    if os.path.exists(abs_path):
                        os.remove(abs_path)
                        print(f"파일이 삭제되었습니다: {abs_path}")
                    else:
                        print(f"파일을 찾을 수 없습니다: {abs_path}")
                except Exception as e:
                    print(f"파일을 삭제하는 중 오류 발생: {e}")

class LibApprovalLineResult(object):
    @staticmethod
    def get_many_postprocessor(result=None, **kw):
        approval_line_result_list = result['objects']
        for approval_line_result in approval_line_result_list:
            if 'fk_approval_id' in approval_line_result:
                approval_id = approval_line_result['fk_approval_id']
                approval_attachments = db.session.query(ApprovalAttachment).filter(ApprovalAttachment.fk_approval_id == approval_id).all()
                for approval_attachment in approval_attachments:
                    if 'approval_attachment' in approval_line_result:
                        approval_line_result['approval_attachment'].append({
                            'file_name': approval_attachment.file_name,
                            'file_path': approval_attachment.file_path,
                            'id': approval_attachment.id,
                            'fk_approval_id': approval_attachment.fk_approval_id
                        })
                    else:
                        approval_line_result['approval_attachment'] = [{
                            'file_name': approval_attachment.file_name,
                            'file_path': approval_attachment.file_path,
                            'id': approval_attachment.id,
                            'fk_approval_id': approval_attachment.fk_approval_id
                        }]

    @staticmethod
    def patch_single_postprocessor(result=None, **kw):
        if 'fk_approval_id' in result:
            approval_id = result['fk_approval_id']
            if approval_id:
                closing_yn = result['closing_yn']
              
                if closing_yn:
                    current_line_order = result['approval_line']['line_order']
                    current_line_type = result.get('line_type') or result.get('approval_line', {}).get('line_type')
                    current_approval = result['approval']
                    
                    if current_approval and current_approval['fk_document_id']:
                        document_id = current_approval['fk_document_id']
                        
                        if current_line_type is not None:
                            next_approval_line = db.session.query(ApprovalLine).filter(
                                ApprovalLine.fk_document_id == document_id,
                                ApprovalLine.fk_request_emp_id == current_approval['fk_request_emp_id'],
                                ApprovalLine.fk_approval_emp_id != None,
                                ApprovalLine.fk_approval_emp_id != '',
                                ApprovalLine.line_type == current_line_type,
                                ApprovalLine.line_order > current_line_order
                            ).order_by(ApprovalLine.line_order.asc()).first()
                        else:
                            next_approval_line = db.session.query(ApprovalLine).filter(
                                ApprovalLine.fk_document_id == document_id,
                                ApprovalLine.fk_request_emp_id == current_approval['fk_request_emp_id'],
                                ApprovalLine.fk_approval_emp_id != None,
                                ApprovalLine.fk_approval_emp_id != '',
                                ApprovalLine.line_type == None,
                                ApprovalLine.line_order > current_line_order
                            ).order_by(ApprovalLine.line_order.asc()).first()

                        if next_approval_line:
                            next_line_result = db.session.query(ApprovalLineResult).filter(
                                ApprovalLineResult.fk_approval_line_id == next_approval_line.id,
                                ApprovalLineResult.fk_approval_id == approval_id
                            ).first()
                            
                            if next_line_result:
                                current_line_result = db.session.query(ApprovalLineResult).filter(
                                    ApprovalLineResult.fk_approval_line_id == result['fk_approval_line_id'],
                                    ApprovalLineResult.fk_approval_id == approval_id
                                ).first()
                                
                                if current_line_result:
                                    current_line_result.active_yn = 0
                                next_line_result.active_yn = 1
                                db.session.commit()
                if are_all_closing_yn_true(approval_id):
                    approval = db.session.query(Approval).filter(Approval.id == approval_id).first()
                    if approval:
                        approval.closing_yn = True
                        approval.approval_result_date = datetime.now()
                        approval.approval_status = '결재완료'
                        db.session.commit()
                else:
                    approval = db.session.query(Approval).filter(Approval.id == approval_id).first()
                    if approval:
                        approval.closing_yn = False
                        approval.approval_result_date = None
                        approval.approval_status = '상신완료'
                        db.session.commit()
                       

def are_all_closing_yn_true(approval_id):
    total_count = db.session.query(func.count(ApprovalLineResult.id)).filter(ApprovalLineResult.fk_approval_id == approval_id).scalar()

    true_count = db.session.query(func.count(ApprovalLineResult.id)).filter(
        ApprovalLineResult.fk_approval_id == approval_id,
        ApprovalLineResult.closing_yn == True
    ).scalar()

    return total_count == true_count

