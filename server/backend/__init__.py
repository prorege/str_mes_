# -*- coding: utf-8 -*
print("module [backend] loaded")

from flask_cors import CORS
from flask_sqlalchemy import get_debug_queries
import os
import platform

from flask import Flask, render_template
from flask_restless import APIManager

from server_configuration.appConfig import *
from backend_lib.lib_excel import response_to_excel
from urllib.parse import quote
import flask
import decimal


class MyJSONEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)


app = Flask(__name__
            , template_folder=os.getcwd()+'/frontend_vue/dist/static'
            , static_folder=os.getcwd()+'/frontend_vue/dist/static'
            , static_url_path='/static')

cors = CORS(app, resources={r"/api/*": {"origins": "*"}}, max_age=86400)
app.json_encoder = MyJSONEncoder


# for debug print
def sql_debug(response):
    queries = list(get_debug_queries())
    query_str = ''
    total_duration = 0.0
    for q in queries:
        total_duration += q.duration
        stmt = str(q.statement).replace('\n', '\n       ')
        params = str(q.parameters)
        query_str += 'Query: {0}\nParams: {1}\nDuration: {2}ms\n\n'.format(stmt, params, round(q.duration * 1000, 2))
 
    print('=' * 80)
    print(' SQL Queries - {0} Queries Executed in {1}ms'.format(len(queries), round(total_duration * 1000, 2)))
    print('=' * 80)
    print(query_str.rstrip('\n'))
    print('=' * 80 + '\n')
 
    return response


if app.debug:
    app.after_request(sql_debug)

# server configuration
cur_system = platform.system()
if cur_system == "Windows" or cur_system == "Darwin":
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)


# table
# from backend_model import *
from backend_model.database import DBManager
DBManager.init(app)

# api
manager = APIManager(app, flask_sqlalchemy_db=DBManager.db)

# login
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)


# page
@app.route("/", methods=["GET"])
def page_index():
    resp = make_response(render_template("index.html"))
    return resp


from backend.api_common import *
from backend.api_base import *
from backend.api_shipment import *
from backend.api_setup import *
from backend.api_purchase import *
from backend.api_production import *
from backend.api_quality import *
from backend.api_stock import *
from backend.api_qr import *
from backend.api_project import *
from backend.api_cost import *
from backend.api_import import *
from backend.api_export import *
from backend.api_barobill import *
from backend.api_approval import *

@app.after_request
def after_request(response):
    output_type = request.headers.get('x-output-type')
    if output_type == 'excel':
        encoded = quote('print')
        response.headers.set('content-type', 'application/octet-stream')
        response.headers.set('Content-Disposition', 'attachment;filename={}.xlsx'.format(encoded))
        raw = response.get_data()

        io = response_to_excel(raw)
        content = io.getvalue()
        response.set_data(content)

    return response
