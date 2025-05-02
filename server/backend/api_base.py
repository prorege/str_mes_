# -*- coding: utf-8 -*-
print("module [backend.api_base] loaded")


from backend import check_token, check_permission, get_user
from backend_model.table_base import *
from flask_restless import ProcessingException
from backend_model.table_common import Users
from backend import manager, app
from backend.api_common import validate_token
from flask import request, make_response, Response, send_file, jsonify
from flask_restful import reqparse
from urllib.parse import quote
from backend_lib.lib_excel import sample_excel, import_excel, import_excel_bom, sample_excel_bom, ImportExcelException
from backend_lib.lib_base import LibBaseItem, LibBaseBom, LibBaseBomLink, LibBaseDepartment, LibBaseClient
import os
db = DBManager.db
# REST API(s) available :
#  - /api/v1/login
#  - /api/v1/logout


manager.create_api(BaseCode,
                   url_prefix='/api/mes/v1/base',
                   collection_name='code',
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


manager.create_api(BaseDepartment,
                   url_prefix='/api/mes/v1/base',
                   collection_name='department',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token, LibBaseDepartment.delete_single_preprocessor]
                   })


@app.route('/api/mes/v1/admin-util/user-patch', methods=['GET'])
def base_admin_util_user_patch():
    employees = db.session.query(BaseEmployee, Users)\
        .outerjoin(Users, Users.user_id == BaseEmployee.emp_code)\
        .filter(Users.id.is_(None))\
        .all()

    for emp, user in employees:
        user = Users()
        user.user_id = emp.emp_code
        user.user_pw = DBManager.password_encoder_512(emp.emp_code)
        user.user_name = emp.emp_name
        user.user_type = 2
        user.user_status = 1
        user.phone = emp.emp_mobile
        user.email = emp.emp_email
        user.fk_company_id = emp.fk_company_id
        DBManager.db.session.add(user)

    DBManager.db.session.commit()
    return make_response('OK', 200)


@app.route('/api/mes/v1/excel/base/employee', methods=['GET'])
def base_employee_excel_sample():
    io = sample_excel(BaseEmployee)
    content = io.getvalue()
    encoded = quote('사원입력양식')

    return Response(
        content,
        mimetype='application/octet-stream',
        headers={'Content-Disposition': 'attachment;filename={}.xlsx'.format(encoded)})


@app.route('/api/mes/v1/excel/base/employee', methods=['POST'])
def base_employee_excel_import():
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
        import_excel(table=BaseEmployee, common_values=common_values, file=f)
        return make_response('success', 200)
    except ImportExcelException as e:
        print(e)
        result = '데이터를 불러오는 중 에러가 발생하였습니다'
        if e.message is not None:
            result = e.message

        return make_response(result, 400)


def post_employee_user(data=None, **kw):
    if 'emp_password' in data:
        user = Users()
        user.user_id = data['emp_code']
        user.user_pw = DBManager.password_encoder_512(data['emp_password'])
        user.user_name = data['emp_name']
        user.user_type = 2
        #user.user_status = 1 if data['resignation_yn'] is False else 2
        user.user_status = 1
        user.phone = data['emp_mobile'] if 'emp_mobile' in data else None
        user.email = data['emp_email'] if 'emp_email' in data else None
        user.fk_company_id = data['fk_company_id']
        DBManager.db.session.add(user)
        del data['emp_password']

@app.route('/api/mes/v1/base/employee/password-rule-check', methods=['POST'])
def password_rule_check():
    parser = reqparse.RequestParser()
    parser.add_argument("emp_code", type=str, location="json")
    parser.add_argument("emp_password", type=str, location="json")
    args = parser.parse_args()

    user = db.session.query(Users).filter(Users.user_id == args['emp_code']).first()
    if user is None:
        return make_response('No User', 400)
    user_pw = DBManager.password_encoder_512(args['emp_password'])
    if user.user_pw != user_pw:
        return make_response('Not Authorized', 410)

    return make_response('OK', 200)

