import RestlessStore from './restless-store';

const stockEtc = new RestlessStore('/api/mes/v1/stock/stock_etc');
const stockEtcItem = new RestlessStore('/api/mes/v1/stock/stock_etc_item');
const stockMoveRequest = new RestlessStore(
  '/api/mes/v1/stock/stock_move_request'
);
const stockMoveRequestItem = new RestlessStore(
  '/api/mes/v1/stock/stock_move_request_item'
);
const stockMoveRelease = new RestlessStore(
  '/api/mes/v1/stock/stock_move_release'
);
const stockMoveReleaseItem = new RestlessStore(
  '/api/mes/v1/stock/stock_move_release_item'
);
const stockCorrection = new RestlessStore('/api/mes/v1/stock/stock_correction');
const stockCorrectionItem = new RestlessStore('/api/mes/v1/stock/stock_correction_item');

const getStockEtc = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/stock/stock_etc');
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getStockEtcItem = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/stock/stock_etc_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getStockMoveRequest = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/stock/stock_move_request');
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getStockMoveRequestItem = defaultFilters => {
  const instance = new RestlessStore(
    '/api/mes/v1/stock/stock_move_request_item'
  );
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getStockMoveRelease = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/stock/stock_move_release');
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getStockMoveReleaseItem = defaultFilters => {
  const instance = new RestlessStore(
    '/api/mes/v1/stock/stock_move_release_item'
  );
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getStockCorrection = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/stock/stock_correction');
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getStockCorrectionItem = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/stock/stock_correction_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

export {
  stockEtc,
  stockEtcItem,
  stockMoveRequest,
  stockMoveRequestItem,
  stockMoveRelease,
  stockMoveReleaseItem,
  stockCorrection,
  stockCorrectionItem,
  getStockEtc,
  getStockEtcItem,
  getStockMoveRequest,
  getStockMoveRequestItem,
  getStockMoveRelease,
  getStockMoveReleaseItem,
  getStockCorrection,
  getStockCorrectionItem,
};
