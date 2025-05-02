# -*- coding: utf-8 -*-

from backend_model.table_setup import *

db = DBManager.db


class LibCommon(object):
    @staticmethod
    def get_item_number(data, number_name, table, column_number, path):
        if not data['fk_company_id']:
            from backend_lib.lib_exception import MesException
            MesException.raise_required_company_id()
        # 입력한 번호가 없는 경우
        if number_name not in data or data[number_name] is None or not data[number_name].strip():
            data[number_name] = LibCommon.create_item_number(table, column_number, path, data['fk_company_id'])
        else:
            # 번호가 이미 존재하는지 확인
            if LibCommon.check_exist_item_number(table, column_number, data[number_name], data['fk_company_id']) is True:
                from backend_lib.lib_exception import MesException
                MesException.raise_exist_item_number()

    @staticmethod
    def create_item_number(table, column_number, path, company_id):
        menu = LibCommon.get_menu(path)
        new_index = LibCommon.create_item_number_index(table, column_number, menu)
        try:
            new_index_integer = int(new_index)
        except:
            new_index_integer = 0
        while True:
            item_number = menu.menu_number_format(count=new_index_integer)
            if LibCommon.check_exist_item_number(table, column_number, item_number, company_id) is True:
                new_index_integer = new_index_integer + 1
                continue
            else:
                return item_number

    @staticmethod
    def get_menu(path):
        menu = db.session.query(SetupMenu).filter(SetupMenu.path == path).first()
        if menu is None:
            from backend_lib.lib_exception import MesException
            MesException.raise_not_exist_mapping_menu()
        return menu

    @staticmethod
    def create_item_number_index(table, column_number, menu: SetupMenu):
        from backend_model.table_shipment import ShipmentQuote
        start, end = menu.get_range()
        datestr = datetime.now().strftime(menu.date_format())
        from sqlalchemy import func, Integer

        query = db.session.query(column_number).filter(
            table.created >= start,
            table.created < end
        )

        if table == ShipmentQuote:
            query = query.filter(
                column_number.like('ONE-'+('_'*len(datestr))+'-___'),
                func.substr(column_number, -menu.menu_last_digit, 1) != '-'
            ).order_by(
                func.cast(func.substr(column_number, -3), Integer).desc()
            )
        else:
            query = query.filter(
                column_number.like(f'{datestr}{menu.menu_last_digit}%')
            ).order_by(
                column_number.desc()
            )

        item = query.first()
        return item[0][-menu.menu_last_digit:] if item else 0
        # if table == ShipmentQuote:
        #   item = db.session.query(column_number).filter(
        #         table.created >= start
        #     ).filter(
        #         table.created < end
        #     ).filter(
        #         column_number.like('ONE-________-___')
        #     ).filter(
        #         func.substr(column_number, -menu.menu_last_digit, 1) != '-'
        #     ).order_by(
        #         func.cast(func.substr(column_number, -3), Integer).desc()
        #     ).first()
        # else:
        #     item = db.session.query(column_number).filter(
        #         table.created >= start
        #     ).filter(
        #         table.created < end
        #     ).filter(
        #         column_number.like(f'%{datestr}%')
        #     ).order_by(
        #         column_number.desc()
        #     ).first()

        # return item[0][-menu.menu_last_digit:] if item else 0

    @staticmethod
    def check_exist_item_number(table, column_number, item_number, company_id):
        exist = db.session.query(table).filter(
            column_number == item_number
        ).filter(
            table.fk_company_id == company_id
        ).first()
        if exist:
            return True
        else:
            return False
