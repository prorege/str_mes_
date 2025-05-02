# -*- coding: utf-8 -*-
print("module [backend.api_common] loaded")

import hashlib
from flask import make_response, jsonify, request, json, send_from_directory, send_file
from flask_restless import ProcessingException
from flask_restful import reqparse
from urllib.parse import urlparse, quote
import os
import json
from functools import wraps
from uuid import uuid4

from backend_model.table_base import *
from backend import app, login_manager
from backend_model.table_common import *
from backend_model.table_setup import SetupMenu, SetupGroupAuth
from backend import manager
from backend_lib.lib_setup import LibSetupBasicStock
from backend_lib.lib_shipment import LibShipmentOrderItem

import requests
db = DBManager.db
# REST API(s) available :
#  - /api/v1/login
#  - /api/v1/logout


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@login_manager.user_loader
def load_user(id):
    user = DBManager.db.session.query(Users).get(id)
    return user


@app.route('/api/monitor/v1/login', methods=['POST'])
def login_api():
    data = json.loads(request.data)
    result = ''

    if data['user_id'] is not None and data['user_pw'] is not None:
        loginuser = db.session.query(Users).filter(Users.user_id == data["user_id"]).first()
        department_data = {
            "id": '',
            "department_name": '',
            "wh_name": '',
            "depart_head_name": '',
        }
        employee = db.session.query(BaseEmployee).filter(BaseEmployee.emp_code == data["user_id"]).first()
        if employee is not None:
            if employee.resignation_yn:
                result = {'status': False, 'reason': 4}  # 퇴사
                return make_response(jsonify(result), 200)
            department = db.session.query(BaseDepartment).filter(BaseDepartment.id == employee.fk_department_id).first()
            department_data = department.serialize()
        if loginuser is None:
            result = {'status': False, 'reason': 1}  # ID 없음
        else:
            if loginuser.user_pw != password_encoder_512(data["user_pw"]):
                result = {'status': False, 'reason': 2}  # PW 틀림
            else:  # Login 성공
                if loginuser.user_status == 2:
                    result = {'status': False, 'reason': 3}  # Activation 안됨
                else:
                    loginuser.last_logon_time = datetime.now()

                    if not loginuser.token or not app.config['ALLOW_DUPLICATED_LOGIN']:
                        loginuser.token = generate_token(data['user_id'])

                    db.session.query(Users).filter(Users.user_id == data["user_id"])\
                        .update(dict(last_logon_time=loginuser.last_logon_time, token=loginuser.token))

                    new_access_history = AccessHistory()
                    new_access_history.type = 0  # Login
                    user_agent = request.environ.get('HTTP_USER_AGENT')
                    new_access_history.os_ver, new_access_history.browser_ver = get_os_browser_from_useragent(user_agent)
                    new_access_history.ip_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                    new_access_history.update_time = datetime.now()
                    new_access_history.user_id = loginuser.user_id
                    new_access_history.FK_user_id = loginuser.id
                    db.session.add(new_access_history)
                    db.session.commit()

                    company = db.session.query(Companies.logo).filter(Companies.id == loginuser.fk_company_id).first()

                    if loginuser.user_type == 1:
                        menus = db.session.query(SetupMenu).filter(SetupMenu.menu_enable == True).all()
                    else:
                        menus = db.session.query(SetupMenu)\
                            .join(SetupGroupAuth, SetupGroupAuth.fk_menu_id == SetupMenu.id)\
                            .filter(SetupGroupAuth.fk_group_id == employee.fk_setup_group_auth)\
                            .filter(SetupGroupAuth.menu_yn == 1)\
                            .filter(SetupMenu.menu_enable == True)

                    result = {
                        'status': True,
                        'reason': 0,
                        'user': {**loginuser.serialize(), 'position': employee.emp_position if employee else ''},
                        'department': department_data,
                        'logo': company.logo,
                        'menu': [
                            dict(id=menu.id, parent_id=menu.parent_id, name=menu.menu_name, path=menu.path, depth=menu.menu_depth, order=menu.menu_order, )
                            for menu in menus]}

    return make_response(jsonify(result), 200)


