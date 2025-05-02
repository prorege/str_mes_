# -*- coding: utf-8 -*-

from backend_model.table_quality import *

db = DBManager.db


class LibQualityManagement(object):
    @staticmethod
    def post_preprocessor(data=None, **kw):
        from backend_lib.lib_common import LibCommon
        LibCommon.get_item_number(data, 'qa_number', QualityManagement, QualityManagement.qa_number,
                                  '/quality/test-registration')

    @staticmethod
    def post_postprocessor(result=None, **kw):
        try:
            if result is None:
                return
            if result['test_type'] == '수입검사':
                from backend_lib.lib_purchase import LibPurchasePreReceivingItem
                LibPurchasePreReceivingItem.update_check_quantity(result['fk_prereceiving_item'],
                                                                  result['process_quantity'], result['bad_quantity'],
                                                                  result['good_quantity'], 1)
            elif result['test_type'] == '출하검사':
                from backend_lib.lib_production import LibPerformanceRegistrationItem1
                LibPerformanceRegistrationItem1.update_check_quantity(result['fk_performance_registration_item'],
                                                                      result['process_quantity'],
                                                                      result['bad_quantity'], result['good_quantity'],
                                                                      1)
        except:
            pass

    @staticmethod
    def patch_single_postprocessor(result=None, **kw):
        try:
            if result is None:
                return
            if result['test_type'] == '수입검사':
                from backend_lib.lib_purchase import LibPurchasePreReceivingItem
                LibPurchasePreReceivingItem.update_check_quantity(result['fk_prereceiving_item'],
                                                                  result['process_quantity'], result['bad_quantity'],
                                                                  result['good_quantity'], 1)
            elif result['test_type'] == '출하검사':
                from backend_lib.lib_production import LibPerformanceRegistrationItem1
                LibPerformanceRegistrationItem1.update_check_quantity(result['fk_performance_registration_item'],
                                                                      result['process_quantity'],
                                                                      result['bad_quantity'], result['good_quantity'],
                                                                      1)
        except:
            pass


class LibNonConformanceAction(object):
    @staticmethod
    def patch_single_postprocessor(result=None, **kw):
        if result is None:
            return
        if 'action_quantity' in result and 'fk_performance_item1_id' in result:
            from backend_model.table_production import PerformanceRegistrationItem1
            performance_item = db.session.query(
                PerformanceRegistrationItem1
            ).filter(
                PerformanceRegistrationItem1.id == result['fk_performance_item1_id']
            ).first()
            if performance_item:
                diff = result['action_quantity'] - performance_item.action_quantity
                performance_item.good_quantity += diff
                performance_item.action_quantity = result['action_quantity']
                db.session.commit()


class LibNonConformanceActionItem(object):
    @staticmethod
    def get_many_postprocessor(result=None, **kw):
        if result is None:
            return
        for row in result['objects']:
            action_id = row['fk_non_conformance_action_id']
            action = NonConformanceAction.query.filter(NonConformanceAction.id == action_id).first()
            if not action:
                continue

            row['item'] = dict(action.item.__dict__)
            del row['item']['_sa_instance_state']

            row['work_order'] = dict(action.work_order.__dict__)
            del row['work_order']['_sa_instance_state']

            row['quality_management'] = dict(action.quality_management.__dict__)
            del row['quality_management']['_sa_instance_state']

            row['non_conformance_action'] = dict(action.__dict__)
            del row['non_conformance_action']['_sa_instance_state']
            del row['non_conformance_action']['item']
            del row['non_conformance_action']['work_order']
            del row['non_conformance_action']['quality_management']
