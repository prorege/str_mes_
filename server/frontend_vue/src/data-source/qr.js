import RestlessStore from './restless-store';

const getQrManagement = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/qr/qr_management');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getLotManagement = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/qr/lot_management');
  instance.defaultFilters = defaultFilters;
  return instance;
};

export {
  getQrManagement,
  getLotManagement
};
