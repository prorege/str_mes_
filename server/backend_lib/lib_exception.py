# -*- coding: utf-8 -*-

from flask_restless import ProcessingException


class MesException(object):
    @staticmethod
    def raise_not_authorized():
        raise ProcessingException(description="not authorized", code=601)

    @staticmethod
    def raise_exist_item_number():
        raise ProcessingException(description="exist item number", code=602)

    @staticmethod
    def raise_not_exist_mapping_menu():
        raise ProcessingException(description="not exist mapping menu", code=603)

    @staticmethod
    def raise_required_company_id():
        raise ProcessingException(description="required company id", code=604)

    @staticmethod
    def raise_exist_connected_data():
        raise ProcessingException(description="exist connected data", code=605)

    @staticmethod
    def raise_overflow_current_stock():
        raise ProcessingException(description="overflow current stock", code=606)

    @staticmethod
    def raise_not_exist_basic_stock():
        raise ProcessingException(description="not exist basic stock", code=607)

    @staticmethod
    def raise_not_add_item():
        raise ProcessingException(description="not add item", code=608)
