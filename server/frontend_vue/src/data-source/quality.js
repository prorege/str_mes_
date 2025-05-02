import RestlessStore from './restless-store';

const qualityTestRegistration = new RestlessStore(
  '/api/mes/v1/quality/quality_management'
);
const qualityTestRegistrationBadCase = new RestlessStore(
  '/api/mes/v1/quality/quality_management_bad_case'
);
const qualityNonconformanceAction = new RestlessStore(
  '/api/mes/v1/quality/non_conformance_action'
);
const qualityNonconformanceActionItem = new RestlessStore(
  '/api/mes/v1/quality/non_conformance_action_item'
);
const qualityMeasuringEquipment = new RestlessStore(
  '/api/mes/v1/quality/measuring_equipment'
);
const qualityQAStandard = new RestlessStore('/api/mes/v1/quality/qa_standard');

const getQualityTestRegistration = defaultFilters => {
  const instance = new RestlessStore(
    '/api/mes/v1/quality/quality_management'
  );
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getQualityNonconformanceAction = defaultFilters => {
  const instance = new RestlessStore(
    '/api/mes/v1/quality/non_conformance_action'
  );
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getQualityNonconformanceActionItem = defaultFilters => {
  const instance = new RestlessStore(
    '/api/mes/v1/quality/non_conformance_action_item'
  );
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getQualityQAStandard = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/quality/qa_standard');
  instance.defaultFilters = defaultFilters;
  return instance;
};

export {
  qualityTestRegistration,
  qualityTestRegistrationBadCase,
  qualityNonconformanceAction,
  qualityNonconformanceActionItem,
  qualityMeasuringEquipment,
  qualityQAStandard,
  getQualityTestRegistration,
  getQualityNonconformanceAction,
  getQualityNonconformanceActionItem,
  getQualityQAStandard,
};
