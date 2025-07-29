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


class LibApprovalDocument(object):
    @staticmethod
    def get_many_preprocessor(emp_id=None):
        if emp_id:
            document_list = db.session.query(ApprovalDocument.id, ApprovalDocument.max_line).all()
            for document_id, max_line in document_list:
                existing_orders_set = {
                    order.line_order for order in db.session.query(ApprovalLine.line_order).filter(
                        ApprovalLine.fk_document_id == document_id,
                        ApprovalLine.fk_submitter_id == emp_id
                    )
                }

                for line_order in range(1, max_line + 1):
                    if line_order not in existing_orders_set:
                        new_line = ApprovalLine(
                            fk_document_id=document_id,
                            fk_submitter_id=emp_id,
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
            print("approval_line_result : ", approval_line_result)
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

