#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib


class CommonConfig(object):
    # User Type
    API_HEADERS = {"Content-type": "application/json"}

    # Find Address
    FIND_ADDR_URL = "https://www.juso.go.kr/addrlink/addrLinkApi.do"
    FIND_ADDR_CKEY = "U01TX0FVVEgyMDIyMDUxNjE1MzUzNzExMjU3MzU="

    FIND_BUSN_NUM_URL = "https://api.odcloud.kr/api/nts-businessman/v1/status"
    FIND_BUSN_NUM_CKEY = "IwShpdPfREFu+vcqtsIAP6NxdwX1dwj1KrmTzT6cFOz0/H25Rzeo8TmNhtLZxhfRM2TiyiyKqseUPtGiPl0Jvg=="

    BAROBILL_MNGR_ID = "strinc"
    BAROBILL_MNGR_NAME = ""

    ALLOW_DUPLICATED_LOGIN = True


class DevelopmentConfig(CommonConfig):
    BIND_PORT = 8081
    SQLALCHEMY_DATABASE_URI = "mysql://dbadmin:p@ssw0rd@127.0.0.1/strmes"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DAEMON_HEADERS = {"Content-type": "application/json"}
    UPLOAD_BASE_DIR = "C:\\Util"

    BAROBILL_CERTKEY = '3B453895-4694-4F54-829E-B883B6A89889'
    BAROBILL_API_URL = "https://ws.baroservice.com/TI.asmx?WSDL"

class ProductionConfig(CommonConfig):
    BIND_PORT = 8081
    SQLALCHEMY_DATABASE_URI = "mysql://dbadmin:p@ssw0rd@127.0.0.1/strmes"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DAEMON_HEADERS = {"Content-type": "application/json"}
    UPLOAD_BASE_DIR = "/home/ubuntu/str/files/"

    BAROBILL_CERTKEY = '3B453895-4694-4F54-829E-B883B6A89889'
    BAROBILL_API_URL = "https://ws.baroservice.com/TI.asmx?WSDL"
    
