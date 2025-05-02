import RestlessStore from './restless-store';

const costClosing = new RestlessStore('/api/mes/v1/cost/closing');

const getCostClosing = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/cost/closing');
  instance.defaultFilters = defaultFilters;
  return instance;
};

export {
  costClosing,
  getCostClosing,
};
