# -*- coding: utf-8 -*-
print("module [backend.api_setup] loaded")

from flask_restful import reqparse
from backend import check_token, check_permission
from backend_model.table_setup import *
from backend_model.table_common import *
from backend_lib.lib_setup import *
from backend import app, manager
from backend.api_common import validate_token
from flask import request, make_response, Response, jsonify
from urllib.parse import quote
from backend_lib.lib_excel import sample_excel, import_excel, ImportExcelException
import base64

db = DBManager.db
# REST API(s) available :
#  - /api/v1/login
#  - /api/v1/logout


@app.route('/api/mes/v1/excel/setup/basic_stock', methods=['GET'])
def setup_basic_stock_excel_sample():
    io = sample_excel(SetupBasicStock)
    content = io.getvalue()
    encoded = quote('기초재고입력양식')

    return Response(
        content,
        mimetype='application/octet-stream',
        headers={'Content-Disposition': 'attachment;filename={}.xlsx'.format(encoded)})


@app.route('/api/mes/v1/excel/setup/basic_stock', methods=['POST'])
def setup_basic_stock_excel_import():
    token = request.headers.get('token')
    if token is None:
        return make_response('Not Authorized', 410)

    user = validate_token(token)
    exc = check_permission(user, method='EXCEL')
    if exc is not None:
        return make_response(exc.description, exc.code)

    f = request.files['file']
    if f is None:
        return make_response('require parameter is missing', 400)

    filepath, ext = f.filename.rsplit('.', 1)
    if ext not in ['xlsx']:
        return make_response('invalid file extension', 400)

    f.seek(0)
    # 모든 행 공통 데이터
    common_values = dict(fk_company_id=user.fk_company_id)

    try:
        import_excel(table=SetupBasicStock, common_values=common_values, file=f)
        return make_response('success', 200)
    except ImportExcelException as e:
        print(e)
        result = '데이터를 불러오는 중 에러가 발생하였습니다'
        if e.message is not None:
            result = e.message

        return make_response(result, 400)


manager.create_api(SetupBasicStock,
                   url_prefix='/api/mes/v1/setup',
                   collection_name='basic_stock',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   },
                   postprocessors={
                       'GET_MANY': [LibSetupBasicStock.get_many_postprocessor]
                   })


manager.create_api(SetupBasicBalance,
                   url_prefix='/api/mes/v1/setup',
                   collection_name='basic_balance',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(SetupMenu,
                   url_prefix='/api/mes/v1/setup',
                   collection_name='menu',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   results_per_page=0,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(SetupGroup,
                   url_prefix='/api/mes/v1/setup',
                   collection_name='group',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token, LibSetupGroup.delete_single_preprocessor]
                   },
                   postprocessors={
                       'POST': [LibSetupGroup.post_postprocessor]
                   })


