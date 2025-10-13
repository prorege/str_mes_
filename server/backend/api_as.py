print("module [backend.api_as] loaded")

import json
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from backend import app, manager
from backend import check_token
from backend_model.database import DBManager
from backend_model.table_as import *
from backend_lib.lib_as import *
from uuid import uuid4
import os
from flask import make_response
db = DBManager.db

manager.create_api(AsReceipt,
                   url_prefix='/api/mes/v1/as',
                   collection_name='receipt',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibAsReceipt.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })

manager.create_api(AsReceiptItem,   
                   url_prefix='/api/mes/v1/as',
                   collection_name='receipt-item',
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

manager.create_api(AsResult,
                   url_prefix='/api/mes/v1/as',
                   collection_name='result',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibAsResult.post_preprocessor],
                       'PATCH_SINGLE': [check_token, LibAsResult.patch_single_preprocessor],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token, LibAsResult.delete_single_preprocessor]
                   },
                   postprocessors={
                       'POST': [LibAsResult.post_postprocessor],
                   })

manager.create_api(AsResultItem,
                   url_prefix='/api/mes/v1/as',
                   collection_name='result-item',
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

manager.create_api(AsResultAttachment,
                   url_prefix='/api/mes/v1/as',
                   collection_name='result-attachment',
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

manager.create_api(AsResultExpense,
                   url_prefix='/api/mes/v1/as',
                   collection_name='result-expense',
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

@app.route('/api/server/v1/as-result-attachment/remove/<int:attachment_id>', methods=['POST'])
def as_result_attachment_remove(attachment_id):
    attachment = db.session.query(AsResultAttachment).filter(AsResultAttachment.id == attachment_id).first()
    file_path = os.path.join(app.config['UPLOAD_BASE_DIR'], attachment.file_path)
    try:
         os.remove(file_path)
    except IsADirectoryError:
        pass

    return make_response('success', 200)