@app.route("/api/monitor/v1/logout", methods=["POST"])
def logout_api():
    print("logout_api 1")
    parser = reqparse.RequestParser()
    parser.add_argument("token", type=str, location="headers")
    token = parser.parse_args()["token"]
    result = ''
    if token is None:
        print("token is none")
    print("logout_api 2")
    print("token :", token)
    login_user = Users.query.filter_by(token=token).first()
    if login_user is None:
        print("user is none")
    else:
        print("logout_api 3")
        new_access_history = AccessHistory()
        new_access_history.type = 1  # Logout
        userAgent = request.environ.get('HTTP_USER_AGENT')
        new_access_history.os_ver, new_access_history.browser_ver = get_os_browser_from_useragent(userAgent)
        new_access_history.ip_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        new_access_history.update_time = datetime.now()
        new_access_history.user_id = login_user.user_id
        new_access_history.fk_user_id = login_user.id

        db.session.add(new_access_history)
        db.session.commit()
        print("logout_api 4")
    return make_response(jsonify(result), 200)


@app.route("/api/mes/v1/find-address", methods=["POST"])
def find_addr():
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int, location="json", default=1)
    parser.add_argument("results_per_page", type=int, location="json", default=20)
    parser.add_argument("keyword", type=str, location="json")
    args = parser.parse_args()

    if args['keyword'] is None:
        response = dict()
        response['totalCount'] = 0
        response['data'] = []
        return make_response(response, 200)

    params = dict()
    params['confmKey'] = app.config['FIND_ADDR_CKEY']
    params['resultType'] = 'json'
    params['currentPage'] = args['page']
    params['countPerPage'] = args['results_per_page']
    params['keyword'] = args['keyword']
    try:
        result = requests.post(app.config['FIND_ADDR_URL'], params)
    except:
        return make_response('API 연결에 실패했습니다', 400)
    json = result.json()
    if json['results']['common']['errorCode'] != '0':
        return make_response(json['results']['common']['errorMessage'], 400)

    response = dict()
    response['totalCount'] = int(json['results']['common']['totalCount'])
    response['data'] = [dict(jibun=item['jibunAddr'], road=item['roadAddrPart1'], eng=item['engAddr'], zip=item['zipNo']) for item in json['results']['juso']]
    return make_response(response, 200)


@app.route("/api/mes/v1/find-business-number/<busn_num>", methods=["GET"])
def find_business_number(busn_num):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Infuser ' + app.config['FIND_BUSN_NUM_CKEY']}
    params = {'b_no': [busn_num]}
    print(json.dumps(params))
    result = requests.post(app.config['FIND_BUSN_NUM_URL'], headers=headers, data=json.dumps(params))

    response = {'message': None, 'result': None}
    if result.status_code == 200:
        obj = result.json()
        response['message'] = obj['status_code']
        response['result'] = obj['data']
        pass
    else:
        try:
            obj = result.json()
            response['message'] = obj['status_code']
        except ValueError:
            response['message'] = result.text

    return make_response(response, result.status_code)


@app.route("/api/mes/v1/update-assign-quantity", methods=["POST"])
def update_stock():
    parser = reqparse.RequestParser()
    parser.add_argument("order_item_id", type=int, location="json")
    parser.add_argument("item_code", type=str, location="json")
    parser.add_argument("warehouse", type=str, location="json")
    args = parser.parse_args()

    # LibSetupBasicStock.update_available_stock(args['item_code'], args['warehouse'])
    LibShipmentOrderItem.update_assign_quantity(args['order_item_id'], args['item_code'], args['warehouse'])

    return make_response('success', 200)


@app.route('/api/mes/v1/mail-attachment', methods=['POST'])
def upload_attachment():
    f = request.files['file']
    if f is None:
        return make_response('require parameter is missing', 400)

    file_root, file_ext = os.path.splitext(f.filename)
    filename = f'{file_root}__{str(uuid4())[:8]}{file_ext}'
    base_path = os.path.join(app.config['UPLOAD_BASE_DIR'], "mail-attachment")
    abs_path = os.path.join(base_path, filename)

    if not os.path.exists(base_path):
        os.makedirs(base_path)

    f.save(abs_path)
    return make_response(filename, 200)


