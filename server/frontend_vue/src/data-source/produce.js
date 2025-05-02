import RestlessStore from './restless-store';

const producePlan = new RestlessStore('/api/mes/v1/production/production_plan');
const producePlanItem = new RestlessStore(
  '/api/mes/v1/production/production_plan_item1'
);
const measureRequirement = new RestlessStore(
  '/api/mes/v1/production/measure_requirement'
);
const measureRequirementItem1 = new RestlessStore(
  '/api/mes/v1/production/measure_requirement_item1'
);
const measureRequirementItem2 = new RestlessStore(
  '/api/mes/v1/production/measure_requirement_item2'
);
const produceWorkOrder = new RestlessStore('/api/mes/v1/production/work_order');
const produceWorkOrderItem1 = new RestlessStore(
  '/api/mes/v1/production/work_order_item1'
);
const produceWorkOrderItem2 = new RestlessStore(
  '/api/mes/v1/production/work_order_item2'
);
const performance = new RestlessStore(
  '/api/mes/v1/production/performance_registration'
);
const performanceItem1 = new RestlessStore(
  '/api/mes/v1/production/performance_registration_item1'
);
const performanceItem2 = new RestlessStore(
  '/api/mes/v1/production/performance_registration_item2'
);
const processPerformanceRegistration = new RestlessStore(
  '/api/mes/v1/production/process_performance_registration', {}, 'processed', 'number'
)

const processMaterialConsumption = new RestlessStore(
  '/api/mes/v1/production/process_material_consumption'
)

const procBasicStock = (result, warehouseCode) => {
  result.data.forEach(item => {
    if (warehouseCode) {
      let basicStock = null;
      if (item.basic_stock) {
        if (Array.isArray(item.basic_stock)) {
          basicStock = item.basic_stock.filter(
            stock => stock.wh_code == warehouseCode
          );
        } else {
          if (item.basic_stock.wh_code == warehouseCode) {
            basicStock = [item.basic_stock];
          }
        }
      }
      item.basic_stock = basicStock ? basicStock[0] : null;
    }
  });
};

const getProducePlan = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/production/production_plan');
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getProducePlanItem = defaultFilters => {
  const instance = new RestlessStore(
    '/api/mes/v1/production/production_plan_item1'
  );
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getMeasureRequirement = defaultFilters => {
  const instance = new RestlessStore(
    '/api/mes/v1/production/measure_requirement'
  );
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getMeasureRequirementItem1 = defaultFilters => {
  const instance = new RestlessStore(
    '/api/mes/v1/production/measure_requirement_item1'
  );
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getMeasureRequirementItem2 = defaultFilters => {
  const instance = new RestlessStore(
    '/api/mes/v1/production/measure_requirement_item2'
  );
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getProduceWorkOrder = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/production/work_order');
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getProduceWorkOrderItem1 = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/production/work_order_item1');
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getProduceWorkOrderItem2 = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/production/work_order_item2');
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getPerformanceRegistration = defaultFilters => {
  const instance = new RestlessStore(
    '/api/mes/v1/production/performance_registration'
  );
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getPerformanceItem1 = defaultFilters => {
  const instance = new RestlessStore(
    '/api/mes/v1/production/performance_registration_item1'
  );
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getPerformanceItem2 = defaultFilters => {
  const instance = new RestlessStore(
    '/api/mes/v1/production/performance_registration_item2'
  );
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getProcessMaterialConsumption = defaultFilters => {
  const instance = new RestlessStore(
    '/api/mes/v1/production/process_material_consumption'
  );
  instance.defaultFilters = defaultFilters;
  return instance;
};

export {
  producePlan,
  producePlanItem,
  measureRequirement,
  measureRequirementItem1,
  measureRequirementItem2,
  produceWorkOrder,
  produceWorkOrderItem1,
  produceWorkOrderItem2,
  performance,
  performanceItem1,
  performanceItem2,
  processPerformanceRegistration,
  processMaterialConsumption,
  getProducePlan,
  getProducePlanItem,
  getMeasureRequirement,
  getMeasureRequirementItem1,
  getMeasureRequirementItem2,
  getProduceWorkOrder,
  getProduceWorkOrderItem1,
  getProduceWorkOrderItem2,
  getPerformanceRegistration,
  getPerformanceItem1,
  getPerformanceItem2,
  getProcessMaterialConsumption
};