def patch_employee_user(instance_id=None, data=None, **kw):
    employee = db.session.query(BaseEmployee).filter(BaseEmployee.id == instance_id).first()
    query = db.session.query(Users).filter(Users.user_id == employee.emp_code)
    user = query.first()
    print("data : ", data)
    if employee is None:
        return make_response('No Employee', 400)

    if 'emp_password' in data:
        user_pw = DBManager.password_encoder_512(data['emp_password'])
        if 'emp_password_new' in data:
            user_pw_new = DBManager.password_encoder_512(data['emp_password_new'])
            print(user_pw)
            print(user_pw_new)

            if user.user_pw != user_pw:
                raise ProcessingException(description="Not Authorized", code=410)

            query.update({'user_pw': user_pw_new})
            db.session.commit()
            del data['emp_password']
            del data['emp_password_new']
        else:
    
            if user is None:
                user = Users()
                user.user_id = employee.emp_code
                user.user_pw = user_pw
                user.user_name = employee.emp_name
                user.user_type = 2
                #user.user_status = 1 if 'resignation_yn' in data and data['resignation_yn'] is False else 2
                user.user_status = 1
                user.phone = employee.emp_mobile
                user.email = employee.emp_email
                user.fk_company_id = employee.fk_company_id
                db.session.add(user)
            else:
                query.update({'user_pw': user_pw})

            db.session.commit()
            del data['emp_password']

    if 'emp_name' in data:
        if user is not None:
            query.update({'user_name': data['emp_name']})
            db.session.commit()

'''
def patch_employee_user(instance_id=None, data=None, **kw):
    print("data : ", data)
    employee = db.session.query(BaseEmployee).filter(BaseEmployee.id == instance_id).first()
    query = db.session.query(Users).filter(Users.user_id == employee.emp_code)
    user = query.first()

    if employee is None:
        return make_response('No Employee', 400)

    if 'emp_password' in data:
        if 'emp_password_new' in data:
            user_pw = DBManager.password_encoder_512(data['emp_password'])
            user_pw_new = DBManager.password_encoder_512(data['emp_password_new'])
            print(user_pw)
            print(user_pw_new)

            if user.user_pw != user_pw:
                raise ProcessingException(description="Not Authorized", code=410)

            query.update({'user_pw': user_pw_new})
            db.session.commit()
            del data['emp_password']
            del data['emp_password_new']
        else:


            user_pw = DBManager.password_encoder_512(data['emp_password'])
            query.update({'user_pw': user_pw})
            db.session.commit()
            del data['emp_password']

'''
def delete_employee_user(instance_id=None, **kw):
    employee = db.session.query(BaseEmployee).filter(BaseEmployee.id == instance_id).first()
    if employee is not None:
        db.session.query(Users).filter(Users.user_id == employee.emp_code).delete()
        db.session.commit()


manager.create_api(BaseEmployee,
                   url_prefix='/api/mes/v1/base',
                   collection_name='employee',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, post_employee_user],
                       'PATCH_SINGLE': [check_token, patch_employee_user],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token, delete_employee_user]
                   })


manager.create_api(BaseWarehouse,
                   url_prefix='/api/mes/v1/base',
                   collection_name='warehouse',
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


@app.route('/api/mes/v1/excel/base/client', methods=['GET'])
def base_client_excel_sample():
    io = sample_excel(BaseClient)
    content = io.getvalue()
    encoded = quote('거래처입력양식')

    return Response(
        content,
        mimetype='application/octet-stream',
        headers={'Content-Disposition': 'attachment;filename={}.xlsx'.format(encoded)})


@app.route('/api/mes/v1/excel/base/client', methods=['POST'])
def base_client_excel_import():
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
    common_values = dict(fk_company_id=user.fk_company_id, register_id=user.user_id)

    try:
        import_excel(table=BaseClient, common_values=common_values, file=f)
        return make_response('success', 200)
    except ImportExcelException as e:
        print(e)
        result = '데이터를 불러오는 중 에러가 발생하였습니다'
        if e.message is not None:
            result = e.message

        return make_response(result, 400)


manager.create_api(BaseClient,
                   url_prefix='/api/mes/v1/base',
                   collection_name='client',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token, LibBaseClient.patch_single_preprocessor],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   })