@app.route('/api/mes/v1/mail-attachment/<filename>', methods=['GET'])
def download_attachment(filename):
    base_path = os.path.join(app.config['UPLOAD_BASE_DIR'], "mail-attachment")
    try:
        encoded_filename = quote(filename.encode('utf-8'))
        r = send_from_directory(base_path, filename=filename, as_attachment=True)
        r.headers.set('Content-Disposition', f'attachment;filename={encoded_filename}')
        return r
    except FileNotFoundError:
        return make_response('file not found', 404)


def generate_token(userID):
    m = hashlib.sha1()

    m.update(userID.encode('utf-8'))
    m.update(datetime.now().isoformat().encode('utf-8'))

    return m.hexdigest()


def validate_token(token):
    user = Users.query.filter_by(token=str(token)).first()

    if user is None:
        raise ProcessingException(description="Not Authorized", code=410)

    return user

@app.route('/api/mes/v1/file-manager/upload', methods=['POST'])
def upload_file():
    f = request.files['file']
    if f is None:
        return make_response('require parameter is missing', 400)
    path = request.form['path']
    filename = str(uuid4())[:8] + '__' + f.filename
    base_path = os.path.join(app.config['UPLOAD_BASE_DIR'], path)
    abs_path = os.path.join(base_path, filename)

    if not os.path.exists(base_path):
        os.makedirs(base_path)

    f.save(abs_path)
    return make_response(filename, 200)
    

@app.route('/api/mes/v1/file-manager/<string:method>/<string:path>/<string:file_name>/<string:real_name>', methods=['GET'])
def file_manager(method, path, file_name, real_name):
    try:
        BASE_DIR = app.config['UPLOAD_BASE_DIR']
        abs_path = os.path.join(BASE_DIR, path, file_name)
        if method == 'read':
            _, file_extension = os.path.splitext(file_name)
            if file_extension.lower() in ['.jpg', '.jpeg']:
                mimetype = 'image/jpeg'
            elif file_extension.lower() == '.png':
                mimetype = 'image/png'
            elif file_extension.lower() == '.pdf':
                mimetype = 'application/pdf'
            else:
                return make_response(jsonify({"error": "지원되지 않는 파일 형식입니다."}), 400)

            return send_file(abs_path, mimetype=mimetype)
    
        elif method == 'download':
            if real_name is None:
                encoded_filename = quote(file_name.encode('utf-8'))
            else:
                encoded_filename = quote(real_name.encode('utf-8'))
            return send_file(
                abs_path,
                    mimetype='application/octet-stream',
                    attachment_filename=encoded_filename,
                    as_attachment=True,
                )
        else:
            return make_response(jsonify({"error": "지원되지 않는 메서드입니다."}), 400)
        
    except FileNotFoundError:
        return make_response(jsonify({"error": "파일을 찾을 수 없음."}), 404)
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "파일을 불러오는 중 오류 발생."}), 500)

def validate_auth_code(method, auth_code):
    if method == 'POST':
        return 1 & auth_code == 1
    elif method == 'PATCH':
        return 2 & auth_code == 2
    elif method == 'DELETE':
        return 4 & auth_code == 4
    elif method == 'PRINT':
        return 8 & auth_code == 8
    elif method == 'EXCEL':
        return 16 & auth_code == 16

    print('Unknown method: {}'.format(method))
    return False


def check_exclude_path(url_path):
    exclude_check_permission_list = ['/profile', '/produce/process-performance-registration', '/produce/process_performance_registration_vietnam']
    for item in exclude_check_permission_list:
        if url_path.startswith(item):
            return True
    return False


def check_permission(user: Users, method=None):
    if user.user_type == 1:
        return None
    else:
        employee = BaseEmployee.query.filter_by(emp_code=user.user_id).first()
        if employee is not None:
            return check_permission_employee(employee, method)
        else:
            return ProcessingException(description="Not Authorized (No Employee Data)", code=411)


