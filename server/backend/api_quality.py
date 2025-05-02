# -*- coding: utf-8 -*-
print("module [backend.api_quality] loaded")


from backend import check_token
from backend_model.table_quality import *
from backend import manager, app, make_response, request, token_required
from flask import send_from_directory, jsonify
from backend_lib.lib_quality import LibQualityManagement, LibNonConformanceAction, LibNonConformanceActionItem
from uuid import uuid4
from urllib import parse
import os
from flask import request, make_response, Response, jsonify
from flask_restful import reqparse
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta

db = DBManager.db
# REST API(s) available :
#  - /api/v1/login
#  - /api/v1/logout


manager.create_api(QualityManagement,
                   url_prefix='/api/mes/v1/quality',
                   collection_name='quality_management',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token, LibQualityManagement.post_preprocessor],
                       'PATCH_SINGLE': [check_token],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   },
                   postprocessors={
                       'POST': [LibQualityManagement.post_postprocessor],
                       'PATCH_SINGLE': [LibQualityManagement.patch_single_postprocessor]
                   })


@token_required
@app.route('/api/mes/v1/quality/quality_management_upload/<int:qa_id>', methods=['PATCH'])
def quality_management_file_upload(qa_id):
    f = request.files['file']
    if f is None:
        return make_response('require parameter is missing', 400)

    filename = str(uuid4())[:8] + '__' + f.filename
    qa = QualityManagement.query.filter(QualityManagement.id == qa_id)
    if not qa.first():
        return make_response('invalid quality management id', 400)

    qa.update({'qa_standard_path': filename})
    db.session.commit()

    base_path = os.path.join(app.config['UPLOAD_BASE_DIR'], "qa-attachment")
    abs_path = os.path.join(base_path, filename)

    if not os.path.exists(base_path):
        os.makedirs(base_path)

    f.save(abs_path)
    return make_response(filename, 200)


@token_required
@app.route('/api/mes/v1/quality/measuring_equipment_upload', methods=['POST'])
def measuring_equipment_file_upload():
    result = dict()
    base_path = os.path.join(app.config['UPLOAD_BASE_DIR'], "qa-attachment")
    me = None
    exist_file_attachments = None
    exist_file_correction = None
    exist_file_receipt = None

    if 'key' in request.form:
        me = MeasuringEquipment.query.filter(MeasuringEquipment.id == request.form['key']).first()
        if me.file_attachments:
            exist_file_attachments = os.path.join(base_path, me.file_attachments)
        if me.file_correction:
            exist_file_correction = os.path.join(base_path, me.file_correction)
        if me.file_receipt:
            exist_file_receipt = os.path.join(base_path, me.file_receipt)

    if request.form['type'] == 'remove':
        if me.file_attachments and os.path.exists(exist_file_attachments):
            os.remove(exist_file_attachments)
        if me.file_correction and os.path.exists(exist_file_correction):
            os.remove(exist_file_correction)
        if me.file_receipt and os.path.exists(exist_file_receipt):
            os.remove(exist_file_receipt)
    else:
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        if 'file_attachments' in request.files:
            if me and exist_file_attachments and os.path.exists(exist_file_attachments):
                os.remove(exist_file_attachments)
            f_attachments = request.files['file_attachments']
            filename = str(uuid4())[:8] + '__' + f_attachments.filename
            abs_path = os.path.join(base_path, filename)
            f_attachments.save(abs_path)
            result['file_attachments'] = filename

        if 'file_correction' in request.files:
            if me and exist_file_correction and os.path.exists(exist_file_correction):
                os.remove(exist_file_correction)
            f_correction = request.files['file_correction']
            filename = str(uuid4())[:8] + '__' + f_correction.filename
            abs_path = os.path.join(base_path, filename)
            f_correction.save(abs_path)
            result['file_correction'] = filename

        if 'file_receipt' in request.files:
            if me and exist_file_receipt and os.path.exists(exist_file_receipt):
                os.remove(exist_file_receipt)
            f_receipt = request.files['file_receipt']
            filename = str(uuid4())[:8] + '__' + f_receipt.filename
            abs_path = os.path.join(base_path, filename)
            f_receipt.save(abs_path)
            result['file_receipt'] = filename

    return make_response(jsonify(result), 200)


@token_required
@app.route('/api/mes/v1/quality/quality_management_download/<filename>', methods=['GET'])
def quality_management_file_download(filename):
    base_path = os.path.join(app.config['UPLOAD_BASE_DIR'], "qa-attachment")
    try:
        encoded_filename = parse.quote(filename.encode('utf-8'))
        r = send_from_directory(base_path, filename=filename, as_attachment=True)
        r.headers.set('Content-Disposition', f'attachment;filename={encoded_filename}')
        return r
    except FileNotFoundError:
        return make_response('file not found', 404)