manager.create_api(SetupGroupAuth,
                   url_prefix='/api/mes/v1/setup',
                   collection_name='group_auth',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   results_per_page=0,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token, LibSetupGroupAuth.get_many_preprocessor],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(SetupCodeChangeHistory,
                   url_prefix='/api/mes/v1/setup',
                   collection_name='code_change_history',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(SetupControl,
                   url_prefix='/api/mes/v1/setup',
                   collection_name='control',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(SetupProduceCost,
                   url_prefix='/api/mes/v1/setup',
                   collection_name='produce_cost',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(SetupSgaExpense,
                   url_prefix='/api/mes/v1/setup',
                   collection_name='sga_expense',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })

@app.route('/api/server/v1/logo-upload/<int:company_id>', methods=['POST'])
def logo_upload(company_id):
    f = request.files['files[]']
    mimetype = f.content_type
    if "image" not in mimetype:
        return make_response('fail', 101)

    f.seek(0)
    data = f.read()
    base64_data = base64.b64encode(data).decode('ascii')
    db.session.query(Companies).filter(Companies.id == company_id).update({'logo': base64_data})
    db.session.commit()
    return make_response('success', 200)


@app.route("/api/mes/v1/setup/calcstock", methods=["POST"])  # 현재고 재계산
def setup_calculate_stock():
    # 기초재고 리스트를 뽑는다
    basic_stock_list = db.session.query(SetupBasicStock).all()
    for basic_stock in basic_stock_list:
        basic_stock_quantity = 0 if not basic_stock.basic_stock else basic_stock.basic_stock

        # 현재고 계산 및 업데이트
        basic_stock.current_stock = LibSetupBasicStock.calculate_current_stock(basic_stock.item_code, basic_stock.wh_code, basic_stock_quantity)
  
        # 가용재고 계산 및 업데이트
        basic_stock.available_stock = LibSetupBasicStock.calculate_available_stock(basic_stock.item_code, basic_stock.wh_code, basic_stock.current_stock)
        db.session.commit()
    return make_response(jsonify('success'), 200)


@app.route("/api/mes/v1/setup/update/item/stock", methods=["POST"])
def setup_update_item_stock():
    parser = reqparse.RequestParser()
    parser.add_argument("item_code", type=str, location="json")
    parser.add_argument("warehouse_code", type=str, location="json")
    args = parser.parse_args()

    LibSetupBasicStock.update_stock_by_item_code(item_code=args['item_code'], warehouse_code=args['warehouse_code'])
    basic_stock = LibSetupBasicStock.get_basic_stock(item_code=args['item_code'], warehouse_code=args['warehouse_code'])

    response = {
        'current_stock': basic_stock.current_stock,
        'available_stock': basic_stock.available_stock
    }
    return make_response(jsonify(response), 200)


@app.route("/api/mes/v1/setup/store-status", methods=["POST"])
def setup_store_status_stock():
    """
    모니터링 - 재고현황
    :return:
    """
    parser = reqparse.RequestParser()
    parser.add_argument("warehouse", type=str, location="json")
    parser.add_argument("asset_type", type=str, location="json")
    args = parser.parse_args()

    result = []
    if args['warehouse'] == '전체':
        basic_stocks = db.session.query(
            SetupBasicStock
        ).all()
    else:
        basic_stocks = db.session.query(
            SetupBasicStock
        ).filter(
            SetupBasicStock.wh_code == args['warehouse']
        ).all()
    for bs in basic_stocks:
        if not bs.item:
            continue
        if bs.available_stock - bs.item.safety_stock < 0:
            item_add = False
            if args['asset_type'] == '전체':
                item_add = True
            else:
                if args['asset_type'] == bs.item.asset_type:
                    item_add = True
            if item_add:
                result.append({
                    'id': bs.id,
                    'created': bs.created,
                    'wh_code': bs.wh_code,
                    'item_code': bs.item_code,
                    'basic_stock': bs.basic_stock,
                    'current_stock': bs.current_stock,
                    'available_stock': bs.available_stock,
                    'diff': bs.available_stock - bs.item.safety_stock,
                    'item': {
                        'item_name': bs.item.item_name,
                        'item_standard': bs.item.item_standard,
                        'safety_stock': bs.item.safety_stock
                    }
                })
    response = {
        'data': result,
    }
    return make_response(jsonify(response), 200)


@app.route("/api/mes/v1/setup/change_code", methods=["POST"])
def change_code():
    parser = reqparse.RequestParser()
    parser.add_argument("change_type", type=int, location="json")
    parser.add_argument("previous_code", type=str, location="json")
    parser.add_argument("after_code", type=str, location="json")
    parser.add_argument("name", type=str, location="json")
    parser.add_argument("change_reason", type=str, location="json")
    parser.add_argument("manager", type=str, location="json")
    parser.add_argument("fk_company_id", type=int, location="json")
    args = parser.parse_args()

    code_history = SetupCodeChangeHistory()
    code_history.change_type = args['change_type']
    code_history.previous_code = args['previous_code']
    code_history.after_code = args['after_code']
    code_history.name = args['name']
    code_history.change_reason = args['change_reason']
    code_history.manager = args['manager']
    code_history.fk_company_id = args['fk_company_id']
    db.session.add(code_history)

    if args['change_type'] == 1:  # 품목(BaseItem)
        item = db.session.query(BaseItem).filter(BaseItem.item_code == args['previous_code']).first()
        if item:
            item.item_code = args['after_code']
    elif args['change_type'] == 2:  # 업체(BaseClient)
        client = db.session.query(BaseClient).filter(BaseClient.alias == args['previous_code']).first()
        if client:
            client.alias = args['after_code']
    db.session.commit()
    return make_response(jsonify('success'), 200)
