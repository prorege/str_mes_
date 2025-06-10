import RestlessStore from './restless-store';

const purchaseOrderPlan = new RestlessStore('/api/mes/v1/purchase/order_plan');
const purchaseOrderPlanItem = new RestlessStore('/api/mes/v1/purchase/order_plan_item');

const purchaseOrder = new RestlessStore('/api/mes/v1/purchase/order');
const purchaseOrderItem = new RestlessStore('/api/mes/v1/purchase/order_item');

const purchasePreReceiving = new RestlessStore('/api/mes/v1/purchase/prereceiving');
const purchasePreReceivingItem = new RestlessStore('/api/mes/v1/purchase/prereceiving_item');

const purchaseReceiving = new RestlessStore('/api/mes/v1/purchase/receiving');
const purchaseReceivingItem = new RestlessStore('/api/mes/v1/purchase/receiving_item');

const purchaseReceivingReturn = new RestlessStore('/api/mes/v1/purchase/receiving_return');
const purchaseReceivingReturnItem = new RestlessStore('/api/mes/v1/purchase/receiving_return_item');

const purchaseOrderReceivingStatus = new RestlessStore('/api/mes/v1/purchase/order_receiving_status');

const purchaseStatement = new RestlessStore('/api/mes/v1/purchase/statement');
const purchaseStatementItem = new RestlessStore('/api/mes/v1/purchase/statement_item');

const purchasePayment = new RestlessStore('/api/mes/v1/purchase/payment');
const purchasePaymentItem = new RestlessStore('/api/mes/v1/purchase/payment_item');

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

const getPurchaseOrderPlanItem = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/purchase/order_plan_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getPurchaseOrderItem = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/purchase/order_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getPurchasePreReceivingItem = (defaultFilters, warehouseCode) => {
  const instance = new RestlessStore('/api/mes/v1/purchase/prereceiving_item', {
    onLoaded: function(result) {
      procBasicStock(result, warehouseCode);
    },
  });
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getPurchaseReceivingItem = (defaultFilters, warehouseCode) => {
  const instance = new RestlessStore('/api/mes/v1/purchase/receiving_item', {
    onLoaded: function(result) {
      procBasicStock(result, warehouseCode);
    },
  });
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getPurchaseReceivingReturnItem = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/purchase/receiving_return_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getPurchaseStatement = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/purchase/statement');
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getPurchaseStatementItem = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/purchase/statement_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getPurchasePayment = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/purchase/payment');
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getPurchasePaymentItem = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/purchase/payment_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

export {
  purchaseOrderPlan,
  purchaseOrderPlanItem,
  purchaseOrder,
  purchaseOrderItem,
  purchasePreReceiving,
  purchasePreReceivingItem,
  purchaseReceiving,
  purchaseReceivingItem,
  purchaseReceivingReturn,
  purchaseReceivingReturnItem,
  purchaseOrderReceivingStatus,
  purchaseStatement,
  purchaseStatementItem,
  purchasePayment,
  purchasePaymentItem,
  getPurchaseOrderPlanItem,
  getPurchaseOrderItem,
  getPurchasePreReceivingItem,
  getPurchaseReceivingItem,
  getPurchaseReceivingReturnItem,
  getPurchaseStatement,
  getPurchaseStatementItem,
  getPurchasePayment,
  getPurchasePaymentItem
};