manager.create_api(NonConformanceAction,
                   url_prefix='/api/mes/v1/quality',
                   collection_name='non_conformance_action',
                   methods=['GET', 'DELETE', 'PATCH', 'POST'],
                   allow_patch_many=True,
                   results_per_page=0,
                   max_results_per_page=100000000,
                   preprocessors={
                       'POST': [check_token],
                       'PATCH_SINGLE': [check_token, LibNonConformanceAction.patch_single_postprocessor],
                       'GET_SINGLE': [check_token],
                       'GET_MANY': [check_token],
                       'DELETE_SINGLE': [check_token]
                   },
                   postprocessors={
                       'PATCH_SINGLE': [LibNonConformanceAction.patch_single_postprocessor]
                   })


manager.create_api(NonConformanceActionItem,
                   url_prefix='/api/mes/v1/quality',
                   collection_name='non_conformance_action_item',
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
                       'GET_MANY': [LibNonConformanceActionItem.get_many_postprocessor]
                   })


manager.create_api(MeasuringEquipment,
                   url_prefix='/api/mes/v1/quality',
                   collection_name='measuring_equipment',
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


manager.create_api(QAStandard,
                   url_prefix='/api/mes/v1/quality',
                   collection_name='qa_standard',
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


@app.route("/api/mes/v1/monitoring/nonconformance/item", methods=["POST"])
def monitoring_nonconformance_item():
    """
    모니터링 - 불량수량 품목
    :return:
    """
    parser = reqparse.RequestParser()
    parser.add_argument("start_date", type=str, location="json")
    parser.add_argument("end_date", type=str, location="json")
    args = parser.parse_args()

    uid = 0
    response = []

    total_items = db.session.query(
        QualityManagement, PerformanceRegistration, PerformanceRegistrationItem1, BaseItem
    ).join(
        PerformanceRegistrationItem1,
        PerformanceRegistrationItem1.id == QualityManagement.fk_performance_registration_item
    ).join(
        PerformanceRegistration,
        PerformanceRegistration.id == PerformanceRegistrationItem1.fk_performance_registration_id
    ).join(
        BaseItem, BaseItem.item_code == PerformanceRegistrationItem1.item_code
    ).filter(
        PerformanceRegistration.target_date >= datetime.strptime(args['start_date'], '%Y-%m-%d %H:%M:%S')
    ).filter(
        PerformanceRegistration.target_date <= datetime.strptime(args['end_date'], '%Y-%m-%d %H:%M:%S')
    ).all()
    for item in total_items:
        bad1 = db.session.query(
            NonConformanceAction
        ).filter(
            NonConformanceAction.fk_quality_management_id == item.QualityManagement.id
        ).filter(
            NonConformanceAction.bad_type == '납땜불량'
        ).first()
        bad2 = db.session.query(
            NonConformanceAction
        ).filter(
            NonConformanceAction.fk_quality_management_id == item.QualityManagement.id
        ).filter(
            NonConformanceAction.bad_type == '하네스불량'
        ).first()
        bad3 = db.session.query(
            NonConformanceAction
        ).filter(
            NonConformanceAction.fk_quality_management_id == item.QualityManagement.id
        ).filter(
            NonConformanceAction.bad_type == '성능불량_ON'
        ).first()
        bad4 = db.session.query(
            NonConformanceAction
        ).filter(
            NonConformanceAction.fk_quality_management_id == item.QualityManagement.id
        ).filter(
            NonConformanceAction.bad_type == '성능불량_OFF'
        ).first()

        bad1_quantity = 0
        if bad1:
            bad1_quantity = bad1.bad_quantity
        bad2_quantity = 0
        if bad2:
            bad2_quantity = bad2.bad_quantity
        bad3_quantity = 0
        if bad3:
            bad3_quantity = bad3.bad_quantity
        bad4_quantity = 0
        if bad4:
            bad4_quantity = bad4.bad_quantity

        response.append({
            'id': uid,
            'target_date': item.PerformanceRegistration.target_date,
            'check_quantity': item.PerformanceRegistrationItem1.check_quantity,
            'good_quantity': item.PerformanceRegistrationItem1.good_quantity,
            'bad_quantity': item.PerformanceRegistrationItem1.bad_quantity,
            'middle_category': item.BaseItem.middle_category,
            'item_code': item.BaseItem.item_code,
            'item_name': item.BaseItem.item_name,
            'item_standard': item.BaseItem.item_standard,
            'bad1': bad1_quantity,
            'bad2': bad2_quantity,
            'bad3': bad3_quantity,
            'bad4': bad4_quantity
        })
        uid += 1

    return make_response(jsonify(response), 200)


@app.route("/api/mes/v1/monitoring/nonconformance", methods=["POST"])
def monitoring_nonconformance():
    """
    모니터링 - 월별 불량수량
    :return:
    """
    parser = reqparse.RequestParser()
    args = parser.parse_args()

    from backend_lib.lib_base import LibBaseCode
    bad_types = LibBaseCode.get_all_code_name('불량유형')

    current_year = datetime.now().strftime('%Y')

    response = []
    for i in range(1, 13):
        response.append({
            'month': f'{i}월',
            'bad1': 0,
            'bad2': 0,
            'bad3': 0,
            'bad4': 0
        })

        first_day, last_day = get_month_rage(int(current_year), i)

        month = f'{i}'
        if i < 10:
            month = f'0{i}'
        if first_day < 10:
            first_day = f'0{first_day}'
        if last_day < 10:
            last_day = f'0{last_day}'

        quality_managements = db.session.query(
            QualityManagement
        ).filter(
            QualityManagement.fk_performance_registration_item
        ).all()
        quality_management_ids = []
        for qm in quality_managements:
            quality_management_ids.append(qm.id)

        actions = db.session.query(
            NonConformanceAction,
            db.func.sum(NonConformanceAction.bad_quantity).label('total_bad_quantity')
        ).filter(
            NonConformanceAction.created >= datetime.strptime(f'{current_year}-{month}-{first_day} 00:00:00', '%Y-%m-%d %H:%M:%S')
        ).filter(
            NonConformanceAction.created <= datetime.strptime(f'{current_year}-{month}-{last_day} 23:59:59', '%Y-%m-%d %H:%M:%S')
        ).filter(
            NonConformanceAction.fk_quality_management_id.in_(quality_management_ids)
        ).group_by(
            NonConformanceAction.bad_type
        ).all()
        for action in actions:
            if action.NonConformanceAction.bad_type == '납땜불량':
                response[len(response) - 1]['bad1'] = action.total_bad_quantity
            elif action.NonConformanceAction.bad_type == '하네스불량':
                response[len(response) - 1]['bad2'] = action.total_bad_quantity
            elif action.NonConformanceAction.bad_type == '성능불량_ON':
                response[len(response) - 1]['bad3'] = action.total_bad_quantity
            elif action.NonConformanceAction.bad_type == '성능불량_OFF':
                response[len(response) - 1]['bad4'] = action.total_bad_quantity
    return make_response(jsonify(response), 200)


def get_month_rage(year, month):
    this_month = datetime(year=year, month=month, day=1).date()
    next_month = this_month + relativedelta.relativedelta(months=1)
    first_day = this_month
    last_day = next_month - timedelta(days=1)
    return first_day.day, last_day.day


@app.route("/api/mes/v1/monitoring/nonconformance/percentage", methods=["POST"])
def monitoring_nonconformance_percentage():
    """
    모니터링 - 타입별 불량비율
    :return:
    """
    parser = reqparse.RequestParser()
    args = parser.parse_args()

    response = [{
        'type': '납땜불량',
        'val': 0
    }, {
        'type': '하네스불량',
        'val': 0
    }, {
        'type': '성능불량_ON',
        'val': 0
    }, {
        'type': '성능불량_OFF',
        'val': 0
    }]

    total = db.session.query(
        db.func.sum(NonConformanceAction.bad_quantity).label('total_bad_quantity')
    ).first()[0]
    if not total:
        total = 0

    quality_managements = db.session.query(
        QualityManagement
    ).filter(
        QualityManagement.fk_performance_registration_item
    ).all()
    quality_management_ids = []
    for qm in quality_managements:
        quality_management_ids.append(qm.id)

    actions = db.session.query(
        NonConformanceAction,
        db.func.sum(NonConformanceAction.bad_quantity).label('total_bad_quantity')
    ).filter(
        NonConformanceAction.fk_quality_management_id.in_(quality_management_ids)
    ).group_by(
        NonConformanceAction.bad_type
    ).all()
    for action in actions:
        if action.NonConformanceAction.bad_type == '납땜불량':
            idx = 0
        elif action.NonConformanceAction.bad_type == '하네스불량':
            idx = 1
        elif action.NonConformanceAction.bad_type == '성능불량_ON':
            idx = 2
        elif action.NonConformanceAction.bad_type == '성능불량_OFF':
            idx = 3
        else:
            continue
        response[idx]['val'] = int((action.total_bad_quantity * 100) / total)
    return make_response(jsonify(response), 200)