def check_permission_employee(employee: BaseEmployee, method=None):
    url = urlparse(request.referrer)

    if check_exclude_path(url.path):
        return None

    paths = url.path.split('/')
    real_path = '/' + paths[1] + '/' + paths[2]
    auth = db.session.query(SetupGroupAuth.menu_auth) \
        .join(SetupMenu, SetupMenu.id == SetupGroupAuth.fk_menu_id) \
        .filter(SetupGroupAuth.fk_group_id == employee.fk_setup_group_auth) \
        .filter(SetupMenu.path == real_path) \
        .filter(SetupMenu.fk_company_id == employee.fk_company_id) \
        .first()

    if auth is None:
        print('auth path: {}'.format(real_path))
        return ProcessingException(description="Not Authorized (No Group Auth)", code=412)

    if method is None:
        method = request.method

    if validate_auth_code(method, auth.menu_auth) is False:
        return ProcessingException(description="Forbidden Content", code=403)

    return None


def check_token(search_params=None, **kw):
    parser = reqparse.RequestParser()
    parser.add_argument("token", type=str, location="headers")
    token = parser.parse_args()["token"]
    print("token:", token)
    user = Users.query.filter_by(token=token).first()
    if user is None:
        raise ProcessingException(description="Not Authorized", code=411)
    print("user:", user.user_id)

    if user.user_type != 1 and request.method != 'GET':
        exc = check_permission(user)
        if exc is not None:
            raise exc


def get_user():
    parser = reqparse.RequestParser()
    parser.add_argument("token", type=str, location="headers")
    token = parser.parse_args()["token"]
    print("token:", token)
    user = Users.query.filter_by(token=token).first()
    if user is None:
        return None
    return user


def token_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument("token", type=str, location="headers")
        token = parser.parse_args()["token"]
        print("token:",token)
        user = Users.query.filter_by(token=token).first()
        if user is None:
            raise ProcessingException(description="Not Authorized", code=411)
        print("user:",user.user_id)
        return fn(*args, **kwargs)
    return decorated


def password_encoder_512(password):
    h = hashlib.sha512()
    h.update(password.encode('utf-8'))
    return h.hexdigest()


def get_os_browser_from_useragent(userAgent):
    os_ver = "Unknown"
    browser_ver = "Unknown"

    if userAgent.find("Linux") != -1:
        os_ver = "Linux"
    elif userAgent.find("Mac") != -1:
        os_ver = "MacOS"
    elif userAgent.find("X11") != -1:
        os_ver = "UNIX"
    elif userAgent.find("Win") != -1:
        os_ver = "Windows"

    if userAgent.find("MSIE 6") != -1:
        browser_ver = "Internet Explorer 6"
    elif userAgent.find("MSIE 7") != -1:
        browser_ver = "Internet Explorer 7"
    elif userAgent.find("MSIE 8") != -1:
        browser_ver = "Internet Explorer 8"
    elif userAgent.find("MSIE 9") != -1:
        browser_ver = "Internet Explorer 9"
    elif userAgent.find("MSIE 10") != -1:
        browser_ver = "Internet Explorer 10"
    elif userAgent.find("Trident") != -1 or userAgent.find("trident") != -1:
        browser_ver = "Internet Explorer 11"
    elif userAgent.find("Firefox") != -1:
        browser_ver = "Firefox"
    elif userAgent.find("Opera") != -1:
        browser_ver = "Opera"
    elif userAgent.find("Chrome") != -1:
        browser_ver = "Chrome"
    elif userAgent.find("Safari") != -1 or userAgent.find("Chrome") == -1:
        browser_ver = "Safari"
    elif userAgent.find("Edge") != -1 or userAgent.find("edge") != -1:
        browser_ver = "Microsoft Edge"

    return os_ver, browser_ver


def date_encoder(thing):
    list_date = str(thing).split(":")

    if hasattr(thing, 'isoformat'):
        if len(list_date[0]) == 1:
            return "0" + thing.isoformat()
        return thing.isoformat()
    else:
        if len(list_date[0]) == 1:
            return "0" + str(thing)
        return str(thing)


manager.create_api(AccessHistory,
                   url_prefix='/api/mes/v1/common',
                   collection_name='access_history',
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


manager.create_api(Companies,
                   url_prefix='/api/mes/v1/common',
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


manager.create_api(Users,
                   url_prefix='/api/mes/v1/common',
                   collection_name='users',
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