manager.create_api(BaseClientManager,
                   url_prefix='/api/mes/v1/base',
                   collection_name='client-manager',
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
from flask import jsonify
from sqlalchemy.orm import class_mapper
@app.route('/api/mes/v1/base/base-bom-link/get-many', methods=['GET'])
def base_bom_link_get_many():
    base_bom_links = db.session.query(
        BaseBOMLink
    ).group_by(BaseBOMLink.parent_id).all()
    response = {'objects': []}
    for link in base_bom_links:
        item = link.parent_bom.item
        
        link_data = {
            'id': item.id,
            'item_code': item.item_code,
            'item_name': item.item_name,
            'item_standard': item.item_standard,
            'item_group': item.item_group,
            'parent_id': link.parent_id
        }
        response['objects'].append(link_data)

    return make_response(response, 200)

@app.route('/api/mes/v1/excel/base/item', methods=['GET'])
def base_item_excel_sample():
    io = sample_excel(BaseItem)
    content = io.getvalue()
    encoded = quote('품목입력양식')

    return Response(
        content,
        mimetype='application/octet-stream',
        headers={'Content-Disposition': 'attachment;filename={}.xlsx'.format(encoded)})


@app.route('/api/mes/v1/excel/base/item', methods=['POST'])
def base_item_excel_import():
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
    common_values = dict(fk_company_id=user.fk_company_id, register_id=user.user_id)

    try:
        import_excel(table=BaseItem, common_values=common_values, file=f)
        return make_response('success', 200)
    except ImportExcelException as e:
        print(e)
        result = '데이터를 불러오는 중 에러가 발생하였습니다'
        if e.message is not None:
            result = e.message

        return make_response(result, 400)


@app.route('/api/mes/v1/base/item-image/<filename>', methods=['GET'])
def base_item_image(filename):
    BASE_DIR = app.config['UPLOAD_BASE_DIR']
    abs_path = os.path.join(BASE_DIR, "item-images", filename)
    return send_file(abs_path)


manager.create_api(BaseItem,
                   url_prefix='/api/mes/v1/base',
                   collection_name='item',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token, LibBaseItem.patch_preprocessor],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token, LibBaseItem.delete_single_preprocessor]
                   },
                   postprocessors={
                       'GET_MANY': [LibBaseItem.get_many_postprocessor],
                       'POST': [LibBaseItem.post_postprocessor]
                   })


