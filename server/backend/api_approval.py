print("module [backend.api_approval] loaded")

import json
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from backend import app, manager
from backend import check_token
from backend_model.database import DBManager
from backend_model.table_approval import *
from backend_lib.lib_approval import *
from flask import request, make_response, Response, jsonify, send_file
from flask_restful import reqparse
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4
import os

db = DBManager.db

manager.create_api(ApprovalManagement,
                   url_prefix='/api/mes/v1/approval',
                   collection_name='management',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })

manager.create_api(Approval,
                   url_prefix='/api/mes/v1/approval',
                   collection_name='approval',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibApproval.approval_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })

manager.create_api(ApprovalLineResult,
                   url_prefix='/api/mes/v1/approval',
                   collection_name='approval-line-result',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   }, 
                   postprocessors={
                       'GET_MANY': [LibApprovalLineResult.get_many_postprocessor],
                       'PATCH_SINGLE': [LibApprovalLineResult.patch_single_postprocessor]
                   })

manager.create_api(ApprovalLine,
                   url_prefix='/api/mes/v1/approval',
                   collection_name='approval-line',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })

manager.create_api(ApprovalDocument,
                   url_prefix='/api/mes/v1/approval',
                   collection_name='approval-document',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })

manager.create_api(ApprovalAttachment,
                   url_prefix='/api/mes/v1/approval',
                   collection_name='approval-attachment',
                   methods=['DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,  
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token, LibApprovalAttachment.delete_single_preprocessor]
                   })   

@app.route("/api/mes/v1/approval/document-status", methods=["GET"])
def get_documents():
    try:
        results_per_page = request.args.get('results_per_page', default=10, type=int)
        page = request.args.get('page', default=1, type=int)
        q = request.args.get('q', default='{}', type=str)

        search_params = json.loads(q)
        
        if search_params['filters'] is None or len(search_params['filters']) == 0:
            return make_response('invalid parameter', 400)
        manager = search_params['filters'][0]['val']

        
        documents = db.session.query(ApprovalDocument).all()
     
        result = []  
        for document in documents:
            approval_lines = db.session.query(ApprovalLine).filter(
                        ApprovalLine.fk_document_id == document.id,
                        ApprovalLine.manager == manager
                    ).all()
            line_result = {}
            for line in approval_lines:
                line_result[str(line.line_order)] = line.approval_manager
                
            result.append({
                'id': document.id,
                'document_number': document.document_number,
                'document_name': document.document_name,
                'document_path': document.document_path,
                'max_line': document.max_line,
                'register': document.register,
                'register_date': document.register_date,
                'approval_line': [
                    {
                        'id': line.id,
                        'created': line.created,
                        'manager': line.manager,
                        'line_order': line.line_order,
                        'approval_manager': line.approval_manager,
                        'fk_document_id': line.fk_document_id
                    } for line in approval_lines
                ],
                **line_result 
            })
        
        total_results = len(result)
    
        response = dict(
            page=page,
            objects=result,
            total_pages=(total_results + results_per_page - 1) // results_per_page,
            num_results=total_results
        )

        return jsonify(response)
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/mes/v1/approval/document-status/<int:instance_id>", methods=['PATCH'])
def update_document_status(instance_id):
    try:
        data = request.json
        manager = data.pop('manager', None)
        for key, value in data.items():
            db.session.query(ApprovalLine).filter(
                ApprovalLine.fk_document_id == instance_id,
                ApprovalLine.manager == manager,
                ApprovalLine.line_order == key
            ).update({ApprovalLine.approval_manager: value})
        db.session.commit()
        return jsonify({"success": True})
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500


# @app.route("/api/mes/v1/approval/approval", methods=["POST"])
# def create_document():
#     try:
#         data = request.json
#         print("data : ", data)
#         approval_attachment = data.pop('approval_attachment', None)
#         approval_document = data.pop('approval_document', None)
#         if data is not None:
#             approval_data = {'fk_company_id': data['fk_company_id']}
#             LibCommon.get_item_number(approval_data, 'approval_number', Approval, Approval.approval_number, '/approval/request')
#             new_approval = Approval() 
#             new_approval.approval_number = approval_data['approval_number']
#             new_approval.approval_date = data['approval_date']
#             new_approval.approval_status = data['approval_status']
#             new_approval.register = data['register']
#             new_approval.title = data['title']
#             new_approval.content = data['content']
#             new_approval.etc = data['etc']
#             new_approval.fk_document_id = data['fk_document_id']
#             new_approval.fk_company_id = data['fk_company_id']
#             new_approval.fk_business_id = data['fk_business_id']
        
