print("module [backend.api_approval] loaded")

import json
from backend import app, manager
from backend import check_token
from backend_model.database import DBManager
from backend_model.table_approval import *
from flask import request, make_response, Response, jsonify
from flask_restful import reqparse
from datetime import datetime, timedelta

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