manager.create_api(BaseClientItem,
                   url_prefix='/api/mes/v1/base',
                   collection_name='client-item',
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


manager.create_api(BaseDesign,
                   url_prefix='/api/mes/v1/base',
                   collection_name='design',
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


manager.create_api(BaseProcess,
                   url_prefix='/api/mes/v1/base',
                   collection_name='process',
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


manager.create_api(BaseBOM,
                   url_prefix='/api/mes/v1/base',
                   collection_name='bom',
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
                       'GET_SINGLE': [LibBaseBom.get_single_postprocessor],
                       'GET_MANY': [LibBaseBom.get_many_postprocessor]
                   })

@app.route('/api/mes/v1/base/item/main-supplier', methods=['POST'])
def base_iem_get_main_supplier():
    parser = reqparse.RequestParser()
    parser.add_argument("item_code", type=str, location="json")
    args = parser.parse_args()
    try:
        result = db.session.query(BaseClient)\
            .join(BaseClientItem, BaseClientItem.client_id == BaseClient.id)\
            .join(BaseItem, BaseItem.item_code == BaseClientItem.item_code)\
            .filter(BaseItem.item_code == args['item_code'])\
            .filter(BaseClientItem.main_supplier == True)\
            .first()

        return result.name if result else ''
    except:
        return None

@app.route('/api/mes/v1/excel/base/bom', methods=['GET'])
def base_bom_excel_sample():
    io = sample_excel_bom()
    content = io.getvalue()
    encoded = quote('BOM자재입력양식')

    return Response(
        content,
        mimetype='application/octet-stream',
        headers={'Content-Disposition': 'attachment;filename={}.xlsx'.format(encoded)})


@app.route('/api/mes/v1/excel/base/bom', methods=['POST'])
def base_bom_excel_import():
    token = request.headers.get('token')
    if token is None:
        return make_response('Not Authorized', 410)

    user = validate_token(token)
    exc = check_permission(user, method='EXCEL')
    if exc is not None:
        return make_response(exc.description, exc.code)

    root_id = request.form['root_id']
    if root_id is None:
        return make_response('require parameter is missing', 400)

    f = request.files['file']
    if f is None:
        return make_response('require parameter is missing', 400)

    filepath, ext = f.filename.rsplit('.', 1)
    if ext not in ['xlsx']:
        return make_response('invalid file extension', 400)

    f.seek(0)
    # 모든 행 공통 데이터
    common_values = dict(root_id=root_id, fk_company_id=user.fk_company_id, register_id=user.user_id)

    try:
        import_excel_bom(common_values=common_values, file=f)
        return make_response('success', 200)
    except ImportExcelException as e:
        print(e)
        result = '데이터를 불러오는 중 에러가 발생하였습니다'
        if e.message is not None:
            result = e.message

        return make_response(result, 400)


@app.route('/api/mes/v1/base/bom-reversal/<int:item_id>', methods=['GET'])
def base_item_bom_reverse(item_id):

    from sqlalchemy.orm import aliased

    ChildBom = aliased(BaseBOM)
    ParentBom = aliased(BaseBOM)
    ParentItem = aliased(BaseItem)
    RootBom = aliased(BaseBOM)
    RootItem = aliased(BaseItem)

    objects = db.session.query(BaseBOMLink.link_id,
                               BaseBOMLink.requirement,
                               BaseBOMLink.consume_yn,
                               BaseBOMLink.lrate,
                               ParentItem.id.label('parent_item_id'),
                               ParentItem.item_code.label('parent_item_code'),
                               ParentItem.item_name.label('parent_item_name'),
                               RootItem.id.label('root_item_id'),
                               RootItem.item_code.label('root_item_code'),
                               RootItem.item_name.label('root_item_name'))\
        .join(ChildBom, BaseBOMLink.child_id == ChildBom.id)\
        .join(ParentBom, BaseBOMLink.parent_id == ParentBom.id) \
        .join(ParentItem, ParentBom.item_id == ParentItem.id) \
        .join(RootBom, BaseBOMLink.root_id == RootBom.id) \
        .join(RootItem, RootBom.item_id == RootItem.id) \
        .filter(ChildBom.item_id == item_id)\
        .all()

    result = [
        dict(link_id=item.link_id,
             requirement=item.requirement,
             consume_yn=item.consume_yn,
             lrate=item.lrate,
             parent_item_id=item.parent_item_id,
             parent_item_code=item.parent_item_code,
             parent_item_name=item.parent_item_name,
             root_item_id=item.root_item_id,
             root_item_code=item.root_item_code,
             root_item_name=item.root_item_name
        ) for item in objects
    ]

    return make_response(jsonify(result), 200)


manager.create_api(BaseBOMLink,
                   url_prefix='/api/mes/v1/base',
                   collection_name='bom-link',
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
                       'GET_SINGLE': [LibBaseBomLink.get_single_postprocessor],
                       'GET_MANY': [LibBaseBomLink.get_many_postprocessor]
                   })


manager.create_api(BaseBOMProcess,
                   url_prefix='/api/mes/v1/base',
                   collection_name='bom-process',
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


manager.create_api(BaseBOMHistory,
                   url_prefix='/api/mes/v1/base',
                   collection_name='bom-history',
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


manager.create_api(BaseBank,
                   url_prefix='/api/mes/v1/base',
                   collection_name='bank',
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