#             db.session.add(new_approval)
#             db.session.commit()
#             approval_attachments = []
#             if approval_attachment is not None:
#                 for attachment in approval_attachment:
#                     new_attachment = ApprovalAttachment()
#                     new_attachment.file_name = attachment['file_name']
#                     new_attachment.file_path = attachment['file_path']
#                     new_attachment.fk_approval_id = new_approval.id
#                     db.session.add(new_attachment)
#                     db.session.commit()
#                     approval_attachments.append(
#                         {
#                             'id': new_attachment.id,
#                             'created': new_attachment.created,
#                             'file_name': new_attachment.file_name,
#                             'file_path': new_attachment.file_path,
#                             'fk_approval_id': new_attachment.fk_approval_id
#                         }
#                     )
#             line_results = []
#             if approval_document is not None:
#                 approval_lines = db.session.query(ApprovalLine).filter(
#                     ApprovalLine.fk_document_id == approval_document['id'],
#                     ApprovalLine.manager == data['register'],
#                      and_(
#                         ApprovalLine.approval_manager.isnot(None),
#                         ApprovalLine.approval_manager != ''
#                     )
#                 ).all()
#                 for line in approval_lines:
#                     new_line_result = ApprovalLineResult()
#                     new_line_result.approval_manager = line.approval_manager
#                     new_line_result.approval_result = '대기중'
#                     new_line_result.fk_approval_line_id = line.id
#                     new_line_result.fk_approval_id = new_approval.id
#                     db.session.add(new_line_result)
#                     db.session.commit()
#                     line_results.append(
#                         {
#                             'id': new_line_result.id,
#                             'created': new_line_result.created,
#                             'approval_manager': new_line_result.approval_manager,
#                             'approval_result': new_line_result.approval_result,
#                             'approval_date': new_line_result.approval_date,
#                             'closing_yn': new_line_result.closing_yn,
#                             'fk_approval_line_id': new_line_result.fk_approval_line_id,
#                             'fk_approval_id': new_line_result.fk_approval_id

#                         }
#                     )
#             approval_data = {
#                 "id": new_approval.id,
#                 "approval_number": new_approval.approval_number,
#                 "approval_date": new_approval.approval_date,
#                 "register": new_approval.register,
#                 "etc": new_approval.etc,
#                 "fk_document_id": new_approval.fk_document_id,
#                 "fk_company_id": new_approval.fk_company_id,
#                 "approval_attachment": approval_attachments,
#                 "approval_line_result": line_results
#             }

#             return jsonify({"success": True, "data": approval_data})
#         return jsonify({"success": False, "message": "Invalid data"}), 400
#     except SQLAlchemyError as e:
#         return jsonify({"error": str(e)}), 500



# @app.route("/api/mes/v1/approval/approval/<int:instance_id>", methods=["PATCH"])
# def update_document(instance_id):
#     try:
#         data = request.json
#         approval_attachment = data.pop('approval_attachment', None)
#         approval_document = data.pop('approval_document', None)
#         if 'approval_line_result' in data:
#             del data['approval_line_result']
#         if data is not None:
#             db.session.query(Approval).filter(Approval.id == instance_id).update(data)
#             db.session.commit()
#             approval_attachments = []
#             if approval_attachment is not None:
#                 for attachment in approval_attachment:
#                     if 'id' not in attachment:
                        
#                         new_attachment = ApprovalAttachment()
#                         new_attachment.file_name = attachment['file_name']
#                         new_attachment.file_path = attachment['file_path']
#                         new_attachment.fk_approval_id = data['id']
#                         db.session.add(new_attachment)
#                         db.session.commit()
#                         approval_attachments.append(
#                             {
#                                 'id': new_attachment.id,
#                                 'created': new_attachment.created,
#                                 'file_name': new_attachment.file_name,
#                                 'file_path': new_attachment.file_path,
#                                 'fk_approval_id': new_attachment.fk_approval_id
#                             }
#                         )
#             new_approval = db.session.query(Approval).filter(Approval.id == instance_id).first()
#             approval_data = {
#                 "id": new_approval.id,
#                 "approval_date": new_approval.approval_date,
#                 "approval_status": new_approval.approval_status,
#                 "approval_reason": new_approval.approval_reason,
#                 "register": new_approval.register,
#                 "etc": new_approval.etc,
#                 "fk_document_id": new_approval.fk_document_id,
#                 "fk_company_id": new_approval.fk_company_id,
#             }
#             if approval_attachments:
#                 approval_data['approval_attachment'] = approval_attachments

#         return jsonify({"success": True, "data": approval_data})
#     except SQLAlchemyError as e:
#         return jsonify({"error": str(e)}), 500


@app.route('/api/mes/v1/approval/approval-attachment/upload', methods=['POST'])
def upload_approval_attachment():
    try:
        f = request.files['file']
        if f is None:
            return make_response(jsonify({"error": "파일이 없습니다."}), 400)
        
        file_root, file_ext = os.path.splitext(f.filename)
        filename = f'{file_root}__{str(uuid4())[:8]}{file_ext}'
        base_path = os.path.join(app.config['UPLOAD_BASE_DIR'], "approval-attachment")
        abs_path = os.path.join(base_path, filename)

        if not os.path.exists(base_path):
            os.makedirs(base_path)

        f.save(abs_path)
        return make_response(filename, 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "파일을 업로드하는 중 오류 발생."}), 500)
 