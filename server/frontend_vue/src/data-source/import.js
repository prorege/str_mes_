import RestlessStore from './restless-store';

const importPurchaseOrder = new RestlessStore('/api/mes/v1/import/purchase_order');
const importPurchaseOrderItem = new RestlessStore('/api/mes/v1/import/purchase_order_item');

const importShipment = new RestlessStore('/api/mes/v1/import/shipment');
const importShipmentItem = new RestlessStore('/api/mes/v1/import/shipment_item');

const importClearance = new RestlessStore('/api/mes/v1/import/clearance');
const importClearanceItem = new RestlessStore('/api/mes/v1/import/clearance_item');

const importCredit = new RestlessStore('/api/mes/v1/import/credit');
const importCreditItem = new RestlessStore('/api/mes/v1/import/credit_item');

const importApproval = new RestlessStore('/api/mes/v1/import/approval');
const importApprovalItem = new RestlessStore('/api/mes/v1/import/approval_item');

const importApprovalCost = new RestlessStore('/api/mes/v1/import/approval_cost');
const importApprovalCostItem = new RestlessStore('/api/mes/v1/import/approval_cost_item');

const importClearanceCost = new RestlessStore('/api/mes/v1/import/clearance_cost');
const importClearanceCostItem = new RestlessStore('/api/mes/v1/import/clearance_cost_item');

const getImportPurchaseOrder = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/import/purchase_order');
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getImportPurchaseOrderItem = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/import/purchase_order_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getImportShipment = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/import/shipment');
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getImportShipmentItem = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/import/shipment_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getImportClearance = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/import/clearance');
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getImportClearanceItem = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/import/clearance_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getImportCredit = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/import/credit');
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getImportCreditItem = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/import/credit_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getImportApproval = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/import/approval');
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getImportApprovalItem = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/import/approval_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getImportApprovalCost = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/import/approval_cost');
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getImportApprovalCostItem = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/import/approval_cost_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getImportClearanceCost = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/import/clearance_cost');
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getImportClearanceCostItem = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/import/clearance_cost_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};


export { 
  importPurchaseOrder, 
  importPurchaseOrderItem,
  importShipment,
  importShipmentItem,
  importClearance,
  importClearanceItem,
  importCredit,
  importCreditItem,
  importApproval,
  importApprovalItem,
  importApprovalCost,
  importApprovalCostItem,
  importClearanceCost,
  importClearanceCostItem,
  getImportPurchaseOrder,
  getImportPurchaseOrderItem,
  getImportShipment,
  getImportShipmentItem,
  getImportClearance,
  getImportClearanceItem,
  getImportCredit,
  getImportCreditItem,
  getImportApproval,
  getImportApprovalItem,
  getImportApprovalCost,
  getImportApprovalCostItem,
  getImportClearanceCost,
  getImportClearanceCostItem,
};
