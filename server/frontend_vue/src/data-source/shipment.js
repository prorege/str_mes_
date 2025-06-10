import RestlessStore from './restless-store';

const shipmentQuote = new RestlessStore('/api/mes/v1/shipment/quote');
const shipmentQuoteItem = new RestlessStore('/api/mes/v1/shipment/quote_item');
const shipmentQuoteItem2 = new RestlessStore(
  '/api/mes/v1/shipment/quote_item2'
);

const shipmentQuoteManual = new RestlessStore(
  '/api/mes/v1/shipment/quote_manual'
);
const shipmentQuoteManualItem = new RestlessStore(
  '/api/mes/v1/shipment/quote_manual_item'
);

const shipmentOrder = new RestlessStore('/api/mes/v1/shipment/order');
const shipmentOrderItem = new RestlessStore('/api/mes/v1/shipment/order_item');

const shipmentRelease = new RestlessStore('/api/mes/v1/shipment/release');
const shipmentReleaseItem = new RestlessStore('/api/mes/v1/shipment/release_item');
const shipmentReleaseItemByRank = new RestlessStore('/api/mes/v1/shipment/release_item_by_rank');
const shipmentReleaseItemWithClient = new RestlessStore('/api/mes/v1/shipment/release_item_with_client');

const shipmentReleaseReturn = new RestlessStore(
  '/api/mes/v1/shipment/release_return'
);
const shipmentReleaseReturnItem = new RestlessStore(
  '/api/mes/v1/shipment/release_return_item'
);

const shipmentLend = new RestlessStore('/api/mes/v1/shipment/lend');
const shipmentRetrieve = new RestlessStore('/api/mes/v1/shipment/retrieve');

const shipmentSalesStatement = new RestlessStore(
  '/api/mes/v1/shipment/sales_statement'
);
const shipmentSalesStatementItem = new RestlessStore(
  '/api/mes/v1/shipment/sales_statement_item'
);

const shipmentDeposit = new RestlessStore('/api/mes/v1/shipment/deposit');
const shipmentDepositItem = new RestlessStore(
  '/api/mes/v1/shipment/deposit_item'
);

const getShipmentQuote = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/shipment/quote');
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getShipmentQuoteItem = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/shipment/quote_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getShipmentQuoteItem2 = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/shipment/quote_item2');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getShipmentQuoteManualItem = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/shipment/quote_manual_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getShipmentOrderItem = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/shipment/order_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getShipmentReleaseItem = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/shipment/release_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getShipmentReleaseItemByRank = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/shipment/release_item_by_rank');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getShipmentReleaseReturnItem = (defaultFilters) => {
  const instance = new RestlessStore(
    '/api/mes/v1/shipment/release_return_item'
  );
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getShipmentSalesStatement = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/shipment/sales_statement');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getShipmentSalesStatementItem = (defaultFilters) => {
  const instance = new RestlessStore(
    '/api/mes/v1/shipment/sales_statement_item'
  );
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getShipmentDepositItem = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/shipment/deposit_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

export {
  shipmentQuote,
  shipmentQuoteItem,
  shipmentQuoteItem2,
  shipmentQuoteManual,
  shipmentQuoteManualItem,
  shipmentOrder,
  shipmentOrderItem,
  shipmentRelease,
  shipmentReleaseItem,
  shipmentReleaseItemByRank,
  shipmentReleaseItemWithClient,
  shipmentReleaseReturn,
  shipmentReleaseReturnItem,
  shipmentLend,
  shipmentRetrieve,
  shipmentSalesStatement,
  shipmentSalesStatementItem,
  shipmentDeposit,
  shipmentDepositItem,
  getShipmentQuote,
  getShipmentQuoteItem,
  getShipmentQuoteItem2,
  getShipmentQuoteManualItem,
  getShipmentOrderItem,
  getShipmentReleaseItem,
  getShipmentReleaseItemByRank,
  getShipmentReleaseReturnItem,
  getShipmentSalesStatement,
  getShipmentSalesStatementItem,
  getShipmentDepositItem,
};